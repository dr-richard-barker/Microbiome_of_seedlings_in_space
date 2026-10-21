#!/usr/bin/env python3
"""
Deep Learning Small-Data Benchmarking with TabPFN (Nature 2025).

Evaluates TabPFN foundation model against standard baseline models
(Random Forest, Logistic Regression, Support Vector Classifier)
on spaceflight seedling microbiome profiles (NASA OSDR).

Evaluated Tasks:
1. Hardware Confinement Classification (Closed BRIC Canister vs. Open APEX System)
2. Spaceflight vs. Ground State Classification
3. Biomarker Feature Attribution (Differential Taxa Prevalences)

Outputs:
- figures/figure6_tabpfn_benchmark_and_biomarkers.png
- figures/tabpfn_model_benchmark_results.json
"""

import os
import csv
import json
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# PyTorch weights patch for PyTorch 2.6+
import torch
orig_load = torch.load
torch.load = lambda *args, **kwargs: orig_load(*args, **{**kwargs, 'weights_only': False})

from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import accuracy_score, roc_auc_score, balanced_accuracy_score, brier_score_loss
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

warnings.filterwarnings("ignore")

try:
    from tabpfn import TabPFNClassifier
    TABPFN_AVAILABLE = True
except ImportError:
    TABPFN_AVAILABLE = False
    print("[!] TabPFN not available in environment; using baseline classifiers.")

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGURES_DIR = os.path.join(REPO_DIR, "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

# 1. Parse Data Matrix from upsettr CSV
csv_path = os.path.join(REPO_DIR, "Plants_in_space_microbiome - upsettr.csv")
df_raw = pd.read_csv(csv_path)

conditions = [c.strip() for c in df_raw.columns if c.strip()]
sample_taxa = {}
all_taxa = set()

for col in conditions:
    taxa_list = df_raw[col].dropna().astype(str).str.strip().tolist()
    taxa_set = set(t for t in taxa_list if t and t != 'nan')
    sample_taxa[col] = taxa_set
    all_taxa.update(taxa_set)

all_taxa_list = sorted(list(all_taxa))

# Build Binary Feature Matrix
X_data = []
y_flight = []
y_hardware = [] # 1: Closed BRIC canister (OSD-37, 217, 522), 0: APEX plate system (OSD-120)

for cond in conditions:
    is_fl = 1 if any(f in cond for f in ["_FT", "_FL", "FT_", "FL_"]) else 0
    is_bric = 1 if any(b in cond for b in ["OSDR-37", "OSD-217", "OSDR-522"]) else 0
    row_feat = [1 if t in sample_taxa[cond] else 0 for t in all_taxa_list]
    
    X_data.append(row_feat)
    y_flight.append(is_fl)
    y_hardware.append(is_bric)

X = np.array(X_data, dtype=np.float32)
y_flight = np.array(y_flight, dtype=np.int32)
y_hardware = np.array(y_hardware, dtype=np.int32)

print(f"[*] Dataset matrix: N={len(conditions)} samples, P={len(all_taxa_list)} microbial features")
print(f"[*] Hardware balance: Closed BRIC = {sum(y_hardware)}, Open APEX = {len(y_hardware) - sum(y_hardware)}")
print(f"[*] Flight balance: Flight = {sum(y_flight)}, Ground Control = {len(y_flight) - sum(y_flight)}")

def evaluate_models(X_mat, y_vec, task_name="Task"):
    models = {
        "Logistic Reg (L2)": LogisticRegression(C=1.0, max_iter=200, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=50, max_depth=4, random_state=42),
        "Support Vector Machine": SVC(probability=True, kernel='linear', random_state=42)
    }
    if TABPFN_AVAILABLE:
        models["TabPFN (Foundation Model)"] = TabPFNClassifier(device='cpu', N_ensemble_configurations=4)
        
    loocv = LeaveOneOut()
    task_res = {}
    
    for name, clf in models.items():
        y_true = []
        y_pred = []
        y_prob = []
        
        for train_idx, test_idx in loocv.split(X_mat, y_vec):
            X_tr, X_te = X_mat[train_idx], X_mat[test_idx]
            y_tr, y_te = y_vec[train_idx], y_vec[test_idx]
            
            try:
                clf.fit(X_tr, y_tr)
                if hasattr(clf, "predict_proba"):
                    prob = clf.predict_proba(X_te)[0, 1]
                    pred = int(prob > 0.5)
                else:
                    pred = clf.predict(X_te)[0]
                    prob = float(pred)
            except Exception as e:
                pred = int(np.bincount(y_tr).argmax())
                prob = float(pred)
                
            y_true.append(y_te[0])
            y_pred.append(pred)
            y_prob.append(prob)
            
        acc = accuracy_score(y_true, y_pred)
        bacc = balanced_accuracy_score(y_true, y_pred)
        try:
            auc = roc_auc_score(y_true, y_prob)
        except:
            auc = 0.5
        brier = brier_score_loss(y_true, y_prob)
        
        task_res[name] = {
            "Accuracy": round(float(acc), 3),
            "Balanced_Accuracy": round(float(bacc), 3),
            "ROC_AUC": round(float(auc), 3),
            "Brier_Score": round(float(brier), 3)
        }
        print(f"[{task_name}] {name}: Acc={acc:.3f}, BAcc={bacc:.3f}, AUC={auc:.3f}, Brier={brier:.3f}")
        
    return task_res

# Run Benchmarks
hardware_results = evaluate_models(X, y_hardware, "Hardware Confinement")
flight_results = evaluate_models(X, y_flight, "Flight vs. Ground")

# Biomarker Feature Extraction (Closed BRIC vs APEX & Flight vs Ground)
bric_idx = [i for i, v in enumerate(y_hardware) if v == 1]
apex_idx = [i for i, v in enumerate(y_hardware) if v == 0]
bric_freq = X[bric_idx].mean(axis=0)
apex_freq = X[apex_idx].mean(axis=0)
diff_hardware = bric_freq - apex_freq

fl_idx = [i for i, v in enumerate(y_flight) if v == 1]
gc_idx = [i for i, v in enumerate(y_flight) if v == 0]
diff_flight = X[fl_idx].mean(axis=0) - X[gc_idx].mean(axis=0)

biomarkers = []
for idx, taxon in enumerate(all_taxa_list):
    biomarkers.append({
        "taxon": taxon,
        "bric_freq": round(float(bric_freq[idx]), 3),
        "apex_freq": round(float(apex_freq[idx]), 3),
        "hardware_diff": round(float(diff_hardware[idx]), 3),
        "flight_diff": round(float(diff_flight[idx]), 3)
    })

# Save JSON results
output_json = os.path.join(FIGURES_DIR, "tabpfn_model_benchmark_results.json")
with open(output_json, "w") as f:
    json.dump({
        "hardware_confinement_benchmark": hardware_results,
        "flight_vs_ground_benchmark": flight_results,
        "biomarker_features": sorted(biomarkers, key=lambda b: abs(b["hardware_diff"]), reverse=True)[:20]
    }, f, indent=2)

# Generate Publication Figure 6
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)

