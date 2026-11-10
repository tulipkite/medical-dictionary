#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
# Copyright (C) 2026 d25037 and contributors
"""Verify source/release equality and optionally a user-selected text export."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

from build import OUTPUT_NAME, ROOT, build_bytes, metrics, validate_row


def parse_export(blob):
    if len(blob) > 1024 * 1024:
        raise ValueError('Export exceeds the 1 MiB check limit')
    encoding = 'utf-16' if blob.startswith((b'\xff\xfe', b'\xfe\xff')) else 'utf-8-sig'
    text = blob.decode(encoding)
    rows, comments = [], 0
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.startswith(('!', '#')):
            continue
        fields = line.split('\t')
        if len(fields) not in (3, 4):
            raise ValueError(f'Invalid column count at line {number}')
        row = tuple(fields[:3])
        validate_row(row)
        comments += int(len(fields) == 4 and bool(fields[3]))
        rows.append(row)
        if len(rows) > 5000:
            raise ValueError('Export exceeds the 5000-row check limit')
    return Counter(rows), comments


def compare_exports(expected, actual):
    want, _ = parse_export(expected)
    got, comments = parse_export(actual)
    return {'matches': want == got, 'expected_rows': sum(want.values()),
            'export_rows': sum(got.values()), 'missing_rows': sum((want - got).values()),
            'extra_rows': sum((got - want).values()), 'rows_with_comments': comments}


def check_recorded_results(root, sha):
    engine = json.loads((root / 'verification/engine-results.json').read_text(encoding='utf-8'))
    gui = json.loads((root / 'verification/app-results.json').read_text(encoding='utf-8'))
    if engine['input_dictionary_sha256'] != sha or gui['input_dictionary_sha256'] != sha:
        raise ValueError('Recorded tests refer to a different dictionary')
    medical = [r for group in engine['medical_groups'].values() for r in group]
    general = [r for group in engine['general_groups'].values() for r in group]
    if len(medical) != 143 or len(general) != 32 or len(engine['standalone_1000']) != 1000:
        raise ValueError('Unexpected historical result counts')
    for row in medical + general + engine['standalone_1000']:
        if row['matches'] != (row['actual'] == row['expected']):
            raise ValueError('Inconsistent recorded comparison')
    if sum(r['matches'] for r in medical) != 143 or sum(r['matches'] for r in general) != 30:
        raise ValueError('Historical score differs from documentation')
    if sum(r['matches'] for r in engine['standalone_1000']) != 999:
        raise ValueError('Standalone score differs from documentation')
    if len(gui['cases']) != 2 or not all(r['actual'] == r['expected'] and r['space_presses'] == 1 and r['pass'] for r in gui['cases']):
        raise ValueError('Historical app test record is inconsistent')
    return {'medical_regression': '143/143', 'general_sentences': '30/32',
            'standalone_first': '999/1000', 'recorded_app_cases': '2/2',
            'note': 'Checked recorded results only; no live IME conversion was run'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export', type=Path, help='Read-only comparison of one selected dictionary export')
    args = parser.parse_args()
    try:
        release = (ROOT / 'dictionary/google' / OUTPUT_NAME).read_bytes()
        if release != build_bytes():
            raise ValueError('Generated source and distributed dictionary differ')
        manifest = json.loads((ROOT / 'dictionary/google/manifest.json').read_text(encoding='utf-8'))
        if manifest != metrics(release):
            raise ValueError('Distributed manifest differs from dictionary contents')
        report = {'dictionary': metrics(release),
                  'recorded_results': check_recorded_results(ROOT, hashlib.sha256(release).hexdigest())}
        if args.export:
            if args.export.stat().st_size > 1024 * 1024:
                raise ValueError('Export exceeds the 1 MiB check limit')
            report['selected_export'] = compare_exports(release, args.export.read_bytes())
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 3 if args.export and not report['selected_export']['matches'] else 0
    except (OSError, UnicodeError, ValueError, KeyError) as error:
        # Do not print file paths or user-selected dictionary contents.
        print('Check failed: ' + (str(error) if not isinstance(error, (OSError, UnicodeError)) else type(error).__name__), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
