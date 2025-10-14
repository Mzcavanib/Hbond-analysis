#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Paleta de colores en orden
colores = [
    (31/255, 119/255, 180/255),  # Azul profundo
    (214/255, 39/255, 40/255),   # Rojo carmín    
    (148/255, 103/255, 189/255), # Púrpura oscuro
    (140/255, 86/255, 75/255),   # Marrón tierra
    (23/255, 190/255, 207/255),  # Cian claro
    (44/255, 160/255, 44/255),   # Verde vibrante
    (255/255, 127/255, 14/255),  # Naranja intenso
    (227/255, 119/255, 194/255), # Rosa fuerte
    (127/255, 127/255, 127/255), # Gris medio
    (188/255, 189/255, 34/255)   # Amarillo dorado
]

def cargar_hbond_xvg(ruta):
    datos = []
    with open(ruta, 'r') as f:
        for linea in f:
            if linea.startswith(('#', '@')):
                continue
            partes = linea.strip().split()
            if len(partes) >= 2:
                try:
                    hbond = float(partes[1])
                    datos.append(hbond)
                except ValueError:
                    continue
    return np.array(datos)

def main():
    if len(sys.argv) < 2:
        print("Uso: ./hbond.py archivo1.xvg archivo2.xvg ...")
        sys.exit(1)

    archivos = sys.argv[1:]
    total = len(archivos)
    plt.figure(figsize=(8, 6))

    for i, archivo in enumerate(archivos):
        if i >= len(colores):
            print(f"Advertencia: no hay color definido para el archivo {archivo}, se omitirá.")
            continue

        datos = cargar_hbond_xvg(archivo)
        if datos.size == 0:
            print(f"Advertencia: el archivo {archivo} no contiene datos válidos.")
            continue

        kde = gaussian_kde(datos)
        x_vals = np.linspace(min(datos), max(datos), 500)
        y_vals = kde(x_vals)

        etiqueta = archivo.split('/')[-1].replace('.xvg', '')
        color = colores[i]
        z = total - i  # zorder inverso: el primero va encima

        # Solo sombreado con transparencia uniforme
        plt.fill_between(x_vals, y_vals, color=color, alpha=0.4, label=etiqueta, zorder=z)

    plt.xlabel("Número de puentes de hidrógeno")
    plt.ylabel("Densidad de kernel")
    plt.title("Distribución KDE de puentes de hidrógeno")
    plt.legend()
    plt.tight_layout()
    plt.savefig("hbond_kde.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    main()

