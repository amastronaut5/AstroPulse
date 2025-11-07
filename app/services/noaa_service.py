import httpx
from typing import Dict, List
from datetime import datetime

class NOAAService:
    def __init__(self):
        self.base_url = "https://services.swpc.noaa.gov"
        
    async def get_solar_wind(self) -> List[Dict]:
        """Get real-time solar wind data"""
        url = f"{self.base_url}/products/solar-wind/mag-7-day.json"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                # Skip header row
                return data[1:] if data else []
            except Exception as e:
                print(f"Error fetching solar wind: {e}")
                return []
    
    async def get_kp_index(self) -> List[Dict]:
        """Get Kp index (geomagnetic activity)"""
        url = f"{self.base_url}/products/noaa-planetary-k-index.json"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                return data[1:] if data else []
            except Exception as e:
                print(f"Error fetching Kp index: {e}")
                return []
    
    async def get_xray_flares(self) -> List[Dict]:
        """Get X-ray flux data"""
        url = f"{self.base_url}/products/goes-xray-flux-primary.json"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                return data[1:] if data else []
            except Exception as e:
                print(f"Error fetching X-ray flux: {e}")
                return []
    
    async def get_proton_flux(self) -> List[Dict]:
        """Get proton flux data"""
        url = f"{self.base_url}/products/goes-proton-flux-primary.json"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                return data[1:] if data else []
            except Exception as e:
                print(f"Error fetching proton flux: {e}")
                return []
    
    async def get_current_conditions(self) -> Dict:
        """Get comprehensive current space weather conditions"""
        solar_wind = await self.get_solar_wind()
        kp_index = await self.get_kp_index()
        xray_flares = await self.get_xray_flares()
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "solar_wind": solar_wind[-10:] if solar_wind else [],
            "kp_index": kp_index[-10:] if kp_index else [],
            "xray_flux": xray_flares[-10:] if xray_flares else []
        }
