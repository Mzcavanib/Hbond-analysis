#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Color palette in order
colors = [
    (31/255, 119/255, 180/255),  # Deep blue
    (214/255, 39/255, 40/255),   # Crimson red    
    (148/255, 103/255, 189/255), # Dark purple
    (140/255, 86/255, 75/255),   # Earth brown
    (23/255, 190/255, 207/255),  # Light cyan
    (44/255, 160/255, 44/255),   # Vibrant green
    (255/255, 127/255, 14/255),  # Intense orange
    (227/255, 119/255, 194/255), # Strong pink
    (127/255, 127/255, 127/255), # Medium gray
    (188/255, 189/255, 34/255)   # Golden yellow
]

def load_hbond_xvg(path):
    data = []
    with open(path, 'r') as f:
        for line in f:
            if line.startswith(('#', '@')):
                continue
            parts = line.strip().split()
            if len(parts) >= 2:
                try:
                    hbond = float(parts[1])
                    data.append(hbond)
                except ValueError:
                    continue
    return np.array(data)

def main():
    if len(sys.argv) < 2:
        print("Usage: ./hbond.py file1.xvg file2.xvg ...")
        sys.exit(1)

    files = sys.argv[1:]
    total = len(files)
    plt.figure(figsize=(8, 6))

    for i, file in enumerate(files):
        if i >= len(colors):
            print(f"Warning: no color defined for file {file}, it will be skipped.")
            continue

        data = load_hbond_xvg(file)
        if data.size == 0:
            print(f"Warning: file {file} contains no valid data.")
            continue

        kde = gaussian_kde(data)
        x_vals = np.linspace(min(data), max(data), 500)
        y_vals = kde(x_vals)

        label = file.split('/')[-1].replace('.xvg', '')
        color = colors[i]
        z = total - i  # inverse z-order: first goes on top

        # Only shaded area with uniform transparency
        plt.fill_between(x_vals, y_vals, color=color, alpha=0.4, label=label, zorder=z)

    plt.xlabel("Number of hydrogen bonds")
    plt.ylabel("Kernel density")
    plt.title("KDE distribution of hydrogen bonds")
    plt.legend()
    plt.tight_layout()
    plt.savefig("hbond_kde.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    main()
