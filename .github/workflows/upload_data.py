import os
import snowflake.connector

# Snowflake connection
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    role=os.getenv("SNOWFLAKE_ROLE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
)

cursor = conn.cursor()
stage = os.getenv("SNOWFLAKE_STAGE")

# upload preprocessed data files from 'data/processed_data' 
data_dir = "data/processed_data"

for file in os.listdir(data_dir):
    file_path = f"{data_dir}/{file}"
    print(f"Uploading {file_path} to {stage}")
    cursor.execute(f"PUT file://{file_path} @{stage}")


# upload finetuneSnowflake.ipynhb to the stage 
notebook_path = "finetune/src/finetuneSnowflake.ipynb"
cursor.execute(f"PUT file://{notebook_path} @my_stage OVERWRITE=TRUE")

cursor.close()
conn.close()
