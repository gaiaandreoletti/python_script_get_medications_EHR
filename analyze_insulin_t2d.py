import pandas as pd

# ---- Load Datasets ----
hba1c_file_path = "merged_hba1c_height_data.tsv"  # Update if necessary
antidiabetic_file_path = "antidiabetic_summary.csv"
t2d_file_path = "filtered_igf1_data_with_category_404pt_T2D_4Feb2025.tsv"

# Load datasets
df_hba1c = pd.read_csv(hba1c_file_path, sep="\t", low_memory=True)
df_antidiabetic = pd.read_csv(antidiabetic_file_path, sep=",", low_memory=True)
df_t2d = pd.read_csv(t2d_file_path, sep="\t", low_memory=True)

# ---- Ensure NFER_PID is in String Format ----
df_hba1c["NFER_PID"] = df_hba1c["NFER_PID"].astype(str)
df_antidiabetic["NFER_PID"] = df_antidiabetic["NFER_PID"].astype(str)
df_t2d["NFER_PID"] = df_t2d["NFER_PID"].astype(str)

# ---- Convert HbA1c Values to Numeric ----
df_hba1c["hba1c_Value"] = pd.to_numeric(df_hba1c["hba1c_Value"], errors="coerce")

# ---- Define HbA1c Categories ----
df_hba1c["HbA1c_Category"] = pd.cut(
    df_hba1c["hba1c_Value"],
    bins=[0, 5.7, 6.4, float("inf")],
    labels=["Normal", "Prediabetes", "Diabetes"]
)

# ---- Identify Patients Taking Insulin ----
insulin_patients = set(df_antidiabetic[df_antidiabetic["NFER_DRUG"].str.contains("insulin", case=False, na=False)]["NFER_PID"].unique())

# ---- Identify Patients with Diabetes or Prediabetes ----
diabetes_prediabetes_patients = set(df_hba1c[df_hba1c["HbA1c_Category"].isin(["Diabetes", "Prediabetes"])]["NFER_PID"].unique())

# ---- Patients on Insulin with Diabetes or Prediabetes ----
insulin_diabetes_prediabetes = len(insulin_patients & diabetes_prediabetes_patients)

# ---- Identify Patients Taking Antidiabetics (Including Insulin) ----
antidiabetic_patients = set(df_antidiabetic["NFER_PID"].unique())

# ---- Patients on Antidiabetics (or Insulin) with Diabetes or Prediabetes ----
antidiabetics_diabetes_prediabetes = len(antidiabetic_patients & diabetes_prediabetes_patients)

# ---- Identify Patients with a T2D Diagnosis (T2D_Flag == "Yes") ----
t2d_diagnosed_patients = set(df_t2d[df_t2d["T2D_Flag"] == "Yes"]["NFER_PID"].unique())

# ---- Patients on Insulin with a T2D Diagnosis ----
insulin_t2d_patients = len(insulin_patients & t2d_diagnosed_patients)

# ---- Patients on Antidiabetics (Including Insulin) with a T2D Diagnosis ----
antidiabetics_t2d_patients = len(antidiabetic_patients & t2d_diagnosed_patients)

# ---- Display Results ----
print("\n--- Analysis Results ---")
print(f"Patients on Insulin with Diabetes or Prediabetes: {insulin_diabetes_prediabetes}")
print(f"Patients on Antidiabetics or Insulin with Diabetes or Prediabetes: {antidiabetics_diabetes_prediabetes}")
print(f"Patients on Insulin with a T2D Diagnosis: {insulin_t2d_patients}")
print(f"Patients on Antidiabetics or Insulin with a T2D Diagnosis: {antidiabetics_t2d_patients}")
