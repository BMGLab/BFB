# Lecture Companion

Complete slide text in a searchable, accessible format. Each module includes core content, a worked example, a formative checkpoint and an optional extension.

# W00 | The biology and numbers bridge

What exactly does a biological measurement measure?

## Outcomes

- Distinguish DNA, a gene, RNA and a protein.
- Read a small matrix and calculate a fraction.
- Separate a biological question from the available measurement.

## Biological bridge
No previous genetics or programming is required. Start with one cell, one sequence and one table.

## From organism to sequence

- Organism: the whole biological system.
- Cell: a compartment containing molecules and processes.
- DNA: a sequence that stores heritable information.

Sources: S01

## A gene is not the same as a protein

- A gene is a genomic region associated with a functional product.
- Some genes produce functional RNAs, not proteins.
- Protein-coding genes can give rise to different transcript isoforms.

Sources: S01

## The measurement ladder

- DNA sequence: which bases are present?
- RNA measurement: which transcripts were detected, and how much?
- Protein / function assay: which molecule or activity was measured?

Sources: S01

## Reading a short DNA sequence

- DNA is written with A, C, G and T; RNA uses U instead of T.
- Sequences have direction: label 5-prime and 3-prime ends.
- An unknown base N is not a fifth ordinary DNA base.

```text
ATGCCATN
```

Sources: S01

## Exons, introns and transcripts

- An RNA precursor can include introns that are removed by splicing.
- Exons are retained in a mature transcript; not every exon base is translated.
- Alternative splicing can produce different transcripts from one gene.

Sources: S01

## Translation is a reading-frame problem

- For an appropriate coding sequence, three RNA bases make a codon.
- AUG encodes methionine; UAA, UAG and UGA are stop codons in the standard code.
- Do not translate an arbitrary genomic interval and assume it is a protein.

```text
AUG | GCU | UAA
```

Sources: S01

## Rows, columns and units

- In this table: rows are genes; columns are samples.
- An entry is an observed count, not a number of patients.
- Always read the labels before doing arithmetic.

| Gene | Sample A | Sample B |
|---|---|---|
| G1 | 10 | 20 |
| G2 | 30 | 30 |
| G3 | 0 | 4 |

Sources: S10

## Ratios and logarithms without fear

- A change from 10 to 20 is a two-fold increase.
- log2(2) = 1; log2(1) = 0; log2(0.5) = -1.
- A denominator of zero needs an explicit rule, not a hidden fix.

| B / A | Meaning | log2 ratio |
|---|---|---|
| 2 | twice as large | +1 |
| 1 | unchanged | 0 |
| 0.5 | half as large | -1 |

## Worked example: what can we conclude?
Gene G1 has RNA counts 10 and 20 in two samples.
- The raw count ratio is 20 / 10 = 2.
- We have not checked sequencing depth or biological replication.
- The data do not yet establish increased protein abundance or a treatment effect.

## Checkpoint
A drug-treated sample has more RNA reads for an enzyme. Name one measurement that would test whether enzyme activity also increased.

### Debrief
An activity assay with matched controls and biological replicates would address activity. RNA alone is not that assay.

## Practical
Use the diagnostic sheet before Week 1. Any missed question directs you to a short bridge section; it does not reduce your grade.

## Optional extension
Optional: draw two different transcripts from the same three-exon gene.

---

# W01 | From a biological question to defensible evidence

Can we explain where every number came from?

## Outcomes

- Match a biological question to an assay and a data type.
- Run and save a small notebook without installing software.
- Distinguish a prediction, an observation and a justified claim.

## Biological bridge
Recall: genes can produce RNA or protein products; RNA counts are not direct protein measurements.

## Start with the question, not the software

- Question: does a treatment change the RNA abundance of selected genes?
- Measurement: RNA sequencing of independent biological samples.
- Claim limit: this experiment does not directly measure protein activity.

Sources: S01, S10

## One case will return all semester

- We study a fictional cell-culture response to a treatment.
- Tutorial data are synthetic unless the file says REAL EXCERPT.
- Known simulation truth lets us test an analysis; it is not a research discovery.

## Evidence has a chain of custody

- Biological sample -> laboratory assay -> raw file.
- Raw file -> processing steps -> table / figure.
- Table / figure -> interpretation, with limitations.

Sources: S10

## Gene counts are versioned answers

- GENCODE release 50 reports 19,442 protein-coding genes under its stated main-chromosome counting rule.
- Changing the annotation release or counting definition can change the answer.
- Record the release and definition; do not memorize one eternal total.

```text
19,442
```

Sources: S02

## Notebook = cells + a running memory

- Text cells explain; code cells calculate.
- The runtime remembers variables in execution order.
- Restart and run all checks whether the notebook works from a clean start.

Sources: S05

## Our scientific loop

- Predict what you expect before running the example.
- Run, compare with a control, and inspect a possible defect.
- Explain one result and one thing the result cannot establish.

## Reproducible is not automatically correct

- A fixed seed can reproduce a synthetic dataset.
- The same wrong method can reproduce the same wrong answer.
- A receipt or checksum checks consistency, not honesty or scientific truth.

Sources: S05

## AI is optional; responsibility is not

- You may ask for explanations or help reading an error where the task permits it.
- Record the tool, use and checks; no AI use is also a valid disclosure.
- Never paste patient data or classmates' submissions into a public service.

Sources: S20, S23

## Worked example: a traceable GC fraction
Toy DNA sequence: ACGTGC. Ignore no positions because all six bases are known.
- There are four G or C bases in six positions.
- GC fraction = 4 / 6 = 0.667, approximately 66.7%.
- The sequence is synthetic; GC content alone does not identify a species.

## Checkpoint
The same notebook gives 66.7% to two students. Is that proof they copied? What evidence would you inspect instead?

