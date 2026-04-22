# G-GG5: Paper-2 Architectural Memo
**Date**: 2026-04-20

## Route R-A: Structural Limits of Attention
**Title Concept**: "Attention is Not All You Need (for Analog): Fundamental Limits of Transformer Mapping on Non-Ideal Crossbars"
**Core Idea**: A deep dive into *why* the ~30% ceiling exists. We transition from "here is a simulator" (Paper 1) to "here is a fundamental theoretical limit of CIM Transformers" (Paper 2).
**Methodology**: Theory-first. We derive the condition number of the analog softmax, then back it up with empirical diagnostics (the CX-J1b/c/d series).
