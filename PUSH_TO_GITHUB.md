# Push To GitHub

SSH exact copy-paste block:

```bash
cd /home/qiaosir/projects/compute_vit/outputs/remote_github_handoff_YYYYMMDD_HHMMSS/compute_vit_remote_handoff
git init
git checkout -B remote-exploration
git add .
git commit -m "remote exploration handoff"
git remote remove origin 2>/dev/null || true
git remote add origin git@github.com:Leslie360/HAT.git
git push -u origin remote-exploration --force
```
