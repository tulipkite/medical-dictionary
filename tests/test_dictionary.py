# SPDX-License-Identifier: GPL-2.0-only
# Copyright (C) 2026 d25037 and contributors
from collections import Counter
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build import ROOT, build_bytes
from check import compare_exports, parse_export


class DictionaryChecks(unittest.TestCase):
    def test_rebuild_is_identical_to_verified_release(self):
        self.assertEqual(build_bytes(), (ROOT / 'dictionary/google/tulipkite-medical-dictionary.txt').read_bytes())

    def test_export_reordering_bom_crlf_and_comment_column(self):
        expected = 'かせいりゅう\t仮性瘤\t名詞\nたぼうせい\t多房性\t名詞\n'.encode()
        actual = '\ufeff! header\r\nたぼうせい\t多房性\t名詞\t\r\nかせいりゅう\t仮性瘤\t名詞\tcomment\r\n'.encode()
        result = compare_exports(expected, actual)
        self.assertTrue(result['matches'])
        self.assertEqual(result['rows_with_comments'], 1)

    def test_duplicate_is_not_hidden_by_set_comparison(self):
        row = 'かせいりゅう\t仮性瘤\t名詞\n'.encode()
        result = compare_exports(row, row + row)
        self.assertFalse(result['matches'])
        self.assertEqual(result['extra_rows'], 1)

    def test_missing_and_changed_entries_fail_comparison(self):
        expected = 'かせいりゅう\t仮性瘤\t名詞\n'.encode()
        actual = 'かせいりゅう\t架空の別表記\t名詞\n'.encode()
        result = compare_exports(expected, actual)
        self.assertEqual((result['missing_rows'], result['extra_rows']), (1, 1))

    def test_unknown_pos_and_html_are_rejected(self):
        for raw in ['<html>not a dictionary</html>', 'かせいりゅう\t仮性瘤\tunknown']:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                parse_export(raw.encode())

    def test_utf16_bom_export(self):
        raw = 'かせいりゅう\t仮性瘤\t名詞\n'
        self.assertEqual(parse_export(raw.encode('utf-16'))[0], Counter({('かせいりゅう', '仮性瘤', '名詞'): 1}))

    def test_export_row_and_byte_limits(self):
        for raw in [b'x' * (1024 * 1024 + 1), ('かせいりゅう\t仮性瘤\t名詞\n' * 5001).encode()]:
            with self.assertRaises(ValueError):
                parse_export(raw)


if __name__ == '__main__':
    unittest.main()