### Debrief
No. Identical answers can be correct, and small datasets can collide. Inspect the submitted work and reasoning; discuss concerns fairly rather than infer misconduct from a number.

## Practical
W01: run the setup, calculate GC on your assigned toy sequence, record a prediction and save a notebook plus a summary JSON.

## Optional extension
Optional: change the sequence by one base and predict how GC changes before running it.

---

# W02 | Files, coordinates and reference versions

Are these two files describing the same stretch of DNA?

## Outcomes

- Recognize the purpose of common biological file formats.
- Convert a positive-length interval between BED and one-based inclusive coordinates.
- Report an unknown reference build rather than guess.

## Biological bridge
A genome is a sequence; an annotation adds named features on a particular sequence version.

## Six file families; six jobs

- FASTA: sequence. FASTQ: sequence plus per-base quality.
- SAM/BAM: read alignments. BED: genomic intervals.
- GTF/GFF: annotated features. VCF: sequence variants.

| File | Primary question |
|---|---|
| FASTA / FASTQ | What sequence, with what quality? |
| SAM / BAM | Where did a read align? |
| BED / GTF / GFF | Where is an interval or feature? |
| VCF | What differs from the reference? |

Sources: S03, S04

## FASTA does not guarantee a reference build

- A header can give an identifier, but it may omit assembly metadata.
- Sequence names such as chr1 do not uniquely identify an assembly.
- Write unknown and request metadata when evidence is absent.

```text
>toy_contig
ACGTACGTAA
```

Sources: S03

## Two coordinate rulers

- One-based inclusive: first base is position 1; both endpoints count.
- BED: start is zero-based; the end is excluded.
- One-based [3, 7] and BED [2, 7) describe the same five bases.

Sources: S03, S04

## Keep the interval length invariant

- Inclusive length = end - start + 1.
- BED length = end - start.
- To convert a positive-length BED interval, add one to start only.

```text
BED [2, 7)  <->  inclusive [3, 7]
```

Sources: S03, S04

## Why adjacency is not overlap

- BED [0, 5) contains indices 0, 1, 2, 3, 4.
- BED [5, 8) contains indices 5, 6, 7.
- These intervals touch but share no base.

Sources: S04

## Reference version versus chromosome name

- GRCh37 and GRCh38 are different human assemblies.
- chr1 versus 1 can be a naming difference, not an assembly conversion.
- Renaming a chromosome does not lift coordinates between assemblies.

Sources: S03, S04

## Read text and binary formats carefully

- SAM text POS uses one-based positions.
- BAM stores coordinates internally using a different convention.
- A software API may expose zero-based values even when the input file is one-based.

Sources: S03

## GENOMES: your reusable audit card

- G: reference + annotation; E: environment + seed; N: dimensions.
- O: coordinates; M: multiplicity + independent unit.
- E: stable entities; S: sources. Use justified N/A where a check does not apply.

## Worked example: recover the same bases
Toy FASTA sequence ACGTACGTAA; select one-based positions 3 through 7.
- Inclusive length: 7 - 3 + 1 = 5.
- Equivalent BED interval: start 2, end 7.
- Python seq[2:7] returns GTACG, five bases.

## Checkpoint
Convert BED [4, 9) to one-based inclusive coordinates. Can a FASTA header reading only >chr1 prove GRCh38?

### Debrief
The interval is [5, 9], length 5. The header alone does not prove the assembly.

## Practical
W02: inspect toy FASTA, BED, GTF and VCF records; fix a start-coordinate error and record reference provenance.

## Optional extension
Optional: inspect how a VCF deletion includes an anchor base; no indel normalization is examined.

---

# W03 | Reading and checking short Python programs

Can a program run successfully and still answer the wrong question?

## Outcomes

- Trace assignment, a loop and a function on a short sequence.
- Explain what a function calculates in biological language.
- Use small tests to detect a denominator or boundary error.

## Biological bridge
GC fraction counts G and C bases among the bases your denominator actually includes.

## Value, name, update

- A variable is a name associated with a value.
- The equals sign in Python assigns; it does not assert a mathematical identity.
- Run the next line using the current value, not the previous one.

```text
count = 0
count = count + 1
print(count)
```

Sources: S05

## Lists and slices have boundaries

- Python starts list indices at zero.
- A slice includes its start but excludes its end.
- For seq = ACGTAC, seq[1:4] is CGT.

```text
seq = "ACGTAC"
print(seq[1:4])
```

Sources: S05

## A loop repeats a small operation

- Start with count = 0.
- For each base, ask whether it is G or C.
- Increase the count when the condition is true.

```text
count = 0
for base in "AGC":
    if base in "GC":
        count += 1
```

Sources: S05

## A function has a contract

- State its input, output and assumptions.
- Decide what an unknown base should do to the denominator.
- Decide what an empty sequence should return or reject.

Sources: S05

## Trace before you execute

- For AGC, the running counts are 0, 1, 2.
- The numerator is 2 and the denominator is 3.
- A trace table makes a hidden assumption visible.

| Base | GC? | Running count |
|---|---|---|
| A | No | 0 |
| G | Yes | 1 |
| C | Yes | 2 |

Sources: S05

## A deliberate bug: the wrong denominator

- Here N means unknown and should be excluded by the stated contract.
- The numerator ignores N but the denominator below includes it.
- The code runs; the biological definition is violated.

```text
seq = "GCNN"
wrong_gc = sum(b in "GC" for b in seq) / len(seq)
```

Sources: S05

## Tests should include awkward inputs

- All GC bases should give 1.0. All AT bases should give 0.0.
- GCNN should give 1.0 under our known-base definition.
- An empty or all-N sequence should be reported as undefined, not 0%.

| Input | Expected |
|---|---|
| GCGC | 1.0 |
| ATAT | 0.0 |
| GCNN | 1.0 |
| NN / empty | Undefined |

