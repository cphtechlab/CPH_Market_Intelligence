# 🔌 CPH Market Intelligence - Data Connectors & Checkpoints

Dette dokument fungerer som vores strategiske køreplan. Her holder vi styr på hvilke datasæt vi har integreret, hvad vi tilbyder, og hvad vores fremtidige byggeklodser ("Checkpoints") er.

---

## 💰 Forretningsmodel & Passiv Indkomst (RapidAPI)
Vores overordnede mål er at skabe **passiv indkomst** ved at hoste og videresælge adgang til komplekse danske og internationale datasæt igennem vores RapidAPI-storefront under brandet **CPH Techlab**. 

* **Prisstruktur:** Vi opererer med et 'Freemium' koncept.
  - **Free:** Begrænset antal kald, til test.
  - **Pro ($9/md):** Mellemstore behov (f.eks. 5.000 kald).
  - **Enterprise ($99/md):** Massiv volumen, ubegrænset markedsdata og tung B2B validering (100.000+ kald). Udbetalingen går direkte ind via PayPal.
* **Skalering:** Jo flere værdifulde datakilder (connectors) vi bygger ind i API'et, desto flere kunder tiltrækker vi. I takt med udvidelsen kan vi opgradere pakkerne og tjene mere.
* **Den Gyldne Regel ("Vaskningen"):** Vores primære værdi (og dét kunderne betaler for) er formidlingen. Alt data vi trækker (uanset kilden) **SKAL** altid vaskes, struktureres og leveres med et kommercielt kundemindset. Det skal være så "Plug & Play" for internationale udviklere, No-Code platforme (Zapier/Make) og AI-agenter, at de med glæde betaler frem for selv at kæmpe med rodet, offentlig infrastruktur.

---

## ✅ Fase 1: Proof of Concept (Aktiv & Live)

### 📍 DAR (Danmarks Adresseregister) via DAWA
* **Status:** 🚀 LIVE & MONETIZED (Hostinger + RapidAPI)
* **Endpoint:** `/api/v1/address/validate?q={adresse}`
* **Data vi leverer:**
  - Valideret adressebetegnelse
  - Præcis Vejnavn, Husnummer, Postnummer, By, Kommune
  - Geografiske Koordinater (Længde/Breddegrad)
* **Forretningsværdi:** En simpel "Lead Magnet". Internationale webshops og AI-agenter bruger dette til at autocomplete og validere danske adresser uden at kende til dansk infrastruktur.

### 📍 Reverse Geocoding (GPS til Adresse) via DAWA
* **Status:** 🚀 LIVE & MONETIZED (Hostinger + RapidAPI)
* **Endpoint:** `/api/v1/address/reverse?lat={lat}&lon={lon}`
* **Data vi leverer:** Præcis vejnavn, husnummer, postnummer og kommune for det givne koordinat.
* **Forretningsværdi:** Kæmpe værdi for kurerer, logistik og taxa-apps, som skal oversætte en chaufførs eller brugers GPS-lokation til en rigtig adresse lynhurtigt.

### 📍 Postnummer Intelligence via DAWA
* **Status:** 🚀 LIVE & MONETIZED (Hostinger + RapidAPI)
* **Endpoint:** `/api/v1/postal/{zipcode}`
* **Data vi leverer:** Hvilke kommuner postnummeret tilhører, og geografisk bounding-box.
* **Forretningsværdi:** E-commerce validering. Sikrer at kunder indtaster et validt dansk postnummer, og tillader geografisk filtrering af levering baseret på kommune.

---

## 🚧 Fase 2: The Money Maker (Næste Skridt)

### 📍 CVR (Det Centrale Virksomhedsregister) via Datafordeleren
* **Status:** 🟡 Afventer udvikling
* **Endpoint:** `/api/v1/company/{cvr_nummer}`
* **Nødvendig Connector:** Datafordeler API Nøgle (Er opsat i `.env`)
* **Data vi skal levere:**
  - Stamdata (Navn, Adresse, Selskabsform)
  - Virksomhedsstatus (Aktiv, Konkurs, Under Tvangsopløsning)
  - Branchekode (NACE) og formål
* **Forretningsværdi:** Essentielt for KYC (Know Your Customer) processer og CRM systemer i udlandet, der skal oprette danske kunder korrekt.

### 📍 Reelle Ejere & Tegningsregler (AML Compliance)
* **Status:** 🟡 Afventer CVR integration
* **Endpoint:** `/api/v1/company/{cvr}/compliance`
* **Data vi skal levere:**
  - Hvem ejer reelt virksomheden? (Reelle ejere)
  - Hvem kan skrive under? (Tegningsregler)
