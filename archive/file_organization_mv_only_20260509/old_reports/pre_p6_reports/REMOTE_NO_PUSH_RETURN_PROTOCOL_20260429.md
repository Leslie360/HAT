# Remote No-Push Return Protocol

**Date:** 2026-04-29
**Owner:** Codex
**Applies to:** Remote 105 / Remote 107 servers

## 1. Rule

Remote servers must not push to GitHub and must not store GitHub credentials or personal tokens.

Use remote servers as pull-only execution nodes:

```bash
git clone -b remote-107-kv-20260429 https://github.com/Leslie360/HAT.git HAT_remote
# or, if already cloned:
cd HAT_remote
git fetch origin remote-107-kv-20260429
git checkout remote-107-kv-20260429
git pull --ff-only
```

If SSH keys or HTTPS tokens are not already approved on the server, do not add them.

## 2. Return Channel

Return results only through the user's approved copy channel as compact Markdown text. Do not try to bypass server copy restrictions.

Preferred output format:

```text
REMOTE_RESULT_CHUNK 001/N
<markdown content, <= 8000 characters>
REMOTE_RESULT_CHUNK_END 001/N
```

If the report is long, split it into multiple chunks of <= 8000 characters.

## 3. What To Return

Return small text only:

- exact commands
- git SHA and diff stat
- environment summary
- compact result tables
- JSON summaries pasted inline only if small
- error trace snippets if needed
- final verdict and next requested action

Do not return:

- checkpoints
- model weights
- large logs
- datasets
- full stdout dumps longer than necessary
- credentials, hostnames beyond what is needed for reproducibility, or private paths if server policy disallows them

## 4. How Remote Should Package A Result Locally

Remote agent may write local files for its own organization:

```bash
mkdir -p remote_returns
cat > remote_returns/REMOTE107_RETURN_YYYYMMDD_HHMM.md <<'EOF_RETURN'
# Remote 107 Return

## Verdict

## Environment

## Commands

## Results

## Failures / Warnings

## Next Requested Action
EOF_RETURN
```

Then print the file in chunks for the user to copy through the approved channel:

```bash
python - <<'PY'
from pathlib import Path
p = Path('remote_returns/REMOTE107_RETURN_YYYYMMDD_HHMM.md')
s = p.read_text()
chunk = 8000
parts = [s[i:i+chunk] for i in range(0, len(s), chunk)]
for i, part in enumerate(parts, 1):
    print(f"REMOTE_RESULT_CHUNK {i:03d}/{len(parts):03d}")
    print(part)
    print(f"REMOTE_RESULT_CHUNK_END {i:03d}/{len(parts):03d}")
PY
```

## 5. If Copy Is Blocked

Stop and ask the server administrator or project owner for an approved export method. Do not attempt to evade copy controls.

Acceptable alternatives if explicitly approved:

- project-approved artifact export folder
- project-approved internal Git remote
- project-approved paste/report portal
- project-approved shared drive

## 6. Local Codex Responsibility

Codex/local side owns Git updates. After receiving remote Markdown chunks, Codex will:

1. reconstruct the return file locally
2. audit the claims and metadata
3. write a reviewed summary under `report_md/_gpt/`
4. update task files if needed
5. push clean branches from the local workstation only

## 7. Current 107 Priority

Remote 107 should not push code. It should return a compact Markdown response to the current validation request:

- digital FP baseline PPL
- analog no-noise/no-quant parity PPL
- exact model/tokenizer
- exact sliding-window settings and loss accounting
- profile equations and retention semantics
- 3-seed PCM/Organic retention on/off table
- commands and git SHA/diff stat
