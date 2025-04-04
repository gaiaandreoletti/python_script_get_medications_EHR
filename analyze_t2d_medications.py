import pandas as pd
import matplotlib.pyplot as plt

# ---- Load the dataset with T2D information ----
file_path = "filtered_igf1_data_with_category_404pt_T2D_antidiabetics_17Feb2025.tsv"  # Update if needed
df = pd.read_csv(file_path, sep="\t", low_memory=False)

# ---- Ensure NFER_PID is a string ----
df["NFER_PID"] = df["NFER_PID"].astype(str)

# ---- Count unique patients by drug combination for T2D and non-T2D groups ----
t2d_drug_counts = df[df["T2D_Flag"] == "Yes"].groupby("Drug_Combination")["NFER_PID"].nunique().reset_index()
non_t2d_drug_counts = df[df["T2D_Flag"] == "No"].groupby("Drug_Combination")["NFER_PID"].nunique().reset_index()

# ---- Rename columns for clarity ----
t2d_drug_counts.columns = ["Drug_Combination", "T2D_Patient_Count"]
non_t2d_drug_counts.columns = ["Drug_Combination", "Non_T2D_Patient_Count"]

# ---- Merge both counts for comparison ----
drug_comparison = t2d_drug_counts.merge(non_t2d_drug_counts, on="Drug_Combination", how="outer").fillna(0)

# ---- Calculate total patients per group ----
total_t2d = drug_comparison["T2D_Patient_Count"].sum()
total_non_t2d = drug_comparison["Non_T2D_Patient_Count"].sum()

# ---- Calculate percentage of each drug combination in T2D and non-T2D groups ----
drug_comparison["T2D_Percentage"] = (drug_comparison["T2D_Patient_Count"] / total_t2d) * 100
drug_comparison["Non_T2D_Percentage"] = (drug_comparison["Non_T2D_Patient_Count"] / total_non_t2d) * 100

# ---- Count unique T2D patients on Insulin ----
t2d_on_insulin = df[(df["T2D_Flag"] == "Yes") & (df["Insulin_Flag"] == "Yes")].groupby("Drug_Combination")["NFER_PID"].nunique().reset_index()
t2d_on_insulin.columns = ["Drug_Combination", "T2D_Insulin_Patient_Count"]

# ---- Count unique T2D patients on Antidiabetic medications ----
t2d_on_antidiabetics = df[(df["T2D_Flag"] == "Yes") & (df["Antidiabetics_Flag"] == "Yes")].groupby("Drug_Combination")["NFER_PID"].nunique().reset_index()
t2d_on_antidiabetics.columns = ["Drug_Combination", "T2D_Antidiabetic_Patient_Count"]

# ---- Plot Pie Chart for T2D Patients ----
plt.figure(figsize=(8, 8))
plt.pie(
    drug_comparison["T2D_Patient_Count"],
    labels=drug_comparison["Drug_Combination"],
    autopct="%1.1f%%",
    startangle=140
)
plt.title("Medication Distribution Among T2D Patients")
plt.show()

# ---- Plot Pie Chart for Non-T2D Patients ----
plt.figure(figsize=(8, 8))
plt.pie(
    drug_comparison["Non_T2D_Patient_Count"],
    labels=drug_comparison["Drug_Combination"],
    autopct="%1.1f%%",
    startangle=140
)
plt.title("Medication Distribution Among Non-T2D Patients")
plt.show()

# ---- Plot Pie Chart for T2D Patients on Insulin ----
plt.figure(figsize=(8, 8))
plt.pie(
    t2d_on_insulin["T2D_Insulin_Patient_Count"],
    labels=t2d_on_insulin["Drug_Combination"],
    autopct="%1.1f%%",
    startangle=140
)
plt.title("Medication Distribution Among T2D Patients on Insulin")
plt.show()

# ---- Plot Pie Chart for T2D Patients on Antidiabetic Medications ----
plt.figure(figsize=(8, 8))
plt.pie(
    t2d_on_antidiabetics["T2D_Antidiabetic_Patient_Count"],
    labels=t2d_on_antidiabetics["Drug_Combination"],
    autopct="%1.1f%%",
    startangle=140
)
plt.title("Medication Distribution Among T2D Patients on Antidiabetic Medications")
plt.show()
