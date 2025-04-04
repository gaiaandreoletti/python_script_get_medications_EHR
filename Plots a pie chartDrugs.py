import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the TSV file containing overlapping medication data
df = pd.read_csv("drug_combination_counts.tsv", sep="\t")

# Check the data
print(df.head())

# Pie Chart: Distribution of Patients by Drug Combination
plt.figure(figsize=(10, 6))
plt.pie(df["Unique_Patient_Count"], labels=df["Drug_Combination"], autopct="%1.1f%%", 
        colors=sns.color_palette("pastel", len(df)), startangle=140)
plt.title("Patient Distribution by Drug Combination", fontsize=14)
plt.axis("equal")  # Ensures pie chart is a circle
plt.show()

# Histogram: Number of Unique Patients per Drug Combination
plt.figure(figsize=(12, 6))
sns.histplot(df["Unique_Patient_Count"], bins=10, kde=True, color="blue")
plt.xlabel("Unique Patient Count", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.title("Histogram of Unique Patients per Drug Combination", fontsize=14)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()