* **Forretningsværdi:** Hjertet i din MLRO baggrund! Dette er B2B guld. Advokater og finansielle platforme er lovmæssigt forpligtet til at hente disse data. De betaler dyrt for et API, der serverer det nemt.

---

## 🔮 Fase 3: The Enterprise Package ($99/mo)

For at retfærdiggøre en $99/måned Enterprise-pakke fokuserer vi på "The Big Three" af B2B data for udenlandske kunder: Valuta, Makroøkonomi og Logistik/HR-kalendere.

### 📍 Valutakurser (Nationalbanken)
* **Status:** 🚀 LIVE & MONETIZED
* **Endpoint:** `/api/v1/finance/exchange-rates`
* **Data:** Daglige officielle valutakurser fra Danmarks Nationalbank. Vi omdanner deres legacy XML til ren JSON.
* **Forretningsværdi:** Udenlandske webshops og ERP-systemer SKAL bruge officielle kurser til bogføring.

### 📍 Makroøkonomi (Danmarks Statistik)
* **Status:** 🚀 LIVE & MONETIZED
* **Endpoint:** `/api/v1/finance/cpi`
* **Data:** Det danske Forbrugerprisindeks (Inflation) fra DST.
* **Forretningsværdi:** Markedsanalyse-dashboards og finansielle institutioner, der screener det danske marked.

### 📍 Danske Helligdage (Kalender/Logistik)
* **Status:** 🚀 LIVE & MONETIZED
* **Endpoint:** `/api/v1/calendar/holidays?year=2024`
* **Data:** Liste over alle officielle banklukkedage og helligdage i Danmark.
* **Forretningsværdi:** Logistikberegning for udenlandske fragtfirmaer (kører PostNord i morgen?) og udenlandske HR-platforme med danske medarbejdere.

### 📍 Smiley-Data (FoodTech)
* **Status:** 🚀 LIVE & MONETIZED
* **Endpoint:** `/api/v1/food/smiley?cvr={cvr}`
* **Data:** Fødevarestyrelsens Smiley-rating for restauranter og butikker i Danmark.
* **Forretningsværdi:** Kæmpe værdi for FoodTech platforme (Wolt, JustEat, Yelp, TripAdvisor), der lovmæssigt skal fremvise Smiley-rapporter, men som her slipper for selv at parse Fødevarestyrelsens massive og ustabile XML-dumps.

---

## 🏗️ Fremtidige Integrationer (Ikke bygget endnu)

### 📍 Vejdirektoratet (Trafik & Logistik)
* **Status:** 🔴 Ikke påbegyndt (Komplekst format)
* **Data vi skal levere:** Live trafik, uheld og vejarbejde fra DATEX II standarden.
* **Forretningsværdi:** Flådestyring og ruteplanlægning. (Udskudt da DATEX II kræver en specifik XML-motor at parse robust).
1. [x] Test at `api.cphtechlab.dk` er live igennem Traefik og DNS.
2. [x] Opret profilen på RapidAPI og forbind det nuværende DAR endpoint (Fase 1).
3. [ ] **BLOKERET:** Start udviklingen af Fase 2 (CVR Opslag via Datafordeler REST). *Afventer oprettelse af 'Webservicebruger' med Brugernavn/Adgangskode på Datafordelerens portal.*

### 🚀 Alternative Datakilder (Kræver IKKE login)
Mens vi venter på Datafordeleren, er her nogle ekstremt stærke, åbne danske API'er, som vi kan koble på vores RapidAPI butik i mellemtiden:

*   **Energi Data Service (energidataservice.dk):** 
    *   Helt åbent API (Ingen API-nøgle kræves).
    *   Vi kan levere **Spotpriser på el** (Time for time) og **CO2-udledning** pr. kWh.
    *   *Salgsværdi:* Enorm! Virksomheder skal bruge dette til ESG-rapportering og intelligent strømstyring.
*   **Danmarks Statistik (API):**
    *   Åbent API (Ingen login kræves).
    *   Demografiske og økonomiske data på postnummer-niveau.
*   **DAWA Udvidet (Geodata):**
    *   Vi har allerede adgang via vores nuværende opsætning.
    *   Vi kan tilføje et "Reverse Geocoding" endpoint (Kunder sender et GPS-koordinat, og vi returnerer nærmeste danske adresse/kommune). Perfekt til logistik og flådestyring.
