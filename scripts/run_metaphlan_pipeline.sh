#!/usr/bin/env bash
# ==============================================================================
# Meta-Transcriptomic Processing & Taxonomic Profiling Pipeline
# ==============================================================================
# Pipeline Overview:
# 1. Download raw unmapped FASTQ reads from NASA OSDR (OSD-37, 38, 120, 217, 522)
# 2. Quality Trimming & Adapter Removal (Trimmomatic / Cutadapt)
# 3. Host Subtraction: Align reads to Arabidopsis thaliana reference (TAIR10) using Bowtie2 / STAR
# 4. Extract unmapped non-host microbial reads
# 5. Taxonomic Profiling via MetaPhlAn 4 / Kraken2
# 6. Generate interactive Krona metagenomic HTML visualization
# ==============================================================================

set -euo pipefail

# Directories
RAW_DIR="data/raw_fastq"
CLEAN_DIR="data/host_subtracted"
RESULTS_DIR="data/metaphlan_results"
REF_GENOME="references/TAIR10_chr_all.fa"

mkdir -p "${RAW_DIR}" "${CLEAN_DIR}" "${RESULTS_DIR}"

echo "[1/5] Fetching study file manifests from NASA OSDR API..."
python3 scripts/fetch_osdr_data.py --studies 37,38,120,217,321,522 --output-json data/osdr_manifest.json

echo "[2/5] Building Host Genome Reference Index (TAIR10)..."
if [ ! -f "${REF_GENOME}.1.bt2" ]; then
    echo "Building Bowtie2 index for TAIR10..."
    # bowtie2-build ${REF_GENOME} references/TAIR10
fi

echo "[3/5] Processing Meta-Transcriptomic Samples..."
# Example sample loop (uncomment when running against raw FASTQ files):
# for R1 in ${RAW_DIR}/*_R1.fastq.gz; do
#     SAMPLE=$(basename ${R1} _R1.fastq.gz)
#     R2="${RAW_DIR}/${SAMPLE}_R2.fastq.gz"
#     
#     # Align to Arabidopsis genome and export UNMAPPED reads (microbial candidate reads)
#     bowtie2 -p 8 -x references/TAIR10 -1 ${R1} -2 ${R2} \
#         --un-conc-gz ${CLEAN_DIR}/${SAMPLE}_unmapped_R%.fastq.gz \
#         -S /dev/null
#     
#     # MetaPhlAn 4 Profiling
#     metaphlan ${CLEAN_DIR}/${SAMPLE}_unmapped_R1.fastq.gz,${CLEAN_DIR}/${SAMPLE}_unmapped_R2.fastq.gz \
#         --bowtie2out ${RESULTS_DIR}/${SAMPLE}_bowtie2.tabular \
#         --nproc 8 \
#         -input_type fastq \
#         -o ${RESULTS_DIR}/${SAMPLE}_profile.txt
# done

echo "[4/5] Merging Taxonomic Profiles across spaceflight conditions..."
# merge_metaphlan_tables.py ${RESULTS_DIR}/*_profile.txt > ${RESULTS_DIR}/merged_abundance_table.txt

echo "[5/5] Generating Krona Metagenomic Sunburst HTML..."
# ktImportMetaPhlAn -o ${RESULTS_DIR}/krona_microbiome.html ${RESULTS_DIR}/merged_abundance_table.txt

echo "=============================================================================="
echo "Meta-Transcriptomic Pipeline Script Documentation Completed."
echo "=============================================================================="
