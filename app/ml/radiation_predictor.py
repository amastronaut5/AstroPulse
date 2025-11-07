import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List

class RadiationPredictor:
    """
    Space Radiation Prediction Model
    Predicts solar energetic particle events and radiation storms
    """
    
    def __init__(self):
        self.model_version = "1.0.0"
        
    def predict_radiation_storm(self, 
                               recent_flares: List[Dict],
                               proton_flux: List = None) -> Dict:
        """
        Predict solar radiation storm probability
        
        Returns:
            Prediction dictionary with S-scale rating
        """
        
        # Analyze recent X-class and M-class flares
        high_energy_flares = [
            f for f in recent_flares 
            if f.get("classType", "").startswith(("X", "M"))
        ]
        
        # Calculate base probability
        base_prob = min(len(high_energy_flares) * 0.2, 0.9)
        
        # Determine S-scale (S1-S5)
        if len(high_energy_flares) >= 3:
            s_scale = "S3-S4"
            severity = "Strong"
            prob = min(base_prob * 1.2, 0.85)
        elif len(high_energy_flares) >= 1:
            s_scale = "S1-S2"
            severity = "Moderate"
            prob = base_prob
        else:
            s_scale = "Below S1"
            severity = "Minor"
            prob = 0.15
        
        # Generate impacts
        impacts = self._get_radiation_impacts(s_scale)
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "forecast_period": "24-72 hours",
            "radiation_storm_probability": round(prob, 2),
            "predicted_scale": s_scale,
            "severity": severity,
            "confidence": 0.72,
            "impacts": impacts,
            "affected_regions": self._get_affected_regions(s_scale),
            "recommendations": self._get_radiation_recommendations(s_scale)
        }
    
    def _get_radiation_impacts(self, s_scale: str) -> List[str]:
        """Get impacts based on S-scale"""
        if "S3" in s_scale or "S4" in s_scale:
            return [
                "Radiation hazard to astronauts on EVA",
                "Satellite operations degraded",
                "HF radio blackouts on sunlit side",
                "Navigation system errors",
                "Increased radiation dose to airline passengers"
            ]
        elif "S1" in s_scale or "S2" in s_scale:
            return [
                "Minor impacts to satellite operations",
                "Small effects on HF radio in polar regions",
                "Elevated radiation levels for astronauts",
                "Minimal impact to aviation"
            ]
        else:
            return [
                "Normal background radiation levels",
                "No significant impacts expected"
            ]
    
    def _get_affected_regions(self, s_scale: str) -> List[str]:
        """Get affected geographical regions"""
        if "S3" in s_scale or "S4" in s_scale:
            return ["Polar regions", "High-latitude areas", "Global HF communications"]
        elif "S1" in s_scale or "S2" in s_scale:
            return ["Polar regions", "High-latitude areas"]
        else:
            return ["None"]
    
    def _get_radiation_recommendations(self, s_scale: str) -> List[str]:
        """Get safety recommendations"""
        if "S3" in s_scale or "S4" in s_scale:
            return [
                "Postpone spacewalks if possible",
                "Satellite operators: implement mitigation procedures",
                "Airlines: consider re-routing polar flights",
                "Increased monitoring of radiation levels"
            ]
        elif "S1" in s_scale or "S2" in s_scale:
            return [
                "Monitor radiation levels",
                "Limit EVA duration if possible",
                "Standard satellite protection adequate"
            ]
        else:
            return [
                "Normal operations",
                "Standard radiation monitoring"
            ]
    
    def predict_proton_flux(self, current_flux: float = 1.0) -> Dict:
        """
        Predict proton flux levels
        
        Args:
            current_flux: Current proton flux in particles/(cm²·s·sr)
        """
        
        # Simulate prediction based on current levels
        if current_flux > 1000:
            predicted_flux = current_flux * 1.2
            trend = "increasing"
        elif current_flux > 100:
            predicted_flux = current_flux * 1.1
            trend = "stable"
        else:
            predicted_flux = current_flux * 0.9
            trend = "decreasing"
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "current_flux": f"{current_flux:.2e}",
            "predicted_flux_6h": f"{predicted_flux:.2e}",
            "trend": trend,
            "alert_level": self._get_proton_alert_level(predicted_flux)
        }
    
    def _get_proton_alert_level(self, flux: float) -> str:
        """Determine alert level based on proton flux"""
        if flux >= 10000:
            return "S3 - Strong"
        elif flux >= 1000:
            return "S2 - Moderate"
        elif flux >= 10:
            return "S1 - Minor"
        else:
            return "Normal"
