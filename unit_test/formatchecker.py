import json
import os

class ValidationError(Exception):
    """Exception for validation errors."""
    pass

def validate_jsonl():
    directory_path = "/home/jkwade/Code/CareConnect/data/processed_data/jsonl"

    # List files in the directory
    try:
        files = os.listdir(directory_path)
    except FileNotFoundError:
        print(f"Directory not found: {directory_path}")
        return

    for file in files:
        if not file.endswith(".jsonl"):
            print(f"Invalid file {file}. Please discard all non-JSONL files.")
            continue  # Skip non-JSONL files

        file_path = os.path.join(directory_path, file)
        with open(file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                try:
                    data = json.loads(line.strip())

                    # Validate keys
                    required_keys = {"instruction", "input", "output"}
                    if not required_keys.issubset(data.keys()):
                        raise ValidationError(f"File {file_path} Line {line_num}: Missing required keys.")
                        

                    # Validate instruction format
                    if not isinstance(data["instruction"], str) or not data["instruction"]:
                        raise ValidationError(f"File {file_path} Line {line_num}: Incorrect instruction text. Instruction should be a non-empty string.")
                        

                    # Validate input format (comma-separated symptoms)
                    if not isinstance(data["input"], str) or not data["input"]:
                        raise ValidationError("File {file_path} Line {line_num}: Incorrect input text. Input should be a non-empty string.")
                        

                    # Validate output format (disease name)
                    if not isinstance(data["output"], str) or not data["output"].strip():
                        raise ValidationError(f"File {file_path} Line {line_num}: Incorrect output text. Output should be a non-empty string.")
                        

                except json.JSONDecodeError:
                    raise ValidationError(f"File {file_path} Line {line_num}: Invalid JSON format.")

    print("Validation completed.")

def main():
    validate_jsonl()

if __name__ == "__main__":
    main()
