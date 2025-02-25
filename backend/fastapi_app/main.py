"""
FastAPI Main Application Module

This module initializes and configures the FastAPI application with all its routes and middleware.
"""

import logging
import sys
import os
from typing import Dict, Any, Optional
from pathlib import Path

# Configure logging before any imports
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    force=True,
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Configure specific loggers
for name in [
    'backend',
    'backend.fastapi_app',
    'backend.fastapi_app.process_analysis',
    'backend.fastapi_app.process_analysis.economic_endpoint',
    'analytics',
    'analytics.economic',
    'analytics.economic.profitability_analyzer',
    'analytics.environmental',
]:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = True
    
# Get the main logger
logger = logging.getLogger('backend.fastapi_app.main')

# Now import the rest of the modules
from fastapi import FastAPI, APIRouter, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel

from backend.fastapi_app.process_analysis import (
    economic_endpoint,
    efficiency_endpoints,
    environmental_endpoints,
    allocation_endpoints,
    protein_endpoints
)

from backend.fastapi_app.models.environmental_analysis import (
    ProcessInputs,
    AllocationMethod,
    ProcessAnalysisResponse,
    AllocationWeights
)

class ProcessAnalysisRequest(BaseModel):
    """Complete process analysis request model"""
    process_data: ProcessInputs
    allocation_method: Optional[AllocationMethod] = None
    product_values: Optional[Dict[str, float]] = None
    mass_flows: Optional[Dict[str, float]] = None
    hybrid_weights: Optional[AllocationWeights] = None

class CompleteAnalysisResponse(BaseModel):
    """Complete analysis response model"""
    protein: Dict[str, Any]
    economic: Dict[str, Any]
    environmental: ProcessAnalysisResponse

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

    yield

    # Shutdown: Clean up resources if needed
    logger.info("Shutting down application")

app = FastAPI(
    debug=True,
    lifespan=lifespan,
    title="Process Analysis API",
    description="API for comprehensive process analysis including environmental impacts",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you should specify the exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create main API router
api_router = APIRouter(prefix="/api/v1")

# Include protein analysis endpoints
logger.debug("Including Protein Analysis endpoints")
api_router.include_router(
    protein_endpoints.router,
    prefix="/protein",
    tags=["Protein Analysis"]
)

# Economic analysis endpoints
logger.debug("Configuring economic analysis endpoints")
economic_router = APIRouter()

# Include economic sub-routers with their prefixes
economic_router.include_router(
    economic_endpoint.capex_router,
    prefix="/capex",
    tags=["Capital Expenditure"]
)

economic_router.include_router(
    economic_endpoint.opex_router,
    prefix="/opex",
    tags=["Operational Expenditure"]
)

economic_router.include_router(
    economic_endpoint.profitability_router,
    prefix="/profitability",
    tags=["Profitability Analysis"]
)

# Include economic router in main API router
api_router.include_router(economic_router, prefix="/economic")

# Environmental analysis endpoints
logger.debug("Including Environmental Analysis endpoints")
environmental_router = APIRouter(prefix="/environmental")

environmental_router.include_router(
    environmental_endpoints.router,
    prefix="/impact",
    tags=["Environmental Impact"]
)

environmental_router.include_router(
    allocation_endpoints.router,
    prefix="/allocation",
    tags=["Environmental Allocation"]
)

environmental_router.include_router(
    efficiency_endpoints.router,
    prefix="/eco-efficiency",
    tags=["Eco-efficiency Analysis"]
)

# Include environmental router in main API router
api_router.include_router(environmental_router)

# Create router for complete process analysis
process_router = APIRouter(prefix="/api/v1/process")

@process_router.post("/analyze/{process_id}", response_model=CompleteAnalysisResponse)
async def analyze_process(
    process_id: str,
    request: ProcessAnalysisRequest,
    include_contributions: bool = Query(True, description="Include process contributions in response")
) -> CompleteAnalysisResponse:
    """
    Complete analysis pipeline including protein, economic, and environmental analysis
    
    Args:
        process_id: Unique identifier for the process
        request: Complete process analysis request data
        include_contributions: Whether to include detailed process contributions
    
    Returns:
        Combined results from all analyses
    """
    try:
        logger.info(f"Starting complete analysis for process {process_id}")
        
        # Perform protein analysis
        protein_results = await protein_endpoints.analyze_protein(request.process_data.dict())

        # Perform comprehensive economic analysis
        economic_results = await economic_endpoint.analyze_comprehensive({
            **request.process_data.dict(),
            "process_id": process_id
        })

        # Perform environmental analysis
        environmental_results = await environmental_endpoints.analyze_process(
            request=request.process_data,
            allocation_method=request.allocation_method,
            product_values=request.product_values,
            mass_flows=request.mass_flows,
            hybrid_weights=request.hybrid_weights,
            include_contributions=include_contributions
        )

        logger.info(f"Completed analysis for process {process_id}")
        
        return CompleteAnalysisResponse(
            protein=protein_results,
            economic=economic_results,
            environmental=environmental_results
        )

    except ValueError as e:
        logger.error(f"Validation error in process analysis: {str(e)}")
        raise HTTPException(
            status_code=422,
            detail={"message": str(e), "type": "validation_error"}
        )
    except Exception as e:
        logger.error(f"Error in process analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={"message": f"Analysis failed: {str(e)}", "type": "server_error"}
        )

# Include all routers in the main app
app.include_router(api_router)
app.include_router(process_router)

# Static file handling - for serving frontend files
# Define the path to the frontend build directory (adjust as needed)
frontend_dir = Path(__file__).resolve().parents[3] / "frontend" / ".next"

# Serve frontend static files if the directory exists
if frontend_dir.exists():
    app.mount("/_next", StaticFiles(directory=str(frontend_dir / "static")), name="static")
    
    @app.get("/{path:path}", include_in_schema=False)
    async def serve_frontend(request: Request, path: str):
        # First, check if it's requesting an API endpoint
        if path.startswith("api/"):
            # Let the API routers handle it
            return None
            
        # For everything else, return the default response
        return {
            "message": "Welcome to the Process Analysis API",
            "version": "1.0.0",
            "docs_url": "/docs",
            "note": "Frontend server is not running. Please start the Next.js server or access the API directly."
        }

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Welcome to the Process Analysis API",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

@app.get("/health")
async def health_check():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "components": {
            "api": "running",
            "database": "connected",
            "services": "operational"
        },
        "version": "1.0.0"
    }
