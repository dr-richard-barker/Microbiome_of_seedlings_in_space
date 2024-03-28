The results of the analysis can be found in this folder.

Summary: Initial analysis performed on sample GLDS-37_rna_seq_Atha_Ler-0_sl-pool_GC_Rep5_R2-GC-C5_R1/2_trimmed.fastq). 
(Pre-trimmed data was downloaded from the OSDR).


**For taxonomy quantitation**

1.      Read QC (**FastQC**)

2.      Present QC for raw reads (**MultiQC**)

3.      Quality trimming (**Trim Galore!**)

4.      Create paired-end reads by combining single-end reads from two separate Fastq files (**FASTQ interlacer**)

5.      To identify bacteria and archaea (**MetaPhlAn**)

-Predicted taxon relative abundance omics levels

- Predicted taxon relative abundances

- Bowtie2 output

- SAM file

- BIOM file

- Predicted taxon relative abundances for KRONA

6.      Visualization (**Krona pie chart**)

For functional quantitation

7.      HuMAnN (it continues...)



**MetaPhlAn performs taxonomic assignments with NCBI.** 

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


![Species_abundance_Ler_test_sample](https://github.com/dr-richard-barker/Microbiome_seedlings_in_space/assets/8679982/4d9fe3e8-c558-4c1a-9cdf-3d3063350d42)


