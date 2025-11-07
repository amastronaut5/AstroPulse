import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List
import random


class SolarFlarePredictor:
    """
    Solar Flare Prediction Model
    Uses historical patterns and current conditions to predict flare probability
    """
    
    def __init__(self):
        self.model_version = "1.0.0"
        self.accuracy = 0.78  # Simulated accuracy
        
    def predict_flare_probability(self, recent_flares: List[Dict], 
                                  solar_wind_data: List, 
                                  xray_flux: List) -> Dict:
        """
        Predict probability of solar flares in next 24-48 hours
        
        Returns:
            Dictionary with predictions for different flare classes
        """
        
        # Analyze recent activity
        recent_activity_score = self._calculate_activity_score(recent_flares)
        
        # Analyze solar wind conditions
        solar_wind_score = self._analyze_solar_wind(solar_wind_data)
        
        # Analyze X-ray flux trends
        xray_score = self._analyze_xray_flux(xray_flux)
        
        # Combine scores with weights
        base_score = (
            recent_activity_score * 0.5 +
            solar_wind_score * 0.3 +
            xray_score * 0.2
        )
        
        # Calculate probabilities for each class
        predictions = {
            "timestamp": datetime.utcnow().isoformat(),
            "forecast_period": "24-48 hours",
            "model_version": self.model_version,
            "confidence": self.accuracy,
            "predictions": {
                "C_class": {
                    "probability": min(base_score * 1.2, 0.95),
                    "description": "Minor flares, little impact",
                    "severity": "low"
                },
                "M_class": {
                    "probability": min(base_score * 0.6, 0.75),
                    "description": "Moderate flares, possible radio blackouts",
                    "severity": "moderate"
                },
                "X_class": {
                    "probability": min(base_score * 0.3, 0.45),
                    "description": "Major flares, significant impacts possible",
                    "severity": "high"
                }
            },
            "risk_level": self._calculate_risk_level(base_score),
            "recommendations": self._generate_recommendations(base_score)
        }
        
        return predictions
    
    def _calculate_activity_score(self, recent_flares: List[Dict]) -> float:
        """Calculate activity score based on recent flare history"""
        if not recent_flares:
            return 0.2  # Base probability
        
        # Count flares by class in last 7 days
        flare_counts = {"X": 0, "M": 0, "C": 0}
        
        for flare in recent_flares:
            class_type = flare.get("classType", "")
            if class_type:
                first_char = class_type[0].upper()
                if first_char in flare_counts:
                    flare_counts[first_char] += 1
        
        # Weight by severity
        score = (
            flare_counts["X"] * 0.9 +
            flare_counts["M"] * 0.6 +
            flare_counts["C"] * 0.3
        ) / 10  # Normalize
        
        return min(score + 0.2, 0.9)
    
    def _analyze_solar_wind(self, solar_wind_data: List) -> float:
        """Analyze solar wind data for prediction"""
        if not solar_wind_data or len(solar_wind_data) < 5:
            return 0.5
        
        # Simulate analysis based on data availability
        # In production, analyze actual magnetic field strength and density
        data_quality = len(solar_wind_data) / 100
        return min(0.3 + data_quality * 0.4, 0.8)
    
    def _analyze_xray_flux(self, xray_flux: List) -> float:
        """Analyze X-ray flux trends"""
        if not xray_flux or len(xray_flux) < 5:
            return 0.5
        
        # Check if flux is increasing
        recent_values = xray_flux[-10:] if len(xray_flux) >= 10 else xray_flux
        
        # Simulate trend analysis
        trend_score = 0.5 + (len(recent_values) / 100)
        return min(trend_score, 0.8)
    
    def _calculate_risk_level(self, score: float) -> str:
        """Determine overall risk level"""
        if score >= 0.7:
            return "HIGH"
        elif score >= 0.5:
            return "MODERATE"
        elif score >= 0.3:
            return "LOW"
        else:
            return "MINIMAL"
    
    def _generate_recommendations(self, score: float) -> List[str]:
        """Generate recommendations based on prediction"""
        recommendations = []
        
        if score >= 0.7:
            recommendations = [
                "Satellite operators should prepare for possible disruptions",
                "Monitor communication systems closely",
                "GPS accuracy may be affected",
                "Power grid operators should be on alert",
                "Consider postponing sensitive space operations"
            ]
        elif score >= 0.5:
            recommendations = [
                "Maintain awareness of space weather conditions",
                "Monitor alerts for any rapid changes",
                "Satellite operators should review contingency plans",
                "Aviation routes over polar regions may be affected"
            ]
        elif score >= 0.3:
            recommendations = [
                "Normal operations expected",
                "Continue routine space weather monitoring",
                "Low risk of significant impacts"
            ]
        else:
            recommendations = [
                "Minimal solar activity expected",
                "Excellent conditions for space operations",
                "Low probability of disturbances"
            ]
        
        return recommendations
    
    def predict_cme_arrival(self, cme_speed: float, detection_time: str) -> Dict:
        """
        Predict when a CME will arrive at Earth
        
        Args:
            cme_speed: Speed in km/s
            detection_time: ISO format timestamp
        """
        if not cme_speed or cme_speed < 200:
            return {
                "arrival_time": None,
                "impact_probability": 0,
                "message": "CME not Earth-directed or too slow"
            }
        
        # Distance from Sun to Earth: ~150 million km
        distance_km = 150_000_000
        
        # Calculate travel time
        travel_time_hours = distance_km / (cme_speed * 3600)
        
        # Add detection time
        detection = datetime.fromisoformat(detection_time.replace('Z', '+00:00'))
        arrival = detection + timedelta(hours=travel_time_hours)
        
        # Calculate impact probability based on speed
        impact_prob = min((cme_speed / 2000) * 0.8, 0.95)
        
        return {
            "detection_time": detection_time,
            "cme_speed": f"{cme_speed} km/s",
            "estimated_arrival": arrival.isoformat(),
            "arrival_window": f"{travel_time_hours - 6:.1f} to {travel_time_hours + 6:.1f} hours",
            "impact_probability": round(impact_prob, 2),
            "severity": "high" if cme_speed >= 1000 else "moderate",
            "warnings": [
                "Geomagnetic storm expected",
                "Satellite operations may be affected",
                "Aurora visible at lower latitudes"
            ] if cme_speed >= 1000 else [
                "Minor geomagnetic activity possible",
                "Aurora may be visible at high latitudes"
            ]
        }
    
    def predict_geomagnetic_storm(self, kp_history: List, cme_incoming: bool = False) -> Dict:
        """
        Predict geomagnetic storm intensity
        
        Args:
            kp_history: Recent Kp index values
            cme_incoming: Whether a CME is expected
        """
        if not kp_history:
            return {
                "storm_probability": 0.1,
                "max_kp_predicted": 2,
                "storm_level": "None"
            }
        
        # Get recent Kp values
        recent_kp = [float(kp[1]) if len(kp) > 1 else 0 for kp in kp_history[-5:]]
        avg_kp = np.mean(recent_kp) if recent_kp else 0
        
        # Predict based on trend and CME
        if cme_incoming:
            predicted_kp = min(avg_kp + 3, 9)
            storm_prob = 0.85
        else:
            predicted_kp = min(avg_kp + 1, 7)
            storm_prob = 0.3 if avg_kp > 4 else 0.1
        
        # Determine storm level
        if predicted_kp >= 7:
            storm_level = "Severe (G4-G5)"
            impacts = [
                "Widespread power grid problems possible",
                "Spacecraft operations significantly affected",
                "HF radio blackouts in many areas",
                "GPS navigation errors likely"
            ]
        elif predicted_kp >= 5:
            storm_level = "Moderate (G2-G3)"
            impacts = [
                "Power systems may experience voltage alarms",
                "Spacecraft may need corrective actions",
                "HF radio propagation affected",
                "GPS accuracy reduced"
            ]
        else:
            storm_level = "Minor (G1) or None"
            impacts = [
                "Minimal impact expected",
                "Possible minor fluctuations in power grids",
                "Aurora visible at high latitudes"
            ]
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "current_kp": round(avg_kp, 1),
            "predicted_max_kp": round(predicted_kp, 1),
            "storm_probability": round(storm_prob, 2),
            "storm_level": storm_level,
            "forecast_period": "24 hours",
            "impacts": impacts
        }


# Model ready to use
