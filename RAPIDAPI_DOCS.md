# How to use the CPH Market Intelligence API

Welcome to the official documentation for the **Danish Market Intelligence API**. This API is designed to be the ultimate bridge between complex Danish government data and modern, international applications.

We have structured our endpoints into intuitive categories: **Address & Geo**, **Energy & ESG**, **FoodTech**, and **Finance & Macro**. All responses are returned as clean, standard JSON.

---

## 🚀 Authentication

All requests to the API must include your unique RapidAPI key in the headers.

```http
X-RapidAPI-Key: YOUR_RAPIDAPI_KEY
X-RapidAPI-Host: danish-market-intelligence.p.rapidapi.com
```

---

## 📍 1. Address & Geo Data (DAWA)
*Perfect for CRM validation, e-commerce checkouts, and logistics.*

### Address Validation & Autocomplete
Validates a Danish address string and returns official data.
* **Endpoint:** `GET /api/v1/address/validate`
* **Query Parameter:** `q` (e.g., "Nyhavn 17")

#### Example: Python (Requests)
```python
import requests

url = "https://danish-market-intelligence.p.rapidapi.com/api/v1/address/validate"
querystring = {"q": "Nyhavn 17"}
headers = {
	"X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",
	"X-RapidAPI-Host": "danish-market-intelligence.p.rapidapi.com"
}
response = requests.get(url, headers=headers, params=querystring)
print(response.json())
```

---

## ⚡ 2. Energy & ESG Data (Energi Data Service)
*Essential for Smart Home platforms and CO2 tracking.*

### Day-Ahead Spot Prices
Get hourly electricity spot prices for Denmark (DK1/DK2) for today and tomorrow.
* **Endpoint:** `GET /api/v1/energy/prices`

### Live CO2 Emissions
Get the real-time CO2 emission (g/kWh) in the Danish power grid.
* **Endpoint:** `GET /api/v1/energy/co2`

---

## 🍔 3. FoodTech Hygiene Ratings (Smiley API)
*Crucial for food delivery apps (Wolt, JustEat) and review platforms.*

### Search Restaurant Ratings
Search the official Danish Veterinary and Food Administration database (Fødevarestyrelsen).
* **Endpoint:** `GET /api/v1/food/smiley`
* **Query Parameters:** `cvr` (VAT number) OR `name` (Restaurant name)

#### Example: Node.js (Axios)
```javascript
const axios = require('axios');

const options = {
  method: 'GET',
  url: 'https://danish-market-intelligence.p.rapidapi.com/api/v1/food/smiley',
  params: {cvr: '43954733'},
  headers: {
    'X-RapidAPI-Key': 'YOUR_RAPIDAPI_KEY',
    'X-RapidAPI-Host': 'danish-market-intelligence.p.rapidapi.com'
  }
};

axios.request(options).then(function (response) {
	console.log(response.data);
}).catch(function (error) {
	console.error(error);
});
```

---

## 💼 4. Enterprise Finance & Macro ("The Big Three")
*Built for ERP systems, market analysts, and HR platforms.*

### Official Exchange Rates
Live daily exchange rates directly from the Danish Central Bank (Nationalbanken).
* **Endpoint:** `GET /api/v1/finance/exchange-rates`

### Consumer Price Index (Inflation)
The official CPI macro data from Statistics Denmark (DST), comparing this year to the previous year.
* **Endpoint:** `GET /api/v1/finance/cpi`

### Danish Public Holidays
Pre-calculated official bank closures and public holidays.
* **Endpoint:** `GET /api/v1/calendar/holidays`
* **Query Parameter:** `year` (e.g., 2024, 2025)

---

## 💡 Best Practices & Rate Limits
1. **Caching:** While our servers are incredibly fast (O(1) lookups for Smiley data), we recommend caching non-volatile data (like Bank Holidays or CPI) on your end to save your RapidAPI quota.
2. **Quotas:** Check your active plan (BASIC, PRO, ULTRA, MEGA) to avoid overage fees. The `X-RateLimit-Requests-Remaining` header will indicate your remaining quota.
3. **Errors:** We return standard HTTP status codes. `400` means a missing parameter, while `500` indicates an upstream failure from the Danish government servers.

*Made with ❤️ by CPH Techlab.*
