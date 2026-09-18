# Reproducibility Suite & Pipeline Scripts

This directory contains standalone CLI scripts and documentation for reproducing the meta-transcriptomic and spaceflight seedling microbiome analysis in this project.

## Scripts Overview

| Script | Language | Description |
| :--- | :--- | :--- |
| [`fetch_osdr_data.py`](file:///Users/drb_laptop/Documents/Microbiome_of_seedlings_in_space/scripts/fetch_osdr_data.py) | Python 3 | Queries NASA OSDR REST API for study file manifests and raw/processed datasets across OSD-37, 38, 120, 217, 321, 522. |
| [`generate_upset_and_heatmaps.py`](file:///Users/drb_laptop/Documents/Microbiome_of_seedlings_in_space/scripts/generate_upset_and_heatmaps.py) | Python 3 | Parses species tables and correlation matrices to generate publication figures (`figures/reproduced_upset_plot.png`, `figures/reproduced_correlation_heatmap.png`, `figures/reproduced_microbe_traits.png`). |
| [`run_metaphlan_pipeline.sh`](file:///Users/drb_laptop/Documents/Microbiome_of_seedlings_in_space/scripts/run_metaphlan_pipeline.sh) | Bash | Documents upstream FASTQ quality filtering, *Arabidopsis thaliana* TAIR10 host alignment subtraction, MetaPhlAn 4 profiling, and Krona HTML export. |

---

## Usage Instructions

### 1. Fetch NASA OSDR Data Manifests
```bash
python3 scripts/fetch_osdr_data.py --studies 37,38,120,217,321,522 --output-json data/osdr_manifest.json
```

### 2. Generate Figures & Plots
```bash
python3 scripts/generate_upset_and_heatmaps.py
```
Output figures will be saved in `figures/`.

### 3. Inspect Upstream Meta-Transcriptomic Commands
```bash
bash scripts/run_metaphlan_pipeline.sh
```
