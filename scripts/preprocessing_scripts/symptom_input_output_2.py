#####################################################################
#       Created by: Jabin Wade 2/5/2025
#   
#       Notes:
#
#       This script is to prprocess the Diseases_symptoms.csv file
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
    # Load the CSV file
    df = pd.read_csv(csv_file)
    
    # Optional: Remove duplicate rows based on 'Symptoms', 'Name', and 'Treatments'
    initial_count = len(df)
    df = df.drop_duplicates(subset=["Symptoms", "Name", "Treatments"])
    deduped_count = len(df)
    print(f"Removed {initial_count - deduped_count} duplicate rows.")
    
    processed_data = []
    
    # Define the instruction prompt for the model
    instruction_text = ("Based on the following symptoms, predict the disease and recommend appropriate treatments.")
    
    # Iterate over each row of the CSV file
    for index, row in df.iterrows():
        # Extract the fields; we ignore the "Code" field for training purposes
        disease_name = row["Name"]
        symptoms = row["Symptoms"]
        treatments = row["Treatments"]
        
        # Combine disease and treatments into one output string
        output_text = f"Disease: {disease_name}; Treatments: {treatments}"
        
        # Create an entry dictionary
        entry = {
            "instruction": instruction_text,
            "input": symptoms,
            "output": output_text
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
    csv_file = "CareConnect/raw_data/symptoms_diagnosis_data/Diseases_Symptoms.csv"
    output_file = "CareConnect/processed_data/symptoms_diagnosis_data/Diseases_Symptoms_processed.jsonl"

    preprocess_csv(csv_file, output_file)

if __name__ == "__main__":
    main()