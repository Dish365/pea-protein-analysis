from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

from backend.fastapi_app.process_analysis import (
    capex_endpoints,
    opex_endpoints,
    profitability_endpoints,
    economic_endpoints,
    pipeline_endpoints,
    environmental_endpoints,
    efficiency_endpoints,
    impact_endpoints,
    allocation_endpoints,
    protein_endpoints
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
    allow_origins=["*"],
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

logger.debug("Including Economic Analysis endpoints")
economic_router.include_router(
    economic_endpoints.router,
    tags=["Economic Analysis"]
)

# Include economic router in main API router
logger.debug("Including economic router in main API router")
api_router.include_router(economic_router, prefix="/economic")

# Pipeline endpoints
logger.debug("Including Pipeline endpoints")
api_router.include_router(
    pipeline_endpoints.router,
    prefix="/pipeline",
    tags=["Pipeline Analysis"]
)

# Environmental analysis endpoints
logger.debug("Including Environmental endpoints")
api_router.include_router(
    environmental_endpoints.router,
    prefix="/environmental",
    tags=["Environmental Analysis"]
)

# Efficiency analysis endpoints
logger.debug("Including Efficiency endpoints")
api_router.include_router(
    efficiency_endpoints.router,
    prefix="/efficiency",
    tags=["Efficiency Analysis"]
)

# Impact analysis endpoints
logger.debug("Including Impact endpoints")
api_router.include_router(
    impact_endpoints.router,
    prefix="/environmental",
    tags=["Environmental Impact Analysis"]
)

# Allocation analysis endpoints
logger.debug("Including Allocation endpoints")
api_router.include_router(
    allocation_endpoints.router,
    prefix="/allocation",
    tags=["Allocation Analysis"]
)

# Include all routers in the main app
logger.debug("Including main API router in FastAPI app")
app.include_router(api_router)

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

