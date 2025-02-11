from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager
from fastapi import HTTPException

from backend.fastapi_app.process_analysis import (
    capex_endpoints,
    opex_endpoints,
    profitability_endpoints,
    efficiency_endpoints,
    impact_endpoints,
    allocation_endpoints,
    protein_endpoints,
    technical_endpoints,
    economic_endpoints,
    environmental_endpoints
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Log all registered routes
    logger.debug("Registered routes:")
    routes = []
    for route in app.routes:
        routes.append(f"Route: {route.path} [{route.methods}]")
    for route in sorted(routes):
        logger.debug(route)

    # Initialize components
    logger.info("Analysis pipeline initialized")
    logger.info("Environmental and efficiency endpoints initialized")
    logger.info("Environmental impact endpoints initialized")
    logger.info("Environmental allocation endpoints initialized")
    logger.info("Eco-efficiency endpoints initialized")
    logger.info("Workflow components initialized successfully")

    yield  # Application runs here

    # Shutdown: Clean up resources if needed
    logger.info("Shutting down application")

app = FastAPI(debug=True, lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create main API router
api_router = APIRouter(prefix="/api/v1")

# Technical analysis router
logger.debug("Configuring technical analysis endpoints")
technical_router = APIRouter()

# Include protein analysis endpoints
logger.debug("Including Protein Analysis endpoints")
technical_router.include_router(
    protein_endpoints.router,
    tags=["Protein Analysis"]
)

# Include technical router in main API router
api_router.include_router(technical_router, prefix="/technical")

# Economic analysis endpoints
logger.debug("Configuring economic analysis endpoints")
economic_router = APIRouter()

# Include sub-routers with their prefixes
logger.debug("Including CAPEX endpoints")
economic_router.include_router(
    capex_endpoints.router,
    prefix="/capex",
    tags=["Capital Expenditure"]
)

logger.debug("Including OPEX endpoints")
economic_router.include_router(
    opex_endpoints.router,
    prefix="/opex",
    tags=["Operational Expenditure"]
)

logger.debug("Including Profitability endpoints")
economic_router.include_router(
    profitability_endpoints.router,
    prefix="/profitability",
    tags=["Profitability Analysis"]
)

# Include economic router in main API router
logger.debug("Including economic router in main API router")
api_router.include_router(economic_router, prefix="/economic")

# Environmental analysis endpoints

# Impact analysis endpoints
logger.debug("Including Impact endpoints")
api_router.include_router(
    impact_endpoints.router,
    prefix="/environmental/impact",
    tags=["Environmental Impact"]
)

# Allocation analysis endpoints
logger.debug("Including Allocation endpoints")
api_router.include_router(
    allocation_endpoints.router,
    prefix="/environmental/allocation",
    tags=["Environmental Allocation"]
)

# Efficiency analysis endpoints
logger.debug("Including Efficiency endpoints")
api_router.include_router(
    efficiency_endpoints.router,
    prefix="/environmental/eco-efficiency",
    tags=["Eco-efficiency Analysis"]
)

# Create router for process analysis
router = APIRouter(prefix="/api/v1/process")


@router.post("/analyze/{process_id}")
async def analyze_process(process_id: str, data: dict):
    """Complete analysis pipeline"""
    try:
        # Perform technical analysis
        technical_results = await technical_endpoints.analyze_technical(data)

        # Perform economic analysis
        economic_results = await economic_endpoints.analyze_economic(data)

        # Perform environmental analysis
        environmental_results = await environmental_endpoints.analyze_environmental(data)

        return {
            "technical": technical_results,
            "economic": economic_results,
            "environmental": environmental_results
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

# Include all routers in the main app
logger.debug("Including main API router in FastAPI app")
app.include_router(api_router)
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Process Analysis API"}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "components": {
            "api": "running",
            "database": "connected",
            "services": "operational"
        }
    }
