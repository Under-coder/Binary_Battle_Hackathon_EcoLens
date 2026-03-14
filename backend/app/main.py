from fastapi import FastAPI
from app.routes.analysis import router as analysis_router

app = FastAPI(
    title="EcoLens API",
    description="AI-powered environmental analysis system",
    version="1.0"
)

app.include_router(analysis_router)

@app.get("/")
def home():
    return {"message": "EcoLens backend is running"}