from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
from app.services.nasa_service import NASAService
from app.services.noaa_service import NOAAService

router = APIRouter()

nasa_service = NASAService()
noaa_service = NOAAService()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = []

# Simple chatbot without external dependencies for MVP
async def generate_response(message: str, history: List[ChatMessage]) -> ChatResponse:
    """Generate AI response about space weather"""
    
    message_lower = message.lower()
    
    # Check if asking about current conditions
    if any(word in message_lower for word in ["current", "now", "today", "latest", "real-time"]):
        conditions = await noaa_service.get_current_conditions()
        solar_wind = conditions.get("solar_wind", [])
        kp_index = conditions.get("kp_index", [])
        
        response = "**Current Space Weather Conditions:**\n\n"
        
        if solar_wind:
            latest = solar_wind[-1]
            response += f"🌊 **Solar Wind:** Data recorded at {latest[0] if latest else 'N/A'}\n"
        
        if kp_index:
            latest_kp = kp_index[-1]
            kp_val = latest_kp[1] if len(latest_kp) > 1 else "N/A"
            response += f"🧲 **Kp Index:** {kp_val} (Geomagnetic activity)\n"
        
        response += "\n📡 Conditions are being monitored in real-time."
        
        return ChatResponse(
            response=response,
            sources=["NOAA Space Weather Prediction Center"]
        )
    
    # Check if asking about solar flares
    elif any(word in message_lower for word in ["solar flare", "flare", "x-ray"]):
        flares = await nasa_service.get_solar_flares(days=7)
        
        if flares:
            recent_flare = flares[-1]
            class_type = recent_flare.get("classType", "Unknown")
            peak_time = recent_flare.get("peakTime", "N/A")
            
            response = f"**Recent Solar Flare Activity:**\n\n"
            response += f"🌟 Most recent: **{class_type}** class flare\n"
            response += f"⏰ Peak time: {peak_time}\n"
            response += f"📊 Total flares in last 7 days: {len(flares)}\n\n"
            response += "Solar flares are classified as A, B, C, M, or X, with X being the most intense. "
            response += "They can affect GPS, communications, and power grids on Earth."
        else:
            response = "No significant solar flare activity detected in the past 7 days. "
            response += "The sun is relatively quiet at the moment."
        
        return ChatResponse(
            response=response,
            sources=["NASA DONKI"]
        )
    
    # Check if asking about CME
    elif any(word in message_lower for word in ["cme", "coronal mass ejection", "ejection"]):
        cme_events = await nasa_service.get_cme_events(days=7)
        
        if cme_events:
            recent_cme = cme_events[-1]
            speed = recent_cme.get("speed", "Unknown")
            start_time = recent_cme.get("startTime", "N/A")
            
            response = f"**Recent CME Activity:**\n\n"
            response += f"💥 Most recent CME detected\n"
            response += f"🚀 Speed: {speed} km/s\n"
            response += f"⏰ Start time: {start_time}\n"
            response += f"📊 Total CMEs in last 7 days: {len(cme_events)}\n\n"
            response += "Coronal Mass Ejections are large expulsions of plasma and magnetic field from the Sun. "
            response += "They can cause geomagnetic storms when directed at Earth."
        else:
            response = "No Coronal Mass Ejections detected in the past 7 days."
        
        return ChatResponse(
            response=response,
            sources=["NASA DONKI"]
        )
    
    # Check if asking about asteroids
    elif any(word in message_lower for word in ["asteroid", "neo", "near earth object"]):
        neos = await nasa_service.get_near_earth_objects(days=7)
        total_count = neos.get("element_count", 0)
        
        response = f"**Near Earth Objects (Asteroids):**\n\n"
        response += f"🪨 **{total_count}** near-Earth objects detected in the past week\n\n"
        
        if total_count > 0:
            response += "Most NEOs pass by Earth at safe distances. NASA tracks all objects that could "
            response += "potentially pose a threat. None of the currently tracked objects present an immediate danger."
        
        return ChatResponse(
            response=response,
            sources=["NASA NEO API"]
        )
    
    # Check if asking about radiation
    elif any(word in message_lower for word in ["radiation", "proton", "particle"]):
        radiation = await nasa_service.get_radiation_belt_enhancement(days=7)
        
        response = f"**Space Radiation Status:**\n\n"
        
        if radiation:
            response += f"⚡ {len(radiation)} radiation belt enhancement event(s) detected in the past week\n\n"
            response += "Radiation belt enhancements can pose risks to satellites and astronauts. "
            response += "These events are closely monitored for space operations."
        else:
            response += "No significant radiation belt enhancements detected in the past week. "
            response += "Radiation levels are within normal ranges."
        
        return ChatResponse(
            response=response,
            sources=["NASA DONKI"]
        )
    
    # Check if asking about satellites
    elif any(word in message_lower for word in ["satellite", "spacecraft", "threat"]):
        response = "**Satellite Threats from Space Weather:**\n\n"
        response += "🛰️ Space weather can affect satellites through:\n\n"
        response += "1. **Solar Flares:** Can damage electronics and solar panels\n"
        response += "2. **Geomagnetic Storms:** Affect satellite orbits and operations\n"
        response += "3. **Radiation Events:** Pose risks to satellite components\n\n"
        response += "Operators receive alerts to take protective measures when severe space weather is expected."
        
        return ChatResponse(
            response=response,
            sources=["General Space Weather Knowledge"]
        )
    
    # General space weather explanation
    else:
        response = "**Space Weather Overview:**\n\n"
        response += "I can help you understand space weather conditions and phenomena:\n\n"
        response += "🌟 **Solar Flares** - Intense bursts of radiation\n"
        response += "💥 **CME** - Coronal Mass Ejections\n"
        response += "🧲 **Geomagnetic Storms** - Disturbances in Earth's magnetic field\n"
        response += "⚡ **Radiation Events** - Energetic particle increases\n"
        response += "🪨 **Asteroids** - Near-Earth objects\n\n"
        response += "Ask me about current conditions, recent events, or specific phenomena!"
        
        return ChatResponse(
            response=response,
            sources=[]
        )

@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """Send a message to the space weather chatbot"""
    try:
        response = await generate_response(request.message, request.history)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@router.get("/health")
async def chat_health():
    """Check if chat service is operational"""
    return {
        "status": "operational",
        "message": "Space Weather Assistant is ready"
    }
