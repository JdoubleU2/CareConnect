import os
import snowflake.connector

# Snowflake connection parameters
connection_params = {
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "stage": os.getenv("SNOWFLAKE_STAGE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA"),  # Ensure schema is set
}

# Establish a connection
conn = snowflake.connector.connect(**connection_params)
cursor = conn.cursor()

# Set Schema explicitly before using PUT
cursor.execute(f"USE DATABASE {connection_params['database']}")
cursor.execute(f"USE SCHEMA {connection_params['schema']}")  # 🔹 Fixes "No schema" error

# Define stage and file to upload

stage = connection_params["stage"]  
data_dir = "data/"


# Walk through all subdirectories and files
for root, dirs, files in os.walk(data_dir):
    for file in files:
        if file.endswith(".jsonl"):
            file_path = os.path.join(root, file)
            print(f"Uploading {file_path} to @{stage}")
            cursor.execute(f"PUT file://{file_path} @{stage} OVERWRITE=TRUE AUTO_COMPRESS=FALSE")

print("✅ All .jsonl files uploaded successfully!")

# Close the connection
cursor.close()
conn.close()
