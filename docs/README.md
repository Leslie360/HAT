# Documentation Index

This directory collects the stable project-facing documentation that should
survive beyond temporary coordination and drafting artifacts.

## Core Guides

- `DEVICE_PROFILE_GUIDE.md`
  - How to define, validate, and interpret device profile JSON files.
- `EXPERIMENT_REGISTRY.md`
  - Canonical experiment families, naming discipline, and reporting rules.
- `PHYSICS_STACK.md`
  - What the simulator models, what it approximates, and what remains out of scope.

## How To Use These Docs

- Start with `EXPERIMENT_REGISTRY.md` if you need to decode experiment IDs such
  as `V4`, `C4`, `Task 34`, or `Task 37`.
- Read `PHYSICS_STACK.md` before interpreting results as physically predictive;
  it lists the first-order assumptions and the major missing effects.
- Use `DEVICE_PROFILE_GUIDE.md` when adding a new literature-derived or
  measured-device profile.

## Scope Boundary

These documents are intended to remain useful after release preparation.
Temporary collaboration logs, handoff notes, and draft audit files should not
be treated as canonical end-user documentation.
