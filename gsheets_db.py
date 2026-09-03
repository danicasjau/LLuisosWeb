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
