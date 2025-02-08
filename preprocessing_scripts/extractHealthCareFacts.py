import re
import csv

def extract(input_file_path, output_file_path):
    # capture everything between [INST] and [/INST]
    inst_pattern = re.compile(r'<s>\[INST\](.*?)\[/INST\]')

    # capture everything after [/INST] until the end
    remainder_pattern = re.compile(r'\[/INST\]\s*(.*)')

    with open(input_file_path, 'r', newline='', encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        
        with open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
            writer = csv.writer(output_file)
            
            writer.writerow(['INST', 'Remainder'])

            for row in reader:
                text = row[0]
                
                # Extract the string between [INST] and [/INST]
                inst_match = inst_pattern.search(text)
                inst_string = inst_match.group(1) if inst_match else ''
                
                # Capture everything after [/INST] until the end (including spaces after [/INST])
                remainder_match = remainder_pattern.search(text)
                remainder_string = remainder_match.group(1).strip() if remainder_match else ''
                
                # Write the extracted strings to the output CSV
                writer.writerow([inst_string, remainder_string])

# Provide the input and output file paths
input_file_path = '/Users/zeronelson/SoftwareDev/CareConnect/raw_data/conversation_data/HealthCareFacts.csv'
output_file_path = '/Users/zeronelson/SoftwareDev/CareConnect/raw_data/conversation_data/2_HealthCareFacts.csv'
extract(input_file_path, output_file_path)
