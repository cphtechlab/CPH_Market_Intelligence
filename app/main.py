from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.services.datafordeler import datafordeler_client
import httpx

app = FastAPI(
    title="CPH Market Intelligence API",
    description="Backend API for RapidAPI, som proxy for danske offentlige data (Datafordeleren).",
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
