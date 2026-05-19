import httpx
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class EnergiDataClient:
    def __init__(self):
        self.base_url = "https://api.energidataservice.dk/dataset"

    async def get_spot_prices(self, price_area: str = "DK1", hours: int = 24):
        """
        Henter el-spotpriser fra DayAheadPrices datasættet.
        Vasker data og returnerer en simpel liste med tid og pris.
        """
        url = f"{self.base_url}/DayAheadPrices"
        
        # Sørger for at PriceArea er uppercase (DK1 eller DK2)
        price_area = price_area.upper()
        if price_area not in ["DK1", "DK2"]:
            price_area = "DK1"

        params = {
            "filter": '{"PriceArea":"' + price_area + '"}',
            "sort": "TimeUTC desc",
            "limit": hours
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                return self._format_spot_prices(data, price_area)
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTPStatusError fra Energi Data Service (Priser): {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Fejl ved hentning af elpriser: {e}")
                raise

    async def get_co2_emissions(self, price_area: str = "DK1", hours: int = 24):
        """
        Henter CO2-udledning (gram pr. kWh) fra CO2Emis.
        """
        url = f"{self.base_url}/CO2Emis"
        
        price_area = price_area.upper()
        if price_area not in ["DK1", "DK2"]:
            price_area = "DK1"

        params = {
            "filter": '{"PriceArea":"' + price_area + '"}',
            "limit": hours * 12 # Data kommer typisk pr. 5 min. 12 x 5 min = 1 time
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                return self._format_co2_data(data, price_area)
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTPStatusError fra Energi Data Service (CO2): {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Fejl ved hentning af CO2 data: {e}")
                raise

    def _format_spot_prices(self, raw_data, price_area):
        """ Vasker elpris data til 'Plug & Play' """
        formatted_prices = []
        records = raw_data.get("records", [])
        
        for item in records:
            formatted = {
                "time_utc": item.get("TimeUTC"),
                "time_dk": item.get("TimeDK"),
                "price_dkk_mwh": item.get("DayAheadPriceDKK"),
                "price_eur_mwh": item.get("DayAheadPriceEUR"),
                # Udregn en letforståelig kwh pris i øre til B2C brug / simpel AI tolkning
                "price_dkk_kwh": round(item.get("DayAheadPriceDKK", 0) / 1000, 4) if item.get("DayAheadPriceDKK") else None
            }
            formatted_prices.append(formatted)

        return {
            "source": "Energinet / Energi Data Service",
            "price_area": price_area,
            "currency": "DKK",
            "count": len(formatted_prices),
            "results": formatted_prices
        }

    def _format_co2_data(self, raw_data, price_area):
        """ Vasker CO2 data """
        formatted_co2 = []
        records = raw_data.get("records", [])
        
        for item in records:
            formatted = {
                "time_utc": item.get("Minutes5UTC"),
                "time_dk": item.get("Minutes5DK"),
                "co2_emission_g_kwh": item.get("CO2Emission") # Gram CO2 pr. kWh
            }
            formatted_co2.append(formatted)

        return {
            "source": "Energinet / Energi Data Service",
            "price_area": price_area,
            "unit": "g/kWh",
            "count": len(formatted_co2),
            "results": formatted_co2
        }

energi_data_client = EnergiDataClient()
