#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot number of hydrogen bonds vs time for multiple .xvg files
with smoothed lines (moving average).
Usage:
    python3 hbond_vs_time.py hbond_wt_complex.xvg hbond_alpha_complex.xvg ...
"""

import sys
import matplotlib.pyplot as plt
import numpy as np

def load_xvg_data(filename):
    times_ns = []
    hbonds = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith(('@', '#')) or not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) >= 2:
                try:
                    time_ps = float(parts[0])
                    count = int(float(parts[1]))
                    times_ns.append(time_ps / 1000.0)  # ps → ns
                    hbonds.append(count)
                except ValueError:
                    continue
    return np.array(times_ns), np.array(hbonds)

def moving_average(y, window=50):
    """Simple smoothing with moving average."""
    if len(y) < window:
        return y
    return np.convolve(y, np.ones(window)/window, mode='valid')

def plot_hbond_lines(all_data, output_file="hbonds_vs_time.png"):
    plt.figure(figsize=(10, 6))
    for label, (times_ns, hbonds) in all_data.items():
        y_smooth = moving_average(hbonds, window=50)
        x_smooth = times_ns[:len(y_smooth)]
        plt.plot(x_smooth, y_smooth, linewidth=1.8, label=label)
    plt.xlabel("Time [ns]", fontsize=12)
    plt.ylabel("Hydrogen bonds", fontsize=12)
    plt.title("Hydrogen bonds vs time (smoothed lines)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 hbond_vs_time.py file1.xvg file2.xvg ...")
        sys.exit(1)

    # Dictionary of custom labels
    labels = {
        "hbond_WT_complex.xvg": "WT",
        "hbond_alpha_complex.xvg": "Alpha",
        "hbond_gamma_complex.xvg": "Gamma",
        "hbond_delta_complex.xvg": "Delta",
        "hbond_omicronba1_complex.xvg": "Omicron BA.1"
    }

    all_data = {}

    for filename in sys.argv[1:]:
        times_ns, hbonds = load_xvg_data(filename)
        if len(times_ns) == 0 or len(hbonds) == 0:
            print(f"{filename}: contains no valid data")
            continue

        # Use defined label, if not available use filename
        label = labels.get(filename, filename)
        all_data[label] = (times_ns, hbonds)

        print(f"\n=== Results for {label} ===")
        print(f"Frames analyzed: {len(times_ns)}")
        print(f"Maximum bonds in a frame: {max(hbonds)}")
        print(f"Average bonds per frame: {np.mean(hbonds):.2f}")

    if all_data:
        plot_hbond_lines(all_data)
        print("\nPlot generated: hbonds_vs_time.png")
