#!/usr/bin/env python3
"""Check local navigation, mathematical source conventions, and preserved code."""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path
from typing import NamedTuple
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def markdown_paths() -> list[Path]:
    """Return project documents, excluding installed dependencies and Git data."""
    excluded = {"node_modules", ".venv", ".git"}
    return sorted(path for path in ROOT.rglob("*.md")
                  if not excluded.intersection(path.relative_to(ROOT).parts))


class MathExpression(NamedTuple):
    """A validated formula, with its source and one-based Markdown line."""

    kind: str  # "inline" or "display"
    source: str
    line: int


def _escaped(text: str, pos: int) -> bool:
    start = pos
    while start and text[start - 1] == "\\":
        start -= 1
    return (pos - start) % 2 == 1


def _fences(text: str, source: str) -> list[tuple[int, int, str, int, int]]:
    """Return complete CommonMark-style backtick/tilde fenced regions.

    Each tuple is (start, end, info, content_start, content_end). Code fence
    length matters: a four-backtick example can contain triple backticks.
    """
    regions = []
    opened = None
    offset = 0
    for line in text.splitlines(keepends=True):
        if opened is not None:
            marker, start, info, content_start = opened
            if re.fullmatch(r" {0,3}" + re.escape(marker[0]) +
                            "{" + str(len(marker)) + r",}[ \t]*\r?\n?", line):
                regions.append((start, offset + len(line), info, content_start, offset))
                opened = None
        else:
            match = re.fullmatch(r" {0,3}(`{3,}|~{3,})([^\r\n]*)\r?\n?", line)
            if match and not (match[1][0] == "`" and "`" in match[2]):
                opened = (match[1], offset, match[2].strip(), offset + len(line))
        offset += len(line)
    if opened is not None:
        line = text.count("\n", 0, opened[1]) + 1
        raise AssertionError(f"Unclosed code/math fence: {source}:{line}")
    return regions


def _mask(text: str, start: int, end: int) -> str:
    return text[:start] + re.sub(r"[^\r\n]", " ", text[start:end]) + text[end:]


def _table_cells(line: str) -> list[str]:
    row = line.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|") and not _escaped(row, len(row) - 1):
        row = row[:-1]
    separators = [i for i, char in enumerate(row) if char == "|" and not _escaped(row, i)]
    boundaries = [-1, *separators, len(row)]
    return [row[left + 1:right] for left, right in zip(boundaries, boundaries[1:])]


def _table_lines(text: str) -> set[int]:
    """Identify pipe-table rows from an actual Markdown separator row."""
    lines = text.splitlines()
    found: set[int] = set()
    block_start = re.compile(r" {0,3}(?:#{1,6}(?:[ \t]|$)|>|(?:[-+*]|\d{1,9}[.)])[ \t])")
    for i, line in enumerate(lines):
        cells = _table_cells(line)
        if (i and "|" in line and lines[i - 1].strip() and
                not block_start.match(lines[i - 1]) and
                len(_table_cells(lines[i - 1])) == len(cells) and
                all(re.fullmatch(r"\s*:?-+:?\s*", cell) for cell in cells)):
            found.update((i, i + 1))  # one-based header and separator
            j = i + 1
            while (j < len(lines) and lines[j].strip() and "|" in lines[j] and
                   not block_start.match(lines[j])):
                found.add(j + 1)
                j += 1
    return found


def _validate_math(formula: str, kind: str, source: str, line: int) -> None:
    where = f"{source}:{line}"
    if not formula.strip():
        raise AssertionError(f"Empty math expression: {where}")
    if "<" in formula:
        raise AssertionError(
            f"HTML-sensitive less-than sign in math: {where}; "
            r"use \lt for strict inequalities or \langle for angle brackets"
        )
    unsupported = re.finditer(r"\\(?:tag\b|(?:begin|end)\s*\{\s*document\s*\})", formula)
    if any(not _escaped(formula, match.start()) for match in unsupported):
        raise AssertionError(f"Unsupported math convention: {where}")
    # This macro was rejected by the observed renderer; this is not a full allowlist.
    operators = re.finditer(r"\\operatorname(?![A-Za-z])", formula)
    if any(not _escaped(formula, match.start()) for match in operators):
        raise AssertionError(
            f"Renderer-rejected \\operatorname: {where}; "
            r"use \mathrm{...} with explicit spacing where needed"
        )
    depth = 0
    for i, char in enumerate(formula):
        if _escaped(formula, i):
            continue
        if char == "\\" and i + 1 < len(formula) and formula[i + 1] in "()[]":
            raise AssertionError(f"Unsupported TeX math delimiter: {where}")
        if char == "$":
            raise AssertionError(f"Unexpected math delimiter inside formula: {where}")
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth < 0:
                raise AssertionError(f"Unbalanced math braces: {where}")
    if depth:
        raise AssertionError(f"Unbalanced math braces: {where}")
    if kind == "display" and max(map(len, formula.splitlines()), default=0) > 180:
        raise AssertionError(f"Split a long display line: {where}")


