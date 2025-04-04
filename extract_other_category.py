import pandas as pd

# Load the dataset
file_path = "medication_category_counts.tsv"  # Update path if necessary
df = pd.read_csv(file_path, sep="\t")

# Check if the expected column exists
if "Medication_Category" not in df.columns:
    print("Error: 'Medication_Category' column not found in the dataset.")
else:
    # Extract rows where category is "Other"
    other_category_df = df[df["Medication_Category"] == "Other"]

    # Save the extracted rows for review
    output_file = "other_category_entries.tsv"
    other_category_df.to_csv(output_file, sep="\t", index=False)
    
    print(f"Extracted 'Other' category entries saved to '{output_file}'.")
    
    # Display first few rows
    print(other_category_df.head())
