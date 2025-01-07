# Windows Installation Guide (PowerShell)

## Prerequisites

1. Install Python (3.8+):
   - Download Python from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Verify installation:
```powershell
python --version
```

2. Install Rust:
   - Download and run rustup-init.exe from [rustup.rs](https://rustup.rs/)
   - Or use PowerShell:
```powershell
Invoke-WebRequest https://win.rustup.rs -OutFile rustup-init.exe
.\rustup-init.exe
# Restart PowerShell after installation
```

3. Install PostgreSQL:
   - Download and install from [postgresql.org](https://www.postgresql.org/download/windows/)
   - Add PostgreSQL bin directory to PATH (typically `C:\Program Files\PostgreSQL\14\bin`)
   - Verify installation:
```powershell
psql --version
```

4. Install Node.js and npm:
   - Download and install from [nodejs.org](https://nodejs.org/)
   - Verify installation:
```powershell
node --version
npm --version
```

5. Install Redis:
   - Download the Windows Subsystem for Linux (WSL2)
```powershell
wsl --install
# Restart your computer after installation
```
   - Then install Redis in WSL:
```powershell
wsl
sudo apt update
sudo apt install redis-server
```

## Project Setup

1. Create and navigate to project directory:
```powershell
cd C:\Users\USER\Desktop\Dev_Projects\nrc
```

2. Create and activate Python virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

3. Install Python dependencies:
```powershell
# Core dependencies
pip install django fastapi uvicorn celery
pip install numpy pandas scipy matplotlib
pip install psycopg2-binary redis
pip install pytest pytest-django

# Create requirements.txt
pip freeze > requirements.txt
```

4. Set up the Django project:
```powershell
cd backend\django_app
python manage.py migrate
python manage.py createsuperuser
```

5. Install Rust dependencies:
```powershell
cd ..\rust_modules
cargo build
```

6. Set up the React frontend:
```powershell
cd ..\frontend
npm install
```

7. Initialize PostgreSQL database:
```powershell
# Start PostgreSQL service
net start postgresql-x64-14  # Replace with your version

# Create database (using psql)
psql -U postgres
# In psql prompt:
CREATE DATABASE pea_protein_db;
\q
```

8. Start Redis (in WSL):
```powershell
wsl
sudo service redis-server start
```

## Development Environment Setup

1. Create environment variables file:
```powershell
New-Item .env
Add-Content .env @"
DATABASE_URL=postgresql://localhost/pea_protein_db
REDIS_URL=redis://localhost:6379
DEBUG=True
SECRET_KEY=your-secret-key
"@
```

2. Install Docker (optional):
   - Download and install Docker Desktop for Windows from [docker.com](https://www.docker.com/products/docker-desktop)
   - Ensure WSL2 is installed and enabled

## Running the Project

1. Start the Django development server:
```powershell
cd backend\django_app
python manage.py runserver
```

2. Start the FastAPI server (in new PowerShell window):
```powershell
cd backend\fastapi_app
uvicorn main:app --reload
```

3. Start the React development server (in new PowerShell window):
```powershell
cd frontend
npm start
```

4. Run with Docker (optional):
```powershell
docker-compose up --build
```

## Testing

Run tests for different components:

```powershell
# Django tests
cd backend\django_app
python manage.py test

# FastAPI tests
cd ..\fastapi_app
pytest

# Rust tests
cd ..\rust_modules
cargo test

# Frontend tests
cd ..\frontend
npm test
```

## Additional Development Tools

```powershell
# Install development tools
pip install black flake8 mypy
cargo install clippy
npm install -g eslint prettier
```

## Troubleshooting

For PostgreSQL issues:
```powershell
# Connect to PostgreSQL
psql -U postgres
# In psql prompt:
ALTER USER postgres WITH PASSWORD 'your_password';
CREATE DATABASE pea_protein_db;
GRANT ALL PRIVILEGES ON DATABASE pea_protein_db TO postgres;
```

For Redis issues:
```powershell
# Check WSL Redis status
wsl
sudo service redis-server status
sudo service redis-server restart
```

Remember to:
1. Run PowerShell as Administrator when needed
2. Use backslashes (`\`) instead of forward slashes for Windows paths
3. Keep WSL running when using Redis
4. Add all necessary directories to Windows PATH 