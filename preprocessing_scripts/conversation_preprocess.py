import pandas as pd
import csv
import string
import os 

def remove_duplicates_from_csv(input_file, output_file):
    df = pd.read_csv(input_file)
    df_cleaned = df.drop_duplicates()
    df_cleaned.to_csv(output_file, index=False)
    print(f"Duplicates removed and saved to {output_file}")

def remove_leading_spaces_from_second_column(df):
    df_new = df.copy()
    if len(df_new.columns) >= 2:
        second_col_name = df_new.columns[1]
        if df_new[second_col_name].dtype == 'object':
            try:
                df_new[second_col_name] = df_new[second_col_name].str.lstrip()
            except AttributeError:
                pass
            except Exception as e:
                print(f"Error processing second column: {e}")
    return df_new

def clean_csv_second_column(input_file, output_file):
    try:
        df = pd.read_csv(input_file)
        df_cleaned = remove_leading_spaces_from_second_column(df)
        df_cleaned.to_csv(output_file, index=False)
    except FileNotFoundError:
        print(f"Error: {input_file} not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: {input_file} is empty.")
    except Exception as e:
        print(f"An error occurred: {e}")

def remove_punctuation(input_file, output_file):
    translation_table = str.maketrans('', '', string.punctuation)
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        rows = [[cell.translate(translation_table) for cell in row] for row in reader]
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)

def convert_csv_to_lowercase(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        rows = [[cell.lower() for cell in row] for row in reader]
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)

input_file = '/Users/zeronelson/SoftwareDev/CareConnect/raw_data/conversation_data/done/pre-chatbot.csv'
output_file = '/Users/zeronelson/SoftwareDev/CareConnect/raw_data/conversation_data/processed/testingscript.csv'
clean_csv_second_column(input_file, output_file)

new_output_file = '/Users/zeronelson/SoftwareDev/CareConnect/raw_data/conversation_data/processed/testingscript2.csv'
remove_punctuation(output_file, new_output_file)




output_file = '/Users/zeronelson/SoftwareDev/CareConnect/raw_data/conversation_data/processed/final.csv'
convert_csv_to_lowercase(new_output_file,
                          output_file)

if os.path.exists(new_output_file):
    os.remove(new_output_file)
