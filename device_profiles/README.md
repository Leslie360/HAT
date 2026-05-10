# device_profiles/

Canonical small JSON device profiles used by the framework.

## Current files

| File | Role | Status |
|:--|:--|:--|
| `literature_profiles_gpt.json` | Literature-derived device profile library | active |
| `synthetic_profiles_gpt.json` | Synthetic profile examples | active/reference |
| `example_measured_device_profile_gpt.json` | Example measured-device profile format | active/reference |

`auto_fitted_profile.json` now lives here with a root compatibility symlink at `../auto_fitted_profile.json`.

## Rules

- Every profile should state source, units, and intended experiment lane when possible.
- Measured/raw data belongs in `data_local/raw_device_data/` or archive, not here.
- Derived profiles belong here only if small, canonical, and documented.