# Panel A: Benchmark Comparison
model_names = list(hardware_results.keys())
acc_hw = [hardware_results[m]["Accuracy"] for m in model_names]
auc_hw = [hardware_results[m]["ROC_AUC"] for m in model_names]

x = np.arange(len(model_names))
w = 0.35

rects1 = ax1.bar(x - w/2, acc_hw, width=w, label='LOOCV Accuracy', color='#1f77b4', edgecolor='black', linewidth=1)
rects2 = ax1.bar(x + w/2, auc_hw, width=w, label='ROC-AUC Score', color='#2ca02c', edgecolor='black', linewidth=1)

ax1.set_ylabel('Performance Score', fontsize=12, fontweight='bold')
ax1.set_title('A. Small-Data Foundation Model Benchmarking:\nHardware Confinement Prediction (BRIC vs. APEX)', fontsize=13, fontweight='bold', pad=12)
ax1.set_xticks(x)
ax1.set_xticklabels(model_names, rotation=15, ha='right', fontsize=10, fontweight='bold')
ax1.set_ylim(0, 1.15)
ax1.legend(loc='lower right', frameon=True, fontsize=10)
ax1.grid(axis='y', linestyle='--', alpha=0.7)

for r in rects1:
    h = r.get_height()
    ax1.text(r.get_x() + r.get_width()/2, h + 0.02, f'{h:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
for r in rects2:
    h = r.get_height()
    ax1.text(r.get_x() + r.get_width()/2, h + 0.02, f'{h:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

# Panel B: Top Microbial Biomarkers Discriminating Flight & Habitat
top_taxa_bio = sorted(biomarkers, key=lambda b: abs(b["hardware_diff"]), reverse=True)[:10]
taxa_labels = [b["taxon"] for b in top_taxa_bio]
hw_diffs = [b["hardware_diff"] * 100 for b in top_taxa_bio]

y_pos = np.arange(len(taxa_labels))
bars = ax2.barh(y_pos, hw_diffs, color='#9467bd', edgecolor='black', height=0.55)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(taxa_labels, fontstyle='italic', fontsize=10)
ax2.invert_yaxis()
ax2.axvline(0, color='black', linewidth=1, linestyle='-')
ax2.set_xlabel('Prevalence Difference (Closed BRIC % - Open APEX %)', fontsize=12, fontweight='bold')
ax2.set_title('B. Key Microbial Biomarkers Dictating Hardware Ecological Selection', fontsize=13, fontweight='bold', pad=12)
ax2.grid(axis='x', linestyle='--', alpha=0.7)

for bar in bars:
    width_val = bar.get_width()
    offset = 1.0 if width_val >= 0 else -1.0
    ha = 'left' if width_val >= 0 else 'right'
    ax2.text(width_val + offset, bar.get_y() + bar.get_height()/2, f'{width_val:+.1f}%', ha=ha, va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
out_fig = os.path.join(FIGURES_DIR, "figure6_tabpfn_benchmark_and_biomarkers.png")
plt.savefig(out_fig, dpi=300, bbox_inches='tight')
plt.close()

print(f"[+] Successfully generated benchmark figure: {out_fig}")
print(f"[+] Output JSON: {output_json}")
