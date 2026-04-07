# LogStreamer API

**LogStreamer API** – tai centralizuotas klaidų registravimo mikroservisas, skirtas AI agentų, `n8n` automatizacijų ir kitų paskirstytų sistemų techninių žurnalų (*logs*) surinkimui, saugojimui ir peržiūrai. Sistema leidžia kaupti klaidas ir techninius įvykius vienoje saugioje vietoje, kad juos būtų galima lengvai analizuoti, stebėti realiuoju laiku ir greitai reaguoti į sutrikimus.

Projektas sukurtas naudojant **Python 3.10+**, **FastAPI**, **SQLite**, **Pydantic** ir **Uvicorn**. API apsaugota naudojant API rakto autentifikaciją per HTTP antraštę `X-API-Key`, o interaktyvi dokumentacija automatiškai pateikiama per **Swagger UI**.

## Pagrindinės galimybės

- Centralizuotas klaidų ir įvykių registravimas
- Žurnalų saugojimas SQLite duomenų bazėje
- Filtravimas pagal klaidos lygį
- Paprasta integracija su kitomis sistemomis per REST API
- API rakto autentifikacija
- Automatiškai generuojama Swagger UI dokumentacija

## Naudojamos technologijos

- **Backend:** Python 3.10+ su **FastAPI**
- **Duomenų bazė:** **SQLite**
- **Duomenų validacija:** **Pydantic**
- **Serveris:** **Uvicorn**
- **Aplinkos kintamieji:** **python-dotenv**

## Diegimas ir paleidimas

Pirmiausia susikurkite virtualią aplinką ir ją aktyvuokite:

```bash
python -m venv venv
```

**Windows**
```bash
venv\Scripts\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

Įdiekite reikalingas bibliotekas:

```bash
pip install -r requirements.txt
```

Projekto šakniniame kataloge sukurkite `.env` failą ir nurodykite API raktą:

```env
API_SECRET_KEY=JUSU_SLAPTAS_RAKTAS_CIA
```

Paleiskite serverį:

```bash
uvicorn main:app --reload
```

## Prieiga

- **API adresas:** `http://127.0.0.1:8000`
- **Interaktyvi dokumentacija:** `http://127.0.0.1:8000/docs`

## Autentifikacija

Visiems maršrutams, išskyrus pagrindinį `/`, būtina perduoti API raktą per HTTP antraštę:

```http
X-API-Key: JUSU_SLAPTAS_RAKTAS_CIA
```

## API naudojimas

### Pagrindinis maršrutas

**Metodas:** `GET /`

Pavyzdinis atsakymas:

```json
{
  "message": "LogStreamer API veikia"
}
```

### Klaidos registravimas

**Metodas:** `POST /logs`

Užklausos turinys:

```json
{
  "source": "n8n_Automation",
  "level": "ERROR",
  "message": "Nepavyko pasiekti API",
  "stack_trace": "Line 12: Connection timeout"
}
```

Laukų reikšmės:

- `source` – sistemos arba serviso pavadinimas
- `level` – žurnalo lygis, pvz. `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- `message` – klaidos arba įvykio aprašymas
- `stack_trace` – papildoma diagnostinė informacija

### Žurnalų gavimas

**Metodas:** `GET /logs`

Pavyzdys be filtravimo:

```http
GET /logs
```

Pavyzdys su filtravimu pagal lygį:

```http
GET /logs?level=CRITICAL
```

## Naudojimo pavyzdžiai su curl

### Įrašyti klaidą

```bash
curl -X POST "http://127.0.0.1:8000/logs" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: JUSU_SLAPTAS_RAKTAS_CIA" \
  -d '{
    "source": "n8n_Automation",
    "level": "ERROR",
    "message": "Nepavyko pasiekti API",
    "stack_trace": "Line 12: Connection timeout"
  }'
```

### Gauti kritinius žurnalus

```bash
curl -X GET "http://127.0.0.1:8000/logs?level=CRITICAL" \
  -H "X-API-Key: JUSU_SLAPTAS_RAKTAS_CIA"
```

## Pritaikymo scenarijai

Šis mikroservisas gali būti naudojamas:

- AI agentų klaidų stebėsenai
- `n8n` darbo eigų diagnostikai
- Vidinių mikroservisų logų centralizavimui
- Automatizuotų procesų incidentų analizei

## Saugumo pastabos

- Nelaikykite tikro API rakto viešame repozitorijos faile
- `.env` failą rekomenduojama įtraukti į `.gitignore`
- Produkcinėje aplinkoje naudokite stiprų ir unikalų API raktą

## Tolimesni patobulinimai

Ateityje projektą galima plėsti pridedant:

- **PostgreSQL** arba **MySQL** palaikymą
- **Webhook** integracijas
- **Slack** ar el. pašto pranešimus apie kritines klaidas
- Išplėstinę autentifikaciją su **JWT**
- **Docker** palaikymą

