import os
import random
from flask import Flask, render_template, jsonify, request, redirect, url_for
from gsheets_db import db

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ae-lluisos-gracia-retro-k2-key-2026')


def shuffle_caps_team(team):
    """Return a shuffled copy of the team list so the layout changes on each visit."""
    shuffled = list(team)
    random.shuffle(shuffled)
    return shuffled

# --------------------------------------------------------------------------
# Page Routes
# --------------------------------------------------------------------------

@app.route('/')
def index():
    """Main Entry Point with Hero, Qui Som, Novetats, and Equip de Caps Carousel"""
    novetats = db.get_novetats()
    team = shuffle_caps_team(db.get_caps())
    return render_template(
        'index.html',
        active_page='index',
        novetats=novetats,
        team=team
    )

@app.route('/novetats')
@app.route('/mercau')
def novetats():
    novetats_data = db.get_novetats()
    return render_template('novetats.html', active_page='novetats', novetats=novetats_data)

@app.route('/calendar')
@app.route('/calendari')
def calendar():
    """Dedicated Full Calendar Page"""
    events = db.get_calendar_events()
    return render_template('calendar.html', active_page='calendar', events=events)

@app.route('/equips')
@app.route('/caps')
def equips():
    """Dedicated Team / All Caps Page"""
    team = shuffle_caps_team(db.get_caps())
    return render_template('equips.html', active_page='equips', team=team)

@app.route('/foulard')
def foulard():
    expeditions = db.get_foulard_expeditions()
    pins = expeditions
    return render_template('foulard.html', active_page='foulard', pins=pins, expeditions=expeditions)

@app.route('/shop')
@app.route('/botiga')
def shop():
    products = db.get_shop_products()
    return render_template('shop.html', active_page='shop', products=products)

@app.route('/quiniela')
@app.route('/kiniela')
def kiniela():
    return render_template('kiniela.html', active_page='kiniela', team=shuffle_caps_team(db.get_caps()))


# --------------------------------------------------------------------------
# API Endpoints (Reading/Writing Google Sheets via gsheets_db.py)
# --------------------------------------------------------------------------

@app.route('/api/novetats', methods=['GET'])
def api_novetats():
    return jsonify({"status": "success", "data": db.get_novetats()})

@app.route('/api/calendari', methods=['GET'])
def api_calendari():
    return jsonify({"status": "success", "data": db.get_calendar_events()})

@app.route('/api/caps', methods=['GET'])
def api_caps():
    return jsonify({"status": "success", "data": shuffle_caps_team(db.get_caps())})

@app.route('/api/foulard', methods=['GET'])
def api_foulard():
    return jsonify({"status": "success", "data": db.get_foulard_pins()})

@app.route('/api/shop', methods=['GET'])
def api_shop():
    return jsonify({"status": "success", "data": db.get_shop_products()})

@app.route('/api/kiniela/save', methods=['POST'])
def api_save_kiniela():
    payload = request.get_json() or {}
    creator_name = payload.get('creator_name', 'Anònim/a').strip()
    kiniela_data = payload.get('assignments', {})

    if not creator_name:
        creator_name = 'Anònim/a'

    result = db.save_kiniela(creator_name, kiniela_data)
    return jsonify(result)

# --------------------------------------------------------------------------
# Main Execution
# --------------------------------------------------------------------------

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5002))
    print(f"==================================================")
    print(f">> AE LLUISOS DE GRACIA Website Running on http://127.0.0.1:{port}")
    print(f"==================================================")
    app.run(host='0.0.0.0', port=port, debug=True)
