import pandas as pd

# Specify the path to the filtered CSV file
filtered_file_path = "filtered_data.csv"  # Replace with the actual path

# Read the filtered CSV file into a DataFrame
filtered_df = pd.read_csv(filtered_file_path)

# Extract the 'Email' column from the DataFrame
emails = filtered_df["Email"].str.lower() + "+"
emails = emails.str.replace("@fpt.edu.vn", "")

# Specify the path for the output file to save the email addresses
output_email_file_path = (
    "extracted_emails.txt"  # Replace with your desired output file path
)

# Save the extracted email addresses to a text file
emails.to_csv(output_email_file_path, index=False, header=False)

# Display a message indicating the file has been saved
print(f"Email addresses have been saved to {output_email_file_path}")
