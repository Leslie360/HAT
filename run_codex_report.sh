#!/bin/bash
# Run this script directly in terminal to generate Codex report
# It takes ~2-3 minutes

cd /home/qiaosir/projects/compute_vit

cat << 'PROMPT' > /tmp/codex_report_prompt.txt
Write a detailed expert review report in markdown format for a post-fix TinyViT analog CIM rerun on CIFAR-10.

Three experiments under severe NL=2.0:
1. Ensemble HAT (uniform noise, epoch-resampled D2D): fresh eval = 81.69±0.64% (10 instances × 5 MC)
2. Standard HAT (uniform noise, fixed D2D): fresh eval = 82.63±0.56% (10 instances × 5 MC)
3. Proportional HAT (proportional noise, epoch-resampled D2D): fresh eval = 90.88±0.11% (10 instances × 5 MC)

Requirements:
- 1000+ words
- Markdown headings
- Comparison table
- Arithmetic verification
- Statistical significance assessment
- Train/eval gap analysis
- Code correctness assessment
- Comparison to prior art (pre-fix 86.37% was buggy)
- Risks and limitations
- Verdict per experiment (High/Medium/Low trustworthiness)
- Manuscript phrasing recommendations
- Overall recommendation

Start with a clear title.
PROMPT

echo "Starting Codex report generation (takes ~2-3 mins)..."
codex exec "$(cat /tmp/codex_report_prompt.txt)" > /tmp/codex_raw.txt 2>&1

# Extract report content
tail -n +$(grep -n "^codex$" /tmp/codex_raw.txt | tail -1 | cut -d: -f1) /tmp/codex_raw.txt | tail -n +2 > CODEX_FULL_REPORT_20260424.md 2>/dev/null || cp /tmp/codex_raw.txt CODEX_FULL_REPORT_20260424.md

echo "Done! Report saved to: $(pwd)/CODEX_FULL_REPORT_20260424.md"
wc -l CODEX_FULL_REPORT_20260424.md
