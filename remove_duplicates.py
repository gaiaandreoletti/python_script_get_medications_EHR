import pandas as pd

# Define the file path (update if necessary)
file_path = "combined_hba1c_values_acromegaly_patients.tsv"

# Load the TSV file into a Pandas DataFrame
df = pd.read_csv(file_path, sep="\t")

# Count occurrences of each NFER_PID
nfer_pid_counts = df["NFER_PID"].value_counts()

# Count how many have duplicates (more than 1 occurrence)
num_duplicates = (nfer_pid_counts > 1).sum()

# Count unique NFER_PID
num_unique = nfer_pid_counts.shape[0]

# Print results
print(f"Number of unique NFER_PID: {num_unique}")
print(f"Number of NFER_PID with more than one test: {num_duplicates}")
