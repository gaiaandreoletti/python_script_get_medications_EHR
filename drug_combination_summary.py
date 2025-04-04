import pandas as pd

# Load the TSV file (Ensure it's in the same directory as this script)
file_path = "medication_data_with_final_overlap.tsv"  # Update path if needed
df = pd.read_csv(file_path, sep="\t")

# Check if required columns exist
required_columns = ["NFER_PID", "NFER_DRUG", "final_overlap"]
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    print(f"Error: Missing columns {missing_columns} in the dataset.")
else:
    # Group by NFER_PID and final_overlap to determine drug combinations taken at the same time
    df["NFER_DRUG"] = df["NFER_DRUG"].astype(str)  # Ensure drug names are strings
    drug_combinations = df.groupby(["NFER_PID", "final_overlap"])["NFER_DRUG"].apply(
        lambda x: "-".join(sorted(set(x)))  # Sort to maintain consistency
    ).reset_index()

    # Count unique patients for each drug combination
    patient_counts = drug_combinations.groupby("NFER_DRUG")["NFER_PID"].nunique().reset_index()
    patient_counts.columns = ["Drug_Combination", "Unique_Patient_Count"]

    # Add percentage column
    total_patients = patient_counts["Unique_Patient_Count"].sum()
    patient_counts["Percentage"] = (patient_counts["Unique_Patient_Count"] / total_patients) * 100
    patient_counts["Percentage"] = patient_counts["Percentage"].round(2)  # Round to 2 decimal places

    # Save the results
    output_file = "drug_combination_patient_counts.tsv"
    patient_counts.to_csv(output_file, sep="\t", index=False)
    print(f"✅ Processed data saved as '{output_file}'.")

    # Display the table
    print(patient_counts)
