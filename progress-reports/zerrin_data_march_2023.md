---
description: OSD_37 preliminary analysis with 1 sample.
---

# Zerrin\_data\_March\_2023              GLDS-37\_RNAseq\_Atha\_Ler-0\_GC

The results of the analysis can be found in this folder.

Summary: Initial analysis performed on sample GLDS-37\_rna\_seq\_Atha\_Ler-0\_sl-pool\_GC\_Rep5\_R2-GC-C5\_R1/2\_trimmed.fastq).&#x20;

Data/ Fastq files was pre-trimmed (See GeneLab pipeline for QC settings) data was downloaded from the OSDR.

**For taxonomy quantitation**

1. ```
    Read QC (**FastQC**)
   ```
2. ```
    Present QC for raw reads (**MultiQC**)
   ```
3. ```
    Quality trimming (**Trim Galore!**)
   ```
4. ```
    Create paired-end reads by combining single-end reads from two separate Fastq files (**FASTQ interlacer**)
   ```
5. ```
    To identify bacteria and archaea (**MetaPhlAn**)
   ```

\-Predicted taxon relative abundance omics levels

* Predicted taxon relative abundances
* Bowtie2 output
* SAM file
* BIOM file
* Predicted taxon relative abundances for KRONA

6. ```
    Visualization (**Krona pie chart**)
   ```

For functional quantitation

7. ```
    HuMAnN (it continues...)
   ```

**MetaPhlAn performs taxonomic assignments with NCBI.**

Here's the species abundance table/

| species                  | species\_id | abundance |
| ------------------------ | ----------- | --------- |
| Ralstonia pickettii      | 329         | 73.00088  |
| Herbaspirillum huttiense | 863372      | 16.31611  |
| Pseudomonas fluorescens  | 294         | 6.973     |
| Curvibacter gracilis     | 230310      | 1.96584   |
| Neisseria subflava       | 28449       | 0.75498   |

Quick bar plot made using "https://julius.ai/"

```python
import pandas as pd

# Load the species.tabular file
df = pd.read_csv('species.tabular', sep='\	')

# Display the first few rows of the dataframe
print(df.head())

import matplotlib.pyplot as plt

# Create a bar plot
plt.figure(facecolor='white')
plt.bar(df['species'], df['abundance'])
plt.xlabel('Species')
plt.ylabel('Abundance')
plt.title('Abundance of Species')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
```

![Species\_abundance\_Ler\_test\_sample](https://github.com/dr-richard-barker/Microbiome\_seedlings\_in\_space/assets/8679982/4d9fe3e8-c558-4c1a-9cdf-3d3063350d42)

<table><thead><tr><th width="194">Microbial Species</th><th>Description</th><th width="118">Habitat</th><th>Known Uses</th><th>Potential Applications</th><th>References</th></tr></thead><tbody><tr><td>Ralstonia pickettii</td><td>Gram-negative, rod-shaped bacterium</td><td>Soil and water</td><td>Can degrade pollutants like toluene and chlorinated solvents [1]</td><td>Bioremediation of contaminated environments</td><td>NCBI: <a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2672333/">link</a></td></tr><tr><td>Herbaspirillum huttiense</td><td>Gram-negative, motile bacterium</td><td>Root systems of plants</td><td>Promotes plant growth by fixing nitrogen [2]</td><td>Biofertilizers to improve crop yields</td><td>NCBI: <a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9247281/">link</a></td></tr><tr><td>Pseudomonas fluorescens</td><td>Gram-negative, rod-shaped bacterium</td><td>Widespread in soil and water</td><td>Produces various beneficial compounds including antibiotics [3]</td><td>Biological pest control, disease suppression in plants</td><td>NCBI: <a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10682437/">link</a></td></tr><tr><td>Curvibacter gracilis</td><td>Gram-negative, curved rod-shaped bacterium</td><td>Soil and water</td><td>Degrades organic matter and plays a role in nutrient cycling [4]</td><td>Improvement of soil health and fertility</td><td>PubMed: <a href="https://pubmed.ncbi.nlm.nih.gov/15545462/">link</a></td></tr><tr><td>Neisseria subflava</td><td>Gram-negative, coccus-shaped bacterium</td><td>Part of human commensal flora, found in the upper respiratory tract</td><td>Can be opportunistic pathogens but also contribute to the immune system [5]</td><td>Research on human health and diseases</td><td>NCBI Bookshelf: <a href="https://www.ncbi.nlm.nih.gov/books/NBK532961/">link</a></td></tr></tbody></table>
