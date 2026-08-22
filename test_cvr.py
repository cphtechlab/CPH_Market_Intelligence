import asyncio
import json
import httpx
import sys
import os

# Tilføj current directory til python path for at kunne importere app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_cvr_endpoints():
    print("Tester CVR og Compliance Services...")
    from app.services.cvr_service import cvr_service
    
    test_cvr = "43954733" # CPH Techlab n Consult ApS CVR
    
    # Test CVR stamdata lookup
    try:
        print(f"\n--- Henter CVR data for CPH Techlab n Consult ({test_cvr}) ---")
        res = await cvr_service.get_company_by_cvr(test_cvr)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        if res.get("found"):
            print("SUCCESS: CVR lookup completed!")
        else:
            print("FAILED: Company not found.")
    except Exception as e:
        print(f"ERROR: CVR lookup failed: {e}")

    # Test Compliance check
    try:
        print(f"\n--- Henter Compliance data for CPH Techlab n Consult ({test_cvr}) ---")
        res_comp = await cvr_service.get_company_compliance(test_cvr)
        print(json.dumps(res_comp, indent=2, ensure_ascii=False))
        if res_comp.get("compliance_status") == "COMPLIANT":
            print("SUCCESS: Compliance assessment completed!")
        else:
            print("FAILED: Compliance status incorrect.")
    except Exception as e:
        print(f"ERROR: Compliance check failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_cvr_endpoints())