def extract_math(text: str, source: str = "<text>") -> list[MathExpression]:
    """Validate and extract GitHub math, ignoring ordinary fenced/inline code.

    Supports math fences, $$ displays, protected $`...`$ inline expressions,
    and legacy $...$ inline expressions. Inline expressions may wrap lines but
    cannot cross a blank paragraph. Bare numeric currency without a matching
    dollar is prose; escape literal dollars in ambiguous mathematical prose.
    This is source validation, not a TeX parser or a GitHub renderer.
    """
    found: list[tuple[int, MathExpression]] = []
    regions = _fences(text, source)
    plain = text
    for start, end, info, content_start, content_end in reversed(regions):
        if info == "math":
            formula = text[content_start:content_end].rstrip("\r\n")
            line = text.count("\n", 0, content_start) + 1
            _validate_math(formula, "display", source, line)
            found.append((start, MathExpression("display", formula, line)))
        plain = _mask(plain, start, end)
    tables = _table_lines(plain)
    i = 0
    while i < len(plain):
        char = plain[i]
        if char == "\\":
            if i + 1 < len(plain) and plain[i + 1] in "()[]":
                line = plain.count("\n", 0, i) + 1
                raise AssertionError(f"Unsupported TeX math delimiter: {source}:{line}")
            i += 2
            continue
        if char == "`":
            marker = re.match(r"`+", plain[i:])[0]
            # Inline code cannot span a blank paragraph or a masked fence.
            tail = re.split(r"\r?\n[ \t]*\r?\n", plain[i + len(marker):], maxsplit=1)[0]
            closing = re.search(r"(?<!`)" + re.escape(marker) + r"(?!`)", tail)
            if closing:
                i += len(marker) + closing.end()
                continue
            if plain.startswith("`$", i):
                line = plain.count("\n", 0, i) + 1
                raise AssertionError(f"Unmatched protected inline math delimiter: {source}:{line}")
            i += len(marker)  # unmatched backticks are literal Markdown
            continue
        if char != "$":
            i += 1
            continue
        start = i
        protected = plain.startswith("$`", i)
        display = plain.startswith("$$", i)
        delimiter = "`$" if protected else ("$$" if display else "$")
        content_start = i + (2 if protected or display else 1)
        end = content_start
        while end < len(plain):
            if not display and re.match(r"\r?\n[ \t]*\r?\n", plain[end:]):
                break
            if plain.startswith(delimiter, end) and not _escaped(plain, end):
                break
            end += 1
        if end >= len(plain) or not plain.startswith(delimiter, end):
            # A bare price is not an unmatched equation delimiter.
            if not protected and not display and re.match(r"\$\d[\d,.]*(?=\s|[;:!?)}\]]|$)", plain[start:]):
                i += 1
                continue
            line = plain.count("\n", 0, start) + 1
            raise AssertionError(f"Unmatched math delimiter: {source}:{line}")
        formula = plain[content_start:end]
        line = plain.count("\n", 0, start) + 1
        kind = "display" if display else "inline"
        _validate_math(formula, kind, source, line)
        if kind == "inline":
            for j, token in enumerate(formula):
                if (token == "|" and not _escaped(formula, j) and
                        plain.count("\n", 0, content_start + j) + 1 in tables):
                    raise AssertionError(f"Escape a table pipe inside inline math: {source}:{line}")
        found.append((start, MathExpression(kind, formula, line)))
        i = end + len(delimiter)
    return [item for _, item in sorted(found)]


def anchors(text: str) -> set[str]:
    found: set[str] = set()
    counts: dict[str, int] = {}
    plain = text
    for start, end, *_ in reversed(_fences(text, "<anchor source>")):
        plain = _mask(plain, start, end)
    for title in re.findall(r"^#{1,6}\s+(.+?)\s*$", plain, re.M):
        name = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        count = counts.get(name, 0)
        counts[name] = count + 1
        found.add(name if count == 0 else f"{name}-{count}")
    return found


def main() -> None:
    links = displays = inlines = 0
    for path in markdown_paths():
        text = path.read_text()
        math = extract_math(text, str(path.relative_to(ROOT)))
        displays += sum(item.kind == "display" for item in math)
        inlines += sum(item.kind == "inline" for item in math)
        for target in re.findall(r"\]\(([^)]+)\)", text):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            dest = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            if not dest.is_relative_to(ROOT) or not dest.is_file():
                raise AssertionError(f"Broken/escaping link: {path}: {target}")
            if parsed.fragment and dest.suffix == ".md":
                if unquote(parsed.fragment) not in anchors(dest.read_text()):
                    raise AssertionError(f"Missing section: {path}: {target}")
            links += 1
    provenance = json.loads((ROOT / "provenance/INPUTS.json").read_text())
    for row in provenance["unchanged_scientific_scripts"]:
        if hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() != row["sha256"]:
            raise AssertionError(f"Preserved script changed: {row['path']}")
    content = (ROOT / "LICENSE").read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
    if blob != "e17a781bf47c4aadf18b68fc593846a1193b86c1":
        raise AssertionError("Original MIT license changed")
    reference = json.loads((ROOT / "checks/reference.json").read_text())
    if abs(reference["ceiling"] - 0.0893163974770409) > 1e-12:
        raise AssertionError("Worked-example reference changed")
    print(f"PASS {links} local destinations/sections; {displays} math displays; {inlines} inline formulas; source hashes and license")


if __name__ == "__main__":
    main()
