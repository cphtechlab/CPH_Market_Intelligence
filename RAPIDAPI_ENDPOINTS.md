# 🚀 RapidAPI Endpoint Descriptions

Her er teksterne du kan kopiere direkte ind i "Description" feltet for hvert af dine 9 endpoints under "Definitions" -> "Endpoints" i RapidAPI.

---

### 1. Address Validation
**Name:** Address Validation  
**Route:** `GET /api/v1/address/validate`  
**Description:**
> Instantly validates any Danish address string using official government data (DAWA). Returns the exact official street name, house number, zip code, municipality, and exact GPS coordinates. Perfect for e-commerce checkouts and CRM data cleansing.

---

### 2. Reverse Geocoding
**Name:** Reverse Geocoding  
**Route:** `GET /api/v1/address/reverse`  
**Description:**
> Convert exact GPS coordinates (Latitude and Longitude) into official Danish street addresses. Ideal for fleet management, logistics routing, and location-based mobile apps.

---

### 3. Postal Info
**Name:** Postal Info  
**Route:** `GET /api/v1/postal/{zipcode}`  
**Description:**
> Retrieve detailed information about a specific Danish postal code (e.g. 1050), including the official city name, municipality mapping, and the exact geographical bounding box of the postal area.

---

### 4. Energy Prices
**Name:** Day-Ahead Energy Prices  
**Route:** `GET /api/v1/energy/prices`  
**Description:**
> Fetch official hourly Day-Ahead electricity spot prices (in DKK/kWh) for Eastern (DK2) and Western (DK1) Denmark. Crucial for smart-home automation, EV charging apps, and energy consumption forecasting.

---

### 5. Energy CO2
**Name:** Live CO2 Emissions  
**Route:** `GET /api/v1/energy/co2`  
**Description:**
> Get the real-time CO2 emission data (g/kWh) in the Danish power grid. Excellent for ESG reporting, sustainability tracking, and green energy optimization.

---

### 6. Smiley Data
**Name:** Restaurant Smiley Ratings  
**Route:** `GET /api/v1/food/smiley`  
**Description:**
> Search the official Danish Veterinary and Food Administration database by VAT number (CVR) or Restaurant Name. Retrieves the latest official hygiene rating (Smiley) and the direct URL to the inspection report. Cached for ultra-fast, O(1) lookups.

---

### 7. Exchange Rates
**Name:** Official Exchange Rates  
**Route:** `GET /api/v1/finance/exchange-rates`  
**Description:**
> Retrieve daily updated, official foreign exchange rates directly from the Danish Central Bank (Nationalbanken). Essential for multi-currency ERP systems, payroll, and accurate market analysis.

---

### 8. Inflation CPI
**Name:** Consumer Price Index (Inflation)  
**Route:** `GET /api/v1/finance/cpi`  
**Description:**
> Access the official macro-economic Consumer Price Index (CPI) data from Statistics Denmark. Returns the precise year-over-year inflation percentage. Perfect for financial forecasting and index-linked contract adjustments.

---

### 9. Holidays
**Name:** Danish Public Holidays  
**Route:** `GET /api/v1/calendar/holidays`  
**Description:**
> Get a complete, accurate list of all official Danish bank closures and public holidays for any given year. A must-have for global HR systems, payroll calculations, and logistics delivery planning.
