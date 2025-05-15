from sqlalchemy import Column, String, DateTime, MetaData, Table, create_engine, text
import os
from dotenv import load_dotenv
import sys

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.database import DATABASE_URL

def run_migration():
    print("Running migration to add one-time code columns to users table...")
    
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    # Define metadata
    metadata = MetaData()
    metadata.reflect(bind=engine)
    
    # Get users table
    users_table = metadata.tables.get('users')
    
    # Check if the columns already exist to avoid errors
    existing_columns = [c.name for c in users_table.columns]
    
    # Add columns if they don't exist
    with engine.begin() as connection:
        if 'one_time_code' not in existing_columns:
            print("Adding one_time_code column...")
            connection.execute(text('ALTER TABLE users ADD COLUMN one_time_code VARCHAR'))
        else:
            print("Column one_time_code already exists.")
            
        if 'one_time_code_expiry' not in existing_columns:
            print("Adding one_time_code_expiry column...")
            connection.execute(text('ALTER TABLE users ADD COLUMN one_time_code_expiry TIMESTAMP'))
        else:
            print("Column one_time_code_expiry already exists.")
            
    print("Migration completed successfully.")

if __name__ == "__main__":
    load_dotenv()
    run_migration() 