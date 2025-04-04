import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "medication_data_with_final_overlap.tsv"  # Update path if necessary
df = pd.read_csv(file_path, sep="\t")

# Ensure drug names are normalized (lowercase, no extra spaces)
df["NFER_DRUG"] = df["NFER_DRUG"].str.strip().str.lower()

# Define SRL as any drug other than Pegvisomant or Cabergoline
df["Is_SRL"] = df["NFER_DRUG"].apply(lambda x: "srl" if x not in ["pegvisomant", "cabergoline"] else x)

# Group by NFER_PID and final_overlap to determine drug combinations taken at the same time
drug_combinations = df.groupby(["NFER_PID", "final_overlap"])["Is_SRL"].apply(
    lambda x: "-".join(sorted(set(x)))  # Sort to maintain consistency
).reset_index(name="Drug_Combination")

# Define medication categories for specific combinations
def assign_category(combination):
    drugs = set(combination.split("-"))

    if drugs == {"pegvisomant"}:
        return "Pegvisomant only"
    elif drugs == {"pegvisomant", "srl"}:
        return "Pegvisomant + SRL"
    elif drugs == {"pegvisomant", "srl", "cabergoline"}:
        return "Pegvisomant + SRL + Cabergoline"
    elif drugs == {"srl"}:
        return "SRL only"
    elif drugs == {"srl", "cabergoline"}:
        return "SRL + Cabergoline"
    elif drugs == {"cabergoline"}:
        return "Cabergoline only"
    else:
        return "Other"

# Apply category assignment
drug_combinations["Medication_Category"] = drug_combinations["Drug_Combination"].apply(assign_category)

# Extract "Other" category entries for review
other_category_entries = drug_combinations[drug_combinations["Medication_Category"] == "Other"]

# Save the extracted "Other" category entries for review
other_output_file = "other_category_entries.tsv"
other_category_entries.to_csv(other_output_file, sep="\t", index=False)
print(f"Extracted 'Other' category entries saved to '{other_output_file}'.")

# Count unique patients in each category
category_counts = drug_combinations.groupby("Medication_Category")["NFER_PID"].nunique().reset_index()
category_counts.columns = ["Medication_Category", "Unique_Patient_Count"]

# Remove "Other" category from the plotting data
category_counts_filtered = category_counts[category_counts["Medication_Category"] != "Other"]

# Plot filtered data without "Other" category

# Bar Plot
plt.figure(figsize=(12, 6))
sns.barplot(data=category_counts_filtered, x="Medication_Category", y="Unique_Patient_Count", palette="pastel")
plt.title("Unique Patient Count by Medication Category (Excluding Other)", fontsize=14)
plt.xlabel("Category", fontsize=12)
plt.ylabel("Unique Patient Count", fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# Pie Chart
plt.figure(figsize=(10, 6))
plt.pie(category_counts_filtered["Unique_Patient_Count"], labels=category_counts_filtered["Medication_Category"],
        autopct="%1.1f%%", colors=sns.color_palette("pastel", len(category_counts_filtered)), startangle=140)
plt.title("Patient Distribution by Medication Category (Excluding Other)", fontsize=14)
plt.axis("equal")  # Ensures pie chart is a circle
plt.show()

# Histogram
plt.figure(figsize=(12, 6))
sns.histplot(category_counts_filtered["Unique_Patient_Count"], bins=10, kde=True, color="blue")
plt.xlabel("Unique Patient Count", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.title("Histogram of Unique Patients per Medication Category (Excluding Other)", fontsize=14)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()
