#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT_DIR="${1:-$ROOT/outputs/remote_github_handoff_$STAMP}"
PKG_DIR="$OUT_DIR/compute_vit_remote_handoff"
MANIFEST="$PKG_DIR/HANDOFF_MANIFEST.txt"

mkdir -p "$PKG_DIR"
: > "$MANIFEST"

copy_path() {
  local rel="$1"
  if [[ ! -e "$ROOT/$rel" ]]; then
    echo "SKIP missing: $rel" >&2
    return 0
  fi
  mkdir -p "$PKG_DIR/$(dirname "$rel")"
  cp -a "$ROOT/$rel" "$PKG_DIR/$rel"
  printf '%s\n' "$rel" >> "$MANIFEST"
}

copy_many() {
  local rel
  for rel in "$@"; do
    copy_path "$rel"
  done
}

# Root files
copy_many \
  "README.md" \
  "LICENSE" \
  "environment.yml" \
  "requirements.txt" \
  "requirements-optional.txt" \
  "repo_bootstrap.py"

# Core code
copy_many \
  "analog_layers.py" \
  "analog_layers_ensemble.py" \
  "device_profile_utils.py" \
  "inference_analysis_utils.py" \
  "physical_noise_pipeline.py" \
  "train_tinyvit.py" \
  "train_tinyvit_ensemble.py" \
  "train_convnext.py" \
  "train_resnet18.py" \
  "eval_measured_profile.py" \
  "eval_imagenet_analog.py"

# Remote handoff docs
copy_many \
  "docs/README.md" \
  "docs/REMOTE_SERVER_GITHUB_HANDOFF.md" \
  "report_md/_gpt/INDEX.md" \
  "report_md/_gpt/AGENT_SYNC_gpt.md" \
  "report_md/_gpt/GPU_REMOTE_EXPLORATION_BRIEF_20260421.md" \
  "report_md/_gpt/GPU_EXTERNAL_TASKLIST_20260421.md" \
  "report_md/_gpt/REMOTE_GITHUB_UPLOAD_MANIFEST_20260421.md"

# Selected theory/context memos that help route-finding.
copy_many \
  "report_md/_gpt/GEMINI_STRUCTURAL_LIMIT_FORMAL_20260420.md" \
  "report_md/_gpt/GEMINI_HIGHER_ORDER_NL_DESIGN_20260420.md" \
  "report_md/_gpt/GEMINI_PATHWAY_DECOMPOSITION_20260420.md" \
  "report_md/_gpt/GEMINI_FIRST_ORDER_LIMIT_20260420.md" \
  "report_md/_gpt/GEMINI_REWRITE_DECISION_TREE_20260420.md"

# Runtime scripts
copy_many \
  "scripts/_gpt/check_locked_numbers.py" \
  "scripts/_gpt/run_tinyvit_groupwise_nl_comp.py" \
  "scripts/_gpt/eval_joint_fresh_instance.py" \
  "scripts/_gpt/eval_spatially_correlated_d2d.py" \
  "scripts/_gpt/eval_heavy_tailed_d2d.py" \
  "scripts/_gpt/retention_comparison_gpt.py" \
  "scripts/run_public_smoke_test.sh"

# Small prior JSONs only.
copy_many \
  "report_md/_gpt/json_gpt/qkv_only_linearization.json" \
  "report_md/_gpt/json_gpt/full_attn_linearization.json" \
  "report_md/_gpt/json_gpt/joint_mlp_linear_ensemble_hat_full_fresh.json" \
  "report_md/_gpt/json_gpt/cx_j2_results.json" \
  "report_md/_gpt/json_gpt/cx_j3_results.json" \
  "report_md/_gpt/json_gpt/cx_j4_results.json" \
  "report_md/_gpt/json_gpt/cx_j5_results.json" \
  "report_md/_gpt/json_gpt/cx_j6_results.json" \
  "report_md/_gpt/json_gpt/cx_j7_results.json" \
  "report_md/_gpt/json_gpt/cx_j8_results.json"

# Optional skeleton/thesis context
copy_many \
  "paper/paper2/skeleton_v0/README.md" \
  "paper/paper2/skeleton_v0/01_intro.md" \
  "paper/paper2/skeleton_v0/02_related.md" \
  "paper/paper2/skeleton_v0/03_methods.md" \
  "paper/paper2/skeleton_v0/04_experiments.md" \
  "paper/thesis_cn/chapter_7_deployment.tex"

cat > "$PKG_DIR/README_REMOTE_GITHUB.md" <<'EOF'
# Remote GitHub Mirror

This package is a curated mirror for remote GPU exploration.

Read in this order:
1. `docs/REMOTE_SERVER_GITHUB_HANDOFF.md`
2. `report_md/_gpt/GPU_REMOTE_EXPLORATION_BRIEF_20260421.md`
3. `report_md/_gpt/GPU_EXTERNAL_TASKLIST_20260421.md`
4. `report_md/_gpt/INDEX.md`

This mirror is not the full research repository. It intentionally excludes:
- raw private data
- bulky logs
- most checkpoints
- internal archives
- manuscript rewrite targets frozen by Rule B

The remote side should return markdown summaries and short diff snippets, not large artifacts.
EOF

cat > "$PKG_DIR/PUSH_TO_GITHUB.md" <<'EOF'
# Push To GitHub

Suggested workflow:

```bash
cd compute_vit_remote_handoff
git init
git branch -M remote-exploration
git add .
git commit -m "remote exploration handoff"
git remote add origin https://github.com/Leslie360/HAT.git
git push -u origin remote-exploration --force
```

If you prefer not to touch the main repository history, create a separate temporary local clone and push this curated mirror there.
EOF

echo "Created remote GitHub handoff directory:"
echo "  $PKG_DIR"
echo
echo "Manifest:"
echo "  $MANIFEST"
echo
echo "Included file count:"
wc -l < "$MANIFEST"
