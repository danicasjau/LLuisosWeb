/**
 * ==============================================================================
 * AE LLUÏSOS DE GRÀCIA - VARIABLES CONFIGURABLES I MODIFICABLES (TOP)
 * ==============================================================================
 * Pots canviar fàcilment aquestes variables per adaptar la pàgina o configurar
 * el teu Worker de Cloudflare per guardar la Quiniela.
 */

// 1. URL del teu Cloudflare Worker per desar i carregar la Quiniela (KV)
// Posa aquí la URL pública del teu Worker desplegat a Cloudflare
// (Exemple: "https://la-teva-quiniela.nom.workers.dev")
const CLOUDFLARE_WORKER_URL = "https://kiniela-worker.el-teu-subdomini.workers.dev";

// 2. Clau del KV utilitzada al Cloudflare Worker
const CLOUDFLARE_KV_KEY = "les_meves_dades";

// 3. Curs escolta i informació general
const SCOUT_YEAR = "2026-2027";
const SCOUT_GROUP_NAME = "AE Lluïsos de Gràcia";
const SCOUT_ADDRESS = "Plaça del Nord, 4 • 08024 Barcelona (Vila de Gràcia)";

// 4. Contacte i xarxes socials
const INSTAGRAM_ACCOUNT = "@aelluisosdegracia";
const INSTAGRAM_LINK = "https://www.instagram.com/aelluisosdegracia/";
const CONTACT_EMAIL_B64_USER = "Y29udGFjdGU="; // 'contacte' en base64
const CONTACT_EMAIL_B64_DOMAIN = "bGx1aXNvc2RlZ3JhY2lhLmNhdA=="; // 'lluisosdegracia.cat' en base64


/**
 * ==============================================================================
 * DADES ESTÀTIQUES DEL WEB (STATIC DATA)
 * ==============================================================================
 */

// ------------------------------------------------------------------------------
// A) EQUIP DE CAPS (21 CAPS ACTIUS)
// ------------------------------------------------------------------------------
const CAPS_DATA = [
  {
    "id": 1,
    "name": "Joana Solà",
    "role": "Cap de Branca",
    "unit": "Castúdrigues",
    "unit_code": "castors",
    "years": "3 anys a l'agrupament",
    "bio": "Creu que la millor manera d'aprendre és riure, jugar i fer petits grans projectes amb la gent del cau.",
    "image": "static/images/caps/deafult.png",
    "quote": "\"Cada aventura comença amb un gran somriure.\""
  },
  {
    "id": 2,
    "name": "Maia de Cock",
    "role": "Cap de Branca",
    "unit": "Castúdrigues",
    "unit_code": "castors",
    "years": "2 anys a l'agrupament",
    "bio": "Entusiasta de la natura i dels jocs d'orientació. Vol ajudar cada infant a trobar el seu ritme i confiança.",
    "image": "static/images/caps/deafult.png",
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
    "image": "static/images/caps/deafult.png",
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
    "image": "static/images/caps/bernatescola.png",
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
    "image": "static/images/caps/deafult.png",
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
    "image": "static/images/caps/deafult.png",
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
    "image": "static/images/caps/deafult.png",
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
    "image": "static/images/caps/maurroda.png",
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
    "image": "static/images/caps/deafult.png",
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
    "image": "static/images/caps/helenaherranz.png",
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
    "image": "static/images/caps/iusales.png",
    "quote": "\"Quan hi ha confiança, hi ha aventura.\""
  },
  {
    "id": 12,
    "name": "Nil Mitjavila",
    "role": "Cap de Branca",
    "unit": "Pionel·les",
    "unit_code": "pios",
    "years": "3 anys a l'agrupament",
    "bio": "Acosta els nens i nenes al món de l'escoltisme amb creativitat, calma i molta energia positiva.",
    "image": "static/images/caps/deafult.png",
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
    "image": "static/images/caps/deafult.png",
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
    "image": "static/images/caps/deafult.png",
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
    "image": "static/images/caps/joanroig.png",
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
    "image": "static/images/caps/deafult.png",
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
    "image": "static/images/caps/deafult.png",
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
    "image": "static/images/caps/ivetroig.png",
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
    "image": "static/images/caps/deafult.png",
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
    "image": "static/images/caps/deafult.png",
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
    "image": "static/images/caps/deafult.png",
    "quote": "\"La millor manera d'aprendre és fent.\""
  }
];

