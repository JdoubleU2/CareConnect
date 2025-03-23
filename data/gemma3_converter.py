import json
import argparse
from pathlib import Path
import snowflake.connector
import os


filepath = "/Users/jabinwade/Coding/CareConnect/data/processed_data/"
output_file = "/Users/jabinwade/Coding/CareConnect/data/gemma3_processed_data/processed_data.jsonl"

gemma_examples = []
for file in os.listdir(filepath):
    if file.endswith('.jsonl'):
        print(file)
        input_file = os.path.join(filepath, file)
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    example = json.loads(line.strip())
                    
                    # Extract the fields
                    instruction = example.get('instruction', '')
                    user_input = example.get('input', '')
                    response = example.get('output', '')
                    
                    # Combine instruction and input for the user message
                    if instruction and user_input:
                        user_message = f"{instruction}\n\n{user_input}"
                    elif instruction:
                        user_message = instruction
                    else:
                        user_message = user_input
                    
                    # Create the Gemma 3 conversation format
                    gemma_example = {
                        "messages": [
                            {"role": "user", "content": user_message},
                            {"role": "assistant", "content": response}
                        ]
                    }
                    
                    gemma_examples.append(gemma_example)
                    
                except json.JSONDecodeError:
                    print(f"Warning: Skipping invalid JSON line: {line.strip()}")

# Write the converted data
with open(output_file, 'w', encoding='utf-8') as f:
    for example in gemma_examples:
        f.write(json.dumps(example) + '\n')

print(f"Conversion complete. Processed {len(gemma_examples)} examples.")
print(f"Output saved to {output_file}")


connection_params = {
    "user": "JWADE",
    "password": "5hyxHhRBNFm44b9",
    "account": "IWB26166",
    "warehouse": "SOFTWARESURGEONS",
    "database": "SOFTWARESURGEONS_DB",
    "stage": "CARECONNECT_GEMMA3_TRAINING_DATA",
    "schema": "GIT",  # Ensure schema is set
}

# Establish a connection
conn = snowflake.connector.connect(**connection_params)
cursor = conn.cursor()

# Set Schema explicitly before using PUT
cursor.execute(f"USE DATABASE {connection_params['database']}")
cursor.execute(f"USE SCHEMA {connection_params['schema']}")  # 🔹 Fixes "No schema" error

# Define stage and file to upload
stage = connection_params["stage"]  


file_path = output_file
print(f"Uploading {file_path} to {stage}")
cursor.execute(f"PUT file://{file_path} @{stage} OVERWRITE=TRUE AUTO_COMPRESS=FALSE")

print(f"✅ Uploaded {file_path} to @{stage} successfully!")