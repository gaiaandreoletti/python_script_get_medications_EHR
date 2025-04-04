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

# Select patients
selected_patients = [11054922, 21180859, 21909666]  # Update with your list of patients

for patient_id in selected_patients:
    # Filter IGF-1 data for the patient
    patient_data = df_igf1[df_igf1["NFER_PID"].astype(str) == str(patient_id)].sort_values(by="LAB_RESULT_DTM")

    if patient_data.empty:
        continue

    # Filter Antidiabetic medication data for the patient
    patient_meds = df_med[df_med["NFER_PID"].astype(str) == str(patient_id)]

    # Create a figure with two subplots (IGF-1 levels + Medications)
    fig, ax = plt.subplots(2, 1, figsize=(12, 6), sharex=True, gridspec_kw={'height_ratios': [2, 1]})

    # --- Plot IGF-1 Levels ---
    ax[0].plot(
        patient_data["LAB_RESULT_DTM"],
        patient_data["RESULT_TXT"],
        marker="o", linestyle="-", color="gray", alpha=0.6, label="IGF-1 Trajectory"
    )

    # Highlight last IGF-1 measurement
    last_igf1 = patient_data.iloc[-1]  # Last row
    last_color = "blue" if last_igf1["IGF1_Status"] == "Normal" else "red"
    ax[0].scatter(
        last_igf1["LAB_RESULT_DTM"], last_igf1["RESULT_TXT"],
        color=last_color, edgecolor="black", s=100, label="Last IGF-1 Measurement"
    )

    # Formatting IGF-1 plot
    ax[0].set_ylabel("IGF-1 Levels")
    ax[0].set_title(f"IGF-1 Levels Over Time for Patient {patient_id}")
    ax[0].legend()
    ax[0].grid(True)

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
        if pd.notna(patient_data[f"{med}_Start"]).any():
            start_date = patient_data[f"{med}_Start"].dropna().iloc[0]
            end_date = patient_data[f"{med}_End"].dropna().iloc[0] if pd.notna(patient_data[f"{med}_End"]).any() else None
            med_events.append((start_date, end_date))
            med_labels.append(med)

    # Plot medication events using categorical placement
    for i, (start, end) in enumerate(med_events):
        ax[1].plot([start, end], [i, i], marker="|", linestyle="-", linewidth=2, label=med_labels[i] if i == 0 else "")

    # Formatting Medications Timeline
    ax[1].set_yticks(range(len(med_labels)))
    ax[1].set_yticklabels(med_labels, fontsize=10)  # Reduce font size for better readability
    ax[1].set_xlabel("Date")
    ax[1].set_title("Medications Timeline (Insulin, Other Antidiabetics & Acromegaly)")
    ax[1].grid(True)

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
