import pandas as pd

# ---- Load the Antidiabetic Medication Data ----
file_path = "antidiabetic_summary.csv"  # Update with the correct path if needed

# Load the dataset
df_antidiabetic = pd.read_csv(file_path, sep=",", low_memory=False)

# Ensure NFER_PID is in string format
df_antidiabetic["NFER_PID"] = df_antidiabetic["NFER_PID"].astype(str)

# Count unique NFER_PID per drug
antidiabetic_counts = df_antidiabetic.groupby("NFER_DRUG")["NFER_PID"].nunique().reset_index()

# Rename columns
antidiabetic_counts.columns = ["Drug", "Unique_Patient_Count"]

# Save results
output_file = "unique_patients_per_antidiabetic_drug.tsv"
antidiabetic_counts.to_csv(output_file, sep="\t", index=False)

# Display results
print("\n--- Unique Patient Counts Per Antidiabetic Drug ---")
print(antidiabetic_counts)

print(f"\n✅ Processed data saved as '{output_file}'.")
