# Working rules

Keep this repository confined to driven reciprocal mechanics. Do not modify other repositories or import an unrelated scientific model, tutorial, collaboration arrangement, or publication policy.

`docs/MODEL.md`, `docs/RESULTS.md`, and `docs/PROOF.md` are the canonical statements. Preserve coordinate/force normalization, constant positive symmetric damping, reciprocal instantaneous stiffness, and the distinctions between fixed measured and global budgets. Keep the stationary-output minimum's extra damping assumption explicit.

Do not equate arbitrary waveform tests with a proof, the tangent spring model with a finite-amplitude theorem, or ideal guides with a fabricated apparatus. Do not silently refresh stored reference values to make a test pass.

No manuscript, new research extension, external outreach, public release tag, or repository visibility/license change is part of routine maintenance. Do not advertise a journal target. Add normal primary-paper citations where used.

Use GitHub-native Markdown with short fenced `math` displays and protected inline math delimited by a dollar sign and backtick on each side. Keep table-cell mathematics free of literal vertical bars; use TeX commands for absolute values and norms. No TeX document wrappers or equation tags. Keep theorem statements, proof, and evidence linked. Verify local section links as well as file destinations. Fruchart–Scheibner–Vitelli's review is the selected teaching anchor; the local tutorial supplies the bridge to this model and does not replace the canonical proofs.

The observed reader renderer rejects `\operatorname`. Use upright `\mathrm{...}` labels with explicit spacing for named operations. A successful standalone MathJax render does not establish compatibility with the reader's macro restrictions.

Use `\lt` for strict less-than inequalities inside mathematics. A raw `<` can be interpreted as an HTML opener and truncate the displayed formula. Keep scalar positivity separate from matrix-order bounds.

Before a merge run `python checks/run.py --output results.local.json`, `python checks/check_docs.py`, `python -m unittest discover -s checks -p 'test_check_docs.py'`, and `npm --prefix checks run check` after installing the locked documentation dependencies with `npm ci --prefix checks --ignore-scripts`. The render gate must preserve every formula through the full Markdown parse and reject TeX errors; its success does not replace a live visual check when a reader reports a display defect. The numerical scripts require assertions enabled. New scientific claims need explicit proofs and declared assumptions, not just more numerical cases. Preserve the source hashes in `provenance/INPUTS.json`.
