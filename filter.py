import pandas as pd
import re

# Read the CSV file into a DataFrame
file_path = "data.csv"  # Replace with the actual file path
df = pd.read_csv(file_path)

# Define the regex pattern to match 'RollNumber' starting with "C.13" followed by exactly four digits
pattern = r"^C.15\d{4}$"

# Use the `str.match` method with the regex pattern to filter rows
filtered_df = df[df["RollNumber"].str.match(pattern, na=False)]

# Specify the path for the new CSV file to save the filtered data
output_file_path = "filtered_data.csv"  # Replace with your desired output file path

# Save the filtered data to a new CSV file
filtered_df.to_csv(output_file_path, index=False)

# Display the filtered DataFrame
print(filtered_df)
