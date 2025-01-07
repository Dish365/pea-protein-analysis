from fastapi import FastAPI

app = FastAPI(title="Pea Protein Analysis API")

@app.get("/")
async def root():
    return {"message": "Pea Protein Analysis API"}
