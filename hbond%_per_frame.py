import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

PDB = "md.pdb"
TPR = "md.tpr"
NDX = "index.ndx"
HBOND_XPM = "hbond_map.xpm"
HBOND_CSV = "hbond_map.csv"
HBOND_NDX = "hbond.ndx"
PAIR_PLOT = "hbond_pairs.png"
RESIDUE_PLOT = "hbond_residues.png"

# === STEP 1: Check required files ===
def check_required_files():
    for f in [PDB, TPR, NDX]:
        if not os.path.exists(f):
            raise FileNotFoundError(f"Missing required file: {f}")

# === STEP 2: Run gmx hbond ===
def run_gmx_hbond():
    print("Running gmx hbond...")
    cmd = [
        "gmx", "hbond",
        "-f", PDB,
        "-s", TPR,
        "-n", NDX,
        "-hbm", HBOND_XPM,
        "-num", "hbonds.xvg",
        "-hbn", HBOND_NDX
    ]
    subprocess.run("echo 1\n1 | " + " ".join(cmd), shell=True, check=True)

# === STEP 3: Convert .xpm to CSV ===
def convert_xpm_to_csv(xpm_file, csv_file):
    with open(xpm_file, 'r') as f:
        lines = f.readlines()

    data_lines = [line.strip().strip('"') for line in lines if line.startswith('"')]
    matrix = [list(line.replace('.', '0').replace('o', '1')) for line in data_lines]

    df = pd.DataFrame(matrix).astype(int)
    df.to_csv(csv_file, index=False)

# === STEP 4: Calculate occurrence by pair ===
def calculate_occurrence(csv_file, ndx_file):
    df = pd.read_csv(csv_file)
    df = df.T  # columns = pairs, rows = frames

    with open(ndx_file, 'r') as f:
        lines = f.readlines()
    pairs = [line.strip() for line in lines if line and not line.startswith('[')]

    df.columns = pairs[:len(df.columns)]
    occurrence = df.mean() * 100
    return df, occurrence.sort_values(ascending=False)

# === STEP 5: Plot pair occurrence ===
def plot_pair_occurrence(occurrence, output_file):
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 8))
    sns.barplot(x=occurrence.values, y=occurrence.index, palette="viridis")
    plt.xlabel("Occurrence percentage (%)", fontsize=12)
    plt.ylabel("Donor-Acceptor pair", fontsize=12)
    plt.title("Hydrogen Bond Frequency", fontsize=14)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()

# === STEP 6: Hydrogen bond occurrence by residue ===
def calculate_residue_occurrence(df):
    residue_counts = {}
    for col in df.columns:
        match = re.match(r"(\S+)-\d+.* - (\S+)-\d+", col)
        if match:
            donor_res = match.group(1)
            acceptor_res = match.group(2)
            total = df[col].sum()
            residue_counts[donor_res] = residue_counts.get(donor_res, 0) + total
            residue_counts[acceptor_res] = residue_counts.get(acceptor_res, 0) + total
    return pd.Series(residue_counts).sort_values(ascending=False)

# === STEP 7: Plot residue occurrence ===
def plot_residue_occurrence(residue_series, output_file):
    plt.figure(figsize=(10, 6))
    sns.barplot(x=residue_series.values, y=residue_series.index, palette="mako")
    plt.xlabel("Total number of occurrences", fontsize=12)
    plt.ylabel("Residue", fontsize=12)
    plt.title("Hydrogen Bond Occurrence by Residue", fontsize=14)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()

# === Complete workflow ===
if __name__ == "__main__":
    check_required_files()
    run_gmx_hbond()
    convert_xpm_to_csv(HBOND_XPM, HBOND_CSV)
    df, pair_occurrence = calculate_occurrence(HBOND_CSV, HBOND_NDX)
    plot_pair_occurrence(pair_occurrence, PAIR_PLOT)
    residue_occurrence = calculate_residue_occurrence(df)
    plot_residue_occurrence(residue_occurrence, RESIDUE_PLOT)
    print(f"Plots generated: {PAIR_PLOT}, {RESIDUE_PLOT}")
