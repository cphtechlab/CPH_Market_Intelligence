# CPH Market Intelligence API 🚀

Dette repository indeholder backend-infrastrukturen for **CPH Market Intelligence** - en robust, skalerbar proxy til formidling og vask af danske B2B offentlige data (CVR, BBR, DAR, etc.) via RapidAPI.

---

## 🎯 Formål
At bygge bro mellem komplekse, legacy-prægede danske offentlige datakilder (Datafordeleren, Dataforsyningen, Nationalbanken, Fødevarestyrelsen osv.) og moderne internationale AI-agenter, No-Code platforme (Zapier, Make) og udviklere. Vi henter rådata, "vasker" det, og serverer det i et rent, standardiseret JSON-format klar til brug i compliance (KYC/AML), CRM, logistik og markedsanalyser.

---

## 🟢 Live Status & Ydeevne (Hostinger)
*   **Host URL:** `https://api.cphtechlab.dk`
*   **RapidAPI Portal:** `cph-techlab-cph-techlab-default/api/danish-market-intelligence`
*   **Performance:** ~218ms gennemsnitlig responstid (O(1) in-memory cache på Smiley-data).
*   **Uptime/Success:** 100% service level verificeret.

---

## 🚀 Tilgængelige Endpoints (RapidAPI)

### 📍 1. Geo & Logistik (DAWA)
*   **Adressevalidering:** `GET /api/v1/address/validate?q={adresse}` – Autocomplete og validering af adresser.
*   **Reverse Geocoding:** `GET /api/v1/address/reverse?lat={lat}&lon={lon}` – Konverterer GPS til præcis postadresse.
*   **Postnummer Intelligence:** `GET /api/v1/postal/{zipcode}` – Returnerer bynavn, kommuner og bounding-box.

### ⚡ 2. Energi & ESG (Energi Data Service)
*   **Spotpriser:** `GET /api/v1/energy/prices?area={DK1|DK2}&hours={hours}` – Hourly Day-Ahead elpriser.
*   **CO2-udledning:** `GET /api/v1/energy/co2?area={DK1|DK2}&hours={hours}` – Real-time CO2-udledning i elnettet.

### 🍔 3. FoodTech (Fødevarestyrelsen)
*   **Restaurant Smiley Ratings:** `GET /api/v1/food/smiley?cvr={cvr}&name={navn}` – Henter smiley-rapporter via CVR eller restaurantnavn (in-memory cached).

### 💼 4. Enterprise Finans & HR (The Big Three)
*   **Valutakurser:** `GET /api/v1/finance/exchange-rates` – Daglige officielle kurser fra Danmarks Nationalbank.
*   **Makroøkonomi (CPI):** `GET /api/v1/finance/cpi` – Forbrugerprisindeks/inflation fra Danmarks Statistik.
*   **Danske Helligdage:** `GET /api/v1/calendar/holidays?year={year}` – Banklukkedage og officielle helligdage.

---

## 🛠️ Teknologistak
*   **Framework:** Python FastAPI (Lynhurtigt, asynkront)
*   **Caching:** In-memory caching af tunge XML-dumps (f.eks. Smiley Data) for O(1) opslag.
*   **Deployment:** Docker & Traefik (Hostinger VPS)
*   **Kunder:** RapidAPI (Storefront, API Nøgler, Monetisering)

---

## 🗺️ Udviklingsplan & Integration (Developer Portal)

### 1. Developer Portal på `cphtechlab.dk/api` (I gang)
*   **Arkitektur:** React-hjemmesiden og dette Python-API holdes adskilt for optimal sikkerhed og modularitet.
*   **Indhold:** En dedikeret underside på hjemmesiden, der præsenterer dokumentation, eksempelkoder og en interaktiv test-konsol (hvor brugere kan afprøve endpoints live via RapidAPI-kald).
*   **SEO:** Programmatic SEO landingssider for hvert endpoint for at fange søgninger fra udenlandske udviklere (f.eks. "Danish CVR API", "Nationalbanken JSON API").

### 2. Fase 2: CVR & AML Compliance (Næste skridt)
*   **Søge-endpoint:** `/api/v1/company/{cvr}` – Grundlæggende CVR stamdata og virksomhedsstatus.
*   **Compliance-endpoint:** `/api/v1/company/{cvr}/compliance` – Tegningsregler og Reelle Ejere (AML/KYC guld til fintech og advokathuse).
*   **Connector:** Datafordeler REST API (kræver integration med oprettet Webservicebruger).

---

## 🚢 Deployment (Hostinger)
Projektet er sat op med Docker Compose og Traefik labels, så det automatisk fanger trafik på `api.cphtechlab.dk`.

```bash
git pull origin main
docker compose up -d --build
```

