import httpx
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os

class NASAService:
    def __init__(self):
        self.api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")
        self.base_url = "https://api.nasa.gov"
        self.donki_url = f"{self.base_url}/DONKI"
        
    async def get_solar_flares(self, days: int = 7) -> List[Dict]:
        """Fetch recent solar flare events"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        url = f"{self.donki_url}/FLR"
        params = {
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "api_key": self.api_key
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Error fetching solar flares: {e}")
                return []
    
    async def get_cme_events(self, days: int = 7) -> List[Dict]:
        """Fetch Coronal Mass Ejection events"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        url = f"{self.donki_url}/CME"
        params = {
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "api_key": self.api_key
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Error fetching CME events: {e}")
                return []
    
    async def get_geomagnetic_storms(self, days: int = 7) -> List[Dict]:
        """Fetch geomagnetic storm events"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        url = f"{self.donki_url}/GST"
        params = {
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "api_key": self.api_key
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Error fetching geomagnetic storms: {e}")
                return []
    
    async def get_near_earth_objects(self, days: int = 7) -> Dict:
        """Fetch Near Earth Objects (asteroids)"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        url = f"{self.base_url}/neo/rest/v1/feed"
        params = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "api_key": self.api_key
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Error fetching NEOs: {e}")
                return {"near_earth_objects": {}}
    
    async def get_radiation_belt_enhancement(self, days: int = 7) -> List[Dict]:
        """Fetch radiation belt enhancement events"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        url = f"{self.donki_url}/RBE"
        params = {
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "api_key": self.api_key
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Error fetching radiation events: {e}")
                return []
