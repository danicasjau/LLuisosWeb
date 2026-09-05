import os
import json
import logging
import datetime
import hashlib
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GSheetsDB:
    def __init__(self, credentials_path="credentials.json", sheet_name="AE_Lluisos_Database"):
        self.credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", credentials_path)
        self.sheet_name = os.getenv("GSHEET_NAME", sheet_name)
        self.client = None
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        os.makedirs(self.data_dir, exist_ok=True)
        self._init_client()
        self._init_json_store()

    def _data_file(self, filename):
        return os.path.join(self.data_dir, filename)

    def _read_data(self, filename, default_val=None):
        filepath = self._data_file(filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Error reading {filepath}: {e}")
        return default_val if default_val is not None else []

    def _write_data(self, filename, data):
        filepath = self._data_file(filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Error writing {filepath}: {e}")
            return False

    def _init_json_store(self):
        """Initializes JSON data storage from defaults if files do not already exist."""
        # 1. Password verification store
        contra_file = self._data_file("contra.json")
        if not os.path.exists(contra_file):
            salt = "ae_lluisos_gracia_salt_2026"
            default_hash = hashlib.sha256((salt + "caps2026").encode('utf-8')).hexdigest()
            self._write_data("contra.json", {
                "algorithm": "sha256_salted",
                "salt": salt,
                "contra_hash": default_hash,
                "note": "AE Lluïsos de Gràcia - Contrasenya per defecte: caps2026"
            })

        # 2. Novetats store
        novetats_file = self._data_file("novetats.json")
        if not os.path.exists(novetats_file):
            self._write_data("novetats.json", self._default_novetats())

        # 3. Calendari store
        cal_file = self._data_file("calendari.json")
        if not os.path.exists(cal_file):
            self._write_data("calendari.json", self._default_calendar_events())

        # 4. Foulard pins store
        foulard_file = self._data_file("foulard.json")
        if not os.path.exists(foulard_file):
            self._write_data("foulard.json", self._default_foulard_pins())

        # 5. Shop store
        shop_file = self._data_file("shop.json")
        if not os.path.exists(shop_file):
            self._write_data("shop.json", self._default_shop_products())

    def verify_contra(self, password):
        """Verify password against data/contra.json with basic salt+sha256 encryption."""
        data = self._read_data("contra.json", None)
        salt = "ae_lluisos_gracia_salt_2026"
        expected = hashlib.sha256((salt + "caps2026").encode('utf-8')).hexdigest()
        if data and isinstance(data, dict):
            salt = data.get("salt", salt)
            expected = data.get("contra_hash", expected)
        computed = hashlib.sha256((salt + str(password).strip()).encode('utf-8')).hexdigest()
        return computed == expected

    def set_contra(self, new_password):
        """Update password in data/contra.json."""
        salt = "ae_lluisos_gracia_salt_2026"
        computed = hashlib.sha256((salt + str(new_password).strip()).encode('utf-8')).hexdigest()
        payload = {
            "algorithm": "sha256_salted",
            "salt": salt,
            "contra_hash": computed,
            "updated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return self._write_data("contra.json", payload)


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
        """Fetch news and posts from JSON store (with fallback)."""
        records = self._read_data("novetats.json", None)
        if records and len(records) > 0:
            return records
        defaults = self._default_novetats()
        self._write_data("novetats.json", defaults)
        return defaults

    def add_novetat(self, data):
        """Add a new novetat to JSON database."""
        items = self.get_novetats()
        next_id = max([item.get('id', 0) for item in items], default=0) + 1
        new_post = {
            "id": next_id,
            "title": data.get('title', '').strip(),
            "date": data.get('date', datetime.datetime.now().strftime("%d %b %Y")).strip().upper(),
            "tag": data.get('tag', 'GENERAL').strip().upper(),
            "author": data.get('author', 'Equip de Caps').strip(),
            "excerpt": data.get('excerpt', '').strip(),
            "content": data.get('content', '').strip(),
            "image": data.get('image', '/static/images/scout_foulard.jpg').strip() or '/static/images/scout_foulard.jpg',
            "read_time": data.get('read_time', '3 min de lectura').strip()
        }
        items.insert(0, new_post)
        self._write_data("novetats.json", items)
        return new_post

    def delete_novetat(self, post_id):
        """Remove a novetat by id."""
        items = self.get_novetats()
        items = [x for x in items if str(x.get('id')) != str(post_id)]
        self._write_data("novetats.json", items)
        return True

    def _default_novetats(self):
        """Default seed news and posts for novetats.html"""
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
        """Fetch events from JSON store across the scout year."""
        records = self._read_data("calendari.json", None)
        if records and len(records) > 0:
            return records
        defaults = self._default_calendar_events()
        self._write_data("calendari.json", defaults)
        return defaults

    def add_calendar_event(self, data):
        """Add a new calendar event."""
        events = self.get_calendar_events()
        next_id = max([e.get('id', 0) for e in events], default=100) + 1
        new_event = {
            "id": next_id,
            "title": data.get('title', '').strip(),
            "date": data.get('date', '').strip(),
            "time": data.get('time', '16:30 - 19:00').strip(),
            "location": data.get('location', 'Local AE Lluïsos de Gràcia').strip(),
            "unit": data.get('unit', 'Assemblea & General').strip(),
            "badge_color": data.get('badge_color', '#0B2545').strip(),
            "image": data.get('image', '/static/images/scout_foulard.jpg').strip() or '/static/images/scout_foulard.jpg',
            "description": data.get('description', '').strip()
        }
        events.append(new_event)
        events.sort(key=lambda x: str(x.get('date', '')))
        self._write_data("calendari.json", events)
        return new_event

    def update_calendar_event(self, event_id, data):
        """Update an existing calendar event by id."""
        events = self.get_calendar_events()
        for idx, event in enumerate(events):
            if str(event.get('id')) == str(event_id):
                event['title'] = data.get('title', event['title']).strip()
                event['date'] = data.get('date', event['date']).strip()
                event['time'] = data.get('time', event.get('time', '')).strip()
                event['location'] = data.get('location', event.get('location', '')).strip()
                event['unit'] = data.get('unit', event.get('unit', '')).strip()
                event['badge_color'] = data.get('badge_color', event.get('badge_color', '#0B2545')).strip()
                if data.get('image'):
                    event['image'] = data.get('image').strip()
                event['description'] = data.get('description', event.get('description', '')).strip()
                events[idx] = event
                events.sort(key=lambda x: str(x.get('date', '')))
                self._write_data("calendari.json", events)
                return event
        return None

    def delete_calendar_event(self, event_id):
        """Remove a calendar event by id."""
        events = self.get_calendar_events()
        events = [x for x in events if str(x.get('id')) != str(event_id)]
        self._write_data("calendari.json", events)
        return True

    def _default_calendar_events(self):
        """Fetch events for calendar.html and calendari.html across the 2026-2027 scout year"""
        records = self._fetch_sheet_records("Calendari")
        if records:
            return records
        
        return [
            # --- SETEMBRE 2026 ---
            {
                "id": 101,
                "title": "Passos d'Unitat i Cau de Benvinguda",
                "date": "2026-09-12",
                "time": "16:00 - 19:30",
                "location": "Plaça del Nord, Gràcia",
                "unit": "Assemblea & General",
                "badge_color": "#0B2545",
                "image": "/static/images/scout_foulard.jpg",
                "description": "Inici oficial del curs 2026-2027. Jocs de retrobament, presentació dels equips de caps i cerimònia de passos de branca a la plaça."
            },
            {
                "id": 102,
                "title": "Primer Cau de Branca i Dinàmica de Colla",
                "date": "2026-09-19",
                "time": "16:30 - 19:00",
                "location": "Local Lluïsos de Gràcia",
                "unit": "Castúdrigues",
                "badge_color": "#F97316",
                "image": "/static/images/backgroundmountains.png",
                "description": "Coneixença dels nous castors i llúdrigues, creació de les sisenes i descoberta del cau secret."
            },
            {
                "id": 103,
                "title": "Excursió de Bivac al Montseny",
                "date": "2026-09-26",
                "time": "Dissabte 08:00 - Diumenge 18:00",
                "location": "Sant Celoni - Turó de l'Home",
                "unit": "Ranguis",
                "badge_color": "#0284C7",
                "image": "/static/images/backgroundmountains.png",
                "description": "Primera sortida amb nit sota les estrelles del curs. Ruta de muntanya de 14km i taller d'orientació amb brúixola."
            },
            {
                "id": 104,
                "title": "Trobada de Responsables de Sector MEG",
                "date": "2026-09-27",
                "time": "10:00 - 14:00",
                "location": "Seu Central MEG (Barcelona)",
                "unit": "MEG",
                "badge_color": "#7C3AED",
                "image": "/static/images/scout_foulard.jpg",
                "description": "Coordinació pedagògica de la Demarcació del Barcelonès i planificació dels projectes de sector per al curs."
            },

            # --- OCTUBRE 2026 ---
            {
                "id": 105,
                "title": "Assemblea General d'Agrupament (AGA)",
                "date": "2026-10-03",
                "time": "18:30 - 21:00",
                "location": "Local AE Lluïsos de Gràcia",
                "unit": "Assemblea & General",
                "badge_color": "#0B2545",
                "image": "/static/images/scout_foulard.jpg",
                "description": "Aprovació del projecte educatiu de curs, memòria econòmica, renovació de càrrecs i trobada de famílies."
            },
            {
                "id": 106,
                "title": "Gran Cacera de Tardor dels Llops",
                "date": "2026-10-10",
                "time": "10:00 - 18:30",
                "location": "Parc de Collserola (Can Masdeu)",
                "unit": "Dainops",
                "badge_color": "#F59E0B",
                "image": "/static/images/backgroundmountains.png",
                "description": "Joc de pistes a la natura basat en el Llibre de la Selva, rastreig de petjades i dinar de carmanyola."
            },
            {
                "id": 107,
                "title": "Fira d'Agrupament i Castanyada Popular",
                "date": "2026-10-24",
                "time": "10:00 - 20:00",
                "location": "Plaça de la Revolució, Gràcia",
                "unit": "Assemblea & General",
                "badge_color": "#0B2545",
                "image": "/static/images/scout_foulard.jpg",
                "description": "Parades d'artesania, mercadet vintage, tast de castanyes i moniatos, i actuació musical de l'agrupament."
            },
            {
                "id": 108,
                "title": "Ruta de Descobriment i Servei Truk",
                "date": "2026-10-31",
                "time": "08:00 - 20:00",
                "location": "Serra de Marina (Badalona)",
                "unit": "Truk",
                "badge_color": "#059669",
                "image": "/static/images/backgroundmountains.png",
                "description": "Projecte comunitari de recuperació de camins forestals i debat sobre sobirania alimentària."
            },

            # --- NOVEMBRE 2026 ---
            {
                "id": 109,
                "title": "Raid de Supervivència i Pionerisme",
                "date": "2026-11-07",
                "time": "Dissabte 08:30 - Diumenge 17:00",
                "location": "Parc Natural de Sant Llorenç del Munt",
                "unit": "Pionel·les",
                "badge_color": "#E11D48",
                "image": "/static/images/backgroundmountains.png",
                "description": "Construccions de fusta amb amarratges i nusos, cuina d'acampada i ascensió a la Mola."
            },
            {
                "id": 110,
                "title": "Taller d'Ecologia i Horta Urbana",
                "date": "2026-11-14",
                "time": "16:00 - 19:00",
                "location": "Hort Comunitari de Gràcia",
                "unit": "Castúdrigues",
                "badge_color": "#F97316",
                "image": "/static/images/scout_foulard.jpg",
                "description": "Descobrim la biodiversitat de l'hort, plantem llavors d'hivern i fem menjadores per a ocells."
            },
            {
                "id": 111,
                "title": "Consell de Roca i Consell d'Honor",
                "date": "2026-11-21",
                "time": "16:30 - 19:30",
                "location": "Local Lluïsos de Gràcia",
                "unit": "Dainops",
                "badge_color": "#F59E0B",
                "image": "/static/images/scout_foulard.jpg",
                "description": "Avaluació del primer trimestre i compromís dels llobatons amb la Llei de la Selva."
            },
            {
                "id": 112,
                "title": "Jornada de Formació MEG per a Caps",
                "date": "2026-11-28",
                "time": "09:30 - 18:00",
                "location": "Casal de Joves Can Ricart (Poblenou)",
                "unit": "MEG",
                "badge_color": "#7C3AED",
                "image": "/static/images/scout_foulard.jpg",
                "description": "Formació en primers auxilis en muntanya, gestió emocional i coeducació per als equips de caps de Catalunya."
            },

            # --- DESEMBRE 2026 ---
            {
                "id": 113,
                "title": "Llum de la Pau de Betlem (MEG)",
                "date": "2026-12-12",
                "time": "17:00 - 20:30",
                "location": "Basílica de Santa Maria del Mar",
                "unit": "MEG",
                "badge_color": "#7C3AED",
                "image": "/static/images/scout_foulard.jpg",
                "description": "Acte central de rebuda de la Llum de la Pau i distribució pels barris i agrupaments escoltes."
            },
            {
                "id": 114,
                "title": "Campament d'Hivern d'Agrupament",
                "date": "2026-12-27",
                "time": "27 Desembre - 30 Desembre",
                "location": "Casa de Colònies La Traüna (Montseny)",
                "unit": "Assemblea & General",
                "badge_color": "#0B2545",
                "image": "/static/images/backgroundmountains.png",
                "description": "4 dies de convivència de totes les branques, focs de camp, vetllades d'hivern i tallers artesanals."
            },

            # --- GENER 2027 ---
            {
                "id": 115,
                "title": "Cau de Reis i Jocs de Taula Gegants",
                "date": "2027-01-09",
                "time": "16:00 - 19:30",
                "location": "Plaça del Nord, Gràcia",
                "unit": "Castúdrigues",
                "badge_color": "#F97316",
                "image": "/static/images/scout_foulard.jpg",
                "description": "Retrobament després de festes, jocs tradicionals cooperatius i berenar amb xocolatada."
            },
            {
                "id": 116,
                "title": "Travessa de Neu i Raquetes",
                "date": "2027-01-23",
                "time": "Dissabte 06:30 - Diumenge 19:00",
                "location": "Vall de Núria - Puigmal",
                "unit": "Truk",
                "badge_color": "#059669",
                "image": "/static/images/backgroundmountains.png",
                "description": "Itinerari d'alta muntanya amb raquetes de neu, bivac hivernal i formació en seguretat davant allaus."
            },

            # --- FEBRER 2027 ---
            {
                "id": 117,
                "title": "Gran Calçotada Escoltes de Gràcia",
                "date": "2027-02-06",
                "time": "11:00 - 18:00",
                "location": "Masia Can Soler (Collserola)",
                "unit": "Assemblea & General",
                "badge_color": "#0B2545",
                "image": "/static/images/scout_foulard.jpg",
                "description": "Trobada festiva per a famílies, antics escoltes, caps i infants amb foc de llenya i dinar comunitari."
            },
            {
                "id": 118,
                "title": "Dia del Pensament Escolta (Thinking Day - MEG)",
                "date": "2027-02-20",
                "time": "10:00 - 18:00",
                "location": "Parc de la Ciutadella",
                "unit": "MEG",
                "badge_color": "#7C3AED",
                "image": "/static/images/scout_foulard.jpg",
                "description": "Commemoració mundial del naixement de Baden-Powell amb més de 2.000 escoltes d'arreu de Catalunya."
            },
            {
                "id": 119,
                "title": "Campionat d'Orientació i Rastreig",
                "date": "2027-02-27",
                "time": "09:00 - 16:30",
                "location": "Parc del Laberint d'Horta",
                "unit": "Ranguis",
                "badge_color": "#0284C7",
                "image": "/static/images/backgroundmountains.png",
                "description": "Cursa d'orientació amb balises cronometrades i reptes de lògica per patrulles."
            },

            # --- MARÇ 2027 ---
            {
                "id": 120,
                "title": "Projecte Comunitari: Neteja del Litoral",
                "date": "2027-03-13",
                "time": "09:30 - 15:00",
                "location": "Platja de la Mar Bella",
                "unit": "Pionel·les",
                "badge_color": "#E11D48",
                "image": "/static/images/scout_foulard.jpg",
                "description": "Acció de voluntariat ambiental per recollir microplàstics i sensibilitzar sobre l'impacte marí."
            },
            {
                "id": 121,
                "title": "Excursió de Primavera al Pedraforca",
                "date": "2027-03-27",
                "time": "Dissabte 07:00 - Diumenge 18:00",
                "location": "Gósol - Refugi Lluís Estasen",
                "unit": "Truk",
                "badge_color": "#059669",
                "image": "/static/images/backgroundmountains.png",
                "description": "Ruta clàssica als contraforts del Pedraforca, observació de fauna pirinenca i nit al refugi."
            },

            # --- ABRIL 2027 ---
            {
                "id": 122,
                "title": "Campament de Pasqua per Branques",
                "date": "2027-04-10",
                "time": "10 Abril - 12 Abril",
                "location": "Ripollès / Garrotxa",
                "unit": "Assemblea & General",
                "badge_color": "#0B2545",
                "image": "/static/images/backgroundmountains.png",
                "description": "Sortides simultànies de cap de setmana llarg per a totes les unitats en terreny de muntanya."
            },
            {
                "id": 123,
                "title": "Diada de Sant Jordi a la Plaça del Nord",
                "date": "2027-04-23",
                "time": "09:00 - 20:30",
                "location": "Plaça del Nord, Gràcia",
                "unit": "Assemblea & General",
                "badge_color": "#0B2545",
                "image": "/static/images/scout_foulard.jpg",
                "description": "Parada oficial de roses, llibres escoltes de segona mà, punt de lectura infantil i cançons de bressol."
            },

            # --- MAIG 2027 ---
            {
                "id": 124,
                "title": "Gran Bivac d'Unitat sota el Cel de Montserrat",
                "date": "2027-05-08",
                "time": "Dissabte 08:00 - Diumenge 17:00",
                "location": "Monestir de Montserrat - Sant Jeroni",
                "unit": "Ranguis",
                "badge_color": "#0284C7",
                "image": "/static/images/backgroundmountains.png",
                "description": "Pujada per les escales dels Pobres, nit al cim de Sant Jeroni i observació d'estels amb telescopi."
            },
            {
                "id": 125,
                "title": "Assemblea de Primavera MEG del Barcelonès",
                "date": "2027-05-15",
                "time": "10:00 - 17:00",
                "location": "Ateneu de Gràcia",
                "unit": "MEG",
                "badge_color": "#7C3AED",
                "image": "/static/images/scout_foulard.jpg",
                "description": "Balanç dels projectes de la demarcació i aprovació de les línies de campaments d'estiu."
            },
            {
                "id": 126,
                "title": "Olimpíades Escoltes Inter-Agrupaments",
                "date": "2027-05-29",
                "time": "10:00 - 18:30",
                "location": "Pista Poliesportiva del Guinardó",
                "unit": "Dainops",
                "badge_color": "#F59E0B",
                "image": "/static/images/scout_foulard.jpg",
                "description": "Jocs esportius, curses de sacs, estirar la corda i relleus cooperatius amb agrupaments veïns."
            },

            # --- JUNY 2027 ---
            {
                "id": 127,
                "title": "Assemblea de Pares i Presentació de Campaments",
                "date": "2027-06-05",
                "time": "18:00 - 20:30",
                "location": "Local Lluïsos de Gràcia",
                "unit": "Assemblea & General",
                "badge_color": "#0B2545",
                "image": "/static/images/scout_foulard.jpg",
                "description": "Reunió informativa clau sobre la logística, material i fitxes mèdiques dels campaments d'estiu 2027."
            },
            {
                "id": 128,
                "title": "Festa de Cloenda del Curs i Sopar de Carmanyola",
                "date": "2027-06-19",
                "time": "17:00 - 23:00",
                "location": "Plaça del Nord, Gràcia",
                "unit": "Assemblea & General",
                "badge_color": "#0B2545",
                "image": "/static/images/scout_foulard.jpg",
                "description": "Vídeo resum de curs, actuacions de les unitats, lliurament d'insígnies i concert acústic de caps."
            },

            # --- JULIOL 2027 ---
            {
                "id": 129,
                "title": "Campament d'Estiu: Pirineus 2027",
                "date": "2027-07-10",
                "time": "10 Juliol - 24 Juliol",
                "location": "Vall de Cardós (Pallars Sobirà)",
                "unit": "Assemblea & General",
                "badge_color": "#0B2545",
                "image": "/static/images/backgroundmountains.png",
                "description": "El gran esdeveniment de l'any! 15 dies de tendes, cuina de campament, rutes de muntanya i banys de riu."
            },
            {
                "id": 130,
                "title": "Expedició Internacional Pionel·les & Truk",
                "date": "2027-07-26",
                "time": "26 Juliol - 08 Agost",
                "location": "Kandersteg International Scout Centre (Suïssa)",
                "unit": "Pionel·les",
                "badge_color": "#E11D48",
                "image": "/static/images/backgroundmountains.png",
                "description": "Experiència internacional al centre scout mundial dels Alps suïssos amb joves de més de 50 països."
            },

            # --- AGOST 2027 ---
            {
                "id": 131,
                "title": "Travessa d'Alta Ruta Truk al Mont Blanc",
                "date": "2027-08-10",
                "time": "10 Agost - 18 Agost",
                "location": "Massís del Mont Blanc (Chamonix)",
                "unit": "Truk",
                "badge_color": "#059669",
                "image": "/static/images/backgroundmountains.png",
                "description": "Ruta circular alpina d'alta exigència per als nois i noies de la unitat gran de l'agrupament."
            },
            {
                "id": 132,
                "title": "Reunió de Coordinació Pedagògica MEG Estiu",
                "date": "2027-08-28",
                "time": "11:00 - 15:00",
                "location": "Seu Central MEG (Barcelona)",
                "unit": "MEG",
                "badge_color": "#7C3AED",
                "image": "/static/images/scout_foulard.jpg",
                "description": "Avaluació dels campaments d'estiu i preparació de la campanya d'inscripcions 2027-2028."
            },

            # --- SETEMBRE 2027 ---
            {
                "id": 133,
                "title": "Consell de Caps d'Inici de Curs 2027-2028",
                "date": "2027-09-04",
                "time": "09:30 - 18:00",
                "location": "Local Lluïsos de Gràcia",
                "unit": "Assemblea & General",
                "badge_color": "#0B2545",
                "image": "/static/images/scout_foulard.jpg",
                "description": "Planificació estratègica de l'equip de caps per al nou curs i assignació de responsabilitats."
            },
            {
                "id": 134,
                "title": "Passos de Branca i Obertura Curs 2027-2028",
                "date": "2027-09-18",
                "time": "16:00 - 19:30",
                "location": "Plaça del Nord, Gràcia",
                "unit": "Assemblea & General",
                "badge_color": "#0B2545",
                "image": "/static/images/scout_foulard.jpg",
                "description": "Benvinguda al curs 2027-2028, cerimònia dels passos d'unitat i retrobament de tota la comunitat escolta."
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
                "name": "Joana Solà",
                "role": "Cap de Branca",
                "unit": "Castúdrigues",
                "unit_code": "castors",
                "years": "3 anys a l'agrupament",
                "bio": "Creu que la millor manera d'aprendre és riure, jugar i fer petits grans projectes amb la gent del cau.",
                "image": "https://api.dicebear.com/9.x/bottts/svg?seed=Joana%20Sola&backgroundColor=FDE68A,FFC0CB,F8FAFC&hairColor=2F1B12&skinColor=F5D0A9",
                "quote": "\"Cada aventura comença amb un gran somriure.\""
            },
            {
                "id": 2,
                "name": "Maia de Cook",
                "role": "Cap de Branca",
                "unit": "Castúdrigues",
                "unit_code": "castors",
                "years": "2 anys a l'agrupament",
                "bio": "Entusiasta de la natura i dels jocs d'orientació. Vol ajudar cada infant a trobar el seu ritme i confiança.",
                "image": "https://api.dicebear.com/9.x/bottts/svg?seed=Maia%20de%20Cook&backgroundColor=C7D2FE,E0F2FE,F8FAFC&hairColor=3B2F2F&skinColor=E7C7A2",
                "quote": "\"Que cada passejada ens ajudi a créixer.\""
            },
            {
                "id": 3,
                "name": "Guillem Rodon",
                "role": "Cap de Branca",
                "unit": "Castúdrigues",
                "unit_code": "castors",
                "years": "4 anys a l'agrupament",
                "bio": "Apassionat de les rutes, la convivència i els projectes col·lectius que fan créixer l'equip.",
                "image": "https://api.dicebear.com/9.x/bottts/svg?seed=Guillem%20Rodon&backgroundColor=FDE68A,DBEAFE,F8FAFC&hairColor=1F2937&skinColor=D8A47B",
                "quote": "\"El bon camí es fa amb companys.\""
            },
            {
                "id": 4,
                "name": "Bernat Escolà",
                "role": "Cap de Branca",
                "unit": "Castúdrigues",
                "unit_code": "castors",
                "years": "5 anys a l'agrupament",
                "bio": "Lidera projectes de muntanya i de grup amb molta cura, previsió i energia positiva.",
                "image": "https://api.dicebear.com/9.x/bottts/svg?seed=Bernat%20Escola&backgroundColor=FECACA,FDE68A,F8FAFC&hairColor=201A1A&skinColor=D7A07F",
                "quote": "\"Cada repte és una oportunitat per aprendre.\""
            },
            {
                "id": 5,
                "name": "Sol Font",
                "role": "Cap de Branca",
                "unit": "Dainops",
                "unit_code": "llops",
                "years": "6 anys a l'agrupament",
                "bio": "Treballa per donar espai a la iniciativa dels joves i promoure la responsabilitat compartida.",
                "image": "https://api.dicebear.com/9.x/bottts/svg?seed=Sol%20Font&backgroundColor=BBF7D0,CCFBF1,F8FAFC&hairColor=4B2E2E&skinColor=EAC7A3",
                "quote": "\"L'autonomia es construeix amb confiança.\""
            },
            {
                "id": 6,
                "name": "Clara Torres",
                "role": "Cap de Branca",
                "unit": "Dainops",
                "unit_code": "llops",
                "years": "4 anys a l'agrupament",
                "bio": "Especialista en dinamització de grup, lideratge i crear espais on tots es sentin part del projecte.",
                "image": "https://api.dicebear.com/9.x/bottts/svg?seed=Clara%20Torres&backgroundColor=C7D2FE,FDE68A,F8FAFC&hairColor=2D1F1F&skinColor=E7C9A0",
                "quote": "\"La millor pinya s'aconsegueix escoltant-s'hi.\""
            },
            {
                "id": 7,
                "name": "Èlia Coll",
                "role": "Cap de Branca",
                "unit": "Dainops",
                "unit_code": "llops",
                "years": "3 anys a l'agrupament",
                "bio": "Té l'hàbit de convertir cada joc en una experiència d'aprenentatge, companyonia i respecte.",
                "image": "https://api.dicebear.com/9.x/bottts/svg?seed=Elia%20Coll&backgroundColor=E0F2FE,FBCFE8,F8FAFC&hairColor=3A2D2D&skinColor=E4BE95",
                "quote": "\"La natura ens ensenya a compartir.\""
            },
            {
                "id": 8,
                "name": "Maür Roda",
                "role": "Cap de Branca",
                "unit": "Dainops",
                "unit_code": "llops",
                "years": "2 anys a l'agrupament",
                "bio": "Va descobrir que els petits detalls també són grans aventures i que la curiositat és la millor eina.",
                "image": "https://api.dicebear.com/9.x/bottts/svg?seed=Maur%20Roda&backgroundColor=FDE68A,FECACA,F8FAFC&hairColor=3D2A22&skinColor=D6A57E",
                "quote": "\"Petits passos, grans descobertes.\""
            },
            {
                "id": 9,
                "name": "Dani Casadevall",
                "role": "Cap de Branca",
                "unit": "Ranguis",
                "unit_code": "ranguis",
                "years": "4 anys a l'agrupament",
                "bio": "Implicat en activitats de muntanya i en construir una dinàmica de grup segura i divertida.",
                "image": "https://api.dicebear.com/9.x/bottts/svg?seed=Dani%20Casadevall&backgroundColor=DBEAFE,FDE68A,F8FAFC&hairColor=1B1B1B&skinColor=C3895C",
                "quote": "\"La millor aventura es comparteix.\""
            },
            {
                "id": 10,
                "name": "Helena Herranz",
                "role": "Coordinació",
                "unit": "Ranguis",
                "unit_code": "ranguis",
                "years": "6 anys a l'agrupament",
                "bio": "Coordina els equips amb una mirada pedagògica i alhora molt pràctica, sempre amb voluntat de cuidar l'agrupament.",
                "image": "https://api.dicebear.com/9.x/bottts/svg?seed=Helena%20Herranz&backgroundColor=DDD6FE,E0F2FE,F8FAFC&hairColor=4A2F2F&skinColor=E7C7A2",
                "quote": "\"L'organització és el motor de la creativitat.\""
            },
            {
                "id": 11,
                "name": "Iu Sales",
                "role": "Cap de Branca",
                "unit": "Ranguis",
                "unit_code": "ranguis",
                "years": "5 anys a l'agrupament",
                "bio": "Aplica el pensament crític i l'autonomia a cada projecte per ajudar el grup a créixer amb criteri.",
                "image": "https://api.dicebear.com/9.x/bottts/svg?seed=Iu%20Sales&backgroundColor=FDE68A,C7D2FE,F8FAFC&hairColor=2B1D1A&skinColor=C98C56",
                "quote": "\"Quan hi ha confiança, hi ha aventura.\""
            },
            {
                "id": 12,
                "name": "Nil Mitjavila",
                "role": "Cap de Branca",
                "unit": "Pionel·les",
                "unit_code": "pios",
                "years": "3 anys a l'agrupament",
                "bio": "Acosta els nens i nenes al món de l'escoltisme amb creativitat, calma i mucha energia positiva.",
                "image": "https://api.dicebear.com/9.x/bottts/svg?seed=Nil%20Mitjavila&backgroundColor=DBEAFE,FECACA,F8FAFC&hairColor=171717&skinColor=C58D5C",
                "quote": "\"Els petits detalls fan grans records.\""
            },
            {
                "id": 13,
                "name": "Aina Salinas",
                "role": "Cap de Branca",
                "unit": "Pionel·les",
                "unit_code": "pios",
                "years": "5 anys a l'agrupament",
                "bio": "Mou el grup amb mirada servicial, idees clares i molt de compromís amb les persones i la comunitat.",
                "image": "https://api.dicebear.com/9.x/bottts/svg?seed=Aina%20Salinas&backgroundColor=E0F2FE,BBF7D0,F8FAFC&hairColor=4B2E2E&skinColor=E4B48B",
                "quote": "\"Serveix i aprèn amb el grup.\""
            },
            {
                "id": 14,
                "name": "Neus Lloses",
                "role": "Coordinació",
                "unit": "Pionel·les",
                "unit_code": "pios",
                "years": "7 anys a l'agrupament",
                "bio": "Aporta calma, rigor i visió de conjunt per acompanyar els caps i fer créixer el projecte educatiu.",
                "image": "https://api.dicebear.com/9.x/bottts/svg?seed=Neus%20Lloses&backgroundColor=C7D2FE,FDE68A,F8FAFC&hairColor=392B2B&skinColor=D9A77A",
                "quote": "\"La comunitat és la nostra gran aventura.\""
            },
            {
                "id": 15,
                "name": "Joan Roig",
                "role": "Cap de Branca",
                "unit": "Pionel·les",
                "unit_code": "pios",
                "years": "4 anys a l'agrupament",
                "bio": "Motiva els joves amb il·lusió per la muntanya, la feina en equip i l'exploració responsable.",
                "image": "https://api.dicebear.com/9.x/bottts/svg?seed=Joan%20Roig&backgroundColor=FDE68A,DBEAFE,F8FAFC&hairColor=202020&skinColor=C89067",
                "quote": "\"Cada viatge ens fa més grans.\""
            },
            {
                "id": 16,
                "name": "Pol Mer",
                "role": "Cap de Branca",
                "unit": "Pionel·les",
                "unit_code": "pios",
                "years": "4 anys a l'agrupament",
                "bio": "Aporta energia, rigor i curiositat per ajudar els joves a organitzar projectes amb propòsit.",
                "image": "https://api.dicebear.com/9.x/bottts/svg?seed=Pol%20Mer&backgroundColor=C7D2FE,FECACA,F8FAFC&hairColor=1F2937&skinColor=D8A577",
                "quote": "\"Amb voluntat, cap projecte és massa gran.\""
            },
            {
                "id": 17,
                "name": "Arnau Escolà",
                "role": "Cap de Branca",
                "unit": "Truk",
                "unit_code": "truk",
                "years": "3 anys a l'agrupament",
                "bio": "Parla amb naturalitat i seguretat, i sap connectar amb cada infant per crear un ambient de confiança.",
                "image": "https://api.dicebear.com/9.x/bottts/svg?seed=Arnau%20Escola&backgroundColor=DBEAFE,FDE68A,F8FAFC&hairColor=2D1F1F&skinColor=D4A792",
                "quote": "\"La confiança és la base de tot.\""
            },
            {
                "id": 18,
                "name": "Ivet Roig",
                "role": "Cap de Branca",
                "unit": "Truk",
                "unit_code": "truk",
                "years": "2 anys a l'agrupament",
                "bio": "Especialista en crear espais on cada nen i nena pot jugar, explorar i sentir-se acollit.",
                "image": "https://api.dicebear.com/9.x/bottts/svg?seed=Ivet%20Roig&backgroundColor=E0F2FE,FBCFE8,F8FAFC&hairColor=3a2b2b&skinColor=E6BA88",
                "quote": "\"La creativitat obre moltes portes.\""
            },
            {
                "id": 19,
                "name": "Júlia Franquesa",
                "role": "Coordinació",
                "unit": "Truk",
                "unit_code": "truk",
                "years": "6 anys a l'agrupament",
                "bio": "Dona forma a les activitats i projectes amb mirada pedagògica, compromís i molta energia.",
                "image": "https://api.dicebear.com/9.x/bottts/svg?seed=Julia%20Franquesa&backgroundColor=FDE68A,E0F2FE,F8FAFC&hairColor=3C2C2A&skinColor=E3BA8A",
                "quote": "\"La millor educació és la que fa estimar.\""
            },
            {
                "id": 20,
                "name": "Lluc Roda",
                "role": "Cap de Branca",
                "unit": "Truk",
                "unit_code": "truk",
                "years": "5 anys a l'agrupament",
                "bio": "Acompanya els joves en la seva autonomia, fent que cada decisió es converteixi en aprenentatge.",
                "image": "https://api.dicebear.com/9.x/bottts/svg?seed=Lluc%20Roda&backgroundColor=C7D2FE,FECACA,F8FAFC&hairColor=2B2B2B&skinColor=C9865B",
                "quote": "\"Un bon equip és la millor eina de transformació.\""
            },
            {
                "id": 21,
                "name": "Simone García",
                "role": "Cap de Branca",
                "unit": "Truk",
                "unit_code": "truk",
                "years": "3 anys a l'agrupament",
                "bio": "Busca provocar reflexió, diversió i compromís a través de projectes amb valor i sentit.",
                "image": "https://api.dicebear.com/9.x/bottts/svg?seed=Simone%20Garcia&backgroundColor=BBF7D0,FDE68A,F8FAFC&hairColor=1E1B4B&skinColor=D7A47E",
                "quote": "\"La millor manera d'aprendre és fent.\""
            }
        ]

    def get_foulard_pins(self):
        """Fetch map pinpoints from JSON store."""
        records = self._read_data("foulard.json", None)
        if records and len(records) > 0:
            return records
        defaults = self._default_foulard_pins()
        self._write_data("foulard.json", defaults)
        return defaults

    def add_foulard_pin(self, data):
        """Add a new foulard destination pin."""
        pins = self.get_foulard_pins()
        next_id = max([p.get('id', 0) for p in pins], default=0) + 1
        try:
            lat = float(data.get('lat', 41.4048))
            lng = float(data.get('lng', 2.1554))
        except (ValueError, TypeError):
            lat, lng = 41.4048, 2.1554

        new_pin = {
            "id": next_id,
            "title": data.get('title', '').strip(),
            "location": data.get('location', '').strip(),
            "country": data.get('country', '').strip(),
            "lat": lat,
            "lng": lng,
            "year": str(data.get('year', datetime.datetime.now().year)).strip(),
            "unit": data.get('unit', 'General').strip(),
            "description": data.get('description', '').strip(),
            "type": data.get('type', 'expedition').strip()
        }
        pins.append(new_pin)
        self._write_data("foulard.json", pins)
        return new_pin

    def delete_foulard_pin(self, pin_id):
        """Remove a foulard pin by id."""
        pins = self.get_foulard_pins()
        pins = [p for p in pins if str(p.get('id')) != str(pin_id)]
        self._write_data("foulard.json", pins)
        return True

    def _default_foulard_pins(self):
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

    def get_foulard_expeditions(self):
        """Return example expeditions displayed below the Foulard map."""
        expeditions = [
            {
                "id": 1,
                "title": "Travessa dels Pirineus",
                "author": "Aina Franquesa",
                "image": "/static/images/backgroundmountains.png",
                "location": "Vall de Núria, Catalunya",
                "lat": 42.3981,
                "lng": 2.1547,
                "year": "2025",
                "date": "12 de Juliol de 2025",
                "description": "Una travessa entre refugis per descobrir els camins d'alta muntanya i cuidar el territori."
            },
            {
                "id": 2,
                "title": "Camí de Sant Jaume",
                "author": "Marc Vila",
                "image": "/static/images/mountains_cutout.png",
                "location": "Galícia, Estat espanyol",
                "lat": 42.8805,
                "lng": -8.5442,
                "year": "2024",
                "date": "18 d'Agost de 2024",
                "description": "Etapes compartides, converses llargues i una arribada a Santiago construïda entre tots."
            },
            {
                "id": 3,
                "title": "Volta al Mont Blanc",
                "author": "Laia Domènech",
                "image": "/static/images/skyline.jpg",
                "location": "Chamonix, França",
                "lat": 45.9237,
                "lng": 6.8694,
                "year": "2025",
                "date": "6 de Setembre de 2025",
                "description": "Una ruta alpina circular per aprendre a moure'ns amb respecte en un entorn exigent."
            },
            {
                "id": 4,
                "title": "Balcans en Bicicleta",
                "author": "Guillem Pujol",
                "image": "/static/images/scout_foulard.jpg",
                "location": "Llac Ohrid, Macedònia del Nord",
                "lat": 41.1231,
                "lng": 20.8016,
                "year": "2023",
                "date": "22 de Juliol de 2023",
                "description": "Pedalant entre pobles i llacs, amb una mirada oberta a les comunitats que ens acullen."
            },
            {
                "id": 5,
                "title": "Cims de la Patagònia",
                "author": "Clara Rius",
                "image": "/static/images/backgroundmountains.png",
                "location": "Torres del Paine, Xile",
                "lat": -50.9423,
                "lng": -73.4068,
                "year": "2022",
                "date": "4 de Gener de 2022",
                "description": "Una expedició de natura i fotografia per conèixer un dels paisatges més espectaculars del planeta."
            },
            {
                "id": 6,
                "title": "Desert i Estrelles",
                "author": "Pau Soler",
                "image": "/static/images/skyline.jpg",
                "location": "Desert del Sàhara, Marroc",
                "lat": 31.0994,
                "lng": -4.0112,
                "year": "2024",
                "date": "15 de Març de 2024",
                "description": "Nits sota les estrelles i una ruta de convivència amb famílies i guies del desert."
            },
            {
                "id": 7,
                "title": "Bosc Atlàntic",
                "author": "Mireia Rovira",
                "image": "/static/images/mountains_cutout.png",
                "location": "Serra do Gerês, Portugal",
                "lat": 41.8175,
                "lng": -8.0386,
                "year": "2023",
                "date": "9 d'Octubre de 2023",
                "description": "Exploració de senders i accions de restauració d'un bosc compartit amb una entitat local."
            },
            {
                "id": 8,
                "title": "Ruta de les Dolomites",
                "author": "Oriol Noguera",
                "image": "/static/images/backgroundmountains.png",
                "location": "Cortina d'Ampezzo, Itàlia",
                "lat": 46.5405,
                "lng": 12.1357,
                "year": "2025",
                "date": "27 de Juny de 2025",
                "description": "Una descoberta de parets, refugis i passos de muntanya feta a ritme de grup."
            },
            {
                "id": 9,
                "title": "Illes i Tramuntana",
                "author": "Núria Comas",
                "image": "/static/images/scout_foulard.jpg",
                "location": "Serra de Tramuntana, Mallorca",
                "lat": 39.7516,
                "lng": 2.7088,
                "year": "2024",
                "date": "3 de Maig de 2024",
                "description": "Camins costaners, pobles de pedra i una campanya per protegir els espais naturals de l'illa."
            },
            {
                "id": 10,
                "title": "Himàlaia Solidari",
                "author": "Bernat Badia",
                "image": "/static/images/skyline.jpg",
                "location": "Pokhara, Nepal",
                "lat": 28.2096,
                "lng": 83.9856,
                "year": "2022",
                "date": "11 de Novembre de 2022",
                "description": "Trobada internacional i projecte de suport a una escola de muntanya als peus de l'Annapurna."
            },
            {
                "id": 11,
                "title": "Camins de Montserrat",
                "author": "Gemma Fortuny",
                "image": "/static/images/backgroundmountains.png",
                "location": "Montserrat, Catalunya",
                "lat": 41.5931,
                "lng": 1.8377,
                "year": "2026",
                "date": "8 de Gener de 2026",
                "description": "Una ruta de descoberta pels camins de Montserrat, entre agulles, boscos i històries del país."
            },
            {
                "id": 12,
                "title": "Bivac al Montseny",
                "author": "Judit Camps",
                "image": "/static/images/mountains_cutout.png",
                "location": "Turó de l'Home, Catalunya",
                "lat": 41.7694,
                "lng": 2.4447,
                "year": "2026",
                "date": "21 de Febrer de 2026",
                "description": "Una nit d'hivern per practicar orientació, preparar el campament i escoltar el bosc."
            },
            {
                "id": 13,
                "title": "Volta al Cadí",
                "author": "Ferran Dalmau",
                "image": "/static/images/skyline.jpg",
                "location": "Parc Natural del Cadí-Moixeró, Catalunya",
                "lat": 42.2762,
                "lng": 1.6994,
                "year": "2026",
                "date": "14 de Març de 2026",
                "description": "Travessa de muntanya per conèixer la cara nord del Cadí i reforçar la confiança de l'equip."
            },
            {
                "id": 14,
                "title": "Racons del Delta",
                "author": "Berta Canal",
                "image": "/static/images/scout_foulard.jpg",
                "location": "Delta de l'Ebre, Catalunya",
                "lat": 40.7134,
                "lng": 0.7347,
                "year": "2026",
                "date": "28 de Març de 2026",
                "description": "Ruta en bicicleta per observar els aiguamolls i col·laborar en la cura d'aquest espai natural."
            },
            {
                "id": 15,
                "title": "Pedraforca en Equip",
                "author": "Arnau Puig",
                "image": "/static/images/backgroundmountains.png",
                "location": "Pedraforca, Catalunya",
                "lat": 42.2361,
                "lng": 1.6882,
                "year": "2026",
                "date": "18 d'Abril de 2026",
                "description": "Ascensió compartida i taller de seguretat per aprendre a preparar una sortida amb responsabilitat."
            },
            {
                "id": 16,
                "title": "Camí de Ronda",
                "author": "Mireia Rovira",
                "image": "/static/images/skyline.jpg",
                "location": "Costa Brava, Catalunya",
                "lat": 41.7185,
                "lng": 3.0346,
                "year": "2026",
                "date": "2 de Maig de 2026",
                "description": "Una travessa litoral per descobrir cales, cuidar els camins i viure la costa amb calma."
            },
            {
                "id": 17,
                "title": "Serra del Montsec",
                "author": "Oriol Noguera",
                "image": "/static/images/mountains_cutout.png",
                "location": "Àger, Catalunya",
                "lat": 42.0006,
                "lng": 0.7653,
                "year": "2026",
                "date": "16 de Maig de 2026",
                "description": "Cap de setmana de roca, cel fosc i observació de les estrelles des de la serra."
            },
            {
                "id": 18,
                "title": "Riu Ter a Peu",
                "author": "Núria Comas",
                "image": "/static/images/scout_foulard.jpg",
                "location": "Rupit i Pruit, Catalunya",
                "lat": 42.0244,
                "lng": 2.4649,
                "year": "2026",
                "date": "30 de Maig de 2026",
                "description": "Seguim el riu entre salts d'aigua i pobles per parlar del valor de l'aigua i el territori."
            },
            {
                "id": 19,
                "title": "Cingles de Bertí",
                "author": "Clara Rius",
                "image": "/static/images/backgroundmountains.png",
                "location": "Sant Miquel del Fai, Catalunya",
                "lat": 41.7167,
                "lng": 2.2333,
                "year": "2026",
                "date": "13 de Juny de 2026",
                "description": "Una caminada entre cingleres i rieres per descobrir la geologia del Vallès Oriental."
            },
            {
                "id": 20,
                "title": "Estanys de la Vall d'Aran",
                "author": "Pau Soler",
                "image": "/static/images/skyline.jpg",
                "location": "Vielha, Catalunya",
                "lat": 42.7028,
                "lng": 0.7956,
                "year": "2026",
                "date": "27 de Juny de 2026",
                "description": "Sortida d'alta muntanya per aprendre a llegir el temps i moure'ns amb prudència."
            },
            {
                "id": 21,
                "title": "Fageda d'en Jordà",
                "author": "Laia Domènech",
                "image": "/static/images/mountains_cutout.png",
                "location": "La Garrotxa, Catalunya",
                "lat": 42.1464,
                "lng": 2.5161,
                "year": "2026",
                "date": "11 de Juliol de 2026",
                "description": "Una passejada de descoberta per un bosc volcànic i les històries de la Garrotxa."
            },
            {
                "id": 22,
                "title": "Navegant pel Cap de Creus",
                "author": "Guillem Pujol",
                "image": "/static/images/scout_foulard.jpg",
                "location": "Cap de Creus, Catalunya",
                "lat": 42.3184,
                "lng": 3.3155,
                "year": "2026",
                "date": "25 de Juliol de 2026",
                "description": "Una sortida de mar i vent per conèixer el litoral i protegir els seus ecosistemes."
            },
            {
                "id": 23,
                "title": "Travessa del Montsec",
                "author": "Aina Franquesa",
                "image": "/static/images/backgroundmountains.png",
                "location": "Congost de Mont-rebei, Catalunya",
                "lat": 42.0875,
                "lng": 0.6958,
                "year": "2026",
                "date": "8 d'Agost de 2026",
                "description": "Camins penjats sobre el riu i una travessa per posar en pràctica el lideratge compartit."
            },
            {
                "id": 24,
                "title": "Nits de Pedra Seca",
                "author": "Marc Vila",
                "image": "/static/images/skyline.jpg",
                "location": "Priorat, Catalunya",
                "lat": 41.1454,
                "lng": 0.8063,
                "year": "2026",
                "date": "22 d'Agost de 2026",
                "description": "Ruta entre vinyes i cabanes de pedra seca amb un projecte de memòria rural."
            },
            {
                "id": 25,
                "title": "Cims de Núria",
                "author": "Bernat Badia",
                "image": "/static/images/mountains_cutout.png",
                "location": "Queralbs, Catalunya",
                "lat": 42.3981,
                "lng": 2.1547,
                "year": "2026",
                "date": "5 de Setembre de 2026",
                "description": "Un cap de setmana de cims, brúixola i convivència a la vall més alta del Ripollès."
            },
            {
                "id": 26,
                "title": "Camins del Pedraforca",
                "author": "Judit Camps",
                "image": "/static/images/scout_foulard.jpg",
                "location": "Catalunya",
                "lat": 42.2272,
                "lng": 1.7358,
                "year": "2026",
                "date": "19 de Setembre de 2026",
                "description": "Sortida de tardor per descobrir els boscos del Berguedà i cuinar plegats al refugi."
            },
            {
                "id": 27,
                "title": "Volta al Montgrí",
                "author": "Ferran Dalmau",
                "image": "/static/images/backgroundmountains.png",
                "location": "L'Estartit, Catalunya",
                "lat": 42.0492,
                "lng": 3.1261,
                "year": "2026",
                "date": "3 d'Octubre de 2026",
                "description": "Una ruta de costa i castells per començar el curs amb energia i mirada de grup."
            },
            {
                "id": 28,
                "title": "Castanyes al Montseny",
                "author": "Berta Canal",
                "image": "/static/images/mountains_cutout.png",
                "location": "Santa Fe del Montseny, Catalunya",
                "lat": 41.7741,
                "lng": 2.4632,
                "year": "2026",
                "date": "17 d'Octubre de 2026",
                "description": "Bosc, tardor i una tarda de descoberta per celebrar els primers dies de fred."
            },
            {
                "id": 29,
                "title": "Vies Verdes de Girona",
                "author": "Arnau Puig",
                "image": "/static/images/scout_foulard.jpg",
                "location": "Girona, Catalunya",
                "lat": 41.9794,
                "lng": 2.8214,
                "year": "2026",
                "date": "7 de Novembre de 2026",
                "description": "Pedalem per antigues vies de tren i connectem pobles, paisatge i comunitat."
            },
            {
                "id": 30,
                "title": "Hivern a la Cerdanya",
                "author": "Gemma Fortuny",
                "image": "/static/images/skyline.jpg",
                "location": "Lles de Cerdanya, Catalunya",
                "lat": 42.3906,
                "lng": 1.6869,
                "year": "2026",
                "date": "12 de Desembre de 2026",
                "description": "Raquetes, neu i una sortida per tancar l'any compartint reptes i paisatges."
            }
        ]

        photo_pool = [
            "/static/images/backgroundmountains.png",
            "/static/images/mountains_cutout.png",
            "/static/images/skyline.jpg",
            "/static/images/scout_foulard.jpg"
        ]
        for index, expedition in enumerate(expeditions):
            expedition["images"] = [
                expedition["image"],
                photo_pool[(index + 1) % len(photo_pool)],
                photo_pool[(index + 2) % len(photo_pool)]
            ]

        return expeditions

    def get_shop_products(self):
        """Fetch e-commerce shop products from JSON store."""
        records = self._read_data("shop.json", None)
        if records and len(records) > 0:
            return records
        defaults = self._default_shop_products()
        self._write_data("shop.json", defaults)
        return defaults

    def add_shop_product(self, data):
        """Add a new product to the shop."""
        products = self.get_shop_products()
        next_id = max([p.get('id', 0) for p in products], default=0) + 1
        try:
            price = float(data.get('price', 0.0))
        except (ValueError, TypeError):
            price = 0.0

        new_prod = {
            "id": next_id,
            "name": data.get('name', '').strip(),
            "price": price,
            "category": data.get('category', 'Material').strip(),
            "tag": data.get('tag', 'NOU').strip().upper(),
            "image": data.get('image', '/static/images/scout_foulard.jpg').strip() or '/static/images/scout_foulard.jpg',
            "description": data.get('description', '').strip(),
            "in_stock": True if str(data.get('in_stock', 'true')).lower() in ['true', '1', 'on', 'yes'] else False
        }
        products.append(new_prod)
        self._write_data("shop.json", products)
        return new_prod

    def update_shop_product(self, prod_id, data):
        """Update an existing shop product by id."""
        products = self.get_shop_products()
        for idx, prod in enumerate(products):
            if str(prod.get('id')) == str(prod_id):
                prod['name'] = data.get('name', prod['name']).strip()
                if 'price' in data and data.get('price') != '':
                    try:
                        prod['price'] = float(data['price'])
                    except (ValueError, TypeError):
                        pass
                prod['category'] = data.get('category', prod.get('category', 'Material')).strip()
                prod['tag'] = data.get('tag', prod.get('tag', 'NOU')).strip().upper()
                if data.get('image'):
                    prod['image'] = data.get('image').strip()
                prod['description'] = data.get('description', prod.get('description', '')).strip()
                if 'in_stock' in data:
                    prod['in_stock'] = True if str(data.get('in_stock')).lower() in ['true', '1', 'on', 'yes'] else False
                products[idx] = prod
                self._write_data("shop.json", products)
                return prod
        return None

    def delete_shop_product(self, prod_id):
        """Remove a shop product by id."""
        products = self.get_shop_products()
        products = [p for p in products if str(p.get('id')) != str(prod_id)]
        self._write_data("shop.json", products)
        return True

    def _default_shop_products(self):
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
