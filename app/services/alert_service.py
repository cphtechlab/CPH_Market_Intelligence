from datetime import datetime
from app.services.cvr_service import cvr_service

class AlertService:
    def __init__(self):
        # Nogle simulatede advarsler til specifikke CVR numre til test/demo brug
        self.mock_alerts = {
            "12345678": {
                "risk_score": 95,
                "warnings": ["Under konkursbehandling (Decree issued 2026-06-12)", "Mangler regnskabsaflevering"],
                "bankruptcy_declared": True,
                "liquidation_in_progress": False
            },
            "87654321": {
                "risk_score": 70,
                "warnings": ["Under frivillig likvidation", "Direktion fratrådt uden erstatning"],
                "bankruptcy_declared": False,
                "liquidation_in_progress": True
            }
        }

    async def get_company_alerts(self, cvr: str):
        company_data = await cvr_service.get_company_by_cvr(cvr)
        if not company_data.get("found"):
            return {"found": False, "message": f"Company with CVR {cvr} not found."}

        # Tjek om vi har en defineret advarsel i vores system
        alert_info = self.mock_alerts.get(cvr)
        
        # Hvis ikke, genererer vi det dynamisk ud fra firmaets status
        if not alert_info:
            status = company_data.get("status", "Aktiv")
            if status == "Aktiv":
                alert_info = {
                    "risk_score": 5, # Low score is good
                    "warnings": [],
                    "bankruptcy_declared": False,
                    "liquidation_in_progress": False
                }
            else:
                alert_info = {
                    "risk_score": 85,
                    "warnings": [f"Company status is reported as: {status}"],
                    "bankruptcy_declared": "Konkurs" in status,
                    "liquidation_in_progress": "Likvidation" in status or "Opløst" in status
                }

        # Tilføj tidsstempler og vaskede compliance data
        return {
            "cvr": cvr,
            "company_name": company_data.get("name", ""),
            "status": company_data.get("status", "Aktiv"),
            "risk_score": alert_info["risk_score"], # 0 (Low) to 100 (High)
            "alerts": alert_info["warnings"],
            "checks": {
                "bankruptcy_declared": alert_info["bankruptcy_declared"],
                "liquidation_in_progress": alert_info["liquidation_in_progress"],
                "reconstruction_active": False,
                "compulsory_dissolution_flag": False
            },
            "last_checked_utc": datetime.utcnow().isoformat() + "Z",
            "verdict": "CLEAR" if alert_info["risk_score"] < 40 else "WARNING_FLAGGED" if alert_info["risk_score"] < 80 else "CRITICAL_RISK"
        }

alert_service = AlertService()
