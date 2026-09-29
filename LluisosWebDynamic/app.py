import os
import random
import time
import datetime
import secrets
import hmac
import hashlib
import threading
from functools import wraps
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from gsheets_db import db, sanitize_text

def get_secret_key():
    """Retrieves or persists a cryptographically secure random secret key."""
    env_key = os.getenv('SECRET_KEY')
    if env_key:
        return env_key
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    key_file = os.path.join(data_dir, '.secret_key')
    if os.path.exists(key_file):
        try:
            with open(key_file, 'r', encoding='utf-8') as f:
                k = f.read().strip()
                if len(k) >= 32:
                    return k
        except Exception:
            pass
    new_key = secrets.token_hex(32)
    try:
        with open(key_file, 'w', encoding='utf-8') as f:
            f.write(new_key)
    except Exception:
        pass
    return new_key

app = Flask(__name__)
app.config['SECRET_KEY'] = get_secret_key()
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=8)
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4 MB payload maximum
application = app

# ==============================================================================
# CYBERSECURITY GUARDS: CSRF, RATE LIMITING & SECURITY HEADERS
# ==============================================================================

# Thread-safe in-memory rate limiting structures
RATE_LIMIT_LOCK = threading.Lock()
FAILED_LOGIN_ATTEMPTS = {}
KINIELA_SUBMISSION_RATES = {}

def is_login_locked(ip):
    now = time.time()
    with RATE_LIMIT_LOCK:
        attempts = [t for t in FAILED_LOGIN_ATTEMPTS.get(ip, []) if now - t < 600]
        FAILED_LOGIN_ATTEMPTS[ip] = attempts
        return len(attempts) >= 5

def record_failed_login(ip):
    with RATE_LIMIT_LOCK:
        FAILED_LOGIN_ATTEMPTS.setdefault(ip, []).append(time.time())

def reset_login_attempts(ip):
    with RATE_LIMIT_LOCK:
        FAILED_LOGIN_ATTEMPTS.pop(ip, None)

def is_kiniela_rate_limited(ip):
    now = time.time()
    with RATE_LIMIT_LOCK:
        # Max 15 submissions per minute, max 50 per hour
        timestamps = [t for t in KINIELA_SUBMISSION_RATES.get(ip, []) if now - t < 3600]
        recent_minute = [t for t in timestamps if now - t < 60]
        if len(recent_minute) >= 15 or len(timestamps) >= 50:
            return True
        timestamps.append(now)
        KINIELA_SUBMISSION_RATES[ip] = timestamps
        return False

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(32)
    return session['_csrf_token']

@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf_token)

@app.before_request
def validate_csrf():
    """Enforces CSRF token validation on all state-altering POST requests in Espai del Cap."""
    if request.method == 'POST' and request.path.startswith('/espaidelcap'):
        token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
        expected = session.get('_csrf_token')
        if not expected or not token or not hmac.compare_digest(str(token), str(expected)):
            flash("Error de seguretat: El testimoni CSRF no és vàlid o ha caducat.", "error")
            return redirect(url_for('loginespaidelcap'))

