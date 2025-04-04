import pandas as pd

# ---- Load Datasets ----
antidiabetic_file_path = "antidiabetic_summary.csv"
t2d_file_path = "filtered_igf1_data_with_category_404pt_T2D_4Feb2025.tsv"

# Load datasets
df_antidiabetic = pd.read_csv(antidiabetic_file_path, sep=",", low_memory=True)
df_t2d = pd.read_csv(t2d_file_path, sep="\t", low_memory=True)

# ---- Ensure NFER_PID is in String Format ----
df_antidiabetic["NFER_PID"] = df_antidiabetic["NFER_PID"].astype(str)
df_t2d["NFER_PID"] = df_t2d["NFER_PID"].astype(str)

# ---- Identify Patients Taking Antidiabetics (Including Insulin) ----
antidiabetic_patients = set(df_antidiabetic["NFER_PID"].unique())

# ---- Identify Patients Taking Insulin ----
insulin_patients = set(df_antidiabetic[df_antidiabetic["NFER_DRUG"].str.contains("insulin", case=False, na=False)]["NFER_PID"].unique())

# ---- Annotate Patients in the T2D Dataset ----
df_t2d["Antidiabetics_Flag"] = df_t2d["NFER_PID"].apply(lambda x: "Yes" if x in antidiabetic_patients else "No")
df_t2d["Insulin_Flag"] = df_t2d["NFER_PID"].apply(lambda x: "Yes" if x in insulin_patients else "No")

# ---- Save Updated Dataset ----
output_file = "t2d_with_medication_flags.tsv"
df_t2d.to_csv(output_file, sep="\t", index=False)

# ---- Display Confirmation ----
print(f"✅ Updated T2D dataset saved as '{output_file}'.")
