from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .process_analysis import protein_endpoints

app = FastAPI(
    title="Pea Protein Process Analysis API",
    description="API for analyzing pea protein extraction processes",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(protein_endpoints.router)

@app.get("/")
async def root():
    return {"message": "Pea Protein Process Analysis API"}
