# Data catalogue and provenance

All toy and notebook-generated datasets are SYNTHETIC. They illustrate specific mathematical or design properties and must not be represented as human, animal, clinical or experimentally collected observations. The seed is derived from a course pseudonym, not an identity credential. All notebooks embed their needed data; these files are convenient inspection copies.

## Toy sequence records
`toy_reference.fasta`, `toy_regions.bed`, `toy_annotation.gtf`, `toy_variant.vcf`: original classroom records. BED interval [2,7) and GTF [3,7] select GTACG. VCF record at position4 replaces T with C. No human genome assembly or actual variant accession applies.

## Real excerpt: pasilla
`REAL_pasilla_two_gene_excerpt.csv` is a manual transcription of head(cts,2) shown in the DESeq2 release vignette, accessed2026-09-14. The matching sample table is likewise transcribed from the vignette and intentionally retains the `fb` suffix for a documented identifier-matching exercise. These are only two rows of a much larger count matrix; do not estimate library size, differential expression, or a complete expression profile from them.
Source: https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html
Underlying experiment/package provenance: https://bioconductor.org/packages/release/data/experiment/html/pasilla.html
Brooks et al. (2011), Drosophila pasilla perturbation. Cite the original experiment and package for substantive reuse; the full package is not bundled.

## Real evidence cards, not empirical reproductions
W11 contains bibliographic summaries of Cui2024 and Kedzierska2025, not downloaded models or reproduced benchmarks. W12 transcribes a summary from RCSB AF_AFP69905F1 (hemoglobin alpha;142 modeled residues; displayed global pLDDT98.06), checked2026-09-14. The subsequent confidence arrays are separate synthetic examples. No PDB coordinate file is bundled and no binding calculation is performed.

## Reuse notice
Original course code, prose and synthetic records are supplied for adaptation by the course team. No open redistribution licence is imposed on institutional material by this package. Confirm the desired licence with the rights holder before public release. Third-party sources retain their own terms; cite them and check those terms for broader reuse. No full third-party paper, model weight or old slide image is bundled.
