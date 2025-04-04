 import pandas as pd

# Load dataset
df_filtered = pd.read_csv('filtered_igf1_data_with_category_404pt_31Jan2025.tsv', sep="\t", low_memory=False)

# Strip spaces from column names to avoid mismatches
df_filtered.columns = df_filtered.columns.str.strip()

# Convert Unix timestamps to numeric
time_columns = ["LAB_RESULT_DTM", "Pegvisomant_End", "Octreotide_End", "Pasireotide_End", "Cabergoline_End", "Lanreotide_End"]
df_filtered[time_columns] = df_filtered[time_columns].apply(pd.to_numeric, errors="coerce")

# Function to categorize Current_Medications
def categorize_medication(row):
    pegvisomant = pd.notna(row["Pegvisomant_End"]) and row["Pegvisomant_End"] > row["LAB_RESULT_DTM"]
    srl = any(pd.notna(row[col]) and row[col] > row["LAB_RESULT_DTM"] for col in ["Octreotide_End", "Lanreotide_End", "Pasireotide_End"])
    cabergoline = pd.notna(row["Cabergoline_End"]) and row["Cabergoline_End"] > row["LAB_RESULT_DTM"]

    if pegvisomant and srl and cabergoline:
        return "Pegvisomant + SRL + Cabergoline"
    elif pegvisomant and srl:
        return "Pegvisomant + SRL"
    elif pegvisomant:
        return "Pegvisomant only"
    elif srl and cabergoline:
        return "SRL + Cabergoline"
    elif srl:
        return "SRL alone"
    else:
        return "No Medication"

# Apply function to create simplified medication column
df_filtered["Current_Medications"] = df_filtered.apply(categorize_medication, axis=1)

# Create a patient-level summary table
patient_summary = df_filtered.groupby("NFER_PID").agg({
    "Surgery_Flag": lambda x: "Yes" if (x == "Yes").any() else "No",
    "IGF1_Status_Pre_Surgery": "first",
    "IGF1_Status_Post_Surgery": "first",
    "Radiosurgery_Flag": lambda x: "Yes" if (x == "Yes").any() else "No",
    "IGF1_Status_Pre_Radiosurgery": "first",
    "IGF1_Status_Post_Radiosurgery": "last",
    "Category": lambda x: x.dropna().iloc[0] if not x.dropna().empty else "None",
    "IGF1_Status_Post_Medications": "first",
    "Current_Medications": "first"  # Include simplified categories
}).reset_index()

# Replace NaNs with 'Unknown' for visualization purposes
patient_summary.fillna("Unknown", inplace=True)

# Save to file
patient_summary.to_csv("patient_summary_updated.tsv", sep="\t", index=False)

print("✅ Updated patient summary with simplified Current_Medications saved as 'patient_summary_updated.tsv'")
