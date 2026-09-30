#!/usr/bin/env node
/* Check TeX conversion and formula survival through the complete GFM parse.
 * This local render gate does not reproduce GitHub's deployment or styling.
 * Run after npm ci --prefix checks: node checks/check_math.cjs
 */
'use strict';

const assert = require('node:assert/strict');
const path = require('node:path');
const {spawnSync} = require('node:child_process');
const {mathjax} = require('mathjax-full/js/mathjax.js');
const {TeX} = require('mathjax-full/js/input/tex.js');
const {SVG} = require('mathjax-full/js/output/svg.js');
const {liteAdaptor} = require('mathjax-full/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = require('mathjax-full/js/handlers/html.js');
require('mathjax-full/js/input/tex/ams/AmsConfiguration.js');

const root = path.resolve(__dirname, '..');
const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
// Explicit packages exclude noerrors/noundefined: errors must not become text.
const tex = new TeX({packages: ['base', 'ams'], formatError: (_, error) => {
  throw new Error(error.message, {cause: error});
}});
const mathDocument = mathjax.document('', {
  InputJax: tex, OutputJax: new SVG({fontCache: 'none'}),
});

function renderMath(source, kind) {
  assert(source.trim(), 'Empty formula');
  const node = mathDocument.convert(source, {display: kind === 'display'});
  const html = adaptor.outerHTML(node);
  assert(!/data-mjx-error|data-mml-node="merror"|<merror\b/.test(html), 'MathJax error node');
  assert(/<svg\b/.test(html) && /<(?:path|use|text|rect|line|polygon)\b/.test(html),
         'Missing or empty rendered mathematics');
  assert.equal((html.match(/<mjx-container\b/g) || []).length, 1, 'Missing math container');
  return html;
}

function checkRejectedTeX() {
  const fixtures = [
    [String.raw`\thisMacroMustNotExist{x}`, /Undefined control sequence/],
    [String.raw`\begin{pmatrix}1&2\\3&4\end{bmatrix}`, /ended with/],
    [String.raw`\left(x+1`, /missing \\right/],
    [String.raw`\right)x`, /Missing \\left/],
    [String.raw`\quad`, /empty rendered/],
  ];
  for (const [source, error] of fixtures) {
    assert.throws(() => renderMath(source, 'inline'), error, `Must reject: ${source}`);
  }
  // Check that rejected expressions do not leave the renderer unusable.
  renderMath(String.raw`\begin{pmatrix}1&2\\3&4\end{pmatrix}`, 'display');
  return fixtures.length;
}

function sourceCells(line) {
  let row = line.trim();
  if (row.startsWith('|')) row = row.slice(1);
  const escaped = index => {
    let n = 0;
    for (let j = index - 1; j >= 0 && row[j] === '\\'; --j) ++n;
    return n % 2 === 1;
  };
  if (row.endsWith('|') && !escaped(row.length - 1)) row = row.slice(0, -1);
  let count = 1;
  for (let i = 0; i < row.length; ++i) if (row[i] === '|' && !escaped(i)) ++count;
  return count;
}

function checkDocument(document, Marked) {
  const actual = [];
  const render = (source, kind) => {
    actual.push({kind, source});  // No trimming, sorting, or TeX normalization.
    return renderMath(source, kind);
  };
  const marked = new Marked({gfm: true, extensions: [{
    name: 'protectedMath', level: 'inline',
    start: source => source.indexOf('$`'),
    tokenizer(source) {
      const match = /^\$`([\s\S]*?)`\$/.exec(source);
      if (match) return {type: 'protectedMath', raw: match[0], text: match[1]};
    },
    renderer: token => render(token.text, 'inline'),
  }], renderer: {
    code(token) {
      if (token.lang === 'math') return render(token.text, 'display');
      return false;
    },
  }});
  const tokens = marked.lexer(document.text);
  let tables = 0, rows = 0;
  marked.walkTokens(tokens, token => {
    assert.notEqual(token.type, 'html', 'Raw HTML requires an explicit format-policy decision');
    if (token.type !== 'table') return;
    ++tables;
    rows += token.rows.length;
    const columns = token.header.length;
    for (const row of token.rows) assert.equal(row.length, columns, 'Nonrectangular table tokens');
    // Marked pads/truncates cells: also compare its raw rows, before that loss.
    const rawRows = token.raw.trimEnd().split(/\r?\n/);
    assert.equal(rawRows.length, token.rows.length + 2, 'Table row lost during parsing');
    for (const row of rawRows) assert.equal(sourceCells(row), columns, 'Nonrectangular source table');
  });
  const html = marked.parser(tokens);
  if (document.text.trim()) assert(html.trim(), 'Empty rendered document');
  const expected = document.math.map(({kind, source}) => ({kind, source}));
  assert.equal(actual.length, expected.length, 'GFM lost or duplicated a formula');
  for (let i = 0; i < expected.length; ++i) {
    assert.deepEqual(actual[i], expected[i],
      `GFM changed or reordered the formula at source line ${document.math[i].line}`);
  }
  assert.equal((html.match(/<mjx-container\b/g) || []).length, expected.length,
               'Rendered formula count differs from source');
  return {formulas: actual.length, tables, rows};
}

async function main() {
  const {Marked} = await import('marked');
  const exportSource = String.raw`
import json, sys
sys.path.insert(0, sys.argv[1])
from check_docs import ROOT, extract_math, markdown_paths
documents = []
for path in markdown_paths():
    text = path.read_text()
    name = str(path.relative_to(ROOT))
    documents.append(dict(path=name, text=text,
                          math=[row._asdict() for row in extract_math(text, name)]))
print(json.dumps(documents))
`;
  const exported = spawnSync(process.env.PYTHON || 'python3',
    ['-c', exportSource, __dirname], {cwd: root, encoding: 'utf8', maxBuffer: 8 * 1024 * 1024});
  if (exported.error) throw exported.error;
  assert.equal(exported.status, 0, `Source extraction failed:\n${exported.stderr}`);
  const documents = JSON.parse(exported.stdout);
  assert(documents.length, 'No Markdown documents found');
  const negativeCases = checkRejectedTeX();
  const totals = {formulas: 0, tables: 0, rows: 0};
  for (const document of documents) {
    try {
      const counts = checkDocument(document, Marked);
      for (const key of Object.keys(totals)) totals[key] += counts[key];
    } catch (error) {
      throw new Error(`${document.path}: ${error.message}`, {cause: error});
    }
  }
  assert(totals.formulas > 0, 'No formulas found');
  console.log(`PASS ${documents.length} Markdown documents; ${totals.formulas} formulas preserved and rendered; ` +
              `${totals.tables} rectangular tables/${totals.rows} body rows; ${negativeCases} malformed/empty-math fixtures rejected`);
}

main().catch(error => {console.error(`FAIL ${error.message}`); process.exitCode = 1;});
