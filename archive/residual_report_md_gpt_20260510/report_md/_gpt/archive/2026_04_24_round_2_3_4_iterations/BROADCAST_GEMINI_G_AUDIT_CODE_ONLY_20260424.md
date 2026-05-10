# BROADCAST - Gemini G-AUDIT-CODE Only
Date: 2026-04-24
Issuer: Codex relaying user directive
Source: `BROADCAST_REBUILD_3WEEK_20260424.md`

Gemini should read `BROADCAST_REBUILD_3WEEK_20260424.md` in full, then do only:

- `G-AUDIT-CODE`

## Scope

Audit `analog_layers.py` at commit `33bed9c` and current local patches from an independent angle:

- look for third bugs missed by Codex
- verify second-order STE branch mapping under edge cases: `NL=1.0`, `NL=0`, `NL>3`
- check AMP / GradScaler interaction with custom STE
- check `convert_to_hybrid` config propagation through nested layers

## Output

- `GEMINI_INDEPENDENT_CODE_AUDIT_20260427.md`

## Explicit Non-Tasks

Per user directive, Gemini should not do anything else now:

- no theory memo
- no design spec
- no decision tree
- no text rewrite
- no Work 2
- no `G-AUDIT-TEXT`
- no `G-HOSTILE`

Those later tasks require explicit future authorization.