// ------------------------------------------------------------------------------
// B) NOUS CAPS (TRUKS PER A LA QUINIELA)
// ------------------------------------------------------------------------------
const NEW_CAPS_DATA = [
  { id: 1001, name: "Pau Nuet", isNewCap: true, image: "static/images/backgroundmountains.png" },
  { id: 1002, name: "Joan Nuet", isNewCap: true, image: "static/images/backgroundmountains.png" },
  { id: 1003, name: "Jana Bosc", isNewCap: true, image: "static/images/backgroundmountains.png" },
  { id: 1004, name: "Iris de Cook", isNewCap: true, image: "static/images/backgroundmountains.png" },
  { id: 1005, name: "Aniol Rovira", isNewCap: true, image: "static/images/backgroundmountains.png" },
  { id: 1006, name: "Júlia Muntada", isNewCap: true, image: "static/images/backgroundmountains.png" },
  { id: 1007, name: "Aina Franquesa", isNewCap: true, image: "static/images/backgroundmountains.png" }
];

// ------------------------------------------------------------------------------
// C) CALENDARI D'ESDEVENIMENTS (CURS 2026-2027)
// ------------------------------------------------------------------------------
const CALENDAR_EVENTS_DATA = [
  {
    "id": 151,
    "title": "Últim Cau",
    "date": "2026-09-19",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Últim cau de la temporada."
  },
  {
    "id": 153,
    "title": "Excursió de Passos",
    "date": "2026-10-03",
    "end_date": "2026-10-04",
    "time": "Dissabte 08:00 - Diumenge 18:30",
    "location": "Entorn natural de Catalunya",
    "unit": "Totes les unitats",
    "badge_color": "#0284C7",
    "image": "static/images/backgroundmountains.png",
    "description": "Excursió de passos de branca del cap de setmana."
  },
  {
    "id": 105,
    "title": "Cau",
    "date": "2026-10-10",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 152,
    "title": "Cau",
    "date": "2026-10-17",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 108,
    "title": "Cau",
    "date": "2026-10-24",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 109,
    "title": "Cau",
    "date": "2026-10-31",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 110,
    "title": "Cau",
    "date": "2026-11-07",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 154,
    "title": "Cau",
    "date": "2026-11-14",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 112,
    "title": "Excursió",
    "date": "2026-11-21",
    "end_date": "2026-11-22",
    "time": "Dissabte 08:00 - Diumenge 18:30",
    "location": "Entorn natural de Catalunya",
    "unit": "Totes les unitats",
    "badge_color": "#0284C7",
    "image": "static/images/backgroundmountains.png",
    "description": "Excursió de cap de setmana amb sortida dissabte al matí i tornada diumenge a la tarda."
  },
  {
    "id": 113,
    "title": "Cau",
    "date": "2026-11-28",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 116,
    "title": "Cau",
    "date": "2026-12-12",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 117,
    "title": "Cau",
    "date": "2026-12-19",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 155,
    "title": "Campaments Hivern (Pionel·les)",
    "date": "2026-12-27",
    "end_date": "2026-12-29",
    "time": "Diumenge 08:00 - Dimarts 18:30",
    "location": "Entorn natural de Catalunya",
    "unit": "Pionel·les",
    "badge_color": "#DC2626",
    "image": "static/images/backgroundmountains.png",
    "description": "Campaments d'hivern de les Pionel·les."
  },
  {
    "id": 120,
    "title": "Cau",
    "date": "2027-01-09",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 121,
    "title": "Cau",
    "date": "2027-01-16",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 122,
    "title": "Excursió",
    "date": "2027-01-23",
    "end_date": "2027-01-24",
    "time": "Dissabte 08:00 - Diumenge 18:30",
    "location": "Entorn natural de Catalunya",
    "unit": "Totes les unitats",
    "badge_color": "#0284C7",
    "image": "static/images/backgroundmountains.png",
    "description": "Excursió de cap de setmana amb sortida dissabte al matí i tornada diumenge a la tarda."
  },
  {
    "id": 123,
    "title": "Cau",
    "date": "2027-01-30",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 124,
    "title": "Cau",
    "date": "2027-02-06",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 125,
    "title": "Cau",
    "date": "2027-02-13",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 127,
    "title": "Cau",
    "date": "2027-02-20",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 128,
    "title": "Excursió",
    "date": "2027-02-27",
    "end_date": "2027-02-28",
    "time": "Dissabte 08:00 - Diumenge 18:30",
    "location": "Entorn natural de Catalunya",
    "unit": "Totes les unitats",
    "badge_color": "#0284C7",
    "image": "static/images/backgroundmountains.png",
    "description": "Excursió de cap de setmana amb sortida dissabte al matí i tornada diumenge a la tarda."
  },
  {
    "id": 129,
    "title": "Cau",
    "date": "2027-03-06",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 130,
    "title": "Cau",
    "date": "2027-03-13",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 150,
    "title": "Campaments Primavera",
    "date": "2027-03-20",
    "end_date": "2027-03-23",
    "time": "Dissabte 08:00 - Dimarts 18:30",
    "location": "Entorn natural de Catalunya",
    "unit": "Totes les unitats",
    "badge_color": "#16A34A",
    "image": "static/images/backgroundmountains.png",
    "description": "Campaments de primavera de l'agrupament."
  },
  {
    "id": 133,
    "title": "Cau",
    "date": "2027-04-03",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 151,
    "title": "Jamborinada",
    "date": "2027-04-10",
    "end_date": "2027-04-11",
    "time": "Dissabte 08:00 - Diumenge 18:30",
    "location": "Entorn natural de Catalunya",
    "unit": "Totes les unitats",
    "badge_color": "#2563EB",
    "image": "static/images/backgroundmountains.png",
    "description": "Sortida de cap de setmana a la Jamborinada."
  },
  {
    "id": 135,
    "title": "Cau",
    "date": "2027-04-17",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 137,
    "title": "Cau",
    "date": "2027-04-24",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 138,
    "title": "Excursió",
    "date": "2027-05-01",
    "end_date": "2027-05-02",
    "time": "Dissabte 08:00 - Diumenge 18:30",
    "location": "Entorn natural de Catalunya",
    "unit": "Totes les unitats",
    "badge_color": "#0284C7",
    "image": "static/images/backgroundmountains.png",
    "description": "Excursió de cap de setmana amb sortida dissabte al matí i tornada diumenge a la tarda."
  },
  {
    "id": 149,
    "title": "Cau",
    "date": "2027-05-08",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 141,
    "title": "Cau",
    "date": "2027-05-22",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 142,
    "title": "Excursió",
    "date": "2027-05-29",
    "end_date": "2027-05-30",
    "time": "Dissabte 08:00 - Diumenge 18:30",
    "location": "Entorn natural de Catalunya",
    "unit": "Totes les unitats",
    "badge_color": "#0284C7",
    "image": "static/images/backgroundmountains.png",
    "description": "Excursió de cap de setmana amb sortida dissabte al matí i tornada diumenge a la tarda."
  },
  {
    "id": 143,
    "title": "Cau",
    "date": "2027-06-05",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 144,
    "title": "Cau",
    "date": "2027-06-12",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  },
  {
    "id": 145,
    "title": "Cau",
    "date": "2027-06-19",
    "time": "16:30 - 19:00",
    "location": "Local AE Lluïsos de Gràcia",
    "unit": "Totes les unitats",
    "badge_color": "#FF5722",
    "image": "static/images/scout_foulard.jpg",
    "description": "Activitat de cau de dissabte per a totes les unitats."
  }
];

