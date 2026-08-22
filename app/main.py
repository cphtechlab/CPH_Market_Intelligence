from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.services.datafordeler import datafordeler_client
from app.services.energi_data_service import energi_data_client
from app.services.nationalbanken import nationalbanken_client
from app.services.dst import dst_client
from app.services.holidays_service import holidays_service
from app.services.smiley_service import smiley_service
from app.services.cvr_service import cvr_service
from app.services.signatory_service import signatory_service
from app.services.alert_service import alert_service
import httpx

app = FastAPI(
    title="CPH Market Intelligence API",
    description="Backend API for RapidAPI, som proxy for danske offentlige data (Datafordeleren, Energi Data, CVR, DST, Nationalbanken m.fl.).",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to CPH Market Intelligence API. Go to /docs for documentation."}

@app.get("/api/v1/address/validate")
async def validate_address(q: str):
    """
    Validerer og søger en dansk adresse via DAR.
    """
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required.")
    
    try:
        results = await datafordeler_client.validate_address(query=q)
        return results
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Datafordeler error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/energy/prices")
async def get_energy_prices(area: str = "DK1", hours: int = 24):
    """
    Henter el-spotpriser fra Energi Data Service.
    area: 'DK1' (Vestdanmark) eller 'DK2' (Østdanmark).
    """
    try:
        results = await energi_data_client.get_spot_prices(price_area=area, hours=hours)
        return results
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Energi Data Service error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/energy/co2")
async def get_co2_emissions(area: str = "DK1", hours: int = 24):
    """
    Henter CO2-udledning fra Energi Data Service.
    area: 'DK1' eller 'DK2'.
    """
    try:
        results = await energi_data_client.get_co2_emissions(price_area=area, hours=hours)
        return results
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Energi Data Service error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/address/reverse")
async def reverse_geocode_address(lat: float, lon: float):
    """
    Finder den nærmeste danske adresse ud fra GPS-koordinater.
    Perfekt til logistik, kurer og taxa-apps.
    """
    try:
        results = await datafordeler_client.reverse_geocode(lat=lat, lon=lon)
        return results
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Datafordeler error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/postal/{zipcode}")
async def get_postal_info(zipcode: str):
    """
    Validerer et dansk postnummer og returnerer information om bl.a. kommuner.
    """
    try:
        results = await datafordeler_client.get_postal_info(zipcode=zipcode)
        return results
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Datafordeler error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/finance/exchange-rates")
async def get_exchange_rates():
    """
    Henter daglige valutakurser fra Danmarks Nationalbank.
    """
    try:
        results = await nationalbanken_client.get_exchange_rates()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/finance/cpi")
async def get_cpi():
    """
    Henter Forbrugerprisindekset (Inflation) fra Danmarks Statistik.
    """
    try:
        results = await dst_client.get_cpi()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/calendar/holidays")
def get_holidays(year: int = 2024):
    """
    Henter danske officielle banklukkedage og helligdage.
    """
    try:
        results = holidays_service.get_holidays(year=year)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/food/smiley")
async def search_smiley(cvr: str = None, name: str = None):
    """
    Søger i Fødevarestyrelsens Smiley-data (cached in-memory for O(1) performance).
    Søg enten på 'cvr' eller 'name'.
    """
    if not cvr and not name:
        raise HTTPException(status_code=400, detail="Enten 'cvr' eller 'name' skal angives som query parameter.")
        
    try:
        if cvr:
            results = await smiley_service.search_by_cvr(cvr)
        else:
            results = await smiley_service.search_by_name(name)
            
        return {
            "source": "Fødevarestyrelsen",
            "count": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/company/{cvr}")
async def get_company(cvr: str):
    """
    Henter CVR stamdata (Navn, Status, Adresse, Branche osv.) for en dansk virksomhed.
    """
    if len(cvr) != 8 or not cvr.isdigit():
        raise HTTPException(status_code=400, detail="CVR nummer skal være præcis 8 cifre.")
        
    try:
        result = await cvr_service.get_company_by_cvr(cvr)
        if not result.get("found"):
            raise HTTPException(status_code=404, detail=result.get("message"))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/company/{cvr}/compliance")
async def get_company_compliance(cvr: str):
    """
    Henter AML/Compliance detaljer (Reelle ejere, tegningsregler og risikovurdering).
    """
    if len(cvr) != 8 or not cvr.isdigit():
        raise HTTPException(status_code=400, detail="CVR nummer skal være præcis 8 cifre.")
        
    try:
        result = await cvr_service.get_company_compliance(cvr)
        if not result.get("found"):
            raise HTTPException(status_code=404, detail=result.get("message"))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/property/parcel")
async def get_parcel(matrikelnr: str, ejerlavkode: int):
    """
    Henter ejerlaug, region, kommune, sogn og grundareal (m2) for et specifikt matrikelnummer og ejerlaugkode.
    """
    if not matrikelnr or not ejerlavkode:
        raise HTTPException(status_code=400, detail="Både 'matrikelnr' og 'ejerlavkode' er påkrævede query parametre.")
        
    try:
        result = await datafordeler_client.get_parcel_info(matrikelnr=matrikelnr, ejerlavkode=ejerlavkode)
        if not result.get("found"):
            raise HTTPException(status_code=404, detail=result.get("message"))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/property/ejerlav")
async def search_ejerlav(q: str):
    """
    Søger efter danske ejerlaug ud fra navn (q) for at finde den korrekte ejerlavkode.
    """
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' er påkrævet.")
        
    try:
        result = await datafordeler_client.search_ejerlav(query=q)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/company/{cvr}/signatories")
async def get_company_signatories(cvr: str):
    """
    Kører rule-based parsing på en virksomheds tegningsregel og leverer strukturerede, maskinlæsbare tegningskrav.
    """
    if len(cvr) != 8 or not cvr.isdigit():
        raise HTTPException(status_code=400, detail="CVR nummer skal være præcis 8 cifre.")
        
    try:
        result = await signatory_service.get_company_signatories(cvr)
        if not result.get("found"):
            raise HTTPException(status_code=404, detail=result.get("message"))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/company/{cvr}/alerts")
async def get_company_alerts(cvr: str):
    """
    Overvåger virksomhedsstatus, konkursdekret-risici og returnerer et samlet risikosignal (risk_score).
    """
    if len(cvr) != 8 or not cvr.isdigit():
        raise HTTPException(status_code=400, detail="CVR nummer skal være præcis 8 cifre.")
        
    try:
        result = await alert_service.get_company_alerts(cvr)
        if not result.get("found"):
            raise HTTPException(status_code=404, detail=result.get("message"))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/energy/mix")
async def get_grid_mix():
    """
    Henter live grøn elnets-fordeling i Danmark (vind, sol, biomasse, kul) samt CO2-aftryk.
    """
    try:
        result = await energi_data_client.get_realtime_grid_mix()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")




