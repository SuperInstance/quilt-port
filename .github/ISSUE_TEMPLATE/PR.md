---
name: 🧵 Stitch — propose a code change
about: Submit a code change
title: "[stitch] "
labels: ["stitch", "code-change"]
---

## What I'm changing

Cite the file(s) and the change. Don't speculate about consequences — only describe what.

## Why

Cite the witness or canon this implements. If it's a fix, cite the failing test. If it's a feature, cite the WORKSHOP.md section.

## Receipts

- Tests added/affected: ...
- Canarying preserved: `python3 canary.py` passes
- Tests pass: `python3 run_tests.py` output

## Doctrine check

- [ ] Reads prior canon before writing
- [ ] Witness references established
- [ ] Fleet canary preserved (`0x24a555471370b18d`)
- [ ] No auto-promotion of canon terms (propose, don't promote)
- [ ] Tier-appropriate (python/web/esp32/ideation/)

---

### What happens next

Stitches are reviewed by community. PR description should match this template. CI runs the canary and test suite.
