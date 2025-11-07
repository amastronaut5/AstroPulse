from fastapi import APIRouter
from typing import List, Dict
from app.services.nasa_service import NASAService
from app.services.noaa_service import NOAAService
from datetime import datetime

router = APIRouter()

nasa_service = NASAService()
noaa_service = NOAAService()

def classify_flare_severity(class_type: str) -> str:
    """Classify solar flare severity"""
    if not class_type:
        return "unknown"
    
    first_char = class_type[0].upper()
    if first_char in ['X']:
        return "extreme"
    elif first_char in ['M']:
        return "high"
    elif first_char in ['C']:
        return "moderate"
    else:
        return "low"

def classify_cme_severity(speed: float) -> str:
    """Classify CME severity based on speed"""
    if speed >= 2000:
        return "extreme"
    elif speed >= 1000:
        return "high"
    elif speed >= 500:
        return "moderate"
    else:
        return "low"

@router.get("/active")
async def get_active_alerts():
    """Get all active space weather alerts"""
    
    # Fetch recent events
    flares = await nasa_service.get_solar_flares(days=2)
    cme_events = await nasa_service.get_cme_events(days=2)
    storms = await nasa_service.get_geomagnetic_storms(days=2)
    radiation = await nasa_service.get_radiation_belt_enhancement(days=2)
    
    alerts = []
    
    # Process solar flares
    for flare in flares:
        severity = classify_flare_severity(flare.get("classType", ""))
        if severity in ["high", "extreme"]:
            alerts.append({
                "id": flare.get("flrID"),
                "type": "solar_flare",
                "severity": severity,
                "title": f"Solar Flare {flare.get('classType', 'Unknown')} detected",
                "description": f"Peak time: {flare.get('peakTime', 'N/A')}",
                "timestamp": flare.get("beginTime"),
                "source": "NASA DONKI"
            })
    
    # Process CME events
    for cme in cme_events:
        speed = float(cme.get("speed", 0)) if cme.get("speed") else 0
        severity = classify_cme_severity(speed)
        if severity in ["high", "extreme"]:
            alerts.append({
                "id": cme.get("activityID"),
                "type": "cme",
                "severity": severity,
                "title": f"Coronal Mass Ejection detected",
                "description": f"Speed: {speed} km/s",
                "timestamp": cme.get("startTime"),
                "source": "NASA DONKI"
            })
    
    # Process geomagnetic storms
    for storm in storms:
        kp_index = float(storm.get("allKpIndex", [{}])[0].get("kpIndex", 0)) if storm.get("allKpIndex") else 0
        severity = "high" if kp_index >= 7 else "moderate" if kp_index >= 5 else "low"
        
        if severity in ["high", "extreme"]:
            alerts.append({
                "id": storm.get("gstID"),
                "type": "geomagnetic_storm",
                "severity": severity,
                "title": f"Geomagnetic Storm (Kp {kp_index})",
                "description": f"Start time: {storm.get('startTime', 'N/A')}",
                "timestamp": storm.get("startTime"),
                "source": "NASA DONKI"
            })
    
    # Process radiation events
    for rad in radiation:
        alerts.append({
            "id": rad.get("rbeID"),
            "type": "radiation",
            "severity": "moderate",
            "title": "Radiation Belt Enhancement",
            "description": f"Event time: {rad.get('eventTime', 'N/A')}",
            "timestamp": rad.get("eventTime"),
            "source": "NASA DONKI"
        })
    
    # Sort by timestamp (most recent first)
    alerts.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    return {
        "status": "success",
        "count": len(alerts),
        "alerts": alerts
    }

@router.get("/summary")
async def get_alerts_summary():
    """Get summary of alert counts by severity"""
    alerts_data = await get_active_alerts()
    alerts = alerts_data["alerts"]
    
    summary = {
        "total": len(alerts),
        "extreme": len([a for a in alerts if a["severity"] == "extreme"]),
        "high": len([a for a in alerts if a["severity"] == "high"]),
        "moderate": len([a for a in alerts if a["severity"] == "moderate"]),
        "low": len([a for a in alerts if a["severity"] == "low"])
    }
    
    return {
        "status": "success",
        "summary": summary
    }
