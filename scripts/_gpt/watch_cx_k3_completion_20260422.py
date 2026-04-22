#!/usr/bin/env python3
import json
import os
import signal
import subprocess
import time
from pathlib import Path

PID = 1735310
REPO = Path('/home/qiaosir/projects/compute_vit')
MAIN_LOG = REPO / 'logs/_gpt/cx_k3_continuation_driver_20260421.log'
OUT_JSON = REPO / 'report_md/_gpt/json_gpt/cx_k3_dgeff_continuation.json'
OUT_MD = REPO / 'report_md/_gpt/CODEX_CX_K3_CONTINUATION_20260421.md'
WATCH_LOG = REPO / 'logs/_gpt/watch_cx_k3_completion_20260422.log'
STAMP = REPO / 'report_md/_gpt/CX_K3_CONTINUATION_FINAL_STATUS_20260422.md'

WATCH_LOG.parent.mkdir(parents=True, exist_ok=True)
STAMP.parent.mkdir(parents=True, exist_ok=True)

with WATCH_LOG.open('a', encoding='utf-8') as f:
    f.write(f"[{time.strftime('%F %T %Z')}] python completion watcher armed pid={PID}\n")

while True:
    try:
        os.kill(PID, 0)
        time.sleep(60)
    except ProcessLookupError:
        break

with WATCH_LOG.open('a', encoding='utf-8') as f:
    f.write(f"[{time.strftime('%F %T %Z')}] target pid drained\n")

for _ in range(20):
    if OUT_JSON.exists():
        break
    time.sleep(15)

lines = []
lines.append('# CX-K3 Continuation Final Status')
lines.append('')
lines.append(f'- Timestamp: {time.strftime("%F %T %Z")}')
lines.append(f'- Target PID: {PID}')
lines.append(f'- Aggregate JSON present: {"yes" if OUT_JSON.exists() else "no"}')
lines.append(f'- Aggregate MD present: {"yes" if OUT_MD.exists() else "no"}')
lines.append('')
lines.append('## Driver Tail')
lines.append('')
lines.append('```text')
if MAIN_LOG.exists():
    tail = subprocess.run(['tail', '-n', '100', str(MAIN_LOG)], capture_output=True, text=True).stdout
    lines.append(tail.rstrip())
lines.append('```')
if OUT_JSON.exists():
    lines.append('')
    lines.append('## Aggregate JSON Head')
    lines.append('')
    lines.append('```json')
    try:
        text = OUT_JSON.read_text(encoding='utf-8')
        lines.append('\n'.join(text.splitlines()[:160]))
    except Exception as e:
        lines.append(json.dumps({'error': str(e)}))
    lines.append('```')
STAMP.write_text('\n'.join(lines) + '\n', encoding='utf-8')
with WATCH_LOG.open('a', encoding='utf-8') as f:
    f.write(f"[{time.strftime('%F %T %Z')}] wrote {STAMP}\n")
