import matplotlib.pyplot as plt

XVGFILENAME = "hbonds.xvg"
NDXFILENAME = "hbond.ndx"
TIMESERIES_PLOT = "hbonds_vs_time.png"

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
                    times_ns.append(time_ps / 1000)  # Convert ps to ns
                    hbonds.append(count)
                except ValueError:
                    continue
    return times_ns, hbonds

def load_ndx_pairs(filename):
    pairs = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('[') or not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) == 2:
                pairs.append((int(parts[0]), int(parts[1])))
    return pairs

def plot_hbond_timeseries(times_ns, hbonds, output_file):
    plt.figure(figsize=(10, 6))
    plt.plot(times_ns, hbonds, color='darkorange', linewidth=1.5)
    plt.xlabel("Tiempo (ns)")
    plt.ylabel("Puentes de hidrógeno")
    plt.title("Cantidad de puentes de hidrógeno a lo largo de la trayectoria")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()

if __name__ == "__main__":
    times_ns, hbonds = load_xvg_data(XVGFILENAME)
    pairs = load_ndx_pairs(NDXFILENAME)

    print(f"Frames analizados: {len(times_ns)}")
    print(f"Máximo de puentes en un frame: {max(hbonds) if hbonds else 'N/A'}")
    print(f"Promedio de puentes por frame: {sum(hbonds)/len(hbonds):.2f}" if hbonds else "N/A")
    print(f"Pares únicos donador–aceptor detectados: {len(pairs)}")

    if times_ns and hbonds:
        plot_hbond_timeseries(times_ns, hbonds, TIMESERIES_PLOT)

