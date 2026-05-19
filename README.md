# CPH Market Intelligence API 🚀

Dette repository indeholder backend-infrastrukturen for **CPH Market Intelligence** - en robust, skalerbar proxy til formidling og vask af danske B2B offentlige data (CVR, BBR, DAR, etc.) via RapidAPI.

## 🎯 Formål
At bygge bro mellem komplekse, legacy-prægede danske offentlige datakilder (Datafordeleren, Dataforsyningen, Nationalbanken, Fødevarestyrelsen osv.) og moderne internationale AI-agenter, No-Code platforme (Zapier, Make) og udviklere. Vi henter rådata, "vasker" det, og serverer det i et rent, standardiseret JSON-format klar til brug i compliance (KYC/AML), CRM, logistik og markedsanalyser.

## 🚀 Tilgængelige Endpoints (RapidAPI)
* **Geodata (DAWA):** Adressevalidering (`/address/validate`), Reverse Geocoding (`/address/reverse`), Postnummer Info (`/postal/{zipcode}`).
* **Energi & ESG:** El-spotpriser (`/energy/prices`), CO2-udledning (`/energy/co2`).
* **FoodTech:** Fødevarestyrelsens Smiley Data (`/food/smiley`).
* **Enterprise Finans & HR:** Valutakurser (`/finance/exchange-rates`), Forbrugerprisindeks (`/finance/cpi`), Helligdage (`/calendar/holidays`).

## 🛠️ Teknologistak
* **Framework:** Python FastAPI (Lynhurtigt, asynkront)
* **Caching:** In-memory caching af tunge XML-dumps (f.eks. Smiley Data) for O(1) opslag.
* **Deployment:** Docker & Traefik (Hostinger VPS)
* **Kunder:** RapidAPI (Storefront, API Nøgler, Monetisering)

## 🚀 Kom Godt I Gang (Lokal Udvikling)

1. **Installer afhængigheder:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Opret .env fil** med din Datafordeler API nøgle:
   ```env
   DATAFORDELER_API_KEY=din_nøgle_her
   ```
3. **Start serveren:**
   ```bash
   uvicorn app.main:app --reload
   ```
4. Gå til `http://localhost:8000/docs` i din browser for at se det interaktive Swagger UI.

## 🚢 Deployment (Hostinger)
Projektet er sat op med Docker Compose og Traefik labels, så det automatisk fanger trafik på `api.cphtechlab.dk`.

```bash
git pull origin main
docker compose up -d --build
```
