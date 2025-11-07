from fastapi import APIRouter
from app.services.prediction_service import PredictionService
from app.services.nasa_service import NASAService
from app.services.noaa_service import NOAAService

router = APIRouter()

prediction_service = PredictionService()
nasa_service = NASAService()
noaa_service = NOAAService()

@router.get("/comprehensive")
async def get_comprehensive_predictions():
    """
    Get comprehensive space weather predictions from all ML models
    """
    # Fetch current data
    recent_flares = await nasa_service.get_solar_flares(days=7)
    cme_events = await nasa_service.get_cme_events(days=7)
    solar_wind = await noaa_service.get_solar_wind()
    xray_flux = await noaa_service.get_xray_flares()
    kp_index = await noaa_service.get_kp_index()
    
    # Get predictions
    predictions = await prediction_service.get_comprehensive_predictions(
        recent_flares=recent_flares,
        cme_events=cme_events,
        solar_wind=solar_wind,
        xray_flux=xray_flux,
        kp_index=kp_index
    )
    
    return predictions

@router.get("/solar-flares")
async def get_solar_flare_predictions():
    """Get solar flare predictions only"""
    recent_flares = await nasa_service.get_solar_flares(days=7)
    solar_wind = await noaa_service.get_solar_wind()
    xray_flux = await noaa_service.get_xray_flares()
    
    predictions = prediction_service.flare_predictor.predict_flare_probability(
        recent_flares=recent_flares,
        solar_wind_data=solar_wind,
        xray_flux=xray_flux
    )
    
    return {
        "status": "success",
        "data": predictions
    }

@router.get("/geomagnetic-storm")
async def get_geomagnetic_storm_predictions():
    """Get geomagnetic storm predictions"""
    kp_index = await noaa_service.get_kp_index()
    cme_events = await nasa_service.get_cme_events(days=3)
    
    # Check for fast CMEs
    has_fast_cme = any(
        float(cme.get("speed", 0)) > 1000 
        for cme in cme_events 
        if cme.get("speed")
    )
    
    predictions = prediction_service.flare_predictor.predict_geomagnetic_storm(
        kp_history=kp_index,
        cme_incoming=has_fast_cme
    )
    
    return {
        "status": "success",
        "data": predictions
    }

@router.get("/radiation-storm")
async def get_radiation_storm_predictions():
    """Get radiation storm predictions"""
    recent_flares = await nasa_service.get_solar_flares(days=7)
    
    predictions = prediction_service.radiation_predictor.predict_radiation_storm(
        recent_flares=recent_flares
    )
    
    return {
        "status": "success",
        "data": predictions
    }

@router.get("/cme-arrival")
async def get_cme_arrival_predictions():
    """Get CME arrival time predictions"""
    cme_events = await nasa_service.get_cme_events(days=3)
    
    # Find recent fast CMEs
    fast_cmes = [
        cme for cme in cme_events 
        if cme.get("speed") and float(cme.get("speed", 0)) > 500
    ]
    
    if not fast_cmes:
        return {
            "status": "success",
            "data": {
                "message": "No Earth-directed CMEs detected recently",
                "predictions": []
            }
        }
    
    # Predict arrival for each fast CME
    predictions = []
    for cme in fast_cmes[-3:]:  # Last 3 fast CMEs
        prediction = prediction_service.flare_predictor.predict_cme_arrival(
            cme_speed=float(cme.get("speed", 0)),
            detection_time=cme.get("startTime", "")
        )
        predictions.append(prediction)
    
    return {
        "status": "success",
        "data": {
            "count": len(predictions),
            "predictions": predictions
        }
    }
