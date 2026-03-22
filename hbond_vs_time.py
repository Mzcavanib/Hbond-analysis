#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graficar número de puentes de hidrógeno vs tiempo para múltiples archivos .xvg
con líneas suavizadas (promedio móvil).
Uso:
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
    """Suavizado simple con promedio móvil."""
    if len(y) < window:
        return y
    return np.convolve(y, np.ones(window)/window, mode='valid')

def plot_hbond_lines(all_data, output_file="hbonds_vs_time.png"):
    plt.figure(figsize=(10, 6))
    for label, (times_ns, hbonds) in all_data.items():
        y_smooth = moving_average(hbonds, window=50)
        x_smooth = times_ns[:len(y_smooth)]
        plt.plot(x_smooth, y_smooth, linewidth=1.8, label=label)
    plt.xlabel("Tiempo [ns]", fontsize=12)
    plt.ylabel("Puentes de hidrógeno", fontsize=12)
    plt.title("Puentes de hidrógeno vs tiempo (líneas suavizadas)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 hbond_vs_time.py archivo1.xvg archivo2.xvg ...")
        sys.exit(1)

    # Diccionario de etiquetas personalizadas
    etiquetas = {
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
            print(f"{filename}: no contiene datos válidos")
            continue

        # Usa la etiqueta definida, si no existe usa el nombre del archivo
        label = etiquetas.get(filename, filename)
        all_data[label] = (times_ns, hbonds)

        print(f"\n=== Resultados para {label} ===")
        print(f"Frames analizados: {len(times_ns)}")
        print(f"Máximo de puentes en un frame: {max(hbonds)}")
        print(f"Promedio de puentes por frame: {np.mean(hbonds):.2f}")

    if all_data:
        plot_hbond_lines(all_data)
        print("\nGráfico generado: hbonds_vs_time.png")

