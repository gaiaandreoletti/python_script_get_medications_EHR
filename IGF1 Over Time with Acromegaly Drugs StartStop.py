import pandas as pd
import matplotlib.pyplot as plt

# ---- Load the main dataset ----
file_path = "filtered_igf1_data_with_category_404pt_T2D_antidiabetics_17Feb2025.tsv"
df = pd.read_csv(file_path, sep="\t", low_memory=False)

# ---- Convert dates to datetime format ----
date_cols = ["LAB_RESULT_DTM", "Pegvisomant_Start", "Pegvisomant_Stop", "SRL_Start", "SRL_Stop", "Cabergoline_Start", "Cabergoline_Stop"]
for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# ---- Filter patients who have IGF1 measurements ----
filtered_patients = df.dropna(subset=["IGF1_Value"])

# ---- Plot IGF1 values over time with acromegaly drug start/stop ----
plt.figure(figsize=(12, 6))

for pid, patient_data in filtered_patients.groupby("NFER_PID"):
    plt.plot(patient_data["LAB_RESULT_DTM"], patient_data["IGF1_Value"], marker="o", linestyle="-", label=f"Patient {pid}")

    # Mark Pegvisomant, SRL, Cabergoline Start/Stop
    for _, row in patient_data.iterrows():
        if pd.notna(row["Pegvisomant_Start"]):
            plt.axvline(row["Pegvisomant_Start"], color="green", linestyle="--", label="Pegvisomant Start")
        if pd.notna(row["Pegvisomant_Stop"]):
            plt.axvline(row["Pegvisomant_Stop"], color="red", linestyle="--", label="Pegvisomant Stop")
        if pd.notna(row["SRL_Start"]):
            plt.axvline(row["SRL_Start"], color="blue", linestyle="--", label="SRL Start")
        if pd.notna(row["SRL_Stop"]):
            plt.axvline(row["SRL_Stop"], color="purple", linestyle="--", label="SRL Stop")
        if pd.notna(row["Cabergoline_Start"]):
            plt.axvline(row["Cabergoline_Start"], color="orange", linestyle="--", label="Cabergoline Start")
        if pd.notna(row["Cabergoline_Stop"]):
            plt.axvline(row["Cabergoline_Stop"], color="brown", linestyle="--", label="Cabergoline Stop")

plt.xlabel("Date")
plt.ylabel("IGF1 Level")
plt.title("IGF1 Over Time with Acromegaly Drug Start/Stop Events")
plt.legend()
plt.grid(True)
plt.show()
