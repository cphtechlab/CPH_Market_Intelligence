import httpx
import asyncio
import json

async def test_geo_endpoints():
    print("Test af DAWA Geodata Endpoints (Lokalt)...\n")
    
    from app.services.datafordeler import datafordeler_client

    try:
        print("--- Tester Reverse Geocoding (Kongens Nytorv) ---")
        # Kongens Nytorv koordinater: lat=55.67938, lon=12.58514
        reverse = await datafordeler_client.reverse_geocode(lat=55.67938, lon=12.58514)
        print(json.dumps(reverse, indent=2))
        print("Reverse Geocoding virker!\n")
    except Exception as e:
        print(f"Fejl i Reverse Geocoding: {e}\n")

    try:
        print("--- Tester Postnummer Info (1050 København K) ---")
        postal = await datafordeler_client.get_postal_info(zipcode="1050")
        print(json.dumps(postal, indent=2))
        print("Postnummer Info virker!\n")
    except Exception as e:
        print(f"Fejl i Postnummer Info: {e}\n")

if __name__ == "__main__":
    asyncio.run(test_geo_endpoints())
