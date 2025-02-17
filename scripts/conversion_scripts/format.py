import json
import os

# Input dataset file path
input_file = "/Users/jabinwade/Coding/CareConnect/processed_data/symptoms_diagnosis_data/Diseases_Symptoms_processed.jsonl"

# Output file path
output_file = "/Users/jabinwade/Coding/CareConnect/training_data/training_data/Diseases_Symptoms_training.jsonl"

# Function to convert the dataset
def convert_to_fine_tuning_format(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: Input file does not exist at {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
        for line in infile:
            try:
                # Load each line as a JSON object
                entry = json.loads(line.strip())
                
                # Ensure required fields exist
                if "instruction" in entry and "input" in entry and "output" in entry:
                    # Combine instruction and input into a single "prompt"
                    prompt = f"{entry['instruction']} Symptoms: {entry['input']}"
                    completion = entry["output"]
                    
                    # Create the JSON object for fine-tuning
                    jsonl_entry = {
                        "prompt": prompt,
                        "completion": completion
                    }
                    
                    # Write to the output file as JSONL
                    outfile.write(json.dumps(jsonl_entry) + "\n")
                else:
                    print(f"Skipping invalid entry: {entry}")
            except json.JSONDecodeError as e:
                print(f"Error decoding line: {line.strip()}. Error: {e}")

    print(f"Dataset successfully converted and saved to {output_path}")

# Run the conversion
convert_to_fine_tuning_format(input_file, output_file)
