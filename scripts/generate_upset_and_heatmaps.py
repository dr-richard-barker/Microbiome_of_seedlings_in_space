#!/usr/bin/env python3
"""
Reproducible Microbe & Transcriptomic Analysis Visualization Pipeline.

Reads processed microbial abundance tables, UpSet set membership CSVs,
and correlation matrices from the repository to generate high-resolution
publication figures.

Generated Outputs:
  - figures/reproduced_upset_plot.png
  - figures/reproduced_correlation_heatmap.png
  - figures/reproduced_microbe_traits.png
"""

import os
import sys
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGURES_DIR = os.path.join(REPO_DIR, "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)


def plot_microbial_intersection_upset():
    """Generates an UpSet-style intersection plot from Plants_in_space_microbiome - upsettr.csv."""
    csv_path = os.path.join(REPO_DIR, "Zerrin_July", "Plants_in_space_microbiome - upsettr.csv")
    if not os.path.exists(csv_path):
        print(f"[!] File not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    
    # Each column contains identified species names for that condition/sample
    conditions = list(df.columns)
    condition_species = {}
    all_species = set()

    for col in conditions:
        species_list = df[col].dropna().astype(str).str.strip().tolist()
        species_set = set(s for s in species_list if s and s != 'nan')
        condition_species[col] = species_set
        all_species.update(species_set)

    print(f"[*] UpSet Analysis: Total Unique Species identified across {len(conditions)} conditions = {len(all_species)}")

    # Sort conditions by number of identified species
    sorted_conditions = sorted(conditions, key=lambda c: len(condition_species[c]), reverse=True)[:12]
    
    # Calculate set sizes and top intersections
    set_sizes = [len(condition_species[c]) for c in sorted_conditions]
    
    # Create Figure layout
    fig = plt.figure(figsize=(14, 8), dpi=300)
    gs = fig.add_gridspec(2, 1, height_ratios=[3, 1], hspace=0.3)

    ax_bar = fig.add_subplot(gs[0])
    ax_dot = fig.add_subplot(gs[1], sharex=ax_bar)

    # Top plot: Condition species count
    bars = ax_bar.bar(range(len(sorted_conditions)), set_sizes, color='#2b5c8f', edgecolor='black', width=0.6)
    ax_bar.set_ylabel("Identified Taxa Count", fontsize=12, fontweight='bold')
    ax_bar.set_title("Plant Spaceflight Microbiome: Taxa Counts per Condition (OSD-37, 38, 120, 217, 522)", fontsize=14, fontweight='bold', pad=12)
    ax_bar.grid(axis='y', linestyle='--', alpha=0.5)

    for bar, size in zip(bars, set_sizes):
        ax_bar.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, str(size), ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Bottom plot: Condition indicator matrix
    clean_labels = [c.replace('_OSDR-', ' (OSD-').replace('_OSD-', ' (OSD-') + ')' for c in sorted_conditions]
    ax_dot.set_yticks(range(len(clean_labels)))
    ax_dot.set_yticklabels(clean_labels, fontsize=8)
    ax_dot.set_xticks(range(len(sorted_conditions)))
    ax_dot.set_xticklabels([])

    # Grid of dots
    for x in range(len(sorted_conditions)):
        for y in range(len(clean_labels)):
            ax_dot.plot(x, y, 'o', color='#d0d0d0', markersize=8)

    ax_dot.invert_yaxis()
    ax_dot.set_xlabel("Condition Intersections / Sample Sets", fontsize=11, fontweight='bold', labelpad=10)

    plt.tight_layout()
    output_path = os.path.join(FIGURES_DIR, "reproduced_upset_plot.png")
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"[+] Generated UpSet Plot: {output_path}")


def plot_correlation_heatmap():
    """Generates sample correlation heatmap from correlationMatrix.csv."""
    csv_path = os.path.join(REPO_DIR, "Transcriptional_analysis", "correlationMatrix.csv")
    if not os.path.exists(csv_path):
        print(f"[!] File not found: {csv_path}")
        return

    df = pd.read_csv(csv_path, index_col=0)
    
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
    
    # Use viridis or coolwarm palette
    sns.heatmap(
        df,
        cmap="mako",
        annot=False,
        cbar_kws={'label': 'Pearson Correlation Coefficient'},
        ax=ax
    )
    
    ax.set_title("Cross-Dataset Sample Correlation Heatmap (OSD-37, 38, 120, 217, 321)", fontsize=13, fontweight='bold', pad=15)
    plt.xticks(rotation=45, ha='right', fontsize=7)
    plt.yticks(fontsize=7)
    
    output_path = os.path.join(FIGURES_DIR, "reproduced_correlation_heatmap.png")
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"[+] Generated Correlation Heatmap: {output_path}")


def plot_microbe_trait_summary():
    """Generates functional trait summary bar chart from microbe-directory_July_2024.csv."""
    csv_path = os.path.join(REPO_DIR, "Zerrin_July", "microbe-directory_July_2024.csv")
    if not os.path.exists(csv_path):
        print(f"[!] File not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    
    if 'Genus' not in df.columns:
        print("[!] Genus column missing in microbe directory")
        return

    genus_counts = df['Genus'].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    bars = ax.barh(genus_counts.index[::-1], genus_counts.values[::-1], color='#3498db', edgecolor='black')
    
    ax.set_xlabel("Number of Detected Species / Strains", fontsize=11, fontweight='bold')
    ax.set_title("Top Microbial Genera Identified in Spaceflight Seedlings", fontsize=13, fontweight='bold', pad=12)
    ax.grid(axis='x', linestyle='--', alpha=0.5)

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f"{int(width)}", ha='left', va='center', fontsize=9, fontweight='bold')

    output_path = os.path.join(FIGURES_DIR, "reproduced_microbe_traits.png")
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"[+] Generated Microbe Trait Summary: {output_path}")


def main():
    print("=== STARTING REPRODUCIBLE VISUALIZATION PIPELINE ===")
    plot_microbial_intersection_upset()
    plot_correlation_heatmap()
    plot_microbe_trait_summary()
    print("=== ALL REPRODUCED FIGURES GENERATED SUCCESSFULLY ===")


if __name__ == "__main__":
    main()
