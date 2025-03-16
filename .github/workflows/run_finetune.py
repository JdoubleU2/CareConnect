import os
from snowflake.snowpark import Session

# Snowflake connection configuration
connection_parameters = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "role": os.getenv("SNOWFLAKE_ROLE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
}

# Start a Snowflake Snowpark session
session = Session.builder.configs(connection_parameters).create()

# Ensure we are using the correct warehouse (GPU-enabled)
session.sql(f"USE WAREHOUSE {os.getenv('SNOWFLAKE_WAREHOUSE')}").collect()

# Set the compute pool for the medium gpu compute pool
compute_pool = "SOFTWARESURGEONS_MEDIUM_GPU" 
session.sql(f"ALTER SESSION SET COMPUTE_POOL = '{compute_pool}'").collect()

# Run the Jupyter notebook inside Snowflake Snowpark
notebook_path = "@my_stage/finetune.ipynb"  # Notebook must be staged in Snowflake
session.sql(f"CALL SYSTEM$EXECUTE_NOTEBOOK('{notebook_path}')").collect()

print("Notebook execution started on Snowpark Medium GPU.")

# Close the session
session.close()
