"""
ML Prediction Service - Integrates all ML models
Supports multiple backends: sklearn, transformers, Ollama
"""

from app.ml.advanced_solar_flare_model import ml_predictor
from app.ml.transformer_predictor import transformer_predictor
from app.ml.radiation_predictor import RadiationPredictor
from typing import Dict, List

class MLPredictionService:
    """
    Unified ML prediction service
    Automatically uses best available model based on installed dependencies
    """
    
    def __init__(self):
        self.advanced_model = ml_predictor
        self.transformer_model = transformer_predictor
        self.radiation_model = RadiationPredictor()
        
        # Detect capabilities
        self.capabilities = {
            "advanced_ml": True,  # sklearn-based
            "transformers": transformer_predictor.use_transformers,
            "ollama": transformer_predictor.use_ollama
        }
        
        print(f"ML Service initialized with capabilities: {self.capabilities}")
    
    async def get_ml_predictions(self,
                                 recent_flares: List[Dict],
                                 cme_events: List[Dict],
                                 solar_wind: List,
                                 xray_flux: List,
                                 kp_index: List) -> Dict:
        """
        Get predictions from best available ML model
        """
        
        # Use advanced sklearn model (always available)
        primary_prediction = self.advanced_model.predict(
            recent_flares=recent_flares,
            solar_wind=solar_wind,
            xray_flux=xray_flux
        )
        
        # Enhance with transformer if available
        if self.capabilities["transformers"]:
            context = f"Recent activity: {len(recent_flares)} flares, {len(cme_events)} CMEs"
            enhanced = self.transformer_model.predict_with_context(
                recent_flares=recent_flares,
                solar_wind=solar_wind,
                xray_flux=xray_flux,
                context=context
            )
            
            # Merge insights
            primary_prediction['transformer_enhancement'] = True
            if 'ai_insights' in enhanced:
                primary_prediction['ai_insights'] = enhanced['ai_insights']
        
        # Add radiation predictions
        radiation_pred = self.radiation_model.predict_radiation_storm(recent_flares)
        
        return {
            "status": "success",
            "generated_at": primary_prediction["timestamp"],
            "model_info": {
                "primary_model": primary_prediction["model_type"],
                "version": primary_prediction["model_version"],
                "capabilities": self.capabilities
            },
            "solar_flare_prediction": primary_prediction,
            "radiation_prediction": radiation_pred,
            "data_quality": self._assess_data_quality(recent_flares, solar_wind, xray_flux)
        }
    
    def _assess_data_quality(self, flares: List, wind: List, xray: List) -> Dict:
        """Assess quality of input data"""
        
        quality_score = 0
        
        if len(flares) >= 5:
            quality_score += 0.4
        elif len(flares) >= 2:
            quality_score += 0.2
        
        if len(wind) >= 10:
            quality_score += 0.3
        elif len(wind) >= 5:
            quality_score += 0.15
        
        if len(xray) >= 10:
            quality_score += 0.3
        elif len(xray) >= 5:
            quality_score += 0.15
        
        if quality_score >= 0.8:
            quality = "Excellent"
        elif quality_score >= 0.6:
            quality = "Good"
        elif quality_score >= 0.4:
            quality = "Fair"
        else:
            quality = "Limited"
        
        return {
            "score": round(quality_score, 2),
            "rating": quality,
            "data_points": {
                "flares": len(flares),
                "solar_wind": len(wind),
                "xray_flux": len(xray)
            }
        }

# Global service instance
ml_service = MLPredictionService()
