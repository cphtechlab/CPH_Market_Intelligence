import httpx
import logging
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

class NationalbankenClient:
    def __init__(self):
        self.url = "https://www.nationalbanken.dk/api/currencyratesxml?lang=en"

    async def get_exchange_rates(self):
        """
        Henter officielle valutakurser fra Danmarks Nationalbank.
        Returnerer vasket JSON i stedet for deres XML.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.url)
                response.raise_for_status()
                
                # Fjern eventuel BOM (Byte Order Mark) fra XML stringen for at undgå parsing fejl
                xml_content = response.text.lstrip('\ufeff')
                root = ET.fromstring(xml_content)
                
                rates = []
                date_str = ""
                
                # Nationalbankens XML struktur: <exchangerates><dailyrates id="YYYY-MM-DD"><currency .../></dailyrates></exchangerates>
                for daily_rates in root.findall('dailyrates'):
                    date_str = daily_rates.attrib.get('id', '')
                    for currency in daily_rates.findall('currency'):
                        rate_val = currency.attrib.get('rate')
                        parsed_rate = float(rate_val) if rate_val and rate_val != '-' else None
                        
                        rates.append({
                            "code": currency.attrib.get('code'),
                            "description": currency.attrib.get('desc'),
                            "rate_dkk_per_100": parsed_rate
                        })
                
                return {
                    "source": "Danmarks Nationalbank",
                    "date": date_str,
                    "count": len(rates),
                    "results": rates
                }
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTPStatusError from Nationalbanken: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Error parsing Nationalbanken XML: {e}")
                raise

nationalbanken_client = NationalbankenClient()
