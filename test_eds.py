import httpx
import asyncio
import json

async def test_eds_endpoints():
    print("Test af Energi Data Service Endpoints (Lokalt)...\n")
    
    # Vi tester "gennem" vores egen FastAPI logik i stedet for at starte serveren.
    # Da energi_data_client er asynkron, kan vi bare kalde dens funktioner direkte.
    from app.services.energi_data_service import energi_data_client

    try:
        print("--- Tester El-spotpriser (DK1, 2 timer) ---")
        prices = await energi_data_client.get_spot_prices(price_area="DK1", hours=2)
        print(json.dumps(prices, indent=2))
        print("El-priser virker!\n")
    except Exception as e:
        print(f"Fejl i El-priser: {e}\n")

    try:
        print("--- Tester CO2-udledning (DK2, 2 timer) ---")
        # CO2Emis bruger 5-minutters intervaller, så 2 timer bør give 24 resultater
        co2 = await energi_data_client.get_co2_emissions(price_area="DK2", hours=2)
        print(json.dumps(co2, indent=2))
        print("CO2-udledning virker!\n")
    except Exception as e:
        print(f"Fejl i CO2: {e}\n")

if __name__ == "__main__":
    asyncio.run(test_eds_endpoints())
