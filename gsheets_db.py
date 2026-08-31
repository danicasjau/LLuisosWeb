import os
import json
import logging
import datetime
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GSheetsDB:
    def __init__(self, credentials_path="credentials.json", sheet_name="AE_Lluisos_Database"):
        self.credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", credentials_path)
        self.sheet_name = os.getenv("GSHEET_NAME", sheet_name)
        self.client = None
        self._init_client()

    def _init_client(self):
        """Initializes gspread client if credentials file is present."""
        if os.path.exists(self.credentials_path):
            try:
                import gspread
                self.client = gspread.service_account(filename=self.credentials_path)
                logger.info("Successfully connected to Google Sheets API with gspread.")
            except Exception as e:
                logger.warning(f"gspread initialization failed: {e}. Falling back to CSV/Mock data.")
                self.client = None
        else:
            logger.info(f"No Google credentials found at '{self.credentials_path}'. Using dynamic fallback dataset.")

    def _fetch_sheet_records(self, worksheet_name):
        """Fetches records from Google Sheets if available, else returns None."""
        if self.client:
            try:
                sheet = self.client.open(self.sheet_name).worksheet(worksheet_name)
                return sheet.get_all_records()
            except Exception as e:
                logger.warning(f"Error fetching worksheet '{worksheet_name}' via gspread: {e}")

        # Check for published CSV URLs via environment variables
        csv_url = os.getenv(f"GSHEET_CSV_{worksheet_name.upper()}")
        if csv_url:
            try:
                import csv
                import io
                resp = requests.get(csv_url, timeout=5)
                if resp.status_code == 200:
                    reader = csv.DictReader(io.StringIO(resp.text))
                    return list(reader)
            except Exception as e:
                logger.warning(f"Error fetching CSV for worksheet '{worksheet_name}': {e}")
        
        return None

    def save_kiniela(self, creator_name, kiniela_data):
        """Save a new Kiniela prediction to Google Sheets (Worksheet: 'Kiniela')"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_str = json.dumps(kiniela_data, ensure_ascii=False)
        
        saved_online = False
        if self.client:
            try:
                spreadsheet = self.client.open(self.sheet_name)
                try:
                    worksheet = spreadsheet.worksheet("Kiniela")
                except Exception:
                    worksheet = spreadsheet.add_worksheet(title="Kiniela", rows="500", cols="4")
                    worksheet.append_row(["Timestamp", "Creator Name", "Assignments JSON"])
                
                worksheet.append_row([timestamp, creator_name, data_str])
                saved_online = True
                logger.info(f"Successfully saved Kiniela prediction for '{creator_name}' to Google Sheets!")
            except Exception as e:
                logger.warning(f"Failed to save to Google Sheets directly: {e}")

        # Fallback local persistence (kiniela_submissions.json)
        local_file = "kiniela_submissions.json"
        submissions = []
        if os.path.exists(local_file):
            try:
                with open(local_file, "r", encoding="utf-8") as f:
                    submissions = json.load(f)
            except Exception:
                submissions = []
        
        new_entry = {
            "id": len(submissions) + 1,
            "timestamp": timestamp,
            "creator_name": creator_name,
            "assignments": kiniela_data,
            "saved_online": saved_online
        }
        submissions.append(new_entry)
        
        with open(local_file, "w", encoding="utf-8") as f:
            json.dump(submissions, f, indent=2, ensure_ascii=False)
            
        return {
            "status": "success",
            "message": f"Kiniela de {creator_name} guardada correctament a la base de dades!",
            "saved_online": saved_online,
            "timestamp": timestamp
        }

    def get_novetats(self):
        """Fetch news and posts for novetats.html"""
        records = self._fetch_sheet_records("Novetats")
        if records:
            return records
        
        return [
            {
                "id": 1,
                "title": "CIM AL K2: L'EXPEDICIÓ D'HIVERN DELS TRUCS",
                "date": "15 AGOST 2026",
                "tag": "EXPEDICIÓ",
                "author": "Equip de Caps",
                "excerpt": "28,000 PEUS. PENJATS DELS DITS. L'adrenalina pura dels nostres equips conquerint els pics més alts del Pirineu en la nova ruta d'hivern.",
                "content": "Els nois i noies de la unitat de Trucs han completat amb èxit la travessa d'alta muntanya. Inspirats en l'esperit d'assalt als grans cims, l'activitat ha demostrat el valor del treball en equip, la superació personal i el respecte per la natura.",
                "image": "/static/images/backgroundmountains.png",
                "read_time": "4 min de lectura"
            },
            {
                "id": 2,
                "title": "INICI DEL CURS ESCOLTA 2026-2027 A GRÀCIA",
                "date": "10 AGOST 2026",
                "tag": "ANUNCI",
                "author": "Cap de Agrupament",
                "excerpt": "Obrim inscripcions per a totes les unitats! Des dels més petits Esquirols fins als Pioners i Trucs. Fem barri, fem escoltisme.",
                "content": "Aquest setembre tornem a omplir la Plaça del Nord i el local dels Lluïsos de Gràcia. Prepareu els foulards i les motxilles per a un any ple d'excursions, cau i projectes comunitaris.",
                "image": "/static/images/scout_foulard.jpg",
                "read_time": "3 min de lectura"
            },
            {
                "id": 3,
                "title": "GRANDIOSA FIRA DEL MERCAU DE TARDOR",
                "date": "02 AGOST 2026",
                "tag": "MERCAU",
                "author": "Comissió de Festes",
                "excerpt": "Roba retro, material d'acampada vintage, samarretes de l'agrupament i parada de menjar casolà per finançar el projecte d'estiu.",
                "content": "Us esperem a tots dissabte vinent. Tindrem música en directe, tallers d'amarratges i nusos escoltes, i paradetes amb productes exclusius del nostre Mercau.",
                "image": "/static/images/scout_foulard.jpg",
                "read_time": "5 min de lectura"
            },
            {
                "id": 4,
                "title": "TALLER D'ORIENTACIÓ I CARTOGRAFIA A COLLSEROLA",
                "date": "25 JULIOL 2026",
                "tag": "FORMACIÓ",
                "author": "Muntanya & Natura",
                "excerpt": "Com orientar-se amb mapa topogràfic i brúixola sense GPS. Una jornada pràctica per a Ràngers i Noies Guies.",
                "content": "Saber llegir les corbes de nivell i interpretar el relleu és fonamental per a qualsevol escolta. La sortida pràctica de dissabte va ser un èxit total.",
                "image": "/static/images/backgroundmountains.png",
                "read_time": "2 min de lectura"
            }
        ]

    def get_calendar_events(self):
        """Fetch events for calendari.html"""
        records = self._fetch_sheet_records("Calendari")
        if records:
            return records
        
        return [
            {
                "id": 101,
                "title": "Cau de Benvinguda i Passos d'Unitat",
                "date": "2026-09-12",
                "time": "16:00 - 19:30",
                "location": "Plaça del Nord, Gràcia",
                "unit": "Totes les unitats",
                "badge_color": "#FF5722",
                "description": "Benvinguda al nou curs escolta! Jocs de retrobament, presentació de nous caps i cerimònia dels passos de branca."
            },
            {
                "id": 102,
                "title": "Excursió de cap de setmana al Montseny",
                "date": "2026-09-26",
                "time": "Dissabte 08:00 - Diumenge 18:00",
                "location": "Sant Celoni - Turó de l'Home",
                "unit": "Ràngers i Pioners",
                "badge_color": "#1B4965",
                "description": "Primera sortida amb nit en tendes del curs. Ruta de 18km amb desnivell positiu i taller d'estrelles."
            },
            {
                "id": 103,
                "title": "Assemblea General d'Agrupament (AGA)",
                "date": "2026-10-03",
                "time": "18:30 - 21:00",
                "location": "Local AE Lluïsos de Gràcia",
                "unit": "Famílies i Caps",
                "badge_color": "#0B2545",
                "description": "Presentació del projecte educatiu anual, pressupostos i elecció de la nova línia pedagògica."
            },
            {
                "id": 104,
                "title": "Fira d'Agrupament i Trobada de Tardor",
                "date": "2026-10-17",
                "time": "10:00 - 20:00",
                "location": "Plaça de la Revolució, Gràcia",
                "unit": "Comunitat i Barri",
                "badge_color": "#FF5722",
                "description": "Paradetes artesanes, intercanvi de material escolta vintage, vermut musical i jocs per a la mainada."
            }
        ]

    def get_caps(self):
        """Fetch team members for caps.html and equips.html"""
        records = self._fetch_sheet_records("Caps")
        if records:
            return records
        
        return [
            {
                "id": 1,
                "name": "Marc Vila i Soler",
                "role": "Cap d'Agrupament & Logística",
                "unit": "Equip de Coordinació",
                "unit_code": "coordinacio",
                "years": "7 anys a l'agrupament",
                "bio": "Passionat per la cartografia de muntanya, el trekking i la pedagogia activa.",
                "image": "/static/images/scout_team.jpg",
                "quote": "\"Deixar el món un xic millor de com l'hem trobat.\""
            },
            {
                "id": 2,
                "name": "Larraitz Echeverria",
                "role": "Cap de Branca - Truk",
                "unit": "Truk (18-20 anys)",
                "unit_code": "truk",
                "years": "5 anys a l'agrupament",
                "bio": "Estudiant de Ciències Ambientals. Lidera els projectes d'internacionalització i servei.",
                "image": "/static/images/scout_team.jpg",
                "quote": "\"L'escoltisme és una actitud davant la vida.\""
            },
            {
                "id": 3,
                "name": "Guillem Pujol i Roca",
                "role": "Cap de Branca - Pionel·les",
                "unit": "Pionel·les (15-17 anys)",
                "unit_code": "pios",
                "years": "6 anys a l'agrupament",
                "bio": "Expert en pionerisme, grans travesses pirinenques i construccions de campament.",
                "image": "/static/images/scout_team.jpg",
                "quote": "\"Sempre a punt!\""
            },
            {
                "id": 4,
                "name": "Aina Fontcuberta",
                "role": "Cap de Branca - Ranguis",
                "unit": "Ranguis (12-14 anys)",
                "unit_code": "ranguis",
                "years": "4 anys a l'agrupament",
                "bio": "Mestra d'educació primària. Coordina les dinàmiques de grup i expressió artística.",
                "image": "/static/images/scout_team.jpg",
                "quote": "\"Tots junts fem la pinya més petita i resistent.\""
            },
            {
                "id": 5,
                "name": "Pol Serra i Bosch",
                "role": "Cap de Branca - Dainops",
                "unit": "Dainops (9-11 anys)",
                "unit_code": "llops",
                "years": "4 anys a l'agrupament",
                "bio": "Entusiasta de la natura i els jocs d'orientació al bosc. Dinamitzador incansable.",
                "image": "/static/images/scout_team.jpg",
                "quote": "\"La millor aventura és la que fem plegats.\""
            },
            {
                "id": 6,
                "name": "Clara Rius i Mas",
                "role": "Cap de Branca - Castúdrigues",
                "unit": "Castúdrigues (6-8 anys)",
                "unit_code": "castors",
                "years": "3 anys a l'agrupament",
                "bio": "Especialista en contacontes, creativitat i primers passos a la muntanya.",
                "image": "/static/images/scout_team.jpg",
                "quote": "\"Fent camí pas a pas, des de la rialla.\""
            },
            {
                "id": 7,
                "name": "Pau Soler i Costa",
                "role": "Equip Pedagògic - Ranguis",
                "unit": "Ranguis (12-14 anys)",
                "unit_code": "ranguis",
                "years": "3 anys a l'agrupament",
                "bio": "Organitzador d'activitats de cohesió i formació de caps.",
                "image": "/static/images/scout_team.jpg",
                "quote": "\"Aprendre fent, viure compartint.\""
            },
            {
                "id": 8,
                "name": "Meritxell Balaguer",
                "role": "Equip Pedagògic - Pionel·les",
                "unit": "Pionel·les (15-17 anys)",
                "unit_code": "pios",
                "years": "5 anys a l'agrupament",
                "bio": "Formadora en primers auxilis a la muntanya i suport psicològic.",
                "image": "/static/images/scout_team.jpg",
                "quote": "\"Cap cim és massa alt amb un bon equip.\""
            },
            {
                "id": 9,
                "name": "Ignasi Mas i Valls",
                "role": "Responsable de Material & Marxen",
                "unit": "Marxen (+20 anys)",
                "unit_code": "marxen",
                "years": "8 anys a l'agrupament",
                "bio": "Gestió del local, tendes de campanya i suport als antics membres.",
                "image": "/static/images/scout_team.jpg",
                "quote": "\"El caliu del foc de camp mai s'apaga.\""
            },
            {
                "id": 10,
                "name": "Berta Canal i Sala",
                "role": "Cap de Branca - Dainops",
                "unit": "Dainops (9-11 anys)",
                "unit_code": "llops",
                "years": "3 anys a l'agrupament",
                "bio": "Aficionada a la botànica i fauna pirinenca.",
                "image": "/static/images/scout_team.jpg",
                "quote": "\"Ulls oberts, orelles atentes!\""
            }
        ]

    def get_foulard_pins(self):
        """Fetch map pinpoints for foulard.html"""
        records = self._fetch_sheet_records("FoulardMap")
        if records:
            return records
        
        return [
            {
                "id": 1,
                "title": "Expedició Karakoram Trail",
                "location": "K2 Base Camp, Baltoro Glacier",
                "country": "Pakistan / Himàlaia",
                "lat": 35.8808,
                "lng": 76.5158,
                "year": "2025",
                "unit": "Trucs",
                "description": "Expedició internacional dels Trucs per donar suport a projectes educatius de muntanya.",
                "type": "expedition"
            },
            {
                "id": 2,
                "title": "Local Social AE Lluïsos de Gràcia",
                "location": "Plaça del Nord, Gràcia (Barcelona)",
                "country": "Catalunya",
                "lat": 41.4048,
                "lng": 2.1554,
                "year": "Des de 1957",
                "unit": "Seu Central",
                "description": "El cor de l'agrupament. Punt de trobada de cada dissabte de cau.",
                "type": "headquarters"
            }
        ]

    def get_shop_products(self):
        """Fetch e-commerce shop products for shop.html"""
        records = self._fetch_sheet_records("Shop")
        if records:
            return records
        
        return [
            {
                "id": 1,
                "name": "Foulard Oficial Lluïsos de Gràcia",
                "price": 12.00,
                "category": "Foulards",
                "tag": "RETRO EDITION",
                "image": "/static/images/scout_foulard.jpg",
                "description": "El foulard tradicional de l'agrupament en blau marí i verd ampolla amb la sanefa cosida a mà.",
                "in_stock": True
            },
            {
                "id": 2,
                "name": "Dessuadora Vintage Scouting",
                "price": 32.00,
                "category": "Roba",
                "tag": "BESTSELLER",
                "image": "/static/images/backgroundmountains.png",
                "description": "Dessuadora de cotó d'alta gramatge amb caputxa i logotip de l'agrupament.",
                "in_stock": True
            }
        ]

# Global DB Instance
db = GSheetsDB()
