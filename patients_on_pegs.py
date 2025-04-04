import pandas as pd

# Load the IGF-1 & Medications data
file_path = "filtered_igf1_data_with_category_404pt_T2D_antidiabetics_17Feb2025.tsv"
df_igf1 = pd.read_csv(file_path, sep="\t", low_memory=False)

# Load HbA1c data
hba1c_file = "hba1c.tsv"
df_hba1c = pd.read_csv(hba1c_file, sep="\t", low_memory=False)

# Convert HbA1c test dates to datetime
df_hba1c["Test_Date"] = pd.to_datetime(pd.to_numeric(df_hba1c["Test_Date"], errors="coerce"), unit="s", errors="coerce")

# Extract patients taking Pegvisomant (Category contains 'Pegvisomant')
pegvisomant_patients = df_igf1[df_igf1["Category"].str.contains("Pegvisomant", na=False)]["NFER_PID"].unique()

# Filter HbA1c data for these patients
hba1c_peg_patients = df_hba1c[df_hba1c["NFER_PID"].isin(pegvisomant_patients)]

# Identify patients with high HbA1c (≥6.5%)
high_hba1c_patients = hba1c_peg_patients[hba1c_peg_patients["Hba1c_Value"] >= 6.5]["NFER_PID"].unique()

# Calculate numbers
total_peg_patients = len(pegvisomant_patients)
high_hba1c_count = len(high_hba1c_patients)
high_hba1c_percentage = round((high_hba1c_count / total_peg_patients) * 100, 2) if total_peg_patients > 0 else 0

# Load Antidiabetic medications data
med_file_path = "antidiabetic_summary.csv"
df_med = pd.read_csv(med_file_path, sep="\t", low_memory=False)

# Identify patients on Insulin
df_med["Medication_Group"] = df_med["NFER_DRUG"].apply(lambda x: "Insulin" if "insulin" in str(x).lower() else "Other Antidiabetic Drugs")
insulin_patients = df_med[df_med["Medication_Group"] == "Insulin"]["NFER_PID"].unique()

# Count how many high HbA1c patients are also on Insulin
high_hba1c_insulin_count = len(set(high_hba1c_patients) & set(insulin_patients))

# Display results
results = {
    "Total Pegvisomant Patients": total_peg_patients,
    "Patients with High HbA1c": high_hba1c_count,
    "Percentage with High HbA1c (%)": high_hba1c_percentage,
    "High HbA1c Patients on Insulin": high_hba1c_insulin_count
}

# Convert to DataFrame for better display
df_results = pd.DataFrame([results])

# Show the table
import ace_tools as tools
tools.display_dataframe_to_user(name="Pegvisomant_High_HbA1c_Stats", dataframe=df_results)

print("Analysis complete! Displaying the table.")
