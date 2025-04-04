import pandas as pd

# Execute the query
query = """
SELECT 
    f.nfer_pid AS NFER_PID,
    f.nfer_dtm AS Test_Date,
    f.nfer_normalised_value AS Hba1c_Value,
    f.nfer_normalised_unit AS Unit,
    f.patient_age_at_event AS Age_At_Test
FROM FACT_LAB_TEST f
WHERE f.nfer_pid IN ({acromegaly_ids_str})
AND (
    LOWER(CAST(f.lab_subtype_code AS STRING)) LIKE '%a1c%' 
    OR LOWER(CAST(f.lab_subtype_code AS STRING)) LIKE '%hba1c%'
)
AND (
    LOWER(f.nfer_variable_name) LIKE '%a1c%'
    OR LOWER(f.nfer_variable_name) LIKE '%hba1c%'
)
ORDER BY f.nfer_pid, f.nfer_dtm;
"""

# Run the SQL query
result = sql_client.query(query)

# Convert to Pandas DataFrame if needed
if hasattr(result, "as_dataframe"):
    result_df = result.as_dataframe()
else:
    result_df = pd.DataFrame(result)

# Save to TSV if data exists
if not result_df.empty:
    output_file = "all_hba1c_tests_acromegaly_patients.tsv"
    result_df.to_csv(output_file, sep="\t", index=False)
    print(f"All HbA1c test results saved to {output_file}")
else:
    print("Query returned no data.")
