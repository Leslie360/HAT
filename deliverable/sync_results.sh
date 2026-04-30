#!/bin/bash
# Sync latest results from pipeline output to deliverable/
# Run this after Phase 3 finishes to pick up seed 123/456 results

OUT=/home/lisq753/projects/HAT_kv107/paper2/results/remote107
DELIV=./results_v2

echo "Syncing v2 eval results..."
cp "$OUT"/eval_hat_*_v2_*.json "$DELIV/" 2>/dev/null

echo "Syncing v2 train results..."
cp "$OUT"/hat_*_v2_seed*.json "$DELIV/" 2>/dev/null

echo "Done. Check for duplicates and commit."
