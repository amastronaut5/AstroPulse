from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import weather, chat, alerts, predictions
import uvicorn

app = FastAPI(
    title="AstroPulse API",
    description="Space Weather Monitoring & Prediction API",
    version="1.0.0"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(weather.router, prefix="/api/weather", tags=["Weather"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["Predictions"])

@app.get("/")
async def root():
    return {
        "message": "AstroPulse API - Space Weather Monitoring",
        "status": "operational",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8080, reload=True)
