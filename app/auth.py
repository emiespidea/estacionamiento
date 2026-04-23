# Archivo: app/auth.py
from flask import render_template, request, redirect, url_for, flash, session
from app import app, get_db_connection
from functools import wraps
from werkzeug.security import check_password_hash

# ==========================================
# 1. DECORADORES DE SEGURIDAD (Tus "Cadeneros")
# ==========================================

def login_required(f):
    """Verifica que haya un usuario logueado antes de mostrar la página"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Por favor, inicia sesión para acceder al sistema.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Verifica que el usuario logueado tenga el perfil de 'admin'"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Primero verificamos si hay sesión, luego el perfil
        if 'perfil' not in session or session['perfil'] != 'admin':
            flash('Acceso denegado. Módulo exclusivo para Administradores.', 'danger')
            # Lo regresamos a su inicio normal
            return redirect(url_for('dashboard')) 
        return f(*args, **kwargs)
    return decorated_function


# ==========================================
# 2. RUTAS DE AUTENTICACIÓN
# ==========================================

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si ya está logueado, lo mandamos directo a trabajar
    if 'usuario_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) # Traemos los datos como Diccionario

        query = "SELECT usuario_id, nombre, username, password, perfil FROM Usuarios WHERE username = %s"
        cursor.execute(query, (username,))
        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        # Validación de contraseña. 
        # NOTA: Si en tu base de datos metiste las contraseñas normales (sin hash),
        # cambia la siguiente línea por: if usuario and usuario['password'] == password:
        if usuario and check_password_hash(usuario['password'], password):
            
            # Guardamos los datos vitales en la 'sesión' (una cookie encriptada)
            session['usuario_id'] = usuario['usuario_id']
            session['username'] = usuario['username']
            session['nombre'] = usuario['nombre']
            session['perfil'] = usuario['perfil']

            flash(f"¡Bienvenido, {usuario['nombre']}!", 'success')
            return redirect(url_for('dashboard')) # dashboard es la vista principal
        else:
            flash('Usuario o contraseña incorrectos. Verifica tus credenciales.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    # Destruye todas las variables de la sesión
    session.clear()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('login'))