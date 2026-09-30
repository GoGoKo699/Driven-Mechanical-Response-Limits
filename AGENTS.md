# Working rules

Keep this repository confined to driven reciprocal mechanics. Do not modify other repositories or import an unrelated scientific model, tutorial, collaboration arrangement, or publication policy.

`docs/MODEL.md`, `docs/RESULTS.md`, and `docs/PROOF.md` are the canonical statements. Preserve coordinate/force normalization, constant positive symmetric damping, reciprocal instantaneous stiffness, and the distinctions between fixed measured and global budgets. Keep the stationary-output minimum's extra damping assumption explicit.

Do not equate arbitrary waveform tests with a proof, the tangent spring model with a finite-amplitude theorem, or ideal guides with a fabricated apparatus. Do not silently refresh stored reference values to make a test pass.

No manuscript, new research extension, external outreach, public release tag, or repository visibility/license change is part of routine maintenance. Do not advertise a journal target. Add normal primary-paper citations where used.

Use GitHub-native Markdown with short display equations and consistent inline math. No TeX document wrappers or equation tags. Keep theorem statements, proof, and evidence linked. Verify local section links as well as file destinations.

Before a merge run `python checks/run.py --output results.local.json` and `python checks/check_docs.py`. The numerical scripts require assertions enabled. New scientific claims need explicit proofs and declared assumptions, not just more numerical cases. Preserve the source hashes in `provenance/INPUTS.json`.
