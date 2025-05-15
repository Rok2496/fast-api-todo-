#!/usr/bin/env python
"""
Migration Template

This template can be used as a starting point for creating new database migrations.
To use this template:

1. Copy this file with a descriptive name: migration_<description>.py
2. Modify the run_migration function to include your migration logic
3. Run the migration script

Example usage:
python scripts/migration_add_new_field.py
"""

from sqlalchemy import Column, String, DateTime, MetaData, Table, create_engine, text
import os
from dotenv import load_dotenv
import sys

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.database import DATABASE_URL

def run_migration():
    """
    Implement your migration logic here.
    This function should:
    1. Connect to the database
    2. Make the necessary schema changes
    3. Print helpful output
    """
    print("Running migration: <MIGRATION_DESCRIPTION>")
    
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    # Define metadata
    metadata = MetaData()
    metadata.reflect(bind=engine)
    
    # Get table
    # table = metadata.tables.get('<TABLE_NAME>')
    
    # Check column existence example
    # existing_columns = [c.name for c in table.columns]
    # if '<COLUMN_NAME>' not in existing_columns:
    #     print(f"Adding <COLUMN_NAME> column...")
    #     with engine.begin() as connection:
    #         connection.execute(text('ALTER TABLE <TABLE_NAME> ADD COLUMN <COLUMN_NAME> <DATA_TYPE>'))
    
    # Example: Add a new column
    # with engine.begin() as connection:
    #     connection.execute(text('ALTER TABLE users ADD COLUMN first_name VARCHAR'))
    
    # Example: Modify a column
    # with engine.begin() as connection:
    #     connection.execute(text('ALTER TABLE users ALTER COLUMN email TYPE VARCHAR(255)'))
    
    # Example: Create a new index
    # with engine.begin() as connection:
    #     connection.execute(text('CREATE INDEX idx_users_email ON users(email)'))
    
    print("Migration completed successfully.")

if __name__ == "__main__":
    load_dotenv()
    run_migration() 