from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .process_analysis import (
    pipeline_endpoints,
    protein_endpoints,
    economic_endpoints,
    environmental_endpoints,
    efficiency_endpoints
)
from .services import streaming, ws_manager  # Import shared ws_manager instance

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Process Analysis API",
    description="API for pea protein extraction process analysis",
    version="1.0.0"
)

# Configure CORS with WebSocket support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with actual frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_websockets=True  # Enable WebSocket support
)

# Include routers
app.include_router(pipeline_endpoints.router)
app.include_router(protein_endpoints.router)
app.include_router(economic_endpoints.router)
app.include_router(environmental_endpoints.router)
app.include_router(efficiency_endpoints.router)
app.include_router(streaming.router)  # Add streaming router

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    try:
        # Start the scheduler and monitoring
        from .process_analysis.pipeline_endpoints import scheduler, monitor
        import asyncio
        
        # Start scheduler and monitoring in background tasks
        asyncio.create_task(scheduler.start_scheduler())
        asyncio.create_task(monitor.start_monitoring())
        
        logger.info("Analysis pipeline initialized")
        logger.info("Real-time streaming services initialized")
        logger.info("Environmental and efficiency endpoints initialized")
        
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    try:
        # Cleanup WebSocket connections
        for client_id in list(ws_manager.active_connections.keys()):
            await ws_manager.disconnect(client_id)
            
        logger.info("Cleaned up WebSocket connections")
        
    except Exception as e:
        logger.error(f"Shutdown error: {str(e)}")

@app.get("/health")
async def health_check():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "websocket_connections": len(ws_manager.active_connections),
        "components": {
            "pipeline": "ok",
            "streaming": "ok",
            "environmental": "ok",
            "efficiency": "ok"
        }
    }
