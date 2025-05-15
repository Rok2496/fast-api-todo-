import os
import subprocess
import sys

print("===== Todo API Database Setup =====")
print("This script will:")
print("1. Create the PostgreSQL database")
print("2. Setup the .env file with credentials")
print("3. Initialize the database tables\n")

# Step 1: Run the database initialization script
print("Step 1: Creating PostgreSQL database...")
try:
    subprocess.run([sys.executable, "scripts/init_db.py"], check=True)
except subprocess.CalledProcessError:
    print("Error creating the database. Make sure PostgreSQL is running.")
    sys.exit(1)

# Step 2: Run the table creation script
print("\nStep 2: Creating database tables...")
try:
    subprocess.run([sys.executable, "scripts/create_tables.py"], check=True)
except subprocess.CalledProcessError:
    print("Error creating the tables. Check your database configuration.")
    sys.exit(1)

print("\n===== Setup Complete! =====")
print("Your Todo API backend is now configured with PostgreSQL.")
print("You can run the API with: uvicorn app.main:app --reload") 