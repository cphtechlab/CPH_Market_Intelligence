# 🔌 CPH Market Intelligence - Data Connectors & Checkpoints

Dette dokument fungerer som vores strategiske køreplan. Her holder vi styr på hvilke datasæt vi har integreret, hvad vi tilbyder, og hvad vores fremtidige byggeklodser ("Checkpoints") er.

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

## 🔮 Fase 3: The Enterprise Package (Fremtiden)

### 📍 BBR (Bygnings- og Boligregistret) & Geodata
* **Status:** 🔴 Ikke påbegyndt
* **Endpoint:** `/api/v1/property/{bbr_uuid}`
* **Data vi skal levere:**
  - Bygningsareal, anvendelse, og byggeår
  - Energimærke og varmeinstallation (ESG Rapportering!)
  - Oplysninger om olietanke eller forurening (hvis muligt)
* **Forretningsværdi:** Forsikringsselskaber, ejendomsinvestorer og ESG-auditors bruger dette. Klima/ESG er det varmeste emne i EU lige nu.

### 📍 DAGI (Danmarks Administrative Geografiske Inddeling)
* **Status:** 🔴 Ikke påbegyndt
* **Data vi skal levere:** Sognegrænser, postnummergrænser m.m.
* **Forretningsværdi:** Niche-brug for logistik- og leveringsfirmaer.

---

## 📝 Udviklings-Checkpoints (Næste opgaver for AI)
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
