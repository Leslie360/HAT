# CX-J1c Summary (Full-Attention Linearization)
**Date:** 2026-04-22
**Executor:** Codex
**Status:** Complete

- Finished to epoch 100.
- Ran 10x5 fresh-instance evaluation.
- **Fresh-instance accuracy:** 28.12 ± 5.1% (Collapse).
- Linearizing both QKV and projection still failed to recover performance. Severe nonlinearity imposes a limit even when attention is protected.
