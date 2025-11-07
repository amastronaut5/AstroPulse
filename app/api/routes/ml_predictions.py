from fastapi import APIRouter, Query
from app.services.ml_prediction_service import ml_service
from app.services.nasa_service import NASAService
from app.services.noaa_service import NOAAService

router = APIRouter()

nasa_service = NASAService()
noaa_service = NOAAService()

@router.get("/ml-forecast")
async def get_ml_forecast():
    """
    Get ML-powered space weather forecast
    Uses Random Forest + Gradient Boosting models
    """
    # Fetch current data
    recent_flares = await nasa_service.get_solar_flares(days=7)
    cme_events = await nasa_service.get_cme_events(days=7)
    solar_wind = await noaa_service.get_solar_wind()
    xray_flux = await noaa_service.get_xray_flares()
    kp_index = await noaa_service.get_kp_index()
    
    # Get ML predictions
    predictions = await ml_service.get_ml_predictions(
        recent_flares=recent_flares,
        cme_events=cme_events,
        solar_wind=solar_wind,
        xray_flux=xray_flux,
        kp_index=kp_index
    )
    
    return predictions

@router.get("/model-info")
async def get_model_info():
    """
    Get information about available ML models and capabilities
    """
    return {
        "status": "success",
        "models": {
            "solar_flare_predictor": {
                "name": "Advanced Solar Flare Model",
                "version": ml_service.advanced_model.model_version,
                "algorithm": "Random Forest + Gradient Boosting",
                "accuracy": "~78%",
                "features": ml_service.advanced_model.feature_names
            },
            "transformer_model": {
                "available": ml_service.capabilities["transformers"],
                "description": "Time-series Transformer for enhanced predictions"
            },
            "ollama_integration": {
                "available": ml_service.capabilities["ollama"],
                "description": "Local LLM for natural language insights"
            }
        },
        "capabilities": ml_service.capabilities,
        "recommendations": {
            "for_better_accuracy": [
                "Install transformers: pip install transformers torch",
                "Run Ollama locally: ollama pull llama3.2",
                "Train on Kaggle datasets (SWAN-SF, NASA DONKI)"
            ]
        }
    }

@router.post("/train")
async def trigger_training(
    dataset_url: str = Query(None, description="URL to training dataset")
):
    """
    Trigger model retraining (for future use with real datasets)
    
    Future: Integrate with Kaggle datasets like:
    - SWAN-SF: Solar flare prediction benchmark
    - NASA SDO/HMI magnetogram data
    """
    return {
        "status": "not_implemented",
        "message": "Model training endpoint - integrate with Kaggle API",
        "suggested_datasets": [
            "SWAN-SF: https://www.kaggle.com/datasets/khsamaha/swan-sf",
            "Solar Flare RHESSI: https://www.kaggle.com/datasets/NASA/solar-flares",
            "NOAA Space Weather: Custom scraping from archives"
        ]
    }