// ------------------------------------------------------------------------------
// D) NOVETATS I NOTÍCIES
// ------------------------------------------------------------------------------
const NOVETATS_DATA = [
  {
    "id": 1,
    "title": "CIM AL K2: L'EXPEDICIÓ D'HIVERN DELS TRUCS",
    "date": "15 AGOST 2026",
    "tag": "EXPEDICIÓ",
    "author": "Equip de Caps",
    "excerpt": "28,000 PEUS. PENJATS DELS DITS. L'adrenalina pura dels nostres equips conquerint els pics més alts del Pirineu en la nova ruta d'hivern.",
    "content": "Els nois i noies de la unitat de Trucs han completat amb èxit la travessa d'alta muntanya. Inspirats en l'esperit d'assalt als grans cims, l'activitat ha demostrat el valor del treball en equip, la superació personal i el respecte per la natura.",
    "image": "static/images/backgroundmountains.png",
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
    "image": "static/images/scout_foulard.jpg",
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
    "image": "static/images/scout_foulard.jpg",
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
    "image": "static/images/backgroundmountains.png",
    "read_time": "2 min de lectura"
  }
];

// ------------------------------------------------------------------------------
// E) MAPA DEL FOULARD VIATGER (XINXETES I SORTIDES)
// ------------------------------------------------------------------------------
const FOULARD_PINS_DATA = [
  {
    "id": 1,
    "title": "Expedició Karakoram Trail",
    "location": "K2 Base Camp, Baltoro Glacier",
    "country": "Pakistan / Himàlaia",
    "lat": 35.8808,
    "lng": 76.5158,
    "year": "2025",
    "date": "15 de Juliol de 2025",
    "author": "Equip Trucs",
    "unit": "Trucs",
    "description": "Expedició internacional dels Trucs per donar suport a projectes educatius de muntanya.",
    "image": "static/images/backgroundmountains.png",
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
    "date": "Tot l'any",
    "author": "Tots els caps",
    "unit": "Seu Central",
    "description": "El cor de l'agrupament. Punt de trobada de cada dissabte de cau.",
    "image": "static/images/scout_team.jpg",
    "type": "headquarters"
  }
];

