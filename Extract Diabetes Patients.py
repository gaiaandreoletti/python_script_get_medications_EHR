import pandas as pd

# Load HbA1c Data
hba1c_file = "hba1c.tsv"  # Update with correct file path
hba1c_df = pd.read_csv(hba1c_file, sep="\t")

# Ensure NFER_PID is a string
hba1c_df["NFER_PID"] = hba1c_df["NFER_PID"].astype(str)

# Convert HbA1c values to numeric
hba1c_df["hba1c_Value"] = pd.to_numeric(hba1c_df["hba1c_Value"], errors="coerce")

# Classify based on HbA1c Levels
hba1c_df["HbA1c_Category"] = pd.cut(
    hba1c_df["hba1c_Value"],
    bins=[0, 5.7, 6.4, float("inf")],
    labels=["Normal", "Prediabetes", "Diabetes"]
)

# Extract unique patients with Diabetes
diabetes_patients = hba1c_df[hba1c_df["HbA1c_Category"] == "Diabetes"]["NFER_PID"].unique()

# Save the list of patients with Diabetes
diabetes_patients_df = pd.DataFrame({"Diabetes_NFER_PID": diabetes_patients})
diabetes_patients_df.to_csv("diabetes_patients.tsv", sep="\t", index=False)

print(f"✅ Found {len(diabetes_patients)} patients with Diabetes HbA1c. Results saved in 'diabetes_patients.tsv'.")
