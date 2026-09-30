#!/usr/bin/env python3
"""Check local navigation, mathematical source conventions, and preserved code."""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def anchors(text: str) -> set[str]:
    found: set[str] = set()
    counts: dict[str, int] = {}
    plain = re.sub(r"```[\s\S]*?```", "", text)
    for title in re.findall(r"^#{1,6}\s+(.+?)\s*$", plain, re.M):
        name = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        count = counts.get(name, 0)
        counts[name] = count + 1
        found.add(name if count == 0 else f"{name}-{count}")
    return found


def main() -> None:
    links = displays = 0
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text()
        if text.count("```") % 2:
            raise AssertionError(f"Unclosed code fence: {path}")
        if text.count("$$") % 2:
            raise AssertionError(f"Unclosed math fence: {path}")
        plain = re.sub(r"```[\s\S]*?```", "", text)
        for block in re.findall(r"\$\$([\s\S]*?)\$\$", plain):
            displays += 1
            if "\\tag" in block or "\\begin{document}" in block:
                raise AssertionError(f"Unsupported display convention: {path}")
            if block.count("{") != block.count("}"):
                raise AssertionError(f"Unbalanced math braces: {path}")
            if max(map(len, block.splitlines()), default=0) > 180:
                raise AssertionError(f"Split a long display line: {path}")
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
    print(f"PASS {links} local destinations/sections; {displays} math displays; source hashes and license")


if __name__ == "__main__":
    main()
