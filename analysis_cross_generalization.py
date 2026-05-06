#!/usr/bin/env python3
"""Direction 4: C2C↔D2D cross-generalization analysis."""
import json, os, sys

OUT_DIR = "/home/lisq753/projects/HAT_kv107/paper2/results/remote107"
CKPT = os.path.join(OUT_DIR, "checkpoints")

def _fmt(x):
    s = str(x)
    if "." not in s: s += ".0"
    return s

def read_ppl(path):
    if os.path.isfile(path):
        try: return json.load(open(path)).get("ppl", None)
        except: return None
    return None

def avg_ppl(fmt, seeds):
    vals = [read_ppl(fmt % s) for s in seeds]
    vals = [v for v in vals if v is not None]
    return sum(vals)/len(vals) if vals else None

D2D_SEEDS = [42, 123, 456, 789, 1001]

print("=" * 70)
print("DIRECTION 4: C2C ↔ D2D CROSS-GENERALIZATION ANALYSIS")
print("=" * 70)

# ── Section 1: Full-layer models ──
print("\n" + "-" * 70)
print("1. FULL-LAYER MODELS (all 24 analog layers)")
print("-" * 70)

models = [
    # (label, ckpt_basename, training_noise)
    ("D2D-only (σd=0.02)", "hat_d2d002_500_v2_seed42", "D2D"),
    ("C2C-only (σc=0.01)", "hat_c2c001_500_v2_seed42", "C2C"),
    ("Combined (σd=0.02/σc=0.01)", "combined_sweep_d2d02_c2c01_v2_seed42", "both"),
]

rows = []
for label, bn, train_type in models:
    # clean
    clean = read_ppl(os.path.join(OUT_DIR, "eval_%s_c2c0.0_d2d0.0_seed42.json" % bn))

    # C2C-only eval (σc=0.01)
    c2c = read_ppl(os.path.join(OUT_DIR, "eval_%s_c2c0.01_d2d0.0_seed42.json" % bn))

    # D2D eval (σd=0.02, same-instance = seed42)
    d2d_same = read_ppl(os.path.join(OUT_DIR, "eval_%s_c2c0.0_d2d0.02_seed42.json" % bn))

    # D2D eval (σd=0.02, cross-instance = 5 seeds)
    d2d_cross = avg_ppl(os.path.join(OUT_DIR, "eval_%s_c2c0.0_d2d0.02_seed%%d.json" % bn), D2D_SEEDS)

    # D2D_strong eval (σd=0.05, cross-instance = 5 seeds)
    d2d_strong = avg_ppl(os.path.join(OUT_DIR, "eval_%s_c2c0.0_d2d0.05_seed%%d.json" % bn), D2D_SEEDS)

    rows.append((label, clean, c2c, d2d_same, d2d_cross, d2d_strong))

print("%-36s %-8s %-8s %-10s %-10s %-8s" % ("Model", "clean", "C2C", "D2Dsame", "D2Dcross", "D2Dstr"))
print("-" * 90)
for label, clean, c2c, same, cross, strong in rows:
    def p(v): return "%.1f" % v if v is not None else "?"
    print("%-36s %-8s %-8s %-10s %-10s %-8s" % (label, p(clean), p(c2c), p(same), p(cross), p(strong)))

print("\n  → D2D-only model under C2C noise:", end="")
d2d_under_c2c = rows[0][2]
print(" PPL=%.1f (clean: %.1f, △=%.1f)" % (d2d_under_c2c, rows[0][1], d2d_under_c2c - rows[0][1]))
print("  → C2C-only model under D2D_strong noise:", end="")
c2c_under_d2ds = rows[1][5]
print(" PPL=%.1f (clean: %.1f, △=%.1f)" % (c2c_under_d2ds, rows[1][1], c2c_under_d2ds - rows[1][1]))
print("  → Combined model under D2D_strong:", end="")
comb_d2ds = rows[2][5]
print(" PPL=%.1f (clean: %.1f, △=%.1f)" % (comb_d2ds, rows[2][1], comb_d2ds - rows[2][1]))

# ── Section 2: Selective models ──
print("\n" + "-" * 70)
print("2. SELECTIVE MODELS (last2 = layers 22-23)")
print("-" * 70)

selective_models = [
    ("D2D last2 (σd=0.02)", "combined_layerlast2_v2_seed42", "D2D"),
    ("High-sigma last2 (σd=0.10)", "highsigma_d2d10_c2c01_v2_seed42", "D2D"),
    ("Combined last2 (σd=0.02/σc=0.01)", "combined_layerlast2_v2_seed42", "both"),
]

# Actually combined last2 uses combined noise for training
# D2D last2 = sigma sweep but only last2 layers — wait, we didn't train D2D-only last2.
# The combined_layerlast2 was trained with combined noise (σd=0.02, σc=0.01).
# The highsigma models are all last2.
# We don't have a D2D-only last2 model trained at σd=0.02.

# Let me adjust: we have combined_layerlast2 (combined noise) and highsigma models (combined noise, higher sigma)
# We can compare full-layer vs selective across training types.

print("\nSelective models all use combined noise (σd=0.02/σc=0.01) during training.")
print("Comparing full-layer vs selective under cross-type evaluation:\n")

