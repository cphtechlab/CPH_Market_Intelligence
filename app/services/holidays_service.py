import holidays
import logging

logger = logging.getLogger(__name__)

class HolidaysService:
    def get_holidays(self, year: int):
        """
        Henter danske helligdage for et givent år.
        """
        try:
            # Sætter sproget til dansk
            dk_holidays = holidays.DK(years=year, language='da')
            
            results = []
            for date, name in sorted(dk_holidays.items()):
                results.append({
                    "date": str(date),
                    "name": name,
                    "is_bank_holiday": True # Danske helligdage er altid banklukkedage
                })

            return {
                "source": "Python Holidays (Internal)",
                "country": "DK",
                "year": year,
                "count": len(results),
                "results": results
            }
        except Exception as e:
            logger.error(f"Fejl ved beregning af helligdage: {e}")
            raise

holidays_service = HolidaysService()
