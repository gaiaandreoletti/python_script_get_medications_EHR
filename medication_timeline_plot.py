# --- Plot Medications Timeline ---
med_events = []  # List to store medication event markers
med_labels = []  # List for medication categories

# Add Antidiabetic medication groups (Insulin / Other Antidiabetic Drugs)
for group in ["Insulin", "Other Antidiabetic Drugs"]:
    med_subset = patient_meds[patient_meds["Medication_Group"] == group]
    if not med_subset.empty:
        start_date = med_subset["STARTED_DTM"].min()
        end_date = med_subset["ENDED_DTM"].max()

        # Ensure dates are valid before appending
        if pd.notna(start_date) and pd.notna(end_date):
            med_events.append((start_date, end_date))
            med_labels.append(group)

# Add Acromegaly medications
for med in acromegaly_meds:
    if pd.notna(patient_igf1[f"{med}_Start"]).any():
        start_date = patient_igf1[f"{med}_Start"].dropna().iloc[0]
        end_date = patient_igf1[f"{med}_End"].dropna().iloc[0] if pd.notna(patient_igf1[f"{med}_End"]).any() else None

        # Ensure dates are valid before appending
        if pd.notna(start_date):
            med_events.append((start_date, end_date))
            med_labels.append(med)

# Plot medication events using categorical placement
for i, (start, end) in enumerate(med_events):
    if pd.notna(start) and pd.notna(end):  # Ensure both start and end are valid
        ax[2].plot([start, end], [i, i], marker="|", linestyle="-", linewidth=2, label=med_labels[i] if i == 0 else "")

# Formatting Medications Timeline
ax[2].set_yticks(range(len(med_labels)))
ax[2].set_yticklabels(med_labels, fontsize=10)
ax[2].set_xlabel("Date")
ax[2].set_title("Medications Timeline (Insulin, Other Antidiabetics & Acromegaly)")
ax[2].grid(True)
