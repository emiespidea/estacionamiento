from flask import render_template, request, redirect, url_for, flash, session
from app import app, get_db_connection
from app.logic import calcular_tarifa, calcular_diferencia_horas, aplicar_descuento_pension
from app.auth import login_required, admin_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


@app.route('/registro_entrada', methods=['POST'])
@login_required
def registro_entrada():
    matricula = request.form['matricula'].upper()
    conn = get_db_connection()
    cursor = conn.cursor()
    ahora = datetime.now()
    try:
        cursor.execute("SELECT matricula FROM Vehiculos WHERE matricula = %s", (matricula,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO Vehiculos (matricula) VALUES (%s)", (matricula,))
        cursor.execute("INSERT INTO Servicios (matricula, fecha_entrada, hora_entrada, tipo_servicio) VALUES (%s, %s, %s, %s)",
                       (matricula, ahora.date(), ahora.time(), request.form['tipo']))
        conn.commit()
        flash('Entrada registrada.', 'success')
    except Exception as e:
        conn.rollback()
        flash('Error al registrar entrada.', 'danger')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('dashboard'))

@app.route('/procesar_salida/<int:folio>', methods=['POST'])
@login_required
def procesar_salida(folio):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.*, c.tipo_cliente FROM Servicios s 
        JOIN Vehiculos v ON s.matricula = v.matricula
        LEFT JOIN Clientes c ON v.cliente_id = c.cliente_id 
        WHERE s.folio_servicio = %s AND s.fecha_salida IS NULL
    """, (folio,))
    s = cursor.fetchone()
    
    if s:
        ahora = datetime.now()
        horas = calcular_diferencia_horas(datetime.combine(s['fecha_entrada'], (datetime.min + s['hora_entrada']).time()), ahora)
        total = calcular_tarifa(horas, s.get('tipo_cliente') == 'frecuente')
        
        cursor.execute("UPDATE Servicios SET fecha_salida=%s, hora_salida=%s WHERE folio_servicio=%s", (ahora.date(), ahora.time(), folio))
        cursor.execute("INSERT INTO Cobros (folio_servicio, matricula, horas_estancia, monto_total, usuario_id) VALUES (%s,%s,%s,%s,%s)",
                       (folio, s['matricula'], horas, total, session['usuario_id']))
        conn.commit()
        flash(f'Salida procesada. Total ${total} MXN', 'success')
    else:
        flash('Folio inválido o ya cobrado.', 'warning')
    cursor.close()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/cobrar_pension', methods=['POST'])
@login_required
def cobrar_pension():
    matricula = request.form['matricula'].upper()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT c.fecha_inicio_pension FROM Vehiculos v
            JOIN Clientes c ON v.cliente_id = c.cliente_id WHERE v.matricula = %s
        """, (matricula,))
        cliente = cursor.fetchone()
        
        if not cliente or not cliente['fecha_inicio_pension']:
            flash('Este vehículo no tiene pensión activa.', 'warning')
        else:
            cursor.execute("SELECT precio FROM Precios WHERE tipo = 'pension' LIMIT 1")
            precio = cursor.fetchone()['precio']
            total = aplicar_descuento_pension(float(precio), cliente['fecha_inicio_pension'])
            
            cursor.execute("INSERT INTO Cobros (matricula, monto_total, usuario_id) VALUES (%s, %s, %s)",
                           (matricula, total, session['usuario_id']))
            conn.commit()
            flash(f'Pensión cobrada. Total: ${total:,.2f} MXN', 'success')
    except Exception as e:
        conn.rollback()
        flash('Error al procesar pensión.', 'danger')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('dashboard'))

@app.route('/reportes')
@login_required
@admin_required
def reportes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # 1. Top Meses
    cursor.execute("SELECT MONTHNAME(fecha_entrada) as mes, COUNT(*) as total_vehiculos FROM Servicios WHERE YEAR(fecha_entrada) = YEAR(CURDATE()) GROUP BY MONTH(fecha_entrada), mes ORDER BY total_vehiculos DESC LIMIT 5;")
    top_meses = cursor.fetchall()
    
    # 2. Top Horarios
    cursor.execute("SELECT HOUR(hora_entrada) as hora_del_dia, COUNT(*) as total_vehiculos FROM Servicios WHERE YEAR(fecha_entrada) = YEAR(CURDATE()) GROUP BY hora_del_dia ORDER BY total_vehiculos DESC LIMIT 5;")
    top_horarios = cursor.fetchall()

    # 3. Ingresos Anuales
    cursor.execute("SELECT YEAR(s.fecha_entrada) as anio, s.tipo_servicio, SUM(c.monto_total) as ingresos FROM Servicios s JOIN Cobros c ON s.folio_servicio = c.folio_servicio GROUP BY anio, s.tipo_servicio ORDER BY anio DESC;")
    ingresos = cursor.fetchall()

    # 4. NUEVO: Historial Detallado (Bitácora)
    cursor.execute("""
        SELECT s.folio_servicio, s.fecha_entrada, s.hora_entrada, s.fecha_salida, s.hora_salida, 
               s.matricula, s.tipo_servicio, c.monto_total 
        FROM Servicios s 
        LEFT JOIN Cobros c ON s.folio_servicio = c.folio_servicio 
        ORDER BY s.fecha_entrada DESC, s.hora_entrada DESC 
        LIMIT 100;
    """)
    historial = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Asegúrate de pasar la nueva variable 'historial' a la vista
    return render_template('reportes.html', top_meses=top_meses, top_horarios=top_horarios, ingresos=ingresos, historial=historial)

@app.route('/cambiar_password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    if request.method == 'POST':
        if request.form['nueva'] != request.form['confirmar']:
            flash('Contraseñas no coinciden.', 'warning')
            return redirect(url_for('cambiar_password'))
            
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT password FROM Usuarios WHERE usuario_id = %s", (session['usuario_id'],))
        u = cursor.fetchone()
        
        if u and check_password_hash(u['password'], request.form['actual']):
            cursor.execute("UPDATE Usuarios SET password = %s WHERE usuario_id = %s", (generate_password_hash(request.form['nueva']), session['usuario_id']))
            conn.commit()
            flash('Contraseña actualizada.', 'success')
            cursor.close()
            conn.close()
            return redirect(url_for('dashboard'))
            
        flash('Contraseña actual incorrecta.', 'danger')
        cursor.close()
        conn.close()
    return render_template('cambiar_password.html')

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Consultamos los vehículos que no han registrado su salida
    cursor.execute("""
        SELECT folio_servicio, matricula, tipo_servicio, hora_entrada 
        FROM Servicios 
        WHERE fecha_salida IS NULL 
        ORDER BY hora_entrada DESC
    """)
    vehiculos_activos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Enviamos la lista de activos a la plantilla HTML
    return render_template('dashboard.html', activos=vehiculos_activos)