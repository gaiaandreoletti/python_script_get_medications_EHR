import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "medication_data_with_final_overlap.tsv"  # Update path if necessary
df = pd.read_csv(file_path, sep="\t")

# Ensure correct data types
df["order_start"] = pd.to_datetime(df["order_start"])  # Convert dates
df["ADMINISTERED_DOSE"] = pd.to_numeric(df["ADMINISTERED_DOSE"], errors="coerce")  # Convert doses

# Sort by Patient, Drug, and Start Date
df = df.sort_values(by=["NFER_PID", "NFER_DRUG", "order_start"])

# Compute dose change per patient & drug
df["Dose_Change"] = df.groupby(["NFER_PID", "NFER_DRUG"])["ADMINISTERED_DOSE"].diff()

# Filter for drugs with available data
unique_drugs = df["NFER_DRUG"].dropna().unique()

# 📈 **Line Plot: Individual Patient Dose Changes Over Time per Drug**
for drug in unique_drugs:
    plt.figure(figsize=(12, 6))
    subset = df[df["NFER_DRUG"] == drug]
    sns.lineplot(data=subset, x="order_start", y="ADMINISTERED_DOSE", hue="NFER_PID", alpha=0.5, legend=False)
    
    plt.title(f"Titration Pattern for {drug}", fontsize=14)
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Dose (mg, IU, etc.)", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

# 📊 **Histogram: Dose Change Distribution per Drug**
for drug in unique_drugs:
    plt.figure(figsize=(12, 6))
    subset = df[df["NFER_DRUG"] == drug]
    
    sns.histplot(subset["Dose_Change"].dropna(), bins=20, kde=True, color="blue")
    plt.xlabel("Dose Change (mg, IU, etc.)", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.title(f"Histogram of Dose Adjustments for {drug}", fontsize=14)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()
