import httpx
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class DatafordelerClient:
    def __init__(self):
        # DAWA (Danmarks Adressers Web API) er Datafordelerens specifikke endpoint 
        # til lynhurtig fritekstsøgning/autocomplete af adresser.
        self.base_url = "https://api.dataforsyningen.dk/adresser"

    async def validate_address(self, query: str):
        params = {
            "q": query,
            "per_side": 10 # Vi henter max 10 resultater for at holde det lynhurtigt
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
                return self._format_dar_response(data)
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTPStatusError from DAWA: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Error fetching data from DAWA: {e}")
                raise

    def _format_dar_response(self, raw_data):
        formatted_addresses = []
        if isinstance(raw_data, list):
            for item in raw_data:
                # DAWA leverer meget data, vi "vasker" det til et rent format for vores kunder
                formatted = {
                    "id": item.get("id", ""),
                    "betegnelse": item.get("adressebetegnelse", ""),
                    "vejnavn": item.get("adgangsadresse", {}).get("vejstykke", {}).get("navn", ""),
                    "husnummer": item.get("adgangsadresse", {}).get("husnr", ""),
                    "postnummer": item.get("adgangsadresse", {}).get("postnummer", {}).get("nr", ""),
                    "postnummernavn": item.get("adgangsadresse", {}).get("postnummer", {}).get("navn", ""),
                    "kommunekode": item.get("adgangsadresse", {}).get("kommune", {}).get("kode", ""),
                    "kommunenavn": item.get("adgangsadresse", {}).get("kommune", {}).get("navn", ""),
                    "koordinater": item.get("adgangsadresse", {}).get("adgangspunkt", {}).get("koordinater", [])
                }
                formatted_addresses.append(formatted)
        
        return {
            "count": len(formatted_addresses),
            "results": formatted_addresses
        }

    async def reverse_geocode(self, lat: float, lon: float):
        url = "https://api.dataforsyningen.dk/adgangsadresser/reverse"
        params = {"x": lon, "y": lat} # DAWA bruger x for længdegrad (lon) og y for breddegrad (lat)

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                if response.status_code == 404:
                    return {"found": False, "message": "Ingen adresse fundet tæt på disse koordinater."}
                response.raise_for_status()
                data = response.json()
                
                # "Vaskning" af data
                return {
                    "found": True,
                    "adressebetegnelse": data.get("adressebetegnelse", ""),
                    "vejnavn": data.get("vejstykke", {}).get("navn", ""),
                    "husnummer": data.get("husnr", ""),
                    "postnummer": data.get("postnummer", {}).get("nr", ""),
                    "postnummernavn": data.get("postnummer", {}).get("navn", ""),
                    "kommunekode": data.get("kommune", {}).get("kode", ""),
                    "kommunenavn": data.get("kommune", {}).get("navn", "")
                }
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTPStatusError from DAWA reverse: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Error fetching data from DAWA reverse: {e}")
                raise

    async def get_postal_info(self, zipcode: str):
        url = f"https://api.dataforsyningen.dk/postnumre/{zipcode}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                if response.status_code == 404:
                    return {"found": False, "message": f"Postnummer {zipcode} ikke fundet."}
                response.raise_for_status()
                data = response.json()
                
                # "Vaskning"
                kommuner = [{"kode": k.get("kode"), "navn": k.get("navn")} for k in data.get("kommuner", [])]
                
                return {
                    "found": True,
                    "postnummer": data.get("nr", ""),
                    "navn": data.get("navn", ""),
                    "kommuner": kommuner,
                    "bbox": data.get("visueltcenter", []) # Visuelt center eller bbox hvis tilgængeligt
                }
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTPStatusError from DAWA postnummer: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Error fetching data from DAWA postnummer: {e}")
                raise

datafordeler_client = DatafordelerClient()
