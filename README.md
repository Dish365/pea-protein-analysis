# Pea Protein Extraction Process Analysis System

## Project Overview
A comprehensive analysis system for comparing three pea protein extraction processes, focusing on technical performance, economic viability, and environmental impact.

### Process Types
1. **Baseline Dry Fractionation**
   - Traditional air classification process
   - Standard protein separation technique
   - Baseline for comparison

2. **RF Pre-treatment with Dry Fractionation**
   - Radio Frequency enhanced process
   - Modified protein structure
   - Improved separation efficiency

3. **IR Pre-treatment with Dry Fractionation**
   - Infrared radiation treatment
   - Thermal modification approach
   - Enhanced protein recovery

## Analysis Components

### Technical Analysis
- Protein recovery tracking
- Separation efficiency calculation
- Particle size distribution
- Product purity assessment

### Economic Analysis
- Capital expenditure (CAPEX) estimation
- Operational costs (OPEX) calculation
- Net Present Value (NPV) analysis
- Return on Investment (ROI) metrics

### Environmental Assessment
- Life Cycle Assessment (LCA)
- Global Warming Potential (GWP)
- Human Carcinogenic Toxicity (HCT)
- Fossil Resource Scarcity (FRS)
- Water Consumption (WC)

## Technology Stack

### Backend
- **Django**: Core application framework
  - User management
  - Data persistence
  - API authentication
- **FastAPI**: Process-specific APIs
  - Real-time calculations
  - High-performance endpoints
  - Process analysis routes

### Computation
- **Rust**: High-performance modules
  - Monte Carlo simulations
  - Matrix operations
  - Particle analysis
  - Statistical computations

### Database
- **PostgreSQL**: Primary database
  - Process data storage
  - Analysis results
  - Time series data

### Frontend
- **React**: User interface
  - Interactive visualizations
  - Real-time data display
  - Analysis dashboards

## Project Structure

```
project_root/
├── analytics/           # Core analysis modules
│   ├── protein_analysis/
│   ├── economic/
│   ├── environmental/
│   └── simulation/
├── backend/
│   ├── django_app/     # Main Django application
│   ├── fastapi_app/    # FastAPI services
│   └── rust_modules/   # Rust computation modules
├── frontend/           # React application
└── docs/              # Documentation
```

## Setup and Installation

### Prerequisites
- Python 3.9+
- Rust 1.70+
- PostgreSQL 13+
- Node.js 16+
- Redis (for caching)

### Development Setup
1. Clone the repository:
```bash
git clone https://github.com/Dish365/pea-protein-analysis.git
cd pea-protein-analysis
```

2. Create and activate Python virtual environment:
```bash
python -m venv venv
.\venv\Scripts\Activate  # Windows
source venv/bin/activate # Unix
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up database:
```bash
.\setup_database.ps1  # Windows
./setup_database.sh   # Unix
```

5. Run migrations:
```bash
cd backend/django_app
python manage.py migrate
```

### Running the Application

1. Start Django server:
```bash
cd backend/django_app
python manage.py runserver
```

2. Start FastAPI server:
```bash
cd backend/fastapi_app
uvicorn main:app --reload
```

3. Start frontend development server:
```bash
cd frontend
npm install
npm start
```

## Development Workflow

1. Create feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make changes and test:
```bash
# Run tests
python manage.py test
pytest

# Format code
black .
flake8
```

3. Commit and push:
```bash
git add .
git commit -m "feat: Add feature description"
git push -u origin feature/your-feature-name
```

4. Create pull request on GitHub
- Analytics/: Core analysis modules
- Backend/: Django and FastAPI applications
- Frontend/: React application
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
- Django tests: `python manage.py test`
- FastAPI tests: `pytest`
- Frontend tests: `npm test`
- Integration tests: `pytest tests/integration`

## Documentation
- API documentation: `/docs/api/`
- Technical documentation: `/docs/technical/`
- User guides: `/docs/guides/`

## Contributing
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License
[MIT License](LICENSE)

## Contact
- Project Maintainer: [Emmanuel Amankrah Kwofie](https://github.com/Amankrah)
- GitHub Issues: [Project Issues](https://github.com/Dish365/pea-protein-analysis/issues)
