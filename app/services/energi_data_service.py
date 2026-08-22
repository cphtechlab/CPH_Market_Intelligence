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

    async def get_realtime_grid_mix(self):
        """
        Henter det øjeblikkelige grønne elnet-mix (Wind, Solar, Coal, etc.)
        fra PowerSystemRightNow datasættet.
        """
        url = f"{self.base_url}/PowerSystemRightNow"
        params = {"limit": 1} # Vi skal kun bruge den allernyeste 5-minutters måling

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                return self._format_grid_mix(data)
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTPStatusError fra Energi Data Service (Grid Mix): {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Fejl ved hentning af grid mix: {e}")
                raise

    def _format_grid_mix(self, raw_data):
        records = raw_data.get("records", [])
        if not records:
            return {"found": False, "message": "Ingen live målinger tilgængelige."}

        item = records[0]
        
        # Hent rå værdier i MW
        solar = item.get("SolarPower", 0.0) or 0.0
        offshore_wind = item.get("OffshoreWindPower", 0.0) or 0.0
        onshore_wind = item.get("OnshoreWindPower", 0.0) or 0.0
        thermal_large = item.get("ProductionGe100MW", 0.0) or 0.0 # Centrale kul/gas værker
        thermal_small = item.get("ProductionLt100MW", 0.0) or 0.0 # Decentrale biomasse/affalds-værker
        
        # Samlet produktion i Danmark lige nu (MW)
        total_generation = solar + offshore_wind + onshore_wind + thermal_large + thermal_small
        
        if total_generation > 0:
            solar_pct = round((solar / total_generation) * 100, 2)
            offshore_wind_pct = round((offshore_wind / total_generation) * 100, 2)
            onshore_wind_pct = round((onshore_wind / total_generation) * 100, 2)
            total_wind_pct = round(offshore_wind_pct + onshore_wind_pct, 2)
            thermal_large_pct = round((thermal_large / total_generation) * 100, 2)
            thermal_small_pct = round((thermal_small / total_generation) * 100, 2)
        else:
            solar_pct = offshore_wind_pct = onshore_wind_pct = total_wind_pct = thermal_large_pct = thermal_small_pct = 0.0
            
        # Grøn andel: Vind, sol samt 70% af de små decentrale værker (hvilket er standardestimat for biomasse/affald i DK)
        green_share_pct = round(solar_pct + total_wind_pct + (thermal_small_pct * 0.7), 2)
        if green_share_pct > 100.0:
            green_share_pct = 100.0

        return {
            "source": "Energinet / Energi Data Service (PowerSystemRightNow)",
            "timestamp_dk": item.get("Minutes1DK"),
            "timestamp_utc": item.get("Minutes1UTC"),
            "carbon_intensity_g_kwh": item.get("CO2Emission", 0.0),
            "total_generation_mw": round(total_generation, 2),
            "generation_mix_mw": {
                "solar": round(solar, 2),
                "onshore_wind": round(onshore_wind, 2),
                "offshore_wind": round(offshore_wind, 2),
                "thermal_large_mw": round(thermal_large, 2),
                "thermal_small_mw": round(thermal_small, 2)
            },
            "generation_mix_pct": {
                "solar_pct": solar_pct,
                "wind_total_pct": total_wind_pct,
                "wind_onshore_pct": onshore_wind_pct,
                "wind_offshore_pct": offshore_wind_pct,
                "fossil_and_other_pct": thermal_large_pct,
                "biomass_and_waste_pct": thermal_small_pct
            },
            "green_energy_share_pct": green_share_pct
        }

energi_data_client = EnergiDataClient()

