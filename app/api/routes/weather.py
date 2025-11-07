from fastapi import APIRouter, Query
from typing import Optional
from app.services.nasa_service import NASAService
from app.services.noaa_service import NOAAService

router = APIRouter()

nasa_service = NASAService()
noaa_service = NOAAService()

@router.get("/current")
async def get_current_weather():
    """Get current space weather conditions"""
    conditions = await noaa_service.get_current_conditions()
    return {
        "status": "success",
        "data": conditions
    }

@router.get("/solar-flares")
async def get_solar_flares(days: int = Query(default=7, ge=1, le=30)):
    """Get recent solar flare events"""
    flares = await nasa_service.get_solar_flares(days)
    return {
        "status": "success",
        "count": len(flares),
        "data": flares
    }

@router.get("/cme")
async def get_cme_events(days: int = Query(default=7, ge=1, le=30)):
    """Get Coronal Mass Ejection events"""
    cme_events = await nasa_service.get_cme_events(days)
    return {
        "status": "success",
        "count": len(cme_events),
        "data": cme_events
    }

@router.get("/geomagnetic-storms")
async def get_geomagnetic_storms(days: int = Query(default=7, ge=1, le=30)):
    """Get geomagnetic storm events"""
    storms = await nasa_service.get_geomagnetic_storms(days)
    return {
        "status": "success",
        "count": len(storms),
        "data": storms
    }

@router.get("/asteroids")
async def get_near_earth_objects(days: int = Query(default=7, ge=1, le=7)):
    """Get Near Earth Objects (asteroids)"""
    neos = await nasa_service.get_near_earth_objects(days)
    return {
        "status": "success",
        "data": neos
    }

@router.get("/radiation")
async def get_radiation_events(days: int = Query(default=7, ge=1, le=30)):
    """Get radiation belt enhancement events"""
    radiation = await nasa_service.get_radiation_belt_enhancement(days)
    return {
        "status": "success",
        "count": len(radiation),
        "data": radiation
    }

@router.get("/solar-wind")
async def get_solar_wind():
    """Get real-time solar wind data"""
    solar_wind = await noaa_service.get_solar_wind()
    return {
        "status": "success",
        "data": solar_wind[-50:] if solar_wind else []
    }

@router.get("/kp-index")
async def get_kp_index():
    """Get Kp index for geomagnetic activity"""
    kp = await noaa_service.get_kp_index()
    return {
        "status": "success",
        "data": kp
    }
