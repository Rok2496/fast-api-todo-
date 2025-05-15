#!/bin/bash
# Setup script for FAST TODO API development environment

set -e

echo "Setting up FAST TODO API development environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 --version | awk '{print $2}')
python_major=$(echo $python_version | cut -d. -f1)
python_minor=$(echo $python_version | cut -d. -f2)

if [ "$python_major" -lt 3 ] || ([ "$python_major" -eq 3 ] && [ "$python_minor" -lt 8 ]); then
    echo "Python 3.8 or higher is required. You have Python $python_version."
    exit 1
fi

echo "Using Python $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "Please update the .env file with your actual configuration values."
    else
        echo "ERROR: .env.example not found. Please create a .env file manually."
        cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/tododb

# Authentication
SECRET_KEY=your_secret_key_at_least_32_chars_long
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Google API Credentials
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
FRONTEND_REDIRECT_URL=http://localhost:3000/settings

# SMTP Configuration for Email
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=user@example.com
SMTP_PASS=your_smtp_password
FROM_EMAIL=noreply@example.com
EOF
        echo "A new .env file has been created with default values. Please update it."
    fi
fi

echo ""
echo "Setup completed successfully!"
echo ""
echo "To start the development server, run:"
echo "source venv/bin/activate  # If not already activated"
echo "uvicorn app.main:app --reload"
echo ""
echo "To run database migrations:"
echo "python scripts/migrate_add_otp_code.py"
echo ""
echo "API documentation will be available at:"
echo "http://localhost:8000/docs" 