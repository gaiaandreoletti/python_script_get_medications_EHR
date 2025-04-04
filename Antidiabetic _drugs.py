import pandas as pd

# Load IGF-1 & Medications data
file_path = "filtered_igf1_data_with_category.tsv"  # Update file name as needed
df_igf1 = pd.read_csv(file_path, sep="\t", low_memory=False)

# Load Antidiabetic medications data
med_file_path = "antidiabetic_summary.csv"
df_med = pd.read_csv(med_file_path, sep=",", low_memory=False)

# Extract Pegvisomant patients
pegvisomant_patients = df_igf1[df_igf1["Category"].str.contains("Pegvisomant", na=False)]["NFER_PID"].unique()

# Identify Pegvisomant patients on Insulin
df_med["Medication Group"] = df_med["NFER_DRUG"].apply(lambda x: "Insulin" if "insulin" in str(x).lower() else "Other Antidiabetic Drugs")
insulin_patients = df_med[df_med["Medication Group"] == "Insulin"]["NFER_PID"].unique()

# Count Pegvisomant patients on Insulin
peg_on_insulin = len(set(pegvisomant_patients) & set(insulin_patients))

# Identify Pegvisomant patients on any Antidiabetic drugs
antidiabetic_patients = df_med["NFER_PID"].unique()
peg_on_antidiabetics = len(set(pegvisomant_patients) & set(antidiabetic_patients))

# Display results
print(f"Total Pegvisomant Patients: {len(pegvisomant_patients)}")
print(f"Pegvisomant Patients on Insulin: {peg_on_insulin}")
print(f"Pegvisomant Patients on Any Antidiabetic Drugs: {peg_on_antidiabetics}")
