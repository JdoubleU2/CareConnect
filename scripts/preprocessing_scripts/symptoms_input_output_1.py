#####################################################################
#       Created by: Jabin Wade 2/5/2025
#   
#       Notes:
#
#       This script is to prprocess the disease_sympts_prec_full-2.csv file
#       in theory we can proably use it on multiple files so this is going to be
#       a common script everyone can use.
#
#
#       You need pandas so install that ask me how if you cant install it or 
#       just google it.
#
#       
#       youre going to need to change the file paths to run this script
#       
############################################################################
#!/usr/bin/env python
import pandas as pd
import json
import argparse

def preprocess_csv(csv_file, output_file):

    # Load the CSV file and remove duplicate rows based on the 'symptoms' and 'disease' columns
    # discuss with team if we need to remove duplicates or not. may or may not be a good idea
    df = pd.read_csv(csv_file)
    initial_count = len(df)
    df = df.drop_duplicates(subset=["disease", "symptoms"])
    deduped_count = len(df)
    print(f"Removed {initial_count - deduped_count} duplicate rows.")
    
    # List to hold each processed record
    processed_data = []
    
    # Define the instruction prompt
    instruction_text = "Predict the disease based on these symptoms."
    
    # Iterate over each row of the CSV file
    for index, row in df.iterrows():
        # Use the "symptoms" column as input and "disease" as output
        symptoms = row["symptoms"]
        disease = row["disease"]
        
        # Create a dictionary for each record
        entry = {
            "instruction": instruction_text,
            "input": symptoms,
            "output": disease
        }
        processed_data.append(entry)
    
    # Write out the processed data in JSON Lines format
    with open(output_file, "w", encoding="utf-8") as f:
        for item in processed_data:
            json_line = json.dumps(item, ensure_ascii=False)
            f.write(json_line + "\n")
    
    print(f"Preprocessed dataset saved to {output_file}")

def main():
    # Use raw strings (prefix with r) to prevent escape sequence issues
    csv_file = r"D:\Jabin\coding\Repos\CareConnect\raw_data\symptoms_diagnosis_data\disease_sympts_prec_full-2.csv"
    output_file = r"D:\Jabin\coding\Repos\CareConnect\processed_data\symptoms_diagnosis_data\disease_sympts_prec_full-2.jsonl"

    preprocess_csv(csv_file, output_file)

if __name__ == "__main__":
    main()