Sources: S05

## A traceback is a location clue

- Read the last line: what kind of error occurred?
- Read upward to the line in your notebook that triggered it.
- A failed test can be more informative than a clean run.

```text
NameError: name 'sequence' is not defined
# Check spelling and execution order.
```

Sources: S05

## Worked example: repair without rewriting
The function should calculate GC among A/C/G/T positions only.
- Make known = [b for b in seq.upper() if b in "ACGT"].
- Divide the GC count by len(known), not len(seq).
- Return None when known is empty; check GCNN and NN as controls.

## Checkpoint
A function returns 0.5 for GCNN. Under our contract, locate the error and predict the correct result.

### Debrief
The denominator includes the two unknown bases. There are two GC bases among two known positions, so the fraction is 1.0.

## Practical
W03: trace four inputs, compare a supplied buggy and corrected function, and explain one test in words. No program from scratch is required.

## Optional extension
Optional: write a new test for lower-case letters and explain why it matters.

---

# W04 | Sequence similarity without overclaiming

What does a good alignment tell us, and what does it not tell us?

## Outcomes

- Distinguish sequence identity, similarity and homology.
- Score a short alignment and interpret a local match.
- Read a BLAST hit using coverage, identity and E-value together.

## Biological bridge
DNA sequences and protein sequences use different alphabets; compare like with like.

## Similarity is observed; homology is inferred

- Identity counts identical aligned symbols.
- Similarity can use a scoring scheme that rewards related amino acids.
- Homology means common ancestry; do not report 70% homology.

Sources: S26

## Global and local answer different questions

- Global alignment compares full sequences under a scoring scheme.
- Local alignment finds a high-scoring matching segment.
- A short local match may cover only a small fraction of a protein.

Sources: S26, S28

## A scoring rule must be stated

- For our toy DNA alignment: match +2, mismatch -1, gap -2 per position.
- Scores from different rules are not directly interchangeable.
- A biological interpretation comes after the arithmetic.

```text
score = 2 x matches - mismatches - 2 x gaps
```

Sources: S28

## One exact local-alignment step

- Each cell considers a match/mismatch, a gap from either direction, or zero.
- Zero permits a local alignment to start fresh.
- The maximum is exact for this recurrence and scoring model, not proof of a biological mechanism.

```text
H[i,j] = max(0,
 H[i-1,j-1] + substitution,
 H[i-1,j] - 2, H[i,j-1] - 2)
```

Sources: S26, S28

## Why search tools use shortcuts

- A database may contain many sequences.
- BLAST uses seed-and-extend heuristics to find useful local matches efficiently.
- A heuristic may miss matches; its output still needs an audit.

Sources: S26

## Read three columns, not one

- Identity: how alike are aligned positions?
- Query coverage: how much of the query is represented?
- E-value: expected chance matches at least this strong under the search model.

| Hit | Identity | Coverage | E-value |
|---|---|---|---|
| A | 95% | 10% | 0.02 |
| B | 70% | 90% | 1e-30 |

Sources: S06

## The E-value depends on the search space

- For a comparable alignment score, a larger search space can increase the E-value.
- An E-value is not the chance the functional annotation is wrong.
- Also inspect low complexity, domains, identifiers and database provenance.

Sources: S06

## Three approaches can be combined

- Exact optimization solves a specified mathematical problem.
- Heuristics trade exhaustive search for speed.
- Learned representations depend on training data; a tool can contain all three.

Sources: S11, S26

## Worked example: score a short alignment
ACGT aligned to ACCT, with match +2 and mismatch -1.
- Positions 1, 2 and 4 match: 3 x 2 = 6.
- Position 3 mismatches: subtract 1.
- Total score = 5; identity = 3 / 4 = 75%.

## Checkpoint
Hit A has 95% identity across 10% of a protein; hit B has 70% identity across 90%. Which is the stronger starting point for a full-length relationship, and what still needs checking?

### Debrief
B covers far more of the query. Inspect domain architecture, alignment quality and provenance; neither hit alone proves identical function.

## Practical
W04: score a fixed alignment, fill a tiny local-alignment table using a supplied function, and audit two hypothetical search hits.

## Optional extension
Optional: inspect affine gap penalties and substitution matrices; deriving log-odds is not examined.

---

# W05 | From sample to reads: designing an experiment

How much sequencing is enough for the stated question?

## Outcomes

- Explain reads, read pairs, quality and depth.
- Calculate nominal and usable average depth with units.
- Choose a feasible design without confusing more reads with more replicates.

## Biological bridge
DNA sequencing measures sequence fragments; RNA sequencing samples molecules derived from RNA.

## A library is a prepared collection of molecules

- Samples are processed into a sequencing library.
- A read is a reported sequence from that library.
- PCR and technical duplication can create repeated observations of the same original material.

Sources: S03, S10

## Short and long reads are design choices

- Longer reads can span larger structures or transcript isoforms.
- Short-read workflows can be useful for many counting and variant questions.
- Choose using the assay question, sample quality and required evidence, not a vendor ranking.

Sources: S03, S10

## FASTQ links bases to quality

- A FASTQ record contains an identifier, sequence, separator and quality string.
- The number of base qualities should match the sequence length.
- Quality is about base-call error, not whether the biological conclusion is true.

```text
@toy_read
ACGT
+
IIII
```

Sources: S03

## Phred quality is a log-scale error measure

- Q = -10 log10(p_error).
- Q20 corresponds to p_error = 0.01; Q30 to 0.001.
- A quality score describes a model of base-call error; quality calibration matters.

| Q | Error probability |
|---|---|
| 20 | 1 / 100 |
| 30 | 1 / 1,000 |
| 40 | 1 / 10,000 |

Sources: S03

## Average depth is a budget calculation

