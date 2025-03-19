import re
import csv

def fix_line(line):
    """
    This function finds text enclosed in double quotes and removes any commas within that quoted text.
    """
    # This lambda will remove commas from the matched quoted text
    def remove_commas(match):
        text = match.group(0)
        # Remove commas inside the quotes, but keep the quotes themselves
        return '"' + text[1:-1].replace(',', '') + '"'
    
    # Replace all occurrences of quoted text using our lambda
    fixed_line = re.sub(r'"[^"]*"', remove_commas, line)
    return fixed_line

# Path to your original CSV file
input_filename = "Data_Mining_Warehouse/sales_data_sample.csv"
# Path for the cleaned CSV file
output_filename = "sales_data_cleaned.csv"

# Open the input and output files
with open(input_filename, 'r', encoding='utf-8') as infile, \
     open(output_filename, 'w', encoding='utf-8', newline='') as outfile:
    
    # Read the header to determine the expected number of fields
    header_line = infile.readline()
    outfile.write(header_line)  # write header as is
    header_fields = list(csv.reader([header_line]))[0]
    expected_fields = len(header_fields)
    
    # Process each subsequent line
    for line in infile:
        # First, try the line as-is
        fields = list(csv.reader([line]))[0]
        if len(fields) == expected_fields:
            outfile.write(line)
        else:
            # Fix the line by removing commas within quoted text
            fixed_line = fix_line(line)
            fixed_fields = list(csv.reader([fixed_line]))[0]
            # If the fixed line now has the correct number of fields, write it out
            if len(fixed_fields) == expected_fields:
                outfile.write(fixed_line)
            else:
                # Optionally, log or print problematic lines for further manual review
                print("Could not fix line correctly, skipping:", line.strip())

print(f"Finished cleaning. Cleaned file saved as {output_filename}.")