const FOULARD_EXPEDITIONS_DATA = [
  {
    "id": 1,
    "title": "Travessa dels Pirineus",
    "author": "Aina Franquesa",
    "image": "static/images/backgroundmountains.png",
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
    "image": "static/images/mountains_cutout.png",
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
    "image": "static/images/skyline.jpg",
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
    "image": "static/images/scout_foulard.jpg",
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
    "image": "static/images/backgroundmountains.png",
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
    "image": "static/images/skyline.jpg",
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
    "image": "static/images/mountains_cutout.png",
    "location": "Astúries, Picos de Europa",
    "lat": 43.1812,
    "lng": -4.8197,
    "year": "2023",
    "date": "10 de Setembre de 2023",
    "description": "Travessa per fagedes atlàntiques i camins de pastors sota els massissos calcaris."
  }
];

// ------------------------------------------------------------------------------
// F) LLISTAT DE CIMS (60 CIMS)
// ------------------------------------------------------------------------------
const CIMS_DATA = [
  { "id": "01", "number": 1, "name": "Bastiments", "levels": ["RNG", "PiC"], "levels_label": "RNG / PiC" },
  { "id": "02", "number": 2, "name": "Besiberri Sud", "levels": ["PiC", "Truk"], "levels_label": "PiC / Truk" },
  { "id": "03", "number": 3, "name": "Canigó", "levels": ["LLiD", "Truk"], "levels_label": "LLiD / Truk" },
  { "id": "04", "number": 4, "name": "Cap de la Gallina Pelada", "levels": ["RNG"], "levels_label": "RNG" },
  { "id": "05", "number": 5, "name": "Carlit", "levels": ["PiC"], "levels_label": "PiC" },
  { "id": "06", "number": 6, "name": "Castell de Burriac", "levels": ["CiLL", "LLiD"], "levels_label": "CiLL / LLiD" },
  { "id": "07", "number": 7, "name": "Cogulló d'Estela", "levels": ["LLiD", "RNG"], "levels_label": "LLiD / RNG" },
  { "id": "08", "number": 8, "name": "Comabona", "levels": ["LLiD"], "levels_label": "LLiD" },
  { "id": "09", "number": 9, "name": "Comanegra", "levels": ["LLiD"], "levels_label": "LLiD" },
  { "id": "10", "number": 10, "name": "Comapedrosa", "levels": ["RNG"], "levels_label": "RNG" },
  { "id": "11", "number": 11, "name": "El Negrell", "levels": ["CiLL"], "levels_label": "CiLL" },
  { "id": "12", "number": 12, "name": "El Salabardar", "levels": ["LLiD"], "levels_label": "LLiD" },
  { "id": "13", "number": 13, "name": "L'Espina", "levels": ["RNG"], "levels_label": "RNG" },
  { "id": "14", "number": 14, "name": "La Mola de Sant Llorenç del Munt", "levels": ["LLiD"], "levels_label": "LLiD" },
  { "id": "15", "number": 15, "name": "La Talaia de Montmell", "levels": ["LLiD"], "levels_label": "LLiD" },
  { "id": "16", "number": 16, "name": "Matagalls", "levels": ["LLiD", "PiC"], "levels_label": "LLiD / PiC" },
  { "id": "17", "number": 17, "name": "Mont-Roig", "levels": ["RNG"], "levels_label": "RNG" },
  { "id": "18", "number": 18, "name": "Montardo", "levels": ["RNG"], "levels_label": "RNG" },
  { "id": "19", "number": 19, "name": "Montcau", "levels": ["CiLL"], "levels_label": "CiLL" },
  { "id": "20", "number": 20, "name": "Monteixo", "levels": ["LLiD", "RNG", "PiC"], "levels_label": "LLiD / RNG / PiC" },
  { "id": "21", "number": 21, "name": "Muntanya del Montgrí", "levels": ["CiLL", "LLiD"], "levels_label": "CiLL / LLiD" },
  { "id": "22", "number": 22, "name": "Noufonts", "levels": ["RNG"], "levels_label": "RNG" },
  { "id": "23", "number": 23, "name": "Pedraforca", "levels": ["RNG"], "levels_label": "RNG" },
  { "id": "24", "number": 24, "name": "Penya Sant Alís", "levels": ["CiLL", "LLiD"], "levels_label": "CiLL / LLiD" },
  { "id": "25", "number": 25, "name": "Penyagolosa", "levels": ["LLiD"], "levels_label": "LLiD" },
  { "id": "26", "number": 26, "name": "Penyes Altes de Moixeró", "levels": ["RNG", "PiC"], "levels_label": "RNG / PiC" },
  { "id": "27", "number": 27, "name": "Perdiguero", "levels": ["Truk"], "levels_label": "Truk" },
  { "id": "28", "number": 28, "name": "Pic d'Amitges", "levels": ["PiC"], "levels_label": "PiC" },
  { "id": "29", "number": 29, "name": "Pic d'Estats", "levels": ["PiC", "Truk"], "levels_label": "PiC / Truk" },
  { "id": "30", "number": 30, "name": "Pic de Canalbona", "levels": ["RNG"], "levels_label": "RNG" },
  { "id": "31", "number": 31, "name": "Pic de Casamanya", "levels": ["LLiD"], "levels_label": "LLiD" },
  { "id": "32", "number": 32, "name": "Pic de Certascan", "levels": ["RNG"], "levels_label": "RNG" },
  { "id": "33", "number": 33, "name": "Pic de Costabona", "levels": ["RNG"], "levels_label": "RNG" },
  { "id": "34", "number": 34, "name": "Pic de l'Infern", "levels": ["RNG", "PiC"], "levels_label": "RNG / PiC" },
  { "id": "35", "number": 35, "name": "Pic de la Dona", "levels": ["LLiD", "RNG"], "levels_label": "LLiD / RNG" },
  { "id": "36", "number": 36, "name": "Pic de la Font Blanca", "levels": ["RNG", "PiC"], "levels_label": "RNG / PiC" },
  { "id": "37", "number": 37, "name": "Pic de Marbore", "levels": ["Truk"], "levels_label": "Truk" },
  { "id": "38", "number": 38, "name": "Pic de Moredo", "levels": ["LLiD", "RNG"], "levels_label": "LLiD / RNG" },
  { "id": "39", "number": 39, "name": "Pic de Salòria", "levels": ["LLiD", "RNG"], "levels_label": "LLiD / RNG" },
  { "id": "40", "number": 40, "name": "Pic de Sotllo", "levels": ["PiC"], "levels_label": "PiC" },
  { "id": "41", "number": 41, "name": "Pic de Subenuix", "levels": ["PiC"], "levels_label": "PiC" },
  { "id": "42", "number": 42, "name": "Pic del Port de Siguer", "levels": ["LLiD"], "levels_label": "LLiD" },
  { "id": "43", "number": 43, "name": "Pica d'Estats", "levels": ["RNG", "PiC", "Truk"], "levels_label": "RNG / PiC / Truk" },
  { "id": "44", "number": 44, "name": "Puig Cerverís", "levels": ["LLiD"], "levels_label": "LLiD" },
  { "id": "45", "number": 45, "name": "Puig de Bassegoda", "levels": ["LLiD"], "levels_label": "LLiD" },
  { "id": "46", "number": 46, "name": "Puig de les Agudes", "levels": ["CiLL", "LLiD"], "levels_label": "CiLL / LLiD" },
  { "id": "47", "number": 47, "name": "Puig del Far", "levels": ["CiLL"], "levels_label": "CiLL" },
  { "id": "48", "number": 48, "name": "Puig Drau", "levels": ["LLiD"], "levels_label": "LLiD" },
  { "id": "49", "number": 49, "name": "Puigllançada", "levels": ["CiLL", "LLiD"], "levels_label": "CiLL / LLiD" },
  { "id": "50", "number": 50, "name": "Puigmal", "levels": ["LLiD", "RNG"], "levels_label": "LLiD / RNG" },
  { "id": "51", "number": 51, "name": "Roca Corbatera", "levels": ["CiLL"], "levels_label": "CiLL" },
  { "id": "52", "number": 52, "name": "Sant Jeroni", "levels": ["CiLL", "LLiD"], "levels_label": "CiLL / LLiD" },
  { "id": "53", "number": 53, "name": "Tagamanent", "levels": ["CiLL"], "levels_label": "CiLL" },
  { "id": "54", "number": 54, "name": "Taga", "levels": ["CiLL", "LLiD"], "levels_label": "CiLL / LLiD" },
  { "id": "55", "number": 55, "name": "Tossal de les Torretes", "levels": ["CiLL"], "levels_label": "CiLL" },
  { "id": "56", "number": 56, "name": "Tossal del Rei", "levels": ["CiLL"], "levels_label": "CiLL" },
  { "id": "57", "number": 57, "name": "Tossa d'Alp", "levels": ["CiLL", "LLiD"], "levels_label": "CiLL / LLiD" },
  { "id": "58", "number": 58, "name": "Tuc de Ratera", "levels": ["PiC"], "levels_label": "PiC" },
  { "id": "59", "number": 59, "name": "Turó de l'Home", "levels": ["CiLL"], "levels_label": "CiLL" },
  { "id": "60", "number": 60, "name": "Turó de Tagamanent", "levels": ["CiLL"], "levels_label": "CiLL" }
];