- For N single reads of length L over target size G: C = N x L / G.
- For read pairs, count both sequenced ends in the base budget.
- This is nominal average depth; overlapping reads and duplicates complicate unique evidence.

```text
C = sequenced bases / target bases
```

Sources: S03

## Average is not the same as everywhere

- The same average depth can hide very different coverage distributions.
- Report the fraction of target positions reaching a threshold.
- No universal depth cutoff guarantees a clinically usable result.

Sources: S03

## Usable yield is smaller than purchased yield

- A toy usable fraction combines retention and duplicate assumptions.
- Keep assumptions explicit; duplicate rate can depend on library complexity.
- Sensitivity analysis: compare what happens when usable yield is lower than expected.

```text
usable depth = nominal depth x usable fraction
```

## Design Notebook 1: the decision, not a shopping list

- Choose target, independent samples and a sequencing budget.
- Compare two designs, including a control and one failure scenario.
- Defend a limited conclusion; all quoted classroom costs are hypothetical.

## Worked example: one million read pairs
1,000,000 pairs, 150 bases per end, target size 5,000,000 bases, usable fraction 0.80.
- Sequenced bases = 1,000,000 x 2 x 150 = 300,000,000.
- Nominal average depth = 300,000,000 / 5,000,000 = 60x.
- Toy usable depth = 60 x 0.80 = 48x; this is not guaranteed depth at every base.

## Checkpoint
Two libraries from the same donor each have 60x depth. How many donors were measured? What does sequencing both libraries more deeply fail to fix?

### Debrief
One donor. More technical observations do not add independent donors or establish between-donor variation.

## Practical
W05 / Project D1: select one of three fully specified budget scenarios, calculate depth, inspect a simulated coverage distribution and write a design justification.

## Optional extension
Optional: derive the ideal Poisson zero-coverage probability exp(-C), then explain why real coverage may violate that model.

---

# W06 | Variation, independence and multiple testing

What would this result look like if nothing biological had changed?

## Outcomes

- Identify the experimental unit and a confounded comparison.
- Interpret a p-value without calling it the probability the hypothesis is true.
- Apply a small BH correction and explain its limits.

## Biological bridge
Technical repeats share biological origins; more observations are not automatically more independent evidence.

## Variation has different sources

- Biological variation: independently sampled experimental units can differ.
- Technical variation: measurement or processing can vary.
- The design determines which differences can be attributed to treatment.

Sources: S07, S12

## Count independent units, not rows

- Three donors, each with 100 measured cells, still give three donors.
- For donor-level claims, uncertainty must account for donor-to-donor variation.
- Cells can be valid observations for other questions; name the question first.

Sources: S12

## Confounding is a design problem

- All treated samples in batch A and all controls in batch B confound treatment and batch.
- A statistical adjustment cannot create the missing comparison.
- Balance conditions across batches before data collection where feasible.

| Bad design | Better design |
|---|---|
| Batch A: treatment only | Batch A: treatment + control |
| Batch B: control only | Batch B: treatment + control |

Sources: S10, S11

## What a p-value actually asks

- Assume the stated null model and its assumptions.
- How probable are data at least as extreme by the chosen test statistic?
- It is not P(the null is true) and not a measure of effect size.

Sources: S07

## Effect, uncertainty and p answer different questions

- Effect size: how large is the estimated difference?
- Uncertainty interval: which values are compatible with the model and data?
- p-value: how incompatible is the chosen statistic with the null model?

Sources: S07

## Testing many nulls generates false positives

- For 1,000 valid null tests at alpha 0.05, expected false positives are 50.
- This expectation does not require all tests to be independent.
- The observed count varies; no single run must equal 50.

```text
1,000 x 0.05 = 50
```

Sources: S07, S08

## BH controls a family-level error quantity

- Sort p-values; compare p(i) with i x q / m.
- Select through the largest passing rank in the step-up rule.
- FDR is an expected false-discovery proportion under assumptions, not each gene's error probability.

| Rank | p | Threshold, q=0.05 |
|---|---|---|
| 1 | 0.001 | 0.0125 |
| 2 | 0.010 | 0.0250 |
| 3 | 0.040 | 0.0375 |
| 4 | 0.200 | 0.0500 |

Sources: S08

## A negative control tests the pipeline

- Simulate a known null or use an appropriate design-respecting permutation.
- Repeat the experiment rather than pick one convenient random seed.
- A control failing to reject does not prove every assumption is correct.

Sources: S07, S11

## Worked example: a four-test BH family
p = 0.001, 0.010, 0.040, 0.200; target FDR q = 0.05.
- BH thresholds are 0.0125, 0.0250, 0.0375, 0.0500.
- The largest passing rank is 2, so reject tests 1 and 2.
- Monotone adjusted p-values are 0.004, 0.020, about 0.0533, 0.200.

## Checkpoint
An analyst calls 100 cells per donor 100 independent replicates. There are two donors per condition. What is the donor-level sample size per condition?

### Debrief
Two donors per condition. Treating all cells as independent for that comparison is pseudoreplication and can underestimate uncertainty.

## Practical
W06: simulate uniformly distributed valid null p-values, compare raw and BH discoveries across repeated runs, and identify an intentionally wrong independence claim.

## Optional extension
Optional: show why dependence affects a multiple-testing guarantee; do not memorize a proof.

---

# W07 | RNA counts, normalization and defensible expression claims

When is a bigger count not evidence of higher expression?

## Outcomes

- Interpret a genes-by-samples count matrix and sample metadata.
- Calculate a toy TPM correctly and distinguish it from count-model input.
- Read a differential-expression summary without claiming protein function.

## Biological bridge
A gene may produce several transcripts; counts depend on what features and assignment rules were used.

## From RNA to a count matrix

- Reads are assigned to genes or transcripts using a stated reference and rule.
- Rows represent features; columns represent samples in our bulk RNA example.
- Sample metadata must match columns by identifier, not accidental order.

