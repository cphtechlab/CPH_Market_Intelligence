import httpx
import logging
import asyncio
import xml.etree.ElementTree as ET
from io import BytesIO

logger = logging.getLogger(__name__)

class SmileyService:
    def __init__(self):
        self.url = "https://www.foedevarestyrelsen.dk/Media/638212360788086849/Smiley_xml.xml"
        self._cache_by_cvr = {}
        self._cache_by_name = []
        self._is_loaded = False
        self._lock = asyncio.Lock()

    async def _load_data_if_needed(self):
        if self._is_loaded:
            return

        async with self._lock:
            # Dobbelt-tjek inde i låsen
            if self._is_loaded:
                return
                
            logger.info("Henter og cacher Fødevarestyrelsens Smiley XML...")
            async with httpx.AsyncClient(follow_redirects=True, timeout=60.0) as client:
                try:
                    response = await client.get(self.url)
                    response.raise_for_status()
                    
                    # Fjern BOM, hvis det findes, og brug BytesIO til iterparse for at spare memory
                    content = response.text.lstrip('\ufeff').encode('utf-8')
                    
                    # Nulstil cache
                    self._cache_by_cvr = {}
                    self._cache_by_name = []
                    
                    # Brug iterparse for memory-effektiv XML parsing
                    for event, elem in ET.iterparse(BytesIO(content), events=('end',)):
                        if elem.tag == 'row':
                            cvr = elem.findtext('cvrnr')
                            navn = elem.findtext('navn1')
                            
                            if cvr and navn:
                                restaurant = {
                                    "cvr": cvr,
                                    "name": navn,
                                    "address": elem.findtext('adresse1'),
                                    "zipcode": elem.findtext('postnr'),
                                    "city": elem.findtext('by'),
                                    "latest_rating": elem.findtext('seneste_kontrol'),
                                    "latest_date": elem.findtext('seneste_kontrol_dato'),
                                    "url": elem.findtext('URL')
                                }
                                
                                # Gem i CVR dictionary for O(1) opslag (en virksomhed kan have flere p-numre, vi gemmer som liste)
                                if cvr not in self._cache_by_cvr:
                                    self._cache_by_cvr[cvr] = []
                                self._cache_by_cvr[cvr].append(restaurant)
                                
                                # Gem i Name liste for tekst-søgning
                                self._cache_by_name.append(restaurant)
                                
                            # Frigør hukommelse for det aktuelle element
                            elem.clear()
                            
                    self._is_loaded = True
                    logger.info(f"Smiley XML cachet! {len(self._cache_by_name)} rækker indlæst.")
                    
                except Exception as e:
                    logger.error(f"Fejl ved indlæsning af Smiley XML: {e}")
                    raise

    async def search_by_cvr(self, cvr: str):
        await self._load_data_if_needed()
        return self._cache_by_cvr.get(cvr, [])

    async def search_by_name(self, name: str, limit: int = 10):
        await self._load_data_if_needed()
        search_term = name.lower()
        results = []
        for r in self._cache_by_name:
            if search_term in r['name'].lower():
                results.append(r)
                if len(results) >= limit:
                    break
        return results

smiley_service = SmileyService()
