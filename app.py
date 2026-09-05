import os
import random
from functools import wraps
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from gsheets_db import db

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ae-lluisos-gracia-retro-k2-key-2026')


def shuffle_caps_team(team):
    """Return a shuffled copy of the team list so the layout changes on each visit."""
    shuffled = list(team)
    random.shuffle(shuffled)
    return shuffled


def login_required_cap(f):
    """Decorator to protect Espai del Cap routes with password-only authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('cap_authenticated'):
            return redirect(url_for('loginespaidelcap'))
        return f(*args, **kwargs)
    return decorated_function


# --------------------------------------------------------------------------
# Public Page Routes
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
    return render_template('novetats.html', active_page='novetats', novetats=novetats_data, posts=novetats_data)

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
    pins = db.get_foulard_pins()
    return render_template('foulard.html', active_page='foulard', pins=pins)

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
# Espai del Cap (Chief/Leader Area) Routes & Password Authentication
# --------------------------------------------------------------------------

@app.route('/loginespaidelcap', methods=['GET', 'POST'])
def loginespaidelcap():
    """Login page for Espai del Cap - unique password, no username required."""
    if request.method == 'POST':
        contra = request.form.get('contra', '')
        if db.verify_contra(contra):
            session['cap_authenticated'] = True
            flash("Benvingut/da a l'Espai del Cap!", "success")
            return redirect(url_for('espaidelcap'))
        else:
            flash("Contrasenya incorrecta. Torna-ho a provar.", "error")
            return render_template('espaidelcap/login.html')

    if session.get('cap_authenticated'):
        return redirect(url_for('espaidelcap'))
    return render_template('espaidelcap/login.html')


@app.route('/espaidelcap')
@login_required_cap
def espaidelcap():
    """Main Espai del Cap dashboard: 3-column subfolder grid layout."""
    novetats_data = db.get_novetats()
    events_data = db.get_calendar_events()
    pins_data = db.get_foulard_pins()
    products_data = db.get_shop_products()
    return render_template(
        'espaidelcap/index.html',
        novetats=novetats_data,
        events=events_data,
        pins=pins_data,
        products=products_data
    )


@app.route('/espaidelcap/logout')
def logout_espaidelcap():
    """Logout endpoint terminating Espai del Cap leader session."""
    session.pop('cap_authenticated', None)
    flash("Sessió de Cap tancada correctament.", "success")
    return redirect(url_for('loginespaidelcap'))


@app.route('/espaidelcap/contra/update', methods=['POST'])
@login_required_cap
def update_contra():
    """Update master password stored in data/contra.json."""
    nova_contra = request.form.get('nova_contra', '').strip()
    if nova_contra:
        db.set_contra(nova_contra)
        flash("Contrasenya mestra actualitzada correctament a data/contra.json!", "success")
    else:
        flash("La contrasenya no pot estar buida.", "error")
    return redirect(url_for('espaidelcap'))


# --------------------------------------------------------------------------
# Espai del Cap Form Processing & Actions
# --------------------------------------------------------------------------

@app.route('/espaidelcap/novetats/add', methods=['POST'])
@login_required_cap
def add_novetat():
    title = request.form.get('title')
    if title:
        db.add_novetat({
            'title': title,
            'tag': request.form.get('tag', 'GENERAL'),
            'author': request.form.get('author', 'Equip de Caps'),
            'date': request.form.get('date'),
            'read_time': request.form.get('read_time', '3 min de lectura'),
            'image': request.form.get('image', '/static/images/backgroundmountains.png'),
            'excerpt': request.form.get('excerpt', ''),
            'content': request.form.get('content', '')
        })
        flash(f"Novetat '{title}' publicada correctament al web!", "success")
    return redirect(url_for('espaidelcap'))


@app.route('/espaidelcap/novetats/delete/<int:post_id>', methods=['POST'])
@login_required_cap
def delete_novetat(post_id):
    db.delete_novetat(post_id)
    flash(f"Novetat #{post_id} eliminada correctament.", "success")
    return redirect(url_for('espaidelcap'))


@app.route('/espaidelcap/calendari/add', methods=['POST'])
@login_required_cap
def add_calendar_event():
    title = request.form.get('title')
    date = request.form.get('date')
    if title and date:
        db.add_calendar_event({
            'title': title,
            'date': date,
            'time': request.form.get('time', '16:30 - 19:00'),
            'location': request.form.get('location', 'Local AE Lluïsos de Gràcia'),
            'unit': request.form.get('unit', 'Assemblea & General'),
            'badge_color': request.form.get('badge_color', '#0B2545'),
            'description': request.form.get('description', '')
        })
        flash(f"Esdeveniment '{title}' afegit correctament al calendari!", "success")
    return redirect(url_for('espaidelcap'))


@app.route('/espaidelcap/calendari/edit/<int:event_id>', methods=['POST'])
@login_required_cap
def edit_calendar_event(event_id):
    updated = db.update_calendar_event(event_id, {
        'title': request.form.get('title'),
        'date': request.form.get('date'),
        'time': request.form.get('time'),
        'location': request.form.get('location'),
        'unit': request.form.get('unit'),
        'badge_color': request.form.get('badge_color'),
        'description': request.form.get('description')
    })
    if updated:
        flash(f"Esdeveniment #{event_id} actualitzat correctament!", "success")
    else:
        flash(f"No s'ha pogut actualitzar l'esdeveniment #{event_id}.", "error")
    return redirect(url_for('espaidelcap'))


@app.route('/espaidelcap/calendari/delete/<int:event_id>', methods=['POST'])
@login_required_cap
def delete_calendar_event(event_id):
    db.delete_calendar_event(event_id)
    flash(f"Esdeveniment #{event_id} suprimit del calendari.", "success")
    return redirect(url_for('espaidelcap'))


@app.route('/foulardviatger', methods=['GET', 'POST'])
def foulardviatger():
    """Dedicated endpoint requested for Foulard Viatger form submissions."""
    if request.method == 'POST':
        title = request.form.get('title')
        location = request.form.get('location')
        if title and location:
            db.add_foulard_pin({
                'title': title,
                'location': location,
                'country': request.form.get('country', 'Catalunya'),
                'lat': request.form.get('lat', 41.4048),
                'lng': request.form.get('lng', 2.1554),
                'year': request.form.get('year', '2026'),
                'unit': request.form.get('unit', 'General'),
                'description': request.form.get('description', '')
            })
            flash(f"Destinació '{title}' afegida correctament al mapa del Foulard Viatger!", "success")
        if session.get('cap_authenticated'):
            return redirect(url_for('espaidelcap'))
        return redirect(url_for('foulard'))
    return redirect(url_for('foulard'))


@app.route('/espaidelcap/foulard/delete/<int:pin_id>', methods=['POST'])
@login_required_cap
def delete_foulard_pin(pin_id):
    db.delete_foulard_pin(pin_id)
    flash(f"Destinació #{pin_id} eliminada del mapa.", "success")
    return redirect(url_for('espaidelcap'))


@app.route('/espaidelcap/shop/add', methods=['POST'])
@login_required_cap
def add_shop_product():
    name = request.form.get('name')
    if name:
        db.add_shop_product({
            'name': name,
            'price': request.form.get('price', 0.0),
            'category': request.form.get('category', 'Material'),
            'tag': request.form.get('tag', 'NOU'),
            'image': request.form.get('image', '/static/images/scout_foulard.jpg'),
            'description': request.form.get('description', ''),
            'in_stock': request.form.get('in_stock', 'true')
        })
        flash(f"Producte '{name}' publicat correctament a la botiga!", "success")
    return redirect(url_for('espaidelcap'))


@app.route('/espaidelcap/shop/edit/<int:prod_id>', methods=['POST'])
@login_required_cap
def edit_shop_product(prod_id):
    updated = db.update_shop_product(prod_id, {
        'name': request.form.get('name'),
        'price': request.form.get('price'),
        'category': request.form.get('category'),
        'description': request.form.get('description')
    })
    if updated:
        flash(f"Producte #{prod_id} actualitzat correctament!", "success")
    else:
        flash(f"No s'ha pogut actualitzar el producte #{prod_id}.", "error")
    return redirect(url_for('espaidelcap'))


@app.route('/espaidelcap/shop/delete/<int:prod_id>', methods=['POST'])
@login_required_cap
def delete_shop_product(prod_id):
    db.delete_shop_product(prod_id)
    flash(f"Producte #{prod_id} eliminat de la botiga.", "success")
    return redirect(url_for('espaidelcap'))


# --------------------------------------------------------------------------
# API Endpoints
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
    port = int(os.getenv('PORT', 5001))
    print(f"==================================================")
    print(f">> AE LLUISOS DE GRACIA Website Running on http://127.0.0.1:{port}")
    print(f"==================================================")
    app.run(host='0.0.0.0', port=port, debug=True)

