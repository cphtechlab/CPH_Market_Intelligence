import httpx
import asyncio
import json

async def test_enterprise_endpoints():
    print("Tester Enterprise Features ($99 Tier)...\n")
    
    from app.services.nationalbanken import nationalbanken_client
    from app.services.dst import dst_client
    from app.services.holidays_service import holidays_service

    try:
        print("--- Tester Nationalbanken (Valutakurser) ---")
        rates = await nationalbanken_client.get_exchange_rates()
        # Print kun de første 3 for ikke at spamme terminalen
        print(f"Hentet {rates['count']} kurser for dato: {rates['date']}")
        print("Første 3:")
        print(json.dumps(rates['results'][:3], indent=2))
        print("Nationalbanken XML Vaskning virker!\n")
    except Exception as e:
        print(f"Fejl i Nationalbanken: {e}\n")

    try:
        print("--- Tester Danmarks Statistik (Inflation/CPI) ---")
        cpi = await dst_client.get_cpi()
        print(f"Kilde: {cpi['source']} - {cpi['description']}")
        print("Seneste 3 år:")
        print(json.dumps(cpi['results'][:3], indent=2))
        print("Danmarks Statistik virker!\n")
    except Exception as e:
        print(f"Fejl i Danmarks Statistik: {e}\n")

    try:
        print("--- Tester Danske Helligdage (2024) ---")
        hols = holidays_service.get_holidays(2024)
        print(f"Fandt {hols['count']} helligdage i {hols['year']}")
        print("Første 3:")
        print(json.dumps(hols['results'][:3], indent=2))
        print("Helligdage virker!\n")
    except Exception as e:
        print(f"Fejl i Helligdage: {e}\n")

if __name__ == "__main__":
    asyncio.run(test_enterprise_endpoints())