Sources: S10

## Counts depend on more than biology

- Library size changes how many molecules are sampled.
- Feature length and composition affect some counting summaries.
- Biological differences and technical biases require an explicit model.

Sources: S09, S10

## Normalization is not one universal operation

- Library-size scaling addresses a sampling-depth component.
- TPM divides by length and rescales within each sample in our toy example.
- For differential expression, use a method with its specified input and assumptions.

Sources: S09, S10

## Toy TPM: length first, sum second

- Divide each feature count by its length in kilobases.
- Sum these length-adjusted rates within the sample.
- Divide each rate by that sum and multiply by one million.

```text
TPM_i = (count_i / length_kb_i) / sum(rates) x 1,000,000
```

Sources: S10

## An invariant can catch the wrong calculation

- TPM should sum to one million within a non-empty sample.
- But sum-to-one-million alone does not prove the calculation is correct.
- Also compare an equal-abundance, unequal-length control.

| Feature | Count | Length kb | Rate |
|---|---|---|---|
| A | 100 | 1 | 100 |
| B | 200 | 2 | 100 |

Sources: S10

## DESeq2 is not a t-test on TPM

- A count model uses sample-level replication and its own normalization.
- Raw count-matrix workflows should not be fed TPM values.
- Approved transcript-quantifier import workflows are a separate route; follow their documentation.

Sources: S09, S10

## Fold change and evidence are separate axes

- log2 fold change describes the estimated direction and magnitude.
- Adjusted p-values address a family of tests under assumptions.
- Large effects can be uncertain; tiny effects can be statistically supported.

| Gene | log2 change | Adjusted p |
|---|---|---|
| Toy A | 2.0 | 0.30 |
| Toy B | 0.2 | 0.001 |

Sources: S07, S09

## A result table is not a mechanism

- RNA changes can reflect cell composition or regulation.
- Enrichment depends on the tested gene universe and annotation choices.
- State what additional protein, functional or replication evidence is needed.

Sources: S01, S09, S10

## Worked example: equal rates, unequal counts
Two toy features: A has 100 counts and length 1 kb; B has 200 counts and length 2 kb.
- Rates are 100 / 1 = 100 and 200 / 2 = 100.
- Their rate sum is 200.
- TPM values are 500,000 each; raw counts differ while length-adjusted rates are equal.

## Checkpoint
An analyst rounds TPM and passes it to a raw-count DESeq2 workflow. Why is this not repaired by rounding?

### Debrief
Rounding cannot reconstruct the original count sampling information or the intended count model. Use the documented raw-count or supported import workflow.

## Practical
W07: repair the TPM order-of-operations bug; then align sample metadata in a real two-gene pasilla excerpt. Do not perform DE on that excerpt.

## Optional extension
Optional: inspect median-of-ratios normalization and effective lengths; no dispersion derivation is assessed.

---

# W08 | Midterm review and the evidence audit

Can we find a claim that outruns the data?

## Outcomes

- Retrieve the foundational skills from Weeks 1-7.
- Classify a statement as supported, contradicted or not established.
- Replace an overclaim with a bounded scientific conclusion.

## Biological bridge
The midterm tests the floor: biology-to-data reasoning, coordinates, short code, depth and statistical interpretation.

## The midterm is about reasoning

- 60 minutes; structured questions; a supplied formula sheet.
- Show units, steps and a limited interpretation.
- No internet or AI during the paper; approved accommodations still apply.

## Retrieve: same interval, different notation

- BED [2, 7) has length 5.
- One-based inclusive [3, 7] describes the same bases.
- A missing assembly must be reported as unknown.

Sources: S03, S04

## Retrieve: count the independent origin

- Two donors with 200 cells each are two donors.
- A replicate label must name the biological unit.
- More sequencing cannot create a missing biological replicate.

Sources: S12

## Retrieve: normalize for the intended task

- Do not confuse observed counts with relative abundance.
- The denominator must match the calculation's definition.
- A successful run is not proof of an appropriate analysis.

Sources: S10

## Three evidence labels

- SUPPORTED: the supplied evidence supports this exact scope.
- CONTRADICTED: the evidence or definition conflicts with the claim.
- NOT ESTABLISHED: additional evidence is required.

## Audit the statement, not the writing style

- A fluent paragraph may mix correct facts with an invalid inference.
- Underline each factual claim and identify its evidence.
- Use tests and sources; do not use an AI-text detector as proof.

Sources: S23

## Worked audit: high counts, strong claim
Claim: Gene X has twice as many RNA reads in one treated sample, so the treatment doubles protein activity.
- The raw-count comparison is supplied evidence.
- The treatment effect lacks independent replication and normalization context.
- Protein activity was not measured; that conclusion is not established.

## Checkpoint
A report says: 1,000 cells from one donor prove the result generalizes to all adults. Assign an evidence label and propose a better sentence.

### Debrief
NOT ESTABLISHED. A better sentence is: this donor's measured cells show the reported pattern; generalization requires independent donors and an appropriate design.

## Practical
W08: audit six supplied statements after the midterm, attach evidence and correct two overclaims. The audit is a completion lab, not an extra exam.

## Optional extension
Optional: exchange one evidence audit with a peer and check whether you agree on the scope.

---

# W09 | Patterns, prediction and data leakage

Does the model recognize biology, or merely recognize the donor?

## Outcomes

- Distinguish clustering from supervised prediction.
- Split repeated observations by the intended independent unit.
- Read a confusion matrix and compare against a negative control.

## Biological bridge
A feature is a measured input; a label is the outcome being predicted. Rows from the same donor can share a signature.

## Two different questions

- Clustering groups observations using similarity without supplied class labels.
- Classification learns a mapping from features to known labels.
- A visual cluster is not automatically a cell type or a disease mechanism.

Sources: S11

