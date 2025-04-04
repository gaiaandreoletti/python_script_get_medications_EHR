import pandas as pd
import matplotlib.pyplot as plt

# Load the IGF-1 & Medications data
file_path = "filtered_igf1_data_with_category_404pt_T2D_antidiabetics_17Feb2025.tsv"
df_igf1 = pd.read_csv(file_path, sep="\t", low_memory=False)

# Convert timestamps to datetime
df_igf1["LAB_RESULT_DTM"] = pd.to_numeric(df_igf1["LAB_RESULT_DTM"], errors="coerce")
df_igf1["LAB_RESULT_DTM"] = pd.to_datetime(df_igf1["LAB_RESULT_DTM"], unit="s", errors="coerce")

# Convert Acromegaly medication start/end dates to datetime
acromegaly_meds = ["Pegvisomant", "Ocreotide", "Cabergoline", "Pasireotide", "Lanreotide"]
for med in acromegaly_meds:
    df_igf1[f"{med}_Start"] = pd.to_datetime(pd.to_numeric(df_igf1[f"{med}_Start"], errors="coerce"), unit="s", errors="coerce")
    df_igf1[f"{med}_End"] = pd.to_datetime(pd.to_numeric(df_igf1[f"{med}_End"], errors="coerce"), unit="s", errors="coerce")

# Load Antidiabetic medications data
med_file_path = "antidiabetic_summary.csv"
df_med = pd.read_csv(med_file_path, sep="\t", low_memory=False)

# Convert Antidiabetic medication start/end dates to datetime
df_med["STARTED_DTM"] = pd.to_datetime(pd.to_numeric(df_med["STARTED_DTM"], errors="coerce"), unit="s", errors="coerce")
df_med["ENDED_DTM"] = pd.to_datetime(pd.to_numeric(df_med["ENDED_DTM"], errors="coerce"), unit="s", errors="coerce")

# Classify Antidiabetic drugs into Insulin or Other
df_med["Medication_Group"] = df_med["NFER_DRUG"].apply(
    lambda x: "Insulin" if "insulin" in str(x).lower() else "Other Antidiabetic Drugs"
)

# Load HbA1c values with corrected column names
hba1c_file = "hba1c.tsv"
df_hba1c = pd.read_csv(hba1c_file, sep="\t", low_memory=False)

# Convert HbA1c test dates to datetime
df_hba1c["Test_Date"] = pd.to_datetime(pd.to_numeric(df_hba1c["Test_Date"], errors="coerce"), unit="s", errors="coerce")

# Select patients
selected_patients = [6209661, 6400793]  # Update with your list of patients

for patient_id in selected_patients:
    # Filter IGF-1 data for the patient
    patient_igf1 = df_igf1[df_igf1["NFER_PID"].astype(str) == str(patient_id)].sort_values(by="LAB_RESULT_DTM")
    
    # Filter HbA1c data for the patient
    patient_hba1c = df_hba1c[df_hba1c["NFER_PID"].astype(str) == str(patient_id)].sort_values(by="Test_Date")

    # Filter Antidiabetic medication data for the patient
    patient_meds = df_med[df_med["NFER_PID"].astype(str) == str(patient_id)]

    if patient_igf1.empty and patient_hba1c.empty:
        continue

    # Create a figure with three subplots (IGF-1 levels, HbA1c Levels, Medications)
    fig, ax = plt.subplots(3, 1, figsize=(12, 9), sharex=True, gridspec_kw={'height_ratios': [2, 2, 1]})

    # --- Plot IGF-1 Levels ---
    if not patient_igf1.empty:
        ax[0].plot(
            patient_igf1["LAB_RESULT_DTM"],
            patient_igf1["RESULT_TXT"],
            marker="o", linestyle="-", color="gray", alpha=0.6, label="IGF-1 Trajectory"
        )

        # Highlight last IGF-1 measurement
        last_igf1 = patient_igf1.iloc[-1]  # Last row
        last_color = "blue" if last_igf1["IGF1_Status"] == "Normal" else "red"
        ax[0].scatter(
            last_igf1["LAB_RESULT_DTM"], last_igf1["RESULT_TXT"],
            color=last_color, edgecolor="black", s=100, label="Last IGF-1 Measurement"
        )

    # Formatting IGF-1 plot
    ax[0].set_ylabel("IGF-1 Levels")
    ax[0].set_title(f"IGF-1 & HbA1c Levels Over Time for Patient {patient_id}")
    ax[0].legend()
    ax[0].grid(True)

    # --- Plot HbA1c Levels ---
    if not patient_hba1c.empty:
        ax[1].plot(
            patient_hba1c["Test_Date"],
            patient_hba1c["Hba1c_Value"],
            marker="o", linestyle="-", color="blue", alpha=0.6, label="HbA1c Levels"
        )

    # Formatting HbA1c plot
    ax[1].set_ylabel("HbA1c (%)")
    ax[1].legend()
    ax[1].grid(True)

    # --- Plot Medications Timeline ---
    med_events = []  # List to store medication event markers
    med_labels = []  # List for medication categories

    # Add Antidiabetic medication groups (Insulin / Other Antidiabetic Drugs)
    for group in ["Insulin", "Other Antidiabetic Drugs"]:
        med_subset = patient_meds[patient_meds["Medication_Group"] == group]
        if not med_subset.empty:
            start_date = med_subset["STARTED_DTM"].min()
            end_date = med_subset["ENDED_DTM"].max()
            med_events.append((start_date, end_date))
            med_labels.append(group)

    # Add Acromegaly medications
    for med in acromegaly_meds:
        if pd.notna(patient_igf1[f"{med}_Start"]).any():
            start_date = patient_igf1[f"{med}_Start"].dropna().iloc[0]
            end_date = patient_igf1[f"{med}_End"].dropna().iloc[0] if pd.notna(patient_igf1[f"{med}_End"]).any() else None
            med_events.append((start_date, end_date))
            med_labels.append(med)

    # Plot medication events using categorical placement
    for i, (start, end) in enumerate(med_events):
        ax[2].plot([start, end], [i, i], marker="|", linestyle="-", linewidth=2, label=med_labels[i] if i == 0 else "")

    # Formatting Medications Timeline
    ax[2].set_yticks(range(len(med_labels)))
    ax[2].set_yticklabels(med_labels, fontsize=10)  # Reduce font size for better readability
    ax[2].set_xlabel("Date")
    ax[2].set_title("Medications Timeline (Insulin, Other Antidiabetics & Acromegaly)")
    ax[2].grid(True)

    plt.xticks(rotation=45)
    plt.tight_layout()

    # **Save the plot as PNG**
    plt.savefig(f"patient_{patient_id}_plot.png", dpi=300, bbox_inches="tight")

    # Show plot
    plt.show()

print("Plots saved successfully!")
