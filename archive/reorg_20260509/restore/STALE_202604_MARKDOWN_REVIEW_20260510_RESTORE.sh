#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SRC="$ROOT/archive/stale_markdown_202604_review_20260510"

mkdir -p "$ROOT/report_md/_gpt" "$ROOT/thesis/cn" "$ROOT/report_md/_gpt/data_releases"

mv "$SRC/report_md_reviewer_response/reviewer_response" "$ROOT/report_md/_gpt/reviewer_response"
mv "$SRC/thesis_cn_agent_notes/KIMI_THESIS_CN_TEMPLATE_20260420.md" "$ROOT/thesis/cn/KIMI_THESIS_CN_TEMPLATE_20260420.md"
mv "$SRC/report_md_data_releases/fig4_source_data_README.md" "$ROOT/report_md/_gpt/data_releases/fig4_source_data_README.md"

rmdir "$SRC/report_md_reviewer_response" "$SRC/thesis_cn_agent_notes" "$SRC/report_md_data_releases" "$SRC" 2>/dev/null || true
