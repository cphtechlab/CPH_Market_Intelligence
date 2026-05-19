import httpx
import asyncio
import json
import time

async def test_smiley_endpoint():
    print("Tester Smiley API (FoodTech)...\n")
    
    from app.services.smiley_service import smiley_service

    try:
        print("--- Søger på CVR (10148782) for at indlæse cachen ---")
        start_time = time.time()
        # Dette CVR-nummer burde eksistere (eks. en tilfældig MacD eller lign. Hvis ikke, viser den bare tom array)
        results = await smiley_service.search_by_cvr("10148782")
        duration = time.time() - start_time
        print(f"Indlæsning & søgning tog: {duration:.2f} sekunder")
        print(f"Fandt {len(results)} resultater.")
        if results:
            print(json.dumps(results[0], indent=2))
        print("CVR søgning virker!\n")

        print("--- Søger på Navn ('McDonald') fra in-memory cache ---")
        start_time = time.time()
        results_name = await smiley_service.search_by_name("McDonald", limit=3)
        duration = time.time() - start_time
        print(f"Søgning fra cache tog: {duration:.4f} sekunder (Bør være instant!)")
        print(f"Fandt {len(results_name)} resultater (limit 3).")
        if results_name:
            print(json.dumps(results_name[0], indent=2))
        print("Navnesøgning virker!\n")

    except Exception as e:
        print(f"Fejl i Smiley API: {e}\n")

if __name__ == "__main__":
    asyncio.run(test_smiley_endpoint())
