# ⚖️ CPH Market Intelligence - Compliance & Sikkerhed

Dette dokument fungerer som vores juridiske og sikkerhedsmæssige rygdækning for driften af CPH Market Intelligence API'et.

## 1. Juridisk Grundlag (Må vi sælge dette data?)
**JA.** Data fra Datafordeleren og Dataforsyningen (CVR, DAR, BBR, Matriklen) hører under de danske regler for "Grunddata" og er underlagt vilkårene for fri videreanvendelse af offentlig information (oftest PSI-direktivet). 

* **Kommercialisering:** Det er 100% lovligt at hente disse data gratis, "vaske" dem, og sælge adgangen eller servicen (API'et) til tredjepart med fortjeneste. Mange store danske virksomheder (f.eks. Bisnode, Krak, Resights) bygger hele deres forretning på præcis dette princip.
* **Krav:** Det eneste krav er oftest, at man ikke fremstiller sig selv som en officiel myndighed, og at man anerkender kilden, hvis det kræves af det specifikke datasæts licens (f.eks. "Indeholder data fra Datafordeleren").
* **GDPR:** Virksomhedsdata (CVR) er generelt undtaget for GDPR, da det er offentligt tilgængelige erhvervsdata. CPR-data (personnumre) har vi bevidst IKKE adgang til og rører IKKE ved.

## 2. Økonomisk Sikkerhed (Bliver jeg ramt af en kæmpe regning?)
**NEJ.** 
* **Datafordeleren:** Tjenesterne vi benytter på Datafordeleren er gratis. Du betaler ikke "per opslag". 
* **Hostinger:** Du kører på en VPS til fast pris. Uanset om dit API får 10 eller 100.000 kald, koster din server det samme. Du får ingen "Cloud-chok" regning som på AWS eller Azure.

## 3. Rate-Limiting & Anti-Spam (Hvordan beskytter vi serveren?)
For at sikre at vi ikke lægger Datafordeleren ned, eller at en ondsindet bot crasher vores Hostinger server, bruger vi **RapidAPI** som vores primære skjold.

* **RapidAPI Gateway:** Kunder kalder ikke din server direkte (den URL holder vi skjult/uudgivet). Kunderne kalder RapidAPI. Inden i RapidAPI opsætter vi "Rate Limits" (f.eks. max 5 kald i sekundet pr. betalende bruger). 
* **Beskyttelse mod DDoS:** Hvis nogen prøver at spamme dit API, bliver de blokeret af RapidAPI *før* trafikken overhovedet når din Hostinger-server.
* **Fremtidig sikring:** Hvis vi får ekstremt meget trafik, kan vi indbygge en "Cache" (hukommelse) i vores FastAPI backend. Hvis 100 kunder slår "Nyhavn 17" op samme dag, spørger vi kun Datafordeleren én gang og gemmer svaret i 24 timer.

## 4. Konklusion for CEO / MLRO
Projektet er "Low Risk / High Reward". Vi opererer fuldt ud inden for lovens rammer for videreanvendelse af offentlige data. Din økonomiske nedside er begrænset til din faste Hostinger-regning. RapidAPI varetager sikkerhedsskjoldet mod kunderne.
