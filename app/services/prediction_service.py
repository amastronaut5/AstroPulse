from app.ml.solar_flare_predictor import SolarFlarePredictor
from app.ml.radiation_predictor import RadiationPredictor
from typing import Dict

class PredictionService:
    """
    Coordinates all prediction models
    """
    
    def __init__(self):
        self.flare_predictor = SolarFlarePredictor()
        self.radiation_predictor = RadiationPredictor()
    
    async def get_comprehensive_predictions(self, 
                                           recent_flares: list,
                                           cme_events: list,
                                           solar_wind: list,
                                           xray_flux: list,
                                           kp_index: list) -> Dict:
        """
        Get comprehensive predictions from all models
        """
        
        # Solar flare predictions
        flare_predictions = self.flare_predictor.predict_flare_probability(
            recent_flares=recent_flares,
            solar_wind_data=solar_wind,
            xray_flux=xray_flux
        )
        
        # Geomagnetic storm predictions
        has_fast_cme = any(
            float(cme.get("speed", 0)) > 1000 
            for cme in cme_events 
            if cme.get("speed")
        )
        
        geomag_predictions = self.flare_predictor.predict_geomagnetic_storm(
            kp_history=kp_index,
            cme_incoming=has_fast_cme
        )
        
        # Radiation storm predictions
        radiation_predictions = self.radiation_predictor.predict_radiation_storm(
            recent_flares=recent_flares
        )
        
        # CME arrival predictions (for most recent fast CME)
        cme_arrival = None
        if cme_events:
            fast_cmes = [
                cme for cme in cme_events 
                if cme.get("speed") and float(cme.get("speed", 0)) > 500
            ]
            if fast_cmes:
                latest_cme = fast_cmes[-1]
                cme_arrival = self.flare_predictor.predict_cme_arrival(
                    cme_speed=float(latest_cme.get("speed", 0)),
                    detection_time=latest_cme.get("startTime", "")
                )
        
        return {
            "status": "success",
            "generated_at": flare_predictions["timestamp"],
            "predictions": {
                "solar_flares": flare_predictions,
                "geomagnetic_storm": geomag_predictions,
                "radiation_storm": radiation_predictions,
                "cme_arrival": cme_arrival
            },
            "overall_risk_assessment": self._calculate_overall_risk(
                flare_predictions,
                geomag_predictions,
                radiation_predictions
            )
        }
    
    def _calculate_overall_risk(self, flare_pred: Dict, geomag_pred: Dict, rad_pred: Dict) -> Dict:
        """Calculate overall space weather risk"""
        
        # Weight different risks
        flare_risk = self._risk_to_score(flare_pred.get("risk_level", "LOW"))
        geomag_risk = geomag_pred.get("storm_probability", 0)
        rad_risk = rad_pred.get("radiation_storm_probability", 0)
        
        overall_score = (flare_risk * 0.4 + geomag_risk * 0.35 + rad_risk * 0.25)
        
        if overall_score >= 0.7:
            level = "HIGH"
            color = "red"
            message = "Significant space weather activity expected"
        elif overall_score >= 0.5:
            level = "ELEVATED"
            color = "orange"
            message = "Moderate space weather activity possible"
        elif overall_score >= 0.3:
            level = "MODERATE"
            color = "yellow"
            message = "Minor space weather activity possible"
        else:
            level = "LOW"
            color = "green"
            message = "Quiet space weather conditions expected"
        
        return {
            "risk_level": level,
            "risk_score": round(overall_score, 2),
            "color": color,
            "message": message,
            "primary_concerns": self._get_primary_concerns(flare_pred, geomag_pred, rad_pred)
        }
    
    def _risk_to_score(self, risk_level: str) -> float:
        """Convert risk level to numerical score"""
        mapping = {
            "HIGH": 0.85,
            "MODERATE": 0.6,
            "LOW": 0.3,
            "MINIMAL": 0.1
        }
        return mapping.get(risk_level, 0.3)
    
    def _get_primary_concerns(self, flare_pred: Dict, geomag_pred: Dict, rad_pred: Dict) -> list:
        """Identify primary concerns"""
        concerns = []
        
        if flare_pred.get("risk_level") in ["HIGH", "MODERATE"]:
            concerns.append("Solar flare activity")
        
        if geomag_pred.get("storm_probability", 0) > 0.5:
            concerns.append("Geomagnetic disturbances")
        
        if rad_pred.get("radiation_storm_probability", 0) > 0.5:
            concerns.append("Radiation hazards")
        
        if not concerns:
            concerns.append("No significant concerns")
        
        return concerns
