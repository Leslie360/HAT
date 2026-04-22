# Remote GitHub Push Guide

Use this guide if you want to upload a curated exploration mirror to GitHub rather than pushing the full working tree.

## Why

The current repository contains:
- internal coordination materials
- bulky logs
- private/raw-data-adjacent notes
- many experiment byproducts

For a remote GPU server, none of that is necessary. A curated mirror is safer and easier to reason about.

## Recommended approach

1. Generate the curated handoff directory:
```bash
bash scripts/export_remote_github_handoff.sh
```

2. Enter the generated directory and initialize a lightweight git repo:
```bash
cd outputs/remote_github_handoff_*/compute_vit_remote_handoff
git init
git branch -M remote-exploration
git add .
git commit -m "remote exploration handoff"
```

3. Push to your GitHub repository:
```bash
git remote add origin https://github.com/Leslie360/HAT.git
git push -u origin remote-exploration --force
```

## Copy-paste block

Use this exact block if you want a single copyable command sequence:

```bash
cd /home/qiaosir/projects/compute_vit/outputs/remote_github_handoff_20260421_110711/compute_vit_remote_handoff
git init
git checkout -B remote-exploration
git add .
git commit -m "remote exploration handoff"
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/Leslie360/HAT.git
git push -u origin remote-exploration --force
```

If you regenerate the handoff later, only the first `cd` line needs to change.

## SSH-ready exact block

If HTTPS asks for username/password or token, use SSH instead. Copy this block exactly:

```bash
cd /home/qiaosir/projects/compute_vit/outputs/remote_github_handoff_20260421_110711/compute_vit_remote_handoff
git init
git checkout -B remote-exploration
git add .
git commit -m "remote exploration handoff" || true
git remote remove origin 2>/dev/null || true
git remote add origin git@github.com:Leslie360/HAT.git
git push -u origin remote-exploration --force
```

## Step-by-step SSH commands

If you prefer to run one line at a time, use exactly these commands:

```bash
cd /home/qiaosir/projects/compute_vit/outputs/remote_github_handoff_20260421_110711/compute_vit_remote_handoff
```

```bash
git init
```

```bash
git checkout -B remote-exploration
```

```bash
git add .
```

```bash
git commit -m "remote exploration handoff" || true
```

```bash
git remote remove origin 2>/dev/null || true
```

```bash
git remote add origin git@github.com:Leslie360/HAT.git
```

```bash
git push -u origin remote-exploration --force
```

## What the remote server should read first

After clone/pull, point the remote agent to:

1. `docs/REMOTE_SERVER_GITHUB_HANDOFF.md`
2. `report_md/_gpt/GPU_REMOTE_EXPLORATION_BRIEF_20260421.md`
3. `report_md/_gpt/GPU_EXTERNAL_TASKLIST_20260421.md`

## Why not push the current working tree

The main working tree is intentionally mixed:
- manuscript work
- archived coordination
- local outputs
- historical experiment traces

Pushing that as-is creates avoidable review and privacy risk.