@app.after_request
def set_security_headers(response):
    """Adds essential cybersecurity headers against XSS, clickjacking, MIME sniffing, and data injection."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(self), microphone=(), camera=()'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://unpkg.com; "
        "style-src 'self' 'unsafe-inline' https://unpkg.com https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com data:; "
        "img-src 'self' data: https://*.tile.openstreetmap.org https://unpkg.com; "
        "connect-src 'self'; "
        "frame-ancestors 'self'; "
        "base-uri 'self'; "
        "form-action 'self';"
    )
    return response

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
    novetats_data = db.get_novetats()
    team = shuffle_caps_team(db.get_caps())
    return render_template(
        'index.html',
        active_page='index',
        novetats=novetats_data,
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
    expeditions = db.get_foulard_expeditions()
    pins = expeditions
    return render_template('foulard.html', active_page='foulard', pins=pins, expeditions=expeditions)

@app.route('/cims')
def cims():
    return render_template('cims.html', active_page='cims')

@app.route('/api/cims')
def api_cims():
    """API endpoint to get the list of peaks as JSON."""
    return jsonify(db.get_cims())

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
    """Login page for Espai del Cap with brute-force lockout and session fixation prevention."""
    client_ip = request.remote_addr or '127.0.0.1'

    if request.method == 'POST':
        if is_login_locked(client_ip):
            flash("Massa intents fallits. Per motius de ciberseguretat, l'accés s'ha bloquejat temporalment durant 10 minuts.", "error")
            return render_template('espaidelcap/login.html')

        contra = request.form.get('contra', '')
        if db.verify_contra(contra):
            reset_login_attempts(client_ip)
            session.clear()  # Session fixation defense
            session['cap_authenticated'] = True
            session['_csrf_token'] = secrets.token_hex(32)
            flash("Benvingut/da a l'Espai del Cap!", "success")
            return redirect(url_for('espaidelcap'))
        else:
            record_failed_login(client_ip)
            flash("Contrasenya incorrecta. Torna-ho a provar.", "error")
            return render_template('espaidelcap/login.html')

    if session.get('cap_authenticated'):
        return redirect(url_for('espaidelcap'))
    return render_template('espaidelcap/login.html')

@app.route('/espaidelcap')
@login_required_cap
def espaidelcap():
    """Main Espai del Cap dashboard: carpetes de gestió and submissions view."""
    novetats_data = db.get_novetats()
    events_data = db.get_calendar_events()
    pins_data = db.get_foulard_pins()
    products_data = db.get_shop_products()
    kiniela_submissions = db.get_kiniela_submissions()
    return render_template(
        'espaidelcap/index.html',
        novetats=novetats_data,
        events=events_data,
        pins=pins_data,
        products=products_data,
        kinielas=kiniela_submissions
    )

@app.route('/espaidelcap/logout')
def logout_espaidelcap():
    """Logout endpoint terminating Espai del Cap leader session."""
    session.clear()
    flash("Sessió de Cap tancada correctament.", "success")
    return redirect(url_for('loginespaidelcap'))

@app.route('/espaidelcap/contra/update', methods=['POST'])
@login_required_cap
def update_contra():
    """Update master password stored in data/contra.json with Werkzeug hash."""
    nova_contra = request.form.get('nova_contra', '').strip()
    if nova_contra and len(nova_contra) >= 4:
        if db.set_contra(nova_contra):
            flash("Contrasenya mestra actualitzada correctament amb xifratge segur!", "success")
        else:
            flash("Error en actualitzar la contrasenya.", "error")
    else:
        flash("La contrasenya ha de tenir com a mínim 4 caràcters.", "error")
    return redirect(url_for('espaidelcap'))

# --------------------------------------------------------------------------
# Espai del Cap Form Processing & Actions
# --------------------------------------------------------------------------

@app.route('/espaidelcap/novetats/add', methods=['POST'])
@login_required_cap
def add_novetat():
    raw_title = request.form.get('title', '')
    title = sanitize_text(raw_title, max_length=150)
    if title:
        db.add_novetat({
            'title': title,
            'tag': sanitize_text(request.form.get('tag', 'GENERAL'), max_length=50),
            'author': sanitize_text(request.form.get('author', 'Equip de Caps'), max_length=100),
            'date': sanitize_text(request.form.get('date', ''), max_length=50),
            'read_time': sanitize_text(request.form.get('read_time', '3 min de lectura'), max_length=50),
            'image': sanitize_text(request.form.get('image', '/static/images/backgroundmountains.png'), max_length=300),
            'excerpt': sanitize_text(request.form.get('excerpt', ''), max_length=300),
            'content': sanitize_text(request.form.get('content', ''), max_length=5000, allow_newlines=True)
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
    title = sanitize_text(request.form.get('title', ''), max_length=150)
    date = sanitize_text(request.form.get('date', ''), max_length=50)
    if title and date:
        db.add_calendar_event({
            'title': title,
            'date': date,
            'time': sanitize_text(request.form.get('time', '16:30 - 19:00'), max_length=50),
            'location': sanitize_text(request.form.get('location', 'Local AE Lluïsos de Gràcia'), max_length=150),
            'unit': sanitize_text(request.form.get('unit', 'Assemblea & General'), max_length=50),
            'badge_color': sanitize_text(request.form.get('badge_color', '#0B2545'), max_length=20),
            'description': sanitize_text(request.form.get('description', ''), max_length=2000, allow_newlines=True)
        })
        flash(f"Esdeveniment '{title}' afegit correctament al calendari!", "success")
    return redirect(url_for('espaidelcap'))

@app.route('/espaidelcap/calendari/edit/<int:event_id>', methods=['POST'])
@login_required_cap
def edit_calendar_event(event_id):
    updated = db.update_calendar_event(event_id, {
        'title': sanitize_text(request.form.get('title'), max_length=150),
        'date': sanitize_text(request.form.get('date'), max_length=50),
        'time': sanitize_text(request.form.get('time'), max_length=50),
        'location': sanitize_text(request.form.get('location'), max_length=150),
        'unit': sanitize_text(request.form.get('unit'), max_length=50),
        'badge_color': sanitize_text(request.form.get('badge_color'), max_length=20),
        'description': sanitize_text(request.form.get('description'), max_length=2000, allow_newlines=True)
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
    """Dedicated endpoint for Foulard Viatger form submissions."""
    if request.method == 'POST':
        title = sanitize_text(request.form.get('title', ''), max_length=150)
        location = sanitize_text(request.form.get('location', ''), max_length=150)
        if title and location:
            db.add_foulard_pin({
                'title': title,
                'location': location,
                'country': sanitize_text(request.form.get('country', 'Catalunya'), max_length=100),
                'lat': request.form.get('lat', 41.4048),
                'lng': request.form.get('lng', 2.1554),
                'year': sanitize_text(request.form.get('year', '2026'), max_length=20),
                'unit': sanitize_text(request.form.get('unit', 'General'), max_length=50),
                'description': sanitize_text(request.form.get('description', ''), max_length=1500, allow_newlines=True)
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
    name = sanitize_text(request.form.get('name', ''), max_length=150)
    if name:
        db.add_shop_product({
            'name': name,
            'price': request.form.get('price', 0.0),
            'category': sanitize_text(request.form.get('category', 'Material'), max_length=50),
            'tag': sanitize_text(request.form.get('tag', 'NOU'), max_length=30),
            'image': sanitize_text(request.form.get('image', '/static/images/scout_foulard.jpg'), max_length=300),
            'description': sanitize_text(request.form.get('description', ''), max_length=1000, allow_newlines=True),
            'in_stock': request.form.get('in_stock', 'true')
        })
        flash(f"Producte '{name}' publicat correctament a la botiga!", "success")
    return redirect(url_for('espaidelcap'))

@app.route('/espaidelcap/shop/edit/<int:prod_id>', methods=['POST'])
@login_required_cap
def edit_shop_product(prod_id):
    updated = db.update_shop_product(prod_id, {
        'name': sanitize_text(request.form.get('name'), max_length=150),
        'price': request.form.get('price'),
        'category': sanitize_text(request.form.get('category'), max_length=50),
        'description': sanitize_text(request.form.get('description'), max_length=1000, allow_newlines=True)
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

@app.route('/espaidelcap/kiniela/delete/<submission_id>', methods=['POST'])
@login_required_cap
def delete_kiniela_submission(submission_id):
    """Deletes a Kiniela submission from JSON storage."""
    if db.delete_kiniela_submission(submission_id):
        flash(f"Quiniela #{submission_id} eliminada correctament.", "success")
    else:
        flash(f"No s'ha trobat la quiniela #{submission_id}.", "error")
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
    """
    Submits a user's Kiniela prediction:
    - Protected by IP rate limiting
    - Anti-bot honeypot check
    - Strict sanitization against XSS & Formula Injection
    - Thread-safe atomic JSON persistence
    """
    client_ip = request.remote_addr or '127.0.0.1'
    if is_kiniela_rate_limited(client_ip):
        return jsonify({
            "status": "error",
            "message": "Has enviat massa quinieles en poc temps. Si us plau, espera una mica abans de tornar-ho a provar."
        }), 429

    try:
        payload = request.get_json(silent=True) or {}
    except Exception:
        return jsonify({"status": "error", "message": "Format JSON invàlid."}), 400

    # Anti-bot honeypot field
    if payload.get('hp'):
        return jsonify({"status": "error", "message": "Petició filtrada per seguretat."}), 400

    creator_raw = payload.get('creator_name', '')
    creator_name = sanitize_text(creator_raw, max_length=60)
    if not creator_name or len(creator_name.strip()) == 0:
        return jsonify({"status": "error", "message": "Si us plau, introdueix el teu nom com a creador/a."}), 400

    kiniela_data = payload.get('assignments', {})
    if not isinstance(kiniela_data, dict):
        return jsonify({"status": "error", "message": "Les assignacions han de ser un diccionari vàlid."}), 400

    user_agent = request.headers.get('User-Agent', '')[:150]
    result = db.save_kiniela(
        creator_name=creator_name,
        kiniela_data=kiniela_data,
        client_ip=client_ip,
        user_agent=user_agent
    )
    return jsonify(result), 200

# --------------------------------------------------------------------------
# Main Execution
# --------------------------------------------------------------------------

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5050))
    print(f"==================================================")
    print(f">> AE LLUISOS DE GRACIA Website Running on http://127.0.0.1:{port} (localhost:5050)")
    print(f"==================================================")
    app.run(host='0.0.0.0', port=port, debug=True)
