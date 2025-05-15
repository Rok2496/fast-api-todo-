import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database credentials
db_user = "postgres"
db_password = "1234"
db_host = "localhost"
db_name = "todo"

# Connect to PostgreSQL server
print("Connecting to PostgreSQL server...")
conn = psycopg2.connect(
    user=db_user,
    password=db_password,
    host=db_host
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()

# Check if database exists
cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
exists = cursor.fetchone()

if not exists:
    print(f"Creating database '{db_name}'...")
    cursor.execute(f"CREATE DATABASE {db_name}")
    print(f"Database '{db_name}' created successfully!")
else:
    print(f"Database '{db_name}' already exists.")

cursor.close()
conn.close()

print("\nCreating .env file with database configuration...")
env_content = f"""DATABASE_URL=postgresql://{db_user}:{db_password}@{db_host}/{db_name}
SECRET_KEY=supersecretkey123456789

# SMTP settings (update these with real values when needed)
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your_smtp_user
SMTP_PASS=your_smtp_password
FROM_EMAIL=noreply@example.com

# Google API credentials (update these with real values when needed)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
"""

with open(".env", "w") as env_file:
    env_file.write(env_content)

print(".env file created successfully!")
print("\nDatabase configuration complete. You can now run your application with:")
print("uvicorn app.main:app --reload") 