import httpx
import logging

logger = logging.getLogger(__name__)

class DSTClient:
    def __init__(self):
        self.base_url = "https://api.statbank.dk/v1/data"

    async def get_cpi(self):
        """
        Henter det årlige Forbrugerprisindeks (Inflation) fra Danmarks Statistik (Tabel: PRIS112).
        Vasker 'JSON-stat' formatet ned til en simpel liste af årstal og indeks-værdier.
        """
        payload = {
            "table": "PRIS112",
            "format": "JSONSTAT",
            "valuePresentation": "Value",
            "variables": [
                {"code": "HOVED", "values": ["1005"]}, # 1005 = Årsgennemsnit
                {"code": "Tid", "values": ["*"]}
            ]
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.base_url, json=payload)
                response.raise_for_status()
                data = response.json()
                
                # Udpak JSON-stat struktur
                # data['dataset']['dimension']['Tid']['category']['index'] indeholder en mapping fra årstal til et array-index
                # data['dataset']['value'] er en liste af de faktiske værdier baseret på array-indexet
                
                years_dict = data['dataset']['dimension']['Tid']['category']['index']
                values_list = data['dataset']['value']
                
                results = []
                for year, index in years_dict.items():
                    # Undgå None værdier, hvis der mangler data for et specifikt år
                    val = values_list[index]
                    if val is not None:
                        results.append({
                            "year": year,
                            "cpi": float(val)
                        })
                
                # Sorter så de nyeste år kommer først
                results.sort(key=lambda x: x["year"], reverse=True)
                
                return {
                    "source": "Danmarks Statistik",
                    "table": "PRIS112",
                    "description": "Forbrugerprisindeks (Årsgennemsnit)",
                    "results": results
                }
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTPStatusError from DST: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Error fetching from DST: {e}")
                raise

dst_client = DSTClient()
