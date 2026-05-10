#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"

rm "$ROOT/auto_fitted_profile.json"
mv "$ROOT/device_profiles/auto_fitted_profile.json" "$ROOT/auto_fitted_profile.json"

rm "$ROOT/download_data.sh"
mv "$ROOT/scripts/download_data.sh" "$ROOT/download_data.sh"
