#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
# Copyright (C) 2026 d25037 and contributors
"""Build dictionary text locally. Does not access the IME or network."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FILES = ('core.tsv', 'priority.tsv', 'context.tsv')
OUTPUT_NAME = 'tulipkite-medical-dictionary.txt'
DICTIONARY_VERSION = '2026-10-21'
ALLOWED_POS = {'名詞', '短縮よみ', '名詞サ変', '名詞形動', '品詞なし',
               '動詞一段', '動詞サ変', '動詞ワ行五段', '動詞タ行五段'}


def validate_row(row):
    if len(row) != 3 or row[2] not in ALLOWED_POS:
        raise ValueError('Expected three fields and a supported part of speech')
    if not re.fullmatch(r'[ぁ-ゖー]+', row[0]):
        raise ValueError('Invalid reading')
    if any(not field or len(field.encode('utf-8')) > 300 or
           any(ord(ch) < 32 or ord(ch) == 127 for ch in field) for field in row):
        raise ValueError('Empty, oversized, or control-character field')


def read_source(path):
    rows = [tuple(line.split('\t')) for line in path.read_text(encoding='utf-8').splitlines()]
    for row in rows:
        validate_row(row)
    return rows


def build_bytes(root=ROOT):
    groups = {name: read_source(root / 'source' / name) for name in FILES}
    core = groups['core.tsv']
    if not core or len({row[1] for row in core}) != len(core) or any(row[2] != '名詞' for row in core):
        raise ValueError('Core must contain distinct nouns')
    core_pairs = {(r[0], r[1]) for r in core}
    if any((r[0], r[1]) not in core_pairs or r[2] != '短縮よみ'
           for r in groups['priority.tsv']):
        raise ValueError('Priority registration must refer to a core term')
    rows = sorted(row for group in groups.values() for row in group)
    if len(set(rows)) != len(rows):
        raise ValueError('Duplicate reading/value/POS')
    return ''.join('\t'.join(row) + '\n' for row in rows).encode('utf-8')


def metrics(blob, root=ROOT):
    rows = [line.split('\t') for line in blob.decode('utf-8').splitlines()]
    return {'dictionary_version': DICTIONARY_VERSION, 'rows': len(rows),
            'basic_terms': len(read_source(root / 'source' / 'core.tsv')), 'distinct_values': len({r[1] for r in rows}),
            'pos_counts': dict(sorted(Counter(r[2] for r in rows).items())),
            'bytes': len(blob), 'sha256': hashlib.sha256(blob).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'build')
    args = parser.parse_args()
    dest = args.output.resolve()
    # Never use the repository root, its ancestors, or maintained input directories.
    protected = [ROOT / name for name in ['source', 'dictionary', 'provenance', 'verification', 'scripts', 'tests', 'docs', '.git', '.github']]
    if dest == ROOT or dest in ROOT.parents or any(dest == p or p in dest.parents for p in protected):
        parser.error('Choose a separate output directory such as build')
    blob = build_bytes()
    dest.mkdir(parents=True, exist_ok=True)
    (dest / OUTPUT_NAME).write_bytes(blob)
    report = metrics(blob)
    (dest / 'manifest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
