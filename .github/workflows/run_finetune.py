import os
from snowflake.snowpark import Session

# Snowflake connection parameters
connection_params = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "role": os.getenv("SNOWFLAKE_ROLE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA"),  # Ensure schema is set
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
}

# Start a Snowflake Snowpark session
session = Session.builder.configs(connection_params).create()

# Ensure correct database, schema, and warehouse are set
session.sql(f"USE DATABASE {connection_params['database']}").collect()
session.sql(f"USE SCHEMA {connection_params['schema']}").collect()
session.sql(f"USE WAREHOUSE {connection_params['warehouse']}").collect()
stage = "CARECONNECT_TRAINING_DATA_STAGE"  

# Set the compute pool for the medium gpu compute pool
compute_pool = "SOFTWARESURGEONS_MEDIUM_GPU"  
session.sql(f"ALTER SESSION SET COMPUTE_POOL = '{compute_pool}'").collect()

# Run the Jupyter notebook from the Snowflake stage
notebook_path = "@{stage}/finetune.ipynb"  # Ensure notebook is staged
session.sql(f"CALL SYSTEM$EXECUTE_NOTEBOOK('{notebook_path}')").collect()

print("✅ Notebook execution started on Snowpark Medium GPU.")

# Close the session
session.close()