# Microbiome of seedling in space

**Microbiome of seedling in space** This repo contains data products produced while exploring the microbial communities present in a series of studies with similar meta-data characteristics

**Goal(s)** To identify evidence for microbes that are differentially abundant in orbit relative to ground controls.

**Keywords:** Spaceflight, Arabidopsis, Microbiome, RNAseq, meta-analysis, plant genetics

**Introductory/Summary:** Spaceflight presents a unique environment for biological experiments, notably due to the presence of microgravity and other space-specific factors. Abidopsis, a widely used model organism in plant biology, has been the focus of numerous studies to explore plant growth and development in space. Here we describe the selection of 5 Open Science Data Resportory (OSDR) datasets, as they provided a comprehensive overview of various Arabidopsis seedling development experiments conducted during spaceflight. Understanding how plants respond to these conditions is crucial for long-term space missions and offers insights into fundamental biological processes, studies collectively comprise 38 observations across 8 primary variables. While their transcriptomes have been extensively researched (see reference on OSDR accession home pages linked below) to date no work has been done to assess if these samples can also provide insight into the microbial response to spaceflight. Overall, these accessions from the GeneLab data repository provide invaluable data for understanding the complex dynamics of Arabidopsis thaliana development and potential interactions with its microbial community development under varied environmental conditions, but particularly focusing on the effects of microgravity.

***



<figure><img src="Slide3.png" alt=""><figcaption><p><strong>Figure:</strong> Filtering using GeneLab metadata identifies similar studies (as described by Barker et al., 2023)</p></figcaption></figure>

***

**Separate analysis:** Combining analysis of OSD-37, OSD-38, OSD-120, OSD-231 and OSD-321 will provide new insights.

Each of the studies' transcriptome can be analysed separately

https://visualization.genelab.nasa.gov/data/OSD-37

https://visualization.genelab.nasa.gov/data/OSD-38

https://visualization.genelab.nasa.gov/data/OSD-120

https://visualization.genelab.nasa.gov/data/OSD-231

https://visualization.genelab.nasa.gov/data/OSD-321

**Separate analysis plan:** Pull raw Fastq files from OSD-37 for WT Col-0 variety, filter reads that align to the Arabidopsis Genome and quantify the transcripts that remain below to the microbial community. Compare flight vs ground abundance. Repeat for OSD-38, OSD-120, OSD-231, OSD-321.

**Combined analysis:** Merge abundance measurements and calculate statistics

**Recommended new method for metatranscriptome analysis**&#x20;

<figure><img src="https://github.com/dr-richard-barker/Microbiome_seedlings_in_space/assets/8679982/a9accf84-2bdd-4e88-96c8-090b21a5749e" alt=""><figcaption><p>https://github.com/nf-core/metatdenovo/tree/dev </p></figcaption></figure>





Then compare with the results from Dixit et al ., suggest that seed surface sanitization could influence the microbiome. Seed sanitization can affect the microbiome of leafy green crops and the persistence of E. coli and other microbial communities.

Persistence of Escherichia coli in the microbiomes of red Romaine lettuce (Lactuca sativa cv. ‘Outredgeous’) and mizuna mustard (Brassica rapa var. japonica) - does seed sanitization matter? Authors: Dixit Anirudha R., Khodadad Christina L. M., Hummerick Mary E., Spern Cory J., Spencer LaShelle E., Fischer Jason A., Curry Aaron B., Gooden Jennifer L., Maldonado Vazquez Gretchen J., Wheeler Raymond M., Massa Gioia D., Romeyn Matthew W. PubMed ID: 34686151 DOI: 10.1186/s12866-021-02345-5

https://osdr.nasa.gov/bio/repo/data/studies/OSD-386

***