## A projection is a view, not the complete data

- PCA summarizes directions of variation.
- UMAP emphasizes a neighborhood representation and depends on parameters.
- Distances between plotted islands do not automatically measure biological separation.

Sources: S11, S13

## Define the prediction target first

- Will the model be applied to another observation from a known donor?
- Or to a new donor, study, hospital or time period?
- The test split must represent the intended use.

Sources: S11

## Repeated donors can leak across a row split

- Near-duplicate observations can identify their donor.
- A row-level split may put the same donor in train and test.
- Keep all observations from a donor together for new-donor evaluation.

Sources: S11

## Preprocessing can leak too

- Split first. Fit scaling and feature selection on training data.
- Use the fitted transform on validation or test data.
- Do not choose a method by repeatedly inspecting the final test score.

Sources: S11

## Four counts explain a classifier

- True positive and false negative describe actual positives.
- False positive and true negative describe actual negatives.
- Sensitivity and specificity use different denominators.

Sources: S11

## Accuracy needs context

- If 95 of 100 samples are negative, always predicting negative gives 95% accuracy.
- But sensitivity is zero.
- Report the class balance, independent sample count and uncertainty.

```text
95% accuracy
```

Sources: S11

## A shuffled-label control respects the design

- For repeated donors, shuffle labels at donor level.
- Keep all observations of a donor assigned the same shuffled label.
- Repeat the control; chance-level performance varies in small test sets.

Sources: S11

## Worked example: read a confusion matrix
TP=8, FN=2, TN=9, FP=1; the test set contains 20 independent individuals.
- Sensitivity = 8 / (8 + 2) = 0.80.
- Specificity = 9 / (9 + 1) = 0.90.
- Accuracy = (8 + 9) / 20 = 0.85; balanced accuracy = (0.80 + 0.90) / 2 = 0.85.

## Checkpoint
A dataset contains six rows for each of 12 donors. A random row split gives 100% accuracy. What split would test performance on new donors?

### Debrief
Hold out whole donors so no donor is shared across train and test, then report donor-level performance and the small independent test size.

## Practical
W09 / Project D2: compare a deliberately leaky row split with an honest donor split, calculate confusion counts and run a donor-level permutation control.

## Optional extension
Optional: nested cross-validation and calibration; no neural-network training is required.

---

# W10 | Single cells and biological replication

Do more cells solve a shortage of donors?

## Outcomes

- Explain a cell-by-gene matrix, a barcode and a UMI.
- Separate exploratory markers from condition-level inference.
- Aggregate counts by donor and cell type and identify the independent sample size.

## Biological bridge
Bulk RNA-seq averages mixtures. Single-cell measurements can separate cell populations, but cells remain nested within samples.

## From a tissue to many cell profiles

- Cells or nuclei are captured and their RNA-derived molecules labeled.
- Cell barcodes identify capture compartments.
- UMIs help distinguish original molecules from amplification copies, subject to error and correction.

Sources: S12, S27

## The matrix has an orientation

- AnnData convention: observations are rows; variables are columns.
- For a typical single-cell dataset: cells x genes.
- Check what X and layers contain; never assume every matrix stores raw counts.

| Object | Meaning |
|---|---|
| obs | Cell / observation metadata |
| var | Gene / variable metadata |
| X or layers | A documented measurement or transform |

Sources: S13

## A zero is not proof of absence

- A molecule may not be captured or sequenced.
- Low counts can reflect biology, sampling or quality.
- Avoid claiming a gene is absent from a tissue based on a few zero entries.

Sources: S12, S27

## Quality control is contextual

- Inspect counts, detected genes, mitochondrial fraction and sample patterns.
- A universal mitochondrial cutoff is not appropriate for all tissues and protocols.
- Doublets and ambient RNA can distort cell profiles.

Sources: S27

## Clustering is a hypothesis generator

- A cluster depends on the representation and chosen resolution.
- Use multiple markers and sample context to propose a cell identity.
- A cluster label and a statistical significance claim are different things.

Sources: S12, S13, S27

## For condition comparisons, keep donor identity

- Many cells from one donor share biological and technical factors.
- Treating them as independent donors can underestimate uncertainty.
- Between-donor replication is essential for a donor-level comparison.

Sources: S12

## Pseudobulk retains the biological unit

- Within each donor and cell type, sum raw counts.
- The resulting columns or rows represent donor-cell-type samples.
- A count model can then represent the experimental design, including pairing when appropriate.

Sources: S09, S12

## Pseudobulk is not a magic rescue

- One donor per condition still lacks between-donor replication.
- Very few donors imply limited precision and power.
- A donor-aware mixed model is another possible approach; method choice depends on the question.

Sources: S12

## Worked example: aggregate, do not multiply donors
A cell type has counts [2,3] in donor A and [4,1,2] in donor B.
- Pseudobulk count for A = 5.
- Pseudobulk count for B = 7.
- There are two donor-cell-type samples, not five independent donors.

## Checkpoint
A study measures 10,000 cells from one control donor and one treated donor. Would doubling the cells enable a defensible population-level treatment comparison?

### Debrief
No. It improves within-donor sampling but does not add independent donors or estimate general between-donor variability.

## Practical
W10: aggregate a synthetic cell table, compare cell and donor sample sizes, and explain why a cell-level shortcut fails. The lab uses no AnnData installation.

## Optional extension
Optional: differential abundance and paired donor designs; no atlas integration pipeline is required.

---

# W11 | Biological AI and the honest model scorecard

Better than what, for which task, on which unseen data?

## Outcomes

- Explain an embedding and the difference between zero-shot use and fine-tuning.
- Compare a model with a simple baseline under a matched evaluation.
- Write a claim limited to the task, data and evidence actually tested.

## Biological bridge
Models see numerical representations of biological measurements. A useful representation does not itself establish a mechanism.

