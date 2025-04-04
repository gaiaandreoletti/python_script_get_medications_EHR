import pandas as pd

# Load the dataset
file_path = "filtered_igf1_data_with_category_404pt_T2D_antidiabetics_17Feb2025.tsv"  # Update with correct path if needed
df = pd.read_csv(file_path, sep="\t", low_memory=False)

# Filter rows where 'Category' contains 'Pegvisomant'
filtered_df = df[df["Category"].str.contains("Pegvisomant", na=False, case=False)]

# Extract unique NFER_PID values
unique_nfer_pid = filtered_df["NFER_PID"].unique()

# Save to a new file
output_file = "pegvisomant_patients.tsv"
pd.DataFrame(unique_nfer_pid, columns=["NFER_PID"]).to_csv(output_file, sep="\t", index=False)

# Print summary
print(f"Total unique NFER_PID for Pegvisomant: {len(unique_nfer_pid)}")
print(f"Filtered NFER_PID saved to: {output_file}")