Then compare with a digital twin lettuce microbe (using data from papers like this [Seasonal variation in lettuce microbiome](https://pubmed.ncbi.nlm.nih.gov/38338730/)) to summarize the variance we see in spaceflight relates to terrestrial microbiome trends.

**Microgravity, its effects on seedling establishment and the space plant endophytic microbial communities:**

Microgravity environments, characterized by the absence or significant reduction of gravitational forces compared to Earth's gravity, present a distinctive context in which plants undergo a myriad of physiological and developmental alterations. The impact of microgravity on flora extends beyond these observable changes, raising pertinent inquiries into the effects on the plant microbiome. Despite the fundamental role of the microbiome in plant health and development, comprehensive understanding of how microgravity conditions influence these microbial communities remains limited. This gap in knowledge highlights the need for further research to elucidate the interactions between microgravity, plant physiology, and microbial ecology.

**Objectives of this essay/paper plan:**

## Quantifying Microbiome-Related Transcripts in Plant RNAseq Data from Space-Based Experiments

The exploration of plant-microbe interactions under the unique conditions of spaceflight represents a critical avenue of research. The adaptation of these relationships in microgravity environments is fundamental to the conception and development of resilient, sustainable agricultural systems beyond Earth. Our study focuses on the methodological approaches for quantifying microbiome-associated transcripts within plant RNAseq datasets derived from experiments conducted in space.

### Introduction

Spaceflight presents an unparalleled environment for examining the dynamics between plants and their symbiotic microbiomes. The microgravity conditions offer a unique setting to observe potential modifications in plant-microbe interactions, which could play a pivotal role in sustaining long-term extraterrestrial colonization efforts through advanced agricultural practices.

### Objectives

1. To delineate the methodology for extracting and quantifying microbiome-related transcripts from plant RNA sequencing data obtained in microgravity conditions.
2. To understand how these interactions between plants and their microbiomes are altered in spaceflight, potentially contributing to the development of robust food production systems for future space missions.

### Methodology

This research will employ state-of-the-art bioinformatic techniques to analyze RNA sequencing (RNAseq) data from plant samples grown in space. The process involves:

* **Sample Preparation**: Isolation of total RNA from plant tissues, ensuring the preservation of microbial RNA.
* **Sequencing**: Utilization of high-throughput sequencing technologies to capture a broad spectrum of plant and microbial transcripts.
* **Data Analysis**: Implementation of computational tools to differentiate plant-derived RNA from microbiome-associated RNA transcripts. This step includes the mapping of RNAseq reads to known databases of plant and microbial genomes to quantify the abundance of specific transcripts related to the microbiome.

### Expected Outcomes

The expected outcomes of this study include a comprehensive understanding of:

* The changes in gene expression profiles of plants and their associated microbiomes under the influence of microgravity.
* The identification of critical microbiome-related genes that could facilitate the development of sustainable agricultural practices in space.
* The establishment of a standardized methodology for analyzing plant-microbiome interactions in extraterrestrial environments.

#### Identifying Key Pathways in Plant-Microbe Interactions Through Meta-transcriptome Analysis

The primary objective of our investigation is to delineate the molecular pathways governing plant-microbe interactions within a space environment. By generating and analyzing a comprehensive meta-transcriptome through RNA sequencing (RNAseq), we aim to elucidate the differential expression patterns of genes that facilitate communication between plants and their associated microbial communities. Understanding these patterns is pivotal to enhancing plant vitality and growth under the unique conditions encountered in extraterrestrial habitats.

#### Microbiome Adaptation in Space: An RNAseq Approach

A secondary, but equally important, aspect of our research focuses on characterizing the shifts within the microbiome of Arabidopsis plants subjected to spaceflight conditions compared to those grown under terrestrial controls. By scrutinizing the RNAseq data, we intend to identify microbial transcripts that are uniquely present or significantly altered in space-grown plants. These insights will shed light on the adaptive strategies employed by the microbiome in a microgravity environment, contributing to our understanding of microbial ecology in space.

#### Advancing Space-Based Agriculture

This investigation is poised to make significant contributions to the field of space-based agricultural sciences. By comprehensively understanding plant-microbe interactions and the microbiome's adaptability to space conditions, we can lay the groundwork for developing robust food production systems for long-duration space exploration missions. Our targeted approach in analyzing RNAseq data from Arabidopsis plants grown under flight and ground conditions, without the confounding effects of varying gravity or radiation, ensures the relevance and applicability of our findings to space agriculture.

#### Conclusion

Focusing exclusively on Arabidopsis, treated under flight versus ground scenarios, and employing RNAseq as our assay methodology, our research endeavors to uncover the vital pathways involved in plant-microbe interactions and the adaptive mechanisms of the microbiome in space. The outcomes of this study are expected to furnish critical insights into optimizing agricultural practices for future space exploration missions, thereby supporting the sustainability of extraterrestrial life.





***

**Similarities and differences in methods GeneLab Metadata mining reveals similarities between these studies** GeneLab Data System (GLDS) Identifiers enable tracking of specific datasets within a larger repository. These identifiers, such as GLDS-37, GLDS-38, GLDS-120, GLDS-218, GLDS-321, etc., are crucial for cross-referencing and detailed analysis of the spaceflight experiments involving Arabidopsis thaliana. By cataloguing experiments in this manner, the GeneLab researchers enabled efficient access allowing comparison of different studies and enhancing our understanding of plant responses to spaceflight conditions.

**A. Key Similarities between studies:** These studies were selected as they have several key methodologies and conditions that are conserved that is the use of agar nutrient gels in petri dishes to be used as the primary source of moisture and nutrients. The use of BRIC hardware has allowed the assessment of a range of ecotypes and genotypes on Phytagel plates in Petri dish fixation units (PDFU). The BRIC hardware has been used as its specialized PDFU growth chambers provide a controlled dark environment for plant growth in orbit. There is a notable uniformity in the short-duration nature of these studies, with plants being harvested in their nascent stages, providing insights into early growth dynamics. The addition of light in GLDS-120, allows comparison of plants that undergo photomorphogenesis in perpetual light to those that undergo skotomorphogensis in complete darkness, which is another pivotal aspect as this enables oxygen production via photosynthesis. The selection of this variation is not arbitrary but deliberate, aimed at unravelling the intricate effects of light on plant growth, development and morphogenesis. The choice of ecotypes/genotypes in these studies is not diverse but rather concentrated on specific, well-characterized strains such as Col-0, WS-0, and mutant variations of Col. This choice indicates a preference for using genetically familiar and extensively studied plant lines, facilitating comparative analysis and consistency in results. Lastly, there's a discernible emphasis on studying specific plant tissues, primarily roots, shoots and etiolated seedlings. This focus is indicative of a keen interest in understanding how different environmental stimuli influence the early stages of root and seedling development, crucial for comprehending the broader aspects of plant growth and adaptability.

**B. Key differences:** The differences between the GLDS studies are quite pronounced, especially when considering the hardware used and the lighting conditions, both of which significantly impact the type of tissue studied. In GLDS-38, GLDS-37, and GLDS-321, the use of BRIC hardware has been a defining feature. This specific type of hardware likely influences the nature of the experiments and the results obtained, particularly in terms of how the plant tissues respond to different environmental conditions. On the other hand, GLDS-120 uses Phytagel plates, and GLDS-218 is conducted with the Vegetable Production System, suggesting variations in how the plants are grown and observed. These differences in hardware may directly influence the types of tissues that can be effectively studied and the conditions under which these tissues develop. In terms of lighting conditions, each study has a unique approach that shapes the nature of the tissue studied. GLDS-38 is unique for its experiments conducted in complete darkness, while GLDS-120 features a variety of lighting conditions including continuous light and a combination of light activation followed by dark growth. GLDS-218's use of continuous purple light is particularly noteworthy, as it represents a specific wavelength that can have unique effects on plant growth and development. GLDS-37 and GLDS-321, meanwhile, incorporate studies in both complete darkness and periods of light activation followed by dark growth. These varied lighting conditions are crucial as they directly affect the physiological and developmental processes in plants, influencing the type of tissue that can be effectively studied in each experiment. The age at harvest and the specific ecotype and genotype being studied are also key differentiators among these studies. GLDS-120 investigates several ecotypes/genotypes including Col-0, WS-0, and Col-0 PhyD, offering a broad perspective on how different genetic backgrounds respond to the experimental conditions. GLDS-37 goes even further by focusing on a wider range of ecotypes/genotypes, such as Ws-2, Ler-0, Cvi-0, and Col-0. This diversity in genetic material is crucial for understanding the range of responses in plant biology. GLDS-321 studies variations of Col, including Col, Col bzip20, and Col bzip 60, allowing for a more nuanced understanding of how slight genetic variations can impact plant responses. Conversely, GLDS-38 and GLDS-218 limit their studies to the Col-0 and WS-0 ecotypes/genotypes, respectively, offering a more focused but potentially less diverse set of data. The age at harvest presents another layer of complexity and interesting research opportunity related to confronting a pseudo time series. GLDS-38 and GLDS-321 are notable for their extremes in harvest ages – as short as 3 days and as long as 14 days, respectively. This contrasts with GLDS-120, GLDS-218, and GLDS-37, which all have similar ages at harvest, around 8-12 days. The age at harvest is crucial, as it determines the developmental stage of the plant tissues being studied. Younger tissues may respond differently to environmental conditions than more mature tissues. This aspect, coupled with the specific ecotypes/genotypes under investigation, provides insights to the natural variation in the plant's developmental response to spaceflight.

**If you want to get started these lines of code might help**

**Thanks for your help**
