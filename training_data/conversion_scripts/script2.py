import json

# Define function to transform the current dataset to the required format
def transform_dataset(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Parse the JSON from each line
            data = json.loads(line.strip())
            
            # Create the new structure for each example
            conversation = [
                {"role": "system", "message": data['instruction']},
                {"role": "user", "message": f"Predict the disease based on these symptoms: {data['input']}"},
                {"role": "assistant", "message": data['output']}
            ]
            
            # Write the transformed conversation into the output file
            json.dump({"conversations": conversation}, outfile)
            outfile.write("\n")

#  input and  file paths
input_file = '/home/jkwade/Code/CareConnect/processed_data/symptoms_diagnosis_data/disease_sympts_prec_full-2.jsonl'  # Replace with your input .jsonl file path
output_file = 'training_data/training_data/Diseases_Symptoms_training.jsonl'  # Output file path

# Call the function to transform the dataset
transform_dataset(input_file, output_file)