## An embedding is a numerical representation

- A sequence or cell profile can be represented by a vector of numbers.
- Nearby vectors may share patterns useful for a particular task.
- The numbers have no automatic biological interpretation.

Sources: S14, S15

## Pretraining and task adaptation are different

- Pretraining uses a broad dataset and a specified objective.
- Fine-tuning updates a model for another task using additional data.
- Zero-shot use does not perform task-specific model training.

Sources: S14, S15

## A biological example: scGPT

- scGPT is one published approach to pretrained single-cell representations.
- Its original study investigated several adapted downstream tasks.
- Those results do not establish success for every tissue or unseen setting.

Sources: S14

## Independent evaluation can ask a different question

- Kedzierska et al. tested zero-shot behavior of specified models and datasets.
- In some tested settings, simpler approaches performed better.
- This is not evidence that all biological foundation models always fail.

Sources: S15

## A fair comparison fixes the rules

- Use the same task, eligible inputs, evaluation split and metric.
- Include a simple baseline and explain training-data overlap where known.
- Separate validation choices from the final test.

Sources: S11, S15

## Record the score and what it leaves out

- Performance on held-out independent units.
- Data coverage, uncertainty, computation and failures.
- A stronger number on one dataset does not prove transfer to another.

Sources: S11, S15

## A virtual cell is a claim to unpack

- Which intervention, biological scale and outcome are modeled?
- Which predictions were checked experimentally or on independent data?
- What is outside the validated scope?

Sources: S14, S15

## Use the least complex sufficient method

- Complexity adds dependencies and opportunities for hidden failure.
- A small baseline is an informative comparator, not an embarrassment.
- Select the method supported by the evaluation and constraints.

Sources: S11, S15

## Worked example: a result with honest scope
A fictional scorecard gives baseline accuracy 0.78 and model accuracy 0.82 on 50 held-out donors.
- The observed difference is 0.04 on this test set.
- Uncertainty and paired errors are needed before declaring a reliable improvement.
- The result does not establish performance in another tissue or hospital.

## Checkpoint
Model A uses leaked donor rows and reports 0.95; model B holds out donors and reports 0.75. Can their scores rank the models fairly?

### Debrief
No. The evaluation targets differ. Re-evaluate on matched independent test units before comparing performance.

## Practical
W11 studio: complete a six-field model scorecard from supplied fictional results and two verified publication evidence cards. No model training or GPU is needed.

## Optional extension
Optional: sketch a domain-shift stress test without implementing a foundation model.

---

# W12 | Protein structures: prediction, confidence and function

What does a confident structure still fail to prove?

## Outcomes

- Distinguish sequence, structure and function.
- Interpret pLDDT and PAE without turning them into binding probabilities.
- Propose an experimental test for a structure-based hypothesis.

## Biological bridge
A protein is an amino-acid chain; its structure and interactions depend on sequence and biological context.

## Structure is one layer of evidence

- A sequence specifies an amino-acid chain.
- An experimental structure and a computational prediction have different provenance.
- Neither a picture nor a confidence score is itself a functional assay.

Sources: S01, S16, S17

## Proteins can have domains and flexible regions

- A domain is a structurally or functionally meaningful region.
- Flexible linkers may allow different arrangements.
- A single structure does not capture every state or partner.

Sources: S01, S16

## pLDDT is local model confidence

- AlphaFold pLDDT is a per-residue score on a 0-100 scale.
- Higher values generally indicate greater confidence in local structure.
- It is not the percent probability that a protein binds its target.

Sources: S16

## PAE asks about relative placement

- Predicted aligned error estimates positional error relative to an alignment reference.
- Low within-domain PAE and high between-domain PAE can indicate uncertain domain arrangement.
- Check units and the matrix axes.

Sources: S16

## Low confidence has several explanations

- It may reflect disorder, flexibility, missing context or a prediction error.
- Do not automatically label every low-score region disordered.
- Use complementary evidence and state alternatives.

Sources: S16

## A real database card, not a new experiment

- AF_AFP69905F1 is a computed hemoglobin alpha model.
- The RCSB record displayed 142 modeled residues and global pLDDT 98.06 when checked.
- The record explicitly distinguishes this model from experimental validation.

```text
98.06
```

Sources: S24

## An interaction score is not an affinity measurement

- Model confidence, geometric plausibility and binding affinity are different quantities.
- A predicted complex can motivate testing, not replace it.
- Binding and specificity need appropriate positive and negative experimental controls.

Sources: S16, S17

## The Structure Report Card

- Record sequence / accession and the model source.
- Describe local confidence and uncertain relative placement.
- Name the proposed use, a limitation and a validation experiment.

Sources: S16, S17

## Worked example: two confident domains
A toy protein has two domains with pLDDT near 90, a linker near 45 and between-domain PAE near 20 angstroms.
- Local domain geometry may be more reliable than the linker.
- Relative domain orientation is uncertain in this example.
- Do not design an interface hypothesis that assumes one exact orientation without further evidence.

## Checkpoint
A model has pLDDT 95. A report says there is a 95% chance that the protein binds a proposed target. What is wrong?

### Debrief
pLDDT is not a binding probability. The claim confuses local structural confidence with interaction evidence.

## Practical
W12 studio: inspect supplied synthetic confidence values and the real hemoglobin database evidence card; write a bounded structure interpretation.

## Optional extension
Optional: inspect a predicted complex with interface metrics; no docking or molecular dynamics is required.

---

# W13 | From a variant to an evidence-based sentence

How do we report uncertainty without turning it into a diagnosis?

## Outcomes

- Distinguish a variant, a predicted consequence and a clinical classification.
- Check reference, transcript, condition, date and review status.
- Write a non-diagnostic interpretation that preserves uncertainty.

## Biological bridge
A sequence difference is a variant. Its effect depends on location, transcript, mechanism and biological context.

