#!/usr/bin/env python3
"""Regression fixtures for observed Markdown/math source failures (stdlib only).

Run: python checks/test_check_docs.py
TeX rendering and whole-document GFM preservation are checked by check_math.cjs.
"""
from __future__ import annotations

import unittest

from check_docs import extract_math


class MathSourceRegressionTests(unittest.TestCase):
    def test_raw_less_than_is_rejected_before_html_truncation(self):
        for text in [r'$`0<m`$', '$0<m$', '```math\n0<mI\n```\n', r'$`a<b>c`$']:
            with self.subTest(text=text), self.assertRaisesRegex(AssertionError, 'less-than'):
                extract_math(text)
        text = r'$`0\lt m`$ and $`\langle x,y\rangle`$'
        self.assertEqual([r.source for r in extract_math(text)],
                         [r'0\lt m', r'\langle x,y\rangle'])

    def test_observed_operatorname_failure(self):
        for text in [r'$`\operatorname{Sym}Q`$', r'$\operatorname*{max}x$',
                     '```math\n\\operatorname{rank}H\n```\n']:
            with self.subTest(text=text), self.assertRaisesRegex(AssertionError, 'operatorname'):
                extract_math(text)
        self.assertEqual(extract_math(r'$`\mathrm{Sym}\,Q`$')[0].source, r'\mathrm{Sym}\,Q')

    def test_mismatched_delimiters_fences_and_braces(self):
        cases = {
            'protected_open': '$`x+y', 'protected_close': 'x`$',
            'legacy_open': '$x+y', 'display_open': '$$\nx+y\n',
            'mixed_delimiters': '$`x+y$', 'blank_paragraph': '$`x\n\ny`$',
            'math_fence': '```math\nx+y\n', 'code_fence': '```sh\necho x\n',
            'wrong_fence_kind': '```math\nx\n~~~\n',
            'short_closing_fence': '````math\nx\n```\n',
            'braces': r'$`\frac{x}{y`$', 'brace_order': '$`}{`$',
            'paren_delimiter': r'\(x\)', 'bracket_delimiter': r'\[x\]',
            'empty_inline': '$``$', 'empty_display': '$$$$',
        }
        for name, text in cases.items():
            with self.subTest(name=name), self.assertRaises(AssertionError):
                extract_math(text, name)

    def test_table_pipe_cannot_split_a_formula(self):
        header = '| Label | Formula |\n| --- | --- |\n'
        for formula in [r'a|b', r'a\\|b']:
            with self.subTest(formula=formula), self.assertRaisesRegex(AssertionError, 'table pipe'):
                extract_math(header + '| x | $`' + formula + '`$ |\n')
        for formula in [r'a\|b', r'a\mid b', r'\lVert x\rVert']:
            with self.subTest(formula=formula):
                rows = extract_math(header + '| x | $`' + formula + '`$ |\n')
                self.assertEqual([(r.source, r.line) for r in rows], [(formula, 3)])
        # A raw pipe outside a table is valid TeX, and a heading ends a table.
        self.assertEqual(extract_math('$`a|b`$')[0].source, 'a|b')
        self.assertEqual(extract_math(header + '## Heading $`a|b`$\n')[0].line, 3)

    def test_code_and_plain_html_are_not_formulas(self):
        cases = [
            '`echo "$HOME"` and `\\operatorname{X}` and `<p`',
            '``an embedded ` and $`formula`$``',
            '```sh\necho "$HOME"\n\\(x\\) <p \\operatorname{X}\n```\n',
            '~~~text\n$`broken\n~~~\n',
            '<span>ordinary {prose}</span>\n',
            '<!-- ordinary comment -->\n',
            r'Escaped \$ and \\(x\\) are prose.',
        ]
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(extract_math(text), [])
        nested = '````text\n```math\n$`inside`$\n```\n````\n$`outside`$\n'
        self.assertEqual([(r.source, r.line) for r in extract_math(nested)], [('outside', 6)])

    def test_exact_source_order_and_locations_survive(self):
        text = ('First $`  x + y  `$ and $`z`$.\n\n'
                '```math\n\\begin{pmatrix}a&b\\\\c&d\\end{pmatrix}\n```\n'
                'Then $`u +\nv`$.\n')
        self.assertEqual([(r.kind, r.source, r.line) for r in extract_math(text)], [
            ('inline', '  x + y  ', 1), ('inline', 'z', 1),
            ('display', r'\begin{pmatrix}a&b\\c&d\end{pmatrix}', 4),
            ('inline', 'u +\nv', 6),
        ])
        self.assertEqual(extract_math('```math\r\nx+y\r\n```\r\n')[0].source, 'x+y')


if __name__ == '__main__':
    unittest.main()
