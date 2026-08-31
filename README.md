# ⚜️ AE Lluïsos de Gràcia - Portal Web

Aplicació web oficial per a l'**Agrupament Escolta Lluïsos de Gràcia**. Aquest lloc web proporciona informació sobre l'agrupament, novetats, el calendari del curs, l'equip de caps per branca, el mapa interactiu "El Foulard pel Món", la botiga de marxandatge i la Quiniela de caps.

---

## 🚀 Característiques

- **Pàgina d'Inici (`/`)**: Secció *Hero*, presentació "Qui som", darreres novetats i carrusel de l'equip de caps.
- **Novetats (`/novetats`)**: Tauler amb avisos, notícies i activitats recents.
- **Calendari (`/calendari`)**: Visualitzador interactiu d'esdeveniments, sortides, campaments i reunions.
- **Equip de Caps (`/equips`)**: Fitxes dels caps organitzats per branques (Castors i Llúdrigues, Llops i Daines, Ràngers i Noies Guia, Pioners i Caravel·les, Ròvers i Caps de Grup).
- **El Foulard pel Món (`/foulard`)**: Mapa interactiu amb xinxetes dels viatges i llocs on ha viatjat el foulard de l'agrupament.
- **Botiga (`/botiga`)**: Catàleg de productes i marxandatge de l'agrupament.
- **Quiniela (`/kiniela`)**: Joc interactiu per endevinar quins caps aniran a cada branca el curs vinent.
- **Integració amb Google Sheets**: Lectura de dades en temps real des de fulls de càlcul de Google i sincronització de les respostes de la Quiniela (amb mode offline de suport integrat si no hi ha connexió o credencials).

---

## 📁 Estructura del Projecte

```text
LLuisosWeb/
├── app.py                   # Servidor Flask principal i rutes HTTP/API
├── gsheets_db.py            # Adaptador de base de dades (Google Sheets + dades locals)
├── requirements.txt         # Dependències de Python
├── run.bat                  # Script per iniciar l'aplicació a Windows
├── .gitignore               # Exclusions per a Git
├── README.md                # Documentació del projecte
├── templates/               # Plantilles HTML (Jinja2)
│   ├── base.html            # Plantilla base amb capçalera i peu
│   ├── index.html           # Pàgina d'inici
│   ├── novetats.html        # Pàgina de notícies
│   ├── calendari.html       # Pàgina de calendari
│   ├── equips.html          # Pàgina de l'equip de caps
│   ├── foulard.html         # Mapa del foulard
│   ├── shop.html            # Botiga de marxandatge
│   └── kiniela.html         # Joc de la quiniela
└── static/                  # Fitxers estàtics
    ├── css/                 # Fulls d'estil CSS
    ├── js/                  # Scripts JavaScript
    ├── images/              # Imatges i icones
    ├── fonts/               # Tipografies
    └── data/                # Dades auxiliars
```

---

## 🛠️ Requisits previs

- **Python** 3.8 o superior instal·lat al sistema ([descarregar Python](https://www.python.org/downloads/)).
- **pip** (gestor de paquets de Python).

---

## 📦 Instal·lació

1. **Clonar o descarregar el repositori:**
   ```bash
   git clone https://github.com/danicasjau/LLuisosWeb.git
   cd LLuisosWeb
   ```

2. **(Opcional recomanat) Crear i activar un entorn virtual:**
   - **A Windows:**
     ```cmd
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - **A macOS / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Instal·lar les dependències:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Executar:**
   ```bash
   python app.py
   ```

---

## ▶️ Com executar l'aplicació

### Opció 1: Amb el fitxer `.bat` (Windows)
Fes doble clic sobre el fitxer **`run.bat`** o executa'l des del terminal:
```cmd
run.bat
```
*(L'script activarà automàticament l'entorn virtual si existeix i arrencarà el servidor).*

### Opció 2: Mitjançant terminal
```bash
python app.py
```

Un cop arrencat el servidor, obre el navegador web i accedeix a:
👉 **[http://localhost:5000](http://localhost:5000)** (o `http://127.0.0.1:5000`)

---

## 🔑 Configuració de Google Sheets (Opcional)

L'aplicació funciona de manera autònoma amb dades de prova sense necessitat de configurar res. Si es vol connectar amb un compte de servei de Google Sheets real:

1. Crea un projecte a [Google Cloud Console](https://console.cloud.google.com/) i activa l'API de Google Sheets i Google Drive.
2. Genera una clau de **Compte de Servei** (JSON) i desa el fitxer com a `credentials.json` a l'arrel del projecte.
3. Comparteix el Google Sheet (`AE_Lluisos_Database`) amb l'adreça de correu del compte de servei donant-li permisos d'edició.
4. Opcionalment, pots crear un fitxer `.env` per personalitzar paràmetres:
   ```env
   PORT=5000
   SECRET_KEY=la_teva_clau_secreta
   GOOGLE_APPLICATION_CREDENTIALS=credentials.json
   GSHEET_NAME=AE_Lluisos_Database
   ```

---

## 🌐 Endpoints de l'API

| Mètode | Endpoint | Descripció |
|---|---|---|
| `GET` | `/api/novetats` | Retorna el llistat de notícies i novetats |
| `GET` | `/api/calendari` | Retorna la llista d'esdeveniments del calendari |
| `GET` | `/api/caps` | Retorna els membres de l'equip de caps |
| `GET` | `/api/foulard` | Retorna les xinxetes del mapa del foulard |
| `GET` | `/api/shop` | Retorna els productes de la botiga |
| `POST` | `/api/kiniela/save` | Desa una nova participació de la quiniela |

---

## 📝 Llicència

Projecte desenvolupat per a l'**AE Lluïsos de Gràcia**.