// ------------------------------------------------------------------------------
// G) BOTIGA D'AGRUPAMENT (PRODUCTES)
// ------------------------------------------------------------------------------
const SHOP_PRODUCTS_DATA = [
  {
    "id": 1,
    "name": "Foulard Oficial Lluïsos de Gràcia",
    "price": 12.0,
    "category": "Foulards",
    "tag": "RETRO EDITION",
    "image": "static/images/scout_foulard.jpg",
    "description": "El foulard tradicional de l'agrupament en blau marí i verd ampolla amb la sanefa cosida a mà.",
    "in_stock": true
  },
  {
    "id": 2,
    "name": "Dessuadora Vintage Scouting",
    "price": 32.0,
    "category": "Roba",
    "tag": "BESTSELLER",
    "image": "static/images/backgroundmountains.png",
    "description": "Dessuadora de cotó d'alta gramatge amb caputxa i logotip de l'agrupament.",
    "in_stock": true
  }
];

// Exposició global
window.CAPS_POOL = CAPS_DATA;
window.RAW_CALENDAR_EVENTS = CALENDAR_EVENTS_DATA;
window.NOVETATS_DATA = NOVETATS_DATA;
window.FOULARD_PINS = FOULARD_PINS_DATA;
window.FOULARD_EXPEDITIONS = FOULARD_EXPEDITIONS_DATA;
window.CIMS_DATA = CIMS_DATA;
window.SHOP_PRODUCTS = SHOP_PRODUCTS_DATA;
