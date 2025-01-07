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
- Analytics/: Core analysis modules
- Backend/: Django and FastAPI applications
- rontend/: React application
- docs/: Project documentation

## Setup
1. Clone the repository
2. Create virtual environment: python -m venv venv
3. Activate virtual environment: .\venv\Scripts\Activate
4. Install dependencies: pip install -r requirements.txt
5. Set up database: .\setup_database.ps1
6. Run migrations: cd backend\django_app && python manage.py migrate

## Development
- Django server: python manage.py runserver
- FastAPI server: uvicorn main:app --reload
- Frontend: cd frontend && npm start

## Testing
Run tests with: python manage.py test

## License
[Your chosen license]
