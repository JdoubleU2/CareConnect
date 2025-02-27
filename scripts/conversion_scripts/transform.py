import json

# Define function to transform the current dataset to the required format
def transform_dataset(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Parse the JSON from each line
            data = json.loads(line.strip())
            
            # Create the new structure for each example
            conversation = {
                "system": data["instruction"],  # Use the instruction for the SYSTEM part
                "user": "Predict the disease based on these symptoms: " + data["input"],  # Add a prefix to the USER part
                "assistant": data["output"]  # Actual output from the dataset
            }
            
            # Write the transformed conversation into the output file
            json.dump(conversation, outfile)
            outfile.write("\n")

# Example chat template (not needed for this adjustment)
chat_template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{SYSTEM}<|eot_id|><|start_header_id|>user<|end_header_id|>
{INPUT}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
{OUTPUT}<|eot_id|>"""

# input and output file paths
input_file = '/home/jkwade/Code/CareConnect/processed_data/symptoms_diagnosis_data/disease_sympts_prec_full-2.jsonl'  # Replace with your input .jsonl file path
output_file = '/home/jkwade/Code/CareConnect/training_data/training_data/Diseases_Symptoms_training.jsonl'  # Output file path

# Call the function to transform the dataset
transform_dataset(input_file, output_file)