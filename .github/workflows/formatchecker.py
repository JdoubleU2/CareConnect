import json
import os

class ValidationError(Exception):
    """Exception for validation errors."""
    pass

def validate_jsonl():
    directory_path = "data/"

    if not os.path.exists(directory_path):
        print(f"Directory not found: {directory_path}")
        return

    # Recursively walk through the directory
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if not file.endswith(".jsonl"):
                print(f"Detected non-JSONL file: {file}")
                exit(1)  # delete non-JSONL files

            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, start=1):
                    try:
                        data = json.loads(line.strip())

                        # Validate keys
                        required_keys = {"instruction", "input", "output"}
                        if not required_keys.issubset(data.keys()):
                            raise ValidationError(f"{file_path} Line {line_num}: Missing required keys.")

                        # Validate instruction format
                        if not isinstance(data["input"], str):
                            raise ValidationError(f"{file_path} Line {line_num}: Invalid input (must be a string).")

                        # Validate input format
                        if not isinstance(data["input"], str) or not data["input"].strip():
                            raise ValidationError(f"{file_path} Line {line_num}: Invalid input (must be non-empty string).")

                        # Validate output format
                        if not isinstance(data["output"], str) or not data["output"].strip():
                            raise ValidationError(f"{file_path} Line {line_num}: Invalid output (must be non-empty string).")

                    except json.JSONDecodeError:
                        raise ValidationError(f"{file_path} Line {line_num}: Invalid JSON format.")

    print("✅ Validation completed for all .jsonl files.")

def main():
    try:
        validate_jsonl()
    except ValidationError as ve:
        print(f"❌ Validation Error: {ve}")
        exit(1)

if __name__ == "__main__":
    main()