compare = [
    ("Full-layer combined", "combined_sweep_d2d02_c2c01_v2_seed42", "full"),
    ("Selective last2", "combined_layerlast2_v2_seed42", "last2"),
    ("Selective last1", "combined_layerlast1_v2_seed42", "last1"),
]

for label, bn, _ in compare:
    clean = read_ppl(os.path.join(OUT_DIR, "eval_%s_c2c0.0_d2d0.0_seed42.json" % bn))
    c2c = read_ppl(os.path.join(OUT_DIR, "eval_%s_c2c0.01_d2d0.0_seed42.json" % bn))
    d2d_weak = avg_ppl(os.path.join(OUT_DIR, "eval_%s_c2c0.0_d2d0.02_seed%%d.json" % bn), D2D_SEEDS)
    d2d_strong = avg_ppl(os.path.join(OUT_DIR, "eval_%s_c2c0.0_d2d0.05_seed%%d.json" % bn), D2D_SEEDS)
    combined = avg_ppl(os.path.join(OUT_DIR, "eval_%s_c2c0.01_d2d0.02_seed%%d.json" % bn), D2D_SEEDS)
    print("  %-22s clean=%.1f C2C=%.1f D2Dw=%.1f D2Ds=%.1f comb=%.1f" % (label, clean, c2c, d2d_weak, d2d_strong, combined))

# ── Section 3: Cross-type degradation matrix ──
print("\n" + "-" * 70)
print("3. DEGRADATION MATRIX (△PPL from clean)")
print("-" * 70)
print("\nShows how much each training type degrades under each eval noise:")
print("%-28s %-8s %-8s %-8s %-8s" % ("Training →", "clean", "C2C", "D2Dw", "D2Ds"))
print("-" * 60)

for label, bn, train_type in models:
    clean = read_ppl(os.path.join(OUT_DIR, "eval_%s_c2c0.0_d2d0.0_seed42.json" % bn))
    if clean is None: continue

    c2c_val = read_ppl(os.path.join(OUT_DIR, "eval_%s_c2c0.01_d2d0.0_seed42.json" % bn))
    d2dw = avg_ppl(os.path.join(OUT_DIR, "eval_%s_c2c0.0_d2d0.02_seed%%d.json" % bn), D2D_SEEDS)
    d2ds = avg_ppl(os.path.join(OUT_DIR, "eval_%s_c2c0.0_d2d0.05_seed%%d.json" % bn), D2D_SEEDS)

    def delta(v):
        return "+%.1f" % (v - clean) if v else "?"
    print("%-28s %-8s %-8s %-8s %-8s" % (label, "%.1f" % clean, delta(c2c_val), delta(d2dw), delta(d2ds)))

# Combined last2 and high sigma
print("\nSelective models:")
for label, bn, _ in compare:
    clean = read_ppl(os.path.join(OUT_DIR, "eval_%s_c2c0.0_d2d0.0_seed42.json" % bn))
    if clean is None: continue
    c2c_val = read_ppl(os.path.join(OUT_DIR, "eval_%s_c2c0.01_d2d0.0_seed42.json" % bn))
    d2dw = avg_ppl(os.path.join(OUT_DIR, "eval_%s_c2c0.0_d2d0.02_seed%%d.json" % bn), D2D_SEEDS)
    d2ds = avg_ppl(os.path.join(OUT_DIR, "eval_%s_c2c0.0_d2d0.05_seed%%d.json" % bn), D2D_SEEDS)
    def delta(v):
        return "+%.1f" % (v - clean) if v else "?"
    print("%-28s %-8s %-8s %-8s %-8s" % (label, "%.1f" % clean, delta(c2c_val), delta(d2dw), delta(d2ds)))

# ── Section 4: C2C noise sweep on C2C-checkpoints (from Phase 7) ──
print("\n" + "-" * 70)
print("4. C2C TRAINING NOISE SWEEP — generalization across C2C eval levels")
print("-" * 70)

c2c_ckpts = [
    ("C2C σc=0.005", "hat_c2c0005_500_v2_seed42"),
    ("C2C σc=0.010", "hat_c2c001_500_v2_seed42"),
    ("C2C σc=0.020", "hat_c2c002_500_v2_seed42"),
    ("C2C σc=0.030", "hat_c2c003_500_v2_seed42"),
]

eval_levels = [0.000, 0.005, 0.010, 0.015, 0.020, 0.025, 0.030]

print("%-20s" % "Train σc↓", end="")
for ec in eval_levels:
    print(" %-6s" % ("e%.3f" % ec), end="")
print()

for label, bn in c2c_ckpts:
    print("%-20s" % label, end="")
    for ec in eval_levels:
        fname = "eval_%s_c2c%.3f_d2d0.0_seed42.json" % (bn, ec)
        ppl = read_ppl(os.path.join(OUT_DIR, fname))
        if ppl:
            print(" %-6s" % "%.1f" % ppl, end="")
        else:
            print(" %-6s" % "?", end="")
    print()

print("\n" + "=" * 70)
print("KEY FINDINGS")
print("=" * 70)
print("""
1. Does D2D training help with C2C noise? → Check D2D model eval'd under C2C
2. Does C2C training help with D2D noise? → Check C2C model eval'd under D2D
3. Is combined training strictly better than single-noise?
4. Do selective models show different cross-generalization patterns?
""")
