# Git setup script
$projectRoot = "C:\Users\USER\Desktop\Dev_Projects\nrc"

# Create .gitignore file
$gitignoreContent = @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
ENV/
env/
.env

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media

# FastAPI
.env
.env.local

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDEs
.idea/
.vscode/
*.swp
*.swo
.DS_Store

# Rust
target/
Cargo.lock
**/*.rs.bk

# Database
*.sql
*.sqlite

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Testing
.coverage
htmlcov/
.tox/
.pytest_cache/
"@

# Create .gitignore file
Set-Content -Path "$projectRoot\.gitignore" -Value $gitignoreContent
Write-Host "Created .gitignore file"

# Initialize Git repository
Set-Location $projectRoot
git init
Write-Host "Initialized Git repository"

# Create initial README.md
$readmeContent = @"
# Pea Protein Extraction Process Analysis System

## Project Overview
A comprehensive backend system for analyzing and comparing three pea protein extraction processes:
- Baseline dry fractionation
- RF (Radio Frequency) pre-treatment with dry fractionation
- IR (Infrared) pre-treatment with dry fractionation

## Technology Stack
- Django: Core application framework
- FastAPI: Process-specific APIs
- Rust: High-performance computations
- PostgreSQL: Database
- React: Frontend visualization

## Project Structure
- `analytics/`: Core analysis modules
- `backend/`: Django and FastAPI applications
- `frontend/`: React application
- `docs/`: Project documentation

## Setup
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: `.\venv\Scripts\Activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up database: `.\setup_database.ps1`
6. Run migrations: `cd backend\django_app && python manage.py migrate`

## Development
- Django server: `python manage.py runserver`
- FastAPI server: `uvicorn main:app --reload`
- Frontend: `cd frontend && npm start`

## Testing
Run tests with: `python manage.py test`

## License
[Your chosen license]
"@

# Create README.md
Set-Content -Path "$projectRoot\README.md" -Value $readmeContent
Write-Host "Created README.md"

# Add all files to git
git add .
git commit -m "Initial commit: Project structure setup"
Write-Host "Created initial commit"

Write-Host "`nGit repository initialized successfully!"
Write-Host "Next steps:"
Write-Host "1. Create a new repository on GitHub"
Write-Host "2. Run the following commands to push to GitHub:"
Write-Host "   git remote add origin <your-github-repo-url>"
Write-Host "   git branch -M main"
Write-Host "   git push -u origin main" 