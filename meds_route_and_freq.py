import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset (Ensure "medication_dataroute.tsv" is in the same directory)
med_data = pd.read_csv("medication_dataroute.tsv", sep="\t")

# Keep relevant columns
med_data_filtered = med_data[["NFER_PID", "NFER_DRUG", "ADMINISTERED_ROUTE", "ADMINISTERED_FREQUENCY"]].dropna()

# Define frequency mapping
frequency_mapping = {
    "daily": ["daily", "every morning", "every evening", "every day", "once", "stat"],
    "multiple-daily": ["3 times a day", "2 times daily", "4 times a day", "twice per day"],
    "weekly": ["weekly", "once a week", "2 times a week", "twice per week"],
    "monthly": ["monthly", "every 28 days", "every 3 months", "every 30 days"],
    "as directed": ["as directed", "per provider instruction", "as needed"],
}

# Define route mapping (handling different spellings and formats)
route_mapping = {
    "subcutaneous": ["subcutaneous", "sc", "subq", "sub-cutaneous"],
    "oral": ["oral", "po", "by mouth"],
    "intravenous": ["intravenous", "iv"],
    "intramuscular": ["intramuscular", "im"],
    "transdermal": ["transdermal", "patch"],
}

# Function to categorize administered frequencies
def categorize_frequency(frequency):
    """Categorizes frequencies into predefined groups."""
    if pd.isna(frequency):
        return "unknown"
    frequency = str(frequency).strip().lower()
    for category, values in frequency_mapping.items():
        if any(frequency in v.lower() for v in values):
            return category
    return "unknown"

# Function to categorize administered routes
def categorize_route(route):
    """Maps different spellings of the same route into a standardized category."""
    if pd.isna(route):
        return "unknown"
    route = str(route).strip().lower()
    for category, values in route_mapping.items():
        if any(route in v.lower() for v in values):
            return category
    return "unknown"

# Apply frequency and route categorization
med_data_filtered["Frequency_Category"] = med_data_filtered["ADMINISTERED_FREQUENCY"].apply(categorize_frequency)
med_data_filtered["Route_Category"] = med_data_filtered["ADMINISTERED_ROUTE"].apply(categorize_route)

# Group by drug, route, and frequency, counting unique patients
med_freq_by_route = med_data_filtered.groupby(["NFER_DRUG", "Route_Category", "Frequency_Category"])["NFER_PID"].nunique().reset_index()

# Rename columns for clarity
med_freq_by_route.columns = ["Medication", "Route", "Frequency", "Unique_Patient_Count"]

# Save processed data for further use
med_freq_by_route.to_csv("medication_route_frequency.tsv", sep="\t", index=False)

# Function to plot unique patient count by route for a given medication
def plot_medication_frequency_by_route(med_name):
    """Plots unique patient count by route for a given medication."""
    subset = med_freq_by_route[med_freq_by_route["Medication"] == med_name]
    
    if subset.empty:
        print(f"No data found for {med_name}")
        return

    plt.figure(figsize=(12, 6))
    sns.barplot(data=subset, x="Frequency", y="Unique_Patient_Count", hue="Route", dodge=True)

    plt.title(f"Unique Patient Count by Route for {med_name}", fontsize=14)
    plt.xlabel("Frequency Category", fontsize=12)
    plt.ylabel("Unique Patient Count", fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title="Route", fontsize=10)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

# Example usage: Plot frequency distribution for Pegvisomant
plot_medication_frequency_by_route("pegvisomant")

print("✅ Process completed! Data saved as 'medication_route_frequency.tsv'.")
