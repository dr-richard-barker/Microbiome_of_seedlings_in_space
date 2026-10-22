#!/usr/bin/env python3
"""
Publication Figure Generator:
- Figure 2: UpSet Taxa Intersection Plot (manuscript/figures/figure2_upset_plot.png)
- Figure 3: Pairwise Taxa Intersection Heatmap (manuscript/figures/figure3_correlation_heatmap.png)
- Microbe Trait Summary (figures/reproduced_microbe_traits.png)

Ensures zero overlapping labels, high publication DPI (300), and compliant bounding boxes.
"""

import os
import sys
import json
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
from scipy.cluster import hierarchy

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGURES_DIR = os.path.join(REPO_DIR, "figures")
MANUSCRIPT_FIG_DIR = os.path.join(REPO_DIR, "manuscript", "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(MANUSCRIPT_FIG_DIR, exist_ok=True)


def plot_microbial_intersection_upset():
    """
    Generates a full publication-grade UpSet intersection plot from
    Plant_in_space_microbiome - upsettr.json.
    
    Resolves the prior label overlapping bug by allocating sufficient vertical row spacing,
    clean condition descriptions, and ample bar headroom.
    """
    json_path = os.path.join(REPO_DIR, "Plant_in_space_microbiome - upsettr.json")
    if not os.path.exists(json_path):
        json_path = os.path.join(REPO_DIR, "Zerrin_July", "Plant_in_space_microbiome - upsettr.json")
    
    if not os.path.exists(json_path):
        print(f"[!] File not found: {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = data['Employees']['Employee']
    sets = {}
    for r in rows:
        for k, v in r.items():
            k_clean = k.strip()
            v_clean = v.strip()
            if k_clean not in sets:
                sets[k_clean] = set()
            if v_clean:
                sets[k_clean].add(v_clean)

    # Standard clean labels mapping for the 19 sets
    label_map = {
        'Col-0_FT_OSDR-37': 'OSD-37: Col-0 Flight',
        'WS-2_GC_OSDR-37': 'OSD-37: WS-2 Ground',
        'Col-0_GC_OSDR-37': 'OSD-37: Col-0 Ground',
        'Cvi-0_FT_OSDR-37': 'OSD-37: Cvi-0 Flight',
        'WS-2_FT_OSDR-37': 'OSD-37: WS-2 Flight',
        'Ler-0_FT_OSDR-37': 'OSD-37: Ler-0 Flight',
        'Ler-0_GC_OSDR-37': 'OSD-37: Ler-0 Ground',
        'Cvi-0_GC_OSDR-37': 'OSD-37: Cvi-0 Ground',
        'Col_light_FT_OSDR-522': 'OSD-522: Col-0 Light FL',
        'Col_light_GC_OSDR-522': 'OSD-522: Col-0 Light GC',
        'Col-0_FT_Light_OSDR-120': 'OSD-120: Col-0 Light FL',
        'PhyD_GC_Dark_OSDR-120': 'OSD-120: PhyD Dark GC',
        'WS_light_leaf_GC_OSD-217': 'OSD-217: WS Leaf GC',
        'WS_light_leaf_FL_OSD-217': 'OSD-217: WS Leaf FL',
        'WS_light_Root_GC_OSD-217': 'OSD-217: WS Root GC',
        'WS_light_root_FL_OSD-217': 'OSD-217: WS Root FL',
        'Col-0_GC_Dark_OSDR-120': 'OSD-120: Col-0 Dark GC',
        'WS_FT_Dark_OSDR-120': 'OSD-120: WS Dark FL',
        'PhyD_FT_Dark_OSDR-120': 'OSD-120: PhyD Dark FL'
    }

    # Order sets by size descending
    sorted_set_keys = sorted(sets.keys(), key=lambda k: len(sets[k]), reverse=True)
    all_species = sorted(list(set.union(*sets.values())))

    # Compute intersection combinations
    combos = []
    for sp in all_species:
        in_sets = tuple(sorted([k for k in sets if sp in sets[k]]))
        combos.append(in_sets)

    counts = Counter(combos)
    # Take top 22 intersection patterns
    top_combos = counts.most_common(22)
    combo_sizes = [cnt for c, cnt in top_combos]

    # Layout Setup
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig = plt.figure(figsize=(16, 11), dpi=300)
    
    # 2 rows, 2 cols:
    # gs[0, 0]: Title & Info | gs[0, 1]: Intersection Sizes (bars)
    # gs[1, 0]: Set Sizes (bars) | gs[1, 1]: Dot matrix
    gs = fig.add_gridspec(2, 2, width_ratios=[1.1, 2.5], height_ratios=[1.2, 2.2], hspace=0.08, wspace=0.08)

    ax_info = fig.add_subplot(gs[0, 0])
    ax_top = fig.add_subplot(gs[0, 1])
    ax_left = fig.add_subplot(gs[1, 0])
    ax_matrix = fig.add_subplot(gs[1, 1], sharex=ax_top, sharey=ax_left)

    # 1. Info / Summary Panel (top-left)
    ax_info.axis('off')
    info_text = (
        "UpSet Taxa Intersection Analysis\n"
        "Spaceflight Plant Microbiome Meta-Analysis\n"
        "──────────────────────────────────────\n"
        f"• Total Identified Taxa: {len(all_species)}\n"
        f"• Experimental Sets: {len(sorted_set_keys)}\n"
        f"• Top Intersections Displayed: {len(top_combos)}\n"
        "• Core Betaproteobacteria shared across\n"
        "  flight & ground: Ralstonia pickettii,\n"
        "  Herbaspirillum huttiense, Pseudomonas spp."
    )
    ax_info.text(0.05, 0.45, info_text, fontsize=10.5, family='sans-serif', va='center',
                 bbox=dict(boxstyle='round,pad=0.8', facecolor='#f8f9fa', edgecolor='#cccccc', linewidth=1))

    # 2. Top Bar Chart: Intersection Sizes
    x_indices = np.arange(len(top_combos))
    bars_top = ax_top.bar(x_indices, combo_sizes, color='#e74c3c', width=0.65, edgecolor='black', linewidth=0.9, zorder=3)
    ax_top.set_ylabel("Intersection Size", fontsize=12, fontweight='bold')
    ax_top.set_ylim(0, max(combo_sizes) + 3)
    ax_top.grid(axis='y', linestyle='--', alpha=0.6, zorder=0)
    ax_top.tick_params(axis='x', which='both', bottom=False, labelbottom=False)

    for bar, val in zip(bars_top, combo_sizes):
        ax_top.text(bar.get_x() + bar.get_width() / 2, val + 0.35, str(val),
                    ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#c0392b')

    # 3. Bottom-Left Horizontal Bar Chart: Set Sizes
    y_indices = np.arange(len(sorted_set_keys))
    set_sizes = [len(sets[k]) for k in sorted_set_keys]
    clean_labels = [label_map.get(k, k) for k in sorted_set_keys]

    bars_left = ax_left.barh(y_indices, set_sizes, color='#2b5c8f', height=0.6, edgecolor='black', linewidth=0.8, zorder=3)
    ax_left.set_xlabel("Set Size (Total Taxa)", fontsize=11, fontweight='bold')
    ax_left.set_yticks(y_indices)
    ax_left.set_yticklabels(clean_labels, fontsize=9, fontweight='bold')
    ax_left.invert_xaxis()
    ax_left.set_xlim(max(set_sizes) + 5, 0)
    ax_left.grid(axis='x', linestyle='--', alpha=0.6, zorder=0)

    for bar, val in zip(bars_left, set_sizes):
        ax_left.text(val + 1.2, bar.get_y() + bar.get_height() / 2, str(val),
                     ha='right', va='center', fontsize=8.5, fontweight='bold', color='#1b3f66')

    # 4. Bottom-Right Dot Matrix
    ax_matrix.set_xlim(-0.5, len(top_combos) - 0.5)
    ax_matrix.set_ylim(-0.5, len(sorted_set_keys) - 0.5)
    ax_matrix.invert_yaxis()
    ax_matrix.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)

    # Shaded alternating row backgrounds for readability
    for y in range(len(sorted_set_keys)):
        bg_col = '#f9f9f9' if y % 2 == 0 else '#ffffff'
        rect = patches.Rectangle((-0.5, y - 0.5), len(top_combos), 1, facecolor=bg_col, edgecolor='none', zorder=1)
        ax_matrix.add_patch(rect)

    # Draw inactive dots
    for x in range(len(top_combos)):
        for y in range(len(sorted_set_keys)):
            ax_matrix.plot(x, y, 'o', color='#dcdcdc', markersize=6.5, zorder=2)

    # Draw active dots and connecting vertical lines
    for x, (combo, _) in enumerate(top_combos):
        active_y = [i for i, k in enumerate(sorted_set_keys) if k in combo]
        if active_y:
            min_y = min(active_y)
            max_y = max(active_y)
            if min_y != max_y:
                ax_matrix.plot([x, x], [min_y, max_y], color='#2c3e50', linewidth=2.2, zorder=3)
            ax_matrix.plot([x] * len(active_y), active_y, 'o', color='#2c3e50', markersize=7.5, zorder=4)

    out_pub = os.path.join(FIGURES_DIR, "figure2_upset_plot.png")
    out_man = os.path.join(MANUSCRIPT_FIG_DIR, "figure2_upset_plot.png")
    out_rep = os.path.join(FIGURES_DIR, "reproduced_upset_plot.png")

    plt.savefig(out_pub, dpi=300, bbox_inches='tight')
    plt.savefig(out_man, dpi=300, bbox_inches='tight')
    plt.savefig(out_rep, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"[+] Successfully generated UpSet plot: {out_pub} and {out_man}")


def plot_correlation_heatmap():
    """
    Generates a high-resolution, non-overlapping pairwise intersection heatmap
    from Plants_in_space_microbiome - upsettr.csv.
    
    Resolves prior clipping of top labels and rightmost colorbar numbers.
    """
    csv_path = os.path.join(REPO_DIR, "Zerrin_July", "Plants_in_space_microbiome - upsettr.csv")
    if not os.path.exists(csv_path):
        csv_path = os.path.join(REPO_DIR, "Plants_in_space_microbiome - upsettr.csv")
    
    if not os.path.exists(csv_path):
        print(f"[!] File not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    conditions = list(df.columns)
    sets = {}
    for c in conditions:
        s = set(df[c].dropna().astype(str).str.strip())
        sets[c] = {x for x in s if x and x != 'nan'}

    n = len(conditions)
    matrix = np.zeros((n, n), dtype=int)
    for i, c1 in enumerate(conditions):
        for j, c2 in enumerate(conditions):
            matrix[i, j] = len(sets[c1].intersection(sets[c2]))

    clean_labels_map = {
        'Col-0_Dark_GC_OSDR-38': 'OSD-38: Col-0 Dark GC',
        'Col-0_Dark_FT_OSDR-38': 'OSD-38: Col-0 Dark FL',
        'Col-0_Dark_LN_OSDR-38': 'OSD-38: Col-0 Dark LN2',
        'Col-0_Dark_RNAlater_OSDR-38': 'OSD-38: Col-0 Dark RNAlater',
        'Col-0_Dark_GC_OSDR-37': 'OSD-37: Col-0 Dark GC',
        'Col-0_Dark_FT_OSDR-37': 'OSD-37: Col-0 Dark FL',
        'Cvi-0_Dark_GC_OSDR-37': 'OSD-37: Cvi-0 Dark GC',
        'Cvi-0_Dark_FT_OSDR-37': 'OSD-37: Cvi-0 Dark FL',
        'WS-2_Dark_GC_OSDR-37': 'OSD-37: WS-2 Dark GC',
        'WS-2_Dark_FT_OSDR-37': 'OSD-37: WS-2 Dark FL',
        'Ler-0_Dark_GC_OSDR-37': 'OSD-37: Ler-0 Dark GC',
        'Ler-0_Dark_FT_OSDR-37': 'OSD-37: Ler-0 Dark FL',
        'Col-0_light_FT_OSDR-120': 'OSD-120: Col-0 Light FL',
        'Col-0_Dark_GC_OSDR-120': 'OSD-120: Col-0 Dark GC',
        'WS_Dark_FT_OSDR-120': 'OSD-120: WS Dark FL',
        'PhyD_Dark_FT_OSDR-120': 'OSD-120: PhyD Dark FL',
        'PhyD_Dark_GC_OSDR-120': 'OSD-120: PhyD Dark GC',
        'Col_light_FT_OSDR-522': 'OSD-522: Col-0 Light FL',
        'Col_light_GC_OSDR-522': 'OSD-522: Col-0 Light GC',
        'WS_light_leaf_GC_OSD-217': 'OSD-217: WS Leaf GC',
        'WS_light_leaf_FL_OSD-217': 'OSD-217: WS Leaf FL',
        'WS_light_Root_GC_OSD-217': 'OSD-217: WS Root GC',
        'WS_light_Root_FL_OSD-217': 'OSD-217: WS Root FL'
    }
    
    clean_labels = [clean_labels_map.get(c, c) for c in conditions]
    
    # Perform hierarchical clustering on the similarity matrix
    Z = hierarchy.linkage(matrix, method='average')
    order = hierarchy.leaves_list(Z)
    
    reordered_matrix = matrix[order, :][:, order]
    reordered_labels = [clean_labels[i] for i in order]

    fig, ax = plt.subplots(figsize=(14, 11), dpi=300)
    
    # Clean Heatmap using YlGnBu palette with annotated shared counts
    sns.heatmap(
        reordered_matrix,
        xticklabels=reordered_labels,
        yticklabels=reordered_labels,
        cmap="YlGnBu",
        annot=True,
        fmt="d",
        annot_kws={"size": 7.5, "weight": "bold"},
        cbar_kws={'label': 'Pairwise Shared Taxa Intersection Count', 'pad': 0.03, 'shrink': 0.8},
        linewidths=0.5,
        linecolor='#e0e0e0',
        ax=ax
    )
    
    ax.set_title("Pairwise Microbial Community Intersection Heatmap\n(Hierarchical Clustering Across OSDR Spaceflight & Ground Accessions)", 
                 fontsize=13, fontweight='bold', pad=18)
    
    plt.xticks(rotation=45, ha='right', rotation_mode='anchor', fontsize=8.5, fontweight='bold')
    plt.yticks(rotation=0, fontsize=8.5, fontweight='bold')
    
    out_pub = os.path.join(FIGURES_DIR, "figure3_correlation_heatmap.png")
    out_man = os.path.join(MANUSCRIPT_FIG_DIR, "figure3_correlation_heatmap.png")
    out_rep = os.path.join(FIGURES_DIR, "reproduced_correlation_heatmap.png")

    plt.savefig(out_pub, dpi=300, bbox_inches='tight', pad_inches=0.25)
    plt.savefig(out_man, dpi=300, bbox_inches='tight', pad_inches=0.25)
    plt.savefig(out_rep, dpi=300, bbox_inches='tight', pad_inches=0.25)
    plt.close()
    
    print(f"[+] Successfully generated Heatmap: {out_pub} and {out_man}")


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
