# Perplexity Targeted Citation Prompts

## Current Status

- The paper-level library in `/paper/参考文献库.md` already contains roughly 50 references.
- The current LaTeX manuscript actively cites 18 keys.
- The issue is **not** "too few references overall."
- The issue is that some high-value background/support slots could still be strengthened if we want a denser journal-style literature frame.

## Highest-Value Missing Citation Buckets

If we expand citations, do it selectively in these buckets:

1. organic optoelectronic device papers that explicitly connect device metrics to network-level implications
2. optical non-uniformity / optical crosstalk in optoelectronic synaptic arrays
3. IR drop / sneak-path / interconnect overhead in analog crossbar CIM
4. ViT / attention acceleration papers that justify why dynamic attention remains digital
5. temperature sensitivity in organic semiconductor synaptic devices

## Prompt 1: Optical Non-Uniformity / Crosstalk

```text
I am writing a paper on organic optoelectronic compute-in-memory inference for edge vision.
I need 3-5 primary-source papers specifically about optical non-uniformity, optical crosstalk, or illumination-induced spatial correlation in optoelectronic synaptic devices / phototransistor arrays / optoelectronic neuromorphic arrays.

Please prioritize papers that contain:
- array-level measurements
- spatial non-uniformity maps or device-to-device optical response variation
- crosstalk between neighboring pixels/synapses
- implications for computation or recognition accuracy

For each paper, provide:
1. full citation
2. DOI / link
3. what exact phenomenon it supports
4. one sentence I could use in a limitations section
5. figure / table / section where the evidence appears

Do not give generic reviews unless no primary papers exist.
```

## Prompt 2: IR Drop / Sneak Path / Interconnect Overhead

```text
I need 5 strong references for a CIM paper to support a limitations discussion about:
- IR drop in analog crossbar arrays
- sneak-path currents
- interconnect / routing overhead between analog arrays and digital logic

Please prioritize compute-in-memory / PIM papers, especially those with quantitative impact on:
- accuracy
- energy
- latency
- scaling behavior with array size

For each paper, provide:
1. full citation
2. DOI / link
3. the main quantified takeaway
4. whether it is most relevant to IR drop, sneak path, or interconnect overhead
5. a short sentence I can use in the manuscript
```

## Prompt 3: Why Dynamic Attention Stays Digital

```text
I need 4-6 strong papers about Vision Transformer / attention acceleration on PIM or CIM systems.
My goal is to support the statement that dense static projections map well to analog arrays, but dynamic attention products (QK^T, AV, softmax) remain harder to analogize and often stay digital or require special treatment.

Please prioritize papers that discuss:
- ViT-on-PIM / ViT accelerators
- operator partitioning
- why QK^T / AV / softmax are difficult
- utilization or data-movement arguments

For each paper, provide:
1. full citation
2. DOI / link
3. the key design conclusion
4. whether it supports keeping attention digital, partially digital, or specialized mixed-signal
5. a short sentence that could fit a methodology or discussion section
```

## Prompt 4: Temperature Effects in Organic Synaptic Devices

```text
I need 3-5 primary-source papers on temperature sensitivity in organic synaptic devices, organic electrochemical transistors, organic phototransistors, or related organic neuromorphic hardware.

I want evidence for statements like:
- threshold voltage / mobility changes with temperature
- retention or conductance drift changes with temperature
- optoelectronic response changes with temperature

For each paper, provide:
1. full citation
2. DOI / link
3. exact device/material system
4. which measured quantity is temperature-sensitive
5. one sentence I can use in a limitations section
```