## One change, several descriptions

- A variant can be described at genomic, transcript or protein level.
- Different transcript choices can change a predicted consequence.
- Record the reference accession and version before comparing labels.

Sources: S03, S19

## Consequence is not clinical classification

- Missense means an amino-acid substitution in a specified coding context.
- A stop-gain or splice prediction does not automatically establish pathogenicity.
- Gene-disease mechanism and other evidence matter.

Sources: S19

## Five categories preserve uncertainty

- Benign; likely benign; uncertain significance; likely pathogenic; pathogenic.
- These categories were established for Mendelian germline variant interpretation.
- Somatic treatment claims require their own framework and clinical context.

Sources: S18, S19

## Evidence comes from different sources

- Population frequency, segregation and functional studies can contribute.
- Computational predictors provide another type of evidence.
- Do not count correlated predictors as independent proof.

Sources: S19

## ClinVar records assertions and review status

- Check the exact variant, condition, submission dates and supporting evidence.
- Conflicts or older assertions may require investigation.
- Review stars describe review status, not a pathogenicity probability.

| Example status | What it describes |
|---|---|
| Expert panel | Level of review |
| Multiple submitters, no conflicts | Concordant assertions with criteria |
| Conflicting classifications | Disagreement to examine |

Sources: S18

## A VUS is not a treatment instruction

- Uncertain significance means available evidence is insufficient or conflicting.
- Do not use a VUS alone to establish a diagnosis or change treatment.
- Escalate real clinical questions to qualified clinical professionals.

Sources: S19

## What a useful sentence contains

- Identity: the exact variant and reference context.
- Evidence: what supports the current interpretation and what is missing.
- Scope: an educational interpretation, not clinical advice.

Sources: S18, S19

## Our cases are deliberately fictional

- EDU-V1, EDU-V2 and EDU-V3 are synthetic evidence cards.
- They have no real patient identifiers or claimed ClinVar accessions.
- The goal is to audit reasoning, not independently certify a clinical classification.

## Worked example: a cautious report
EDU-V1 is a rare fictional missense variant with only two correlated computational predictions and no functional or segregation evidence.
- Rarity and predicted damage do not alone establish disease causality.
- The evidence is insufficient for a confident pathogenic interpretation.
- Report the uncertainty and request relevant independent evidence; do not diagnose.

## Checkpoint
A variant is rare and a predictor calls it damaging. Does this establish pathogenicity? Name one independent type of evidence to investigate.

### Debrief
No. Examples include appropriate functional evidence, segregation with the relevant phenotype, or well-curated condition-specific evidence evaluated in context.

## Practical
W13 studio: inspect three synthetic variant cards and write three short evidence-bounded statements. No patient data or clinical recommendation is required.

## Optional extension
Optional: explore current gene-specific ClinGen specifications as a supervised follow-on topic.

---

# W14 | Responsible bioinformatics and your scientific record

What can you share, claim and sign your name to?

## Outcomes

- Distinguish pseudonymized data from a justified anonymity claim.
- Identify when a data flow needs institutional privacy review.
- Submit a reproducible portfolio with a precise AI-use disclosure.

## Biological bridge
Genetic and health information can be sensitive even when a name column has been removed.

## Removing names does not remove all risk

- A code can replace a name while a linkage key remains elsewhere.
- Genomic patterns and combinations of metadata can permit re-identification.
- Anonymity is a contextual assessment, not a blanket promise about a file format.

Sources: S20, S22

## Map the data flow before uploading

- What data leave which institution?
- Who receives them, where are they processed, and for what purpose?
- Who can access them, for how long, and under what approval?

Sources: S20, S21, S22

## KVKK and GDPR are not interchangeable labels

- KVKK treats genetic and health data within special categories.
- Processing conditions and international-transfer requirements must both be considered.
- GDPR applicability and obligations depend on the situation; seek institutional advice.

Sources: S20, S21, S22

## Consent is not a universal shortcut

- A legitimate processing basis does not by itself solve every transfer or security obligation.
- Minimize data, limit access and document purpose and retention.
- Use the institution's approved environment for real sensitive data.

Sources: S20, S21, S22

## The classroom uses safer data by design

- Synthetic examples do not represent real patients.
- Public excerpts remain subject to source and license conditions.
- Use course pseudonyms; do not embed student numbers in public notebooks.

Sources: S20, S23

## Make an AI disclosure that can be checked

- Name the tool and date or version where known.
- Describe what it assisted with and which checks you performed.
- State responsibility for the submitted result; No AI used is acceptable.

Sources: S23

## Reproducibility has a practical minimum

- Data provenance, code or steps, versions, parameters and independent unit.
- A clean rerun plus a plain-language explanation of limitations.
- A record of corrections is more useful than a claim of perfection.

Sources: S05, S10, S23

## Your portfolio is evidence of skills

- D1: an experiment you can justify.
- D2: a prediction you can evaluate honestly.
- A model card, structure card and variant statement showing the limits of your claims.

## Worked example: the cloud-upload decision
A colleague removes names from patient VCF files and proposes uploading them to a public chatbot for annotation.
- Genetic information remains; removing names does not establish anonymity.
- The data flow and vendor processing can require privacy and transfer review.
- Do not upload; consult the authorized institutional process and use synthetic examples for teaching.

## Checkpoint
Write a one-sentence AI disclosure for a notebook where a tool explained a Python error but did not choose the biological conclusion.

### Debrief
Example: I used [tool and date] to explain a Python error, checked the revised calculation with the stated test inputs, and independently wrote and take responsibility for the interpretation.

## Practical
W14 studio: complete a data-flow decision card, a disclosure and a skills-ledger reflection. Bring your D1 notebook for the individual oral check.

## Optional extension
Optional: compare controlled-access and federated analysis designs without moving real patient data.

---
