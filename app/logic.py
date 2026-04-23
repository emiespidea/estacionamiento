from datetime import datetime

def calcular_tarifa(horas, es_frecuente=False):
    if horas <= 0: return 0
    
    # Tarifas según Requerimiento 5
    if not es_frecuente:
        t_base, t_extra = 30.0, 25.0
    else:
        t_base, t_extra = 26.0, 22.0
        
    if horas <= 5:
        return horas * t_base
    else:
        return (5 * t_base) + ((horas - 5) * t_extra)

def aplicar_descuento_pension(monto_base, fecha_inicio):
    hoy = datetime.now()
    antiguedad = hoy.year - fecha_inicio.year - ((hoy.month, hoy.day) < (fecha_inicio.month, fecha_inicio.day))
    return monto_base * 0.85 if antiguedad >= 2 else monto_base # 15% descuento

def calcular_diferencia_horas(entrada_dt, salida_dt):
    diferencia = salida_dt - entrada_dt
    segundos = diferencia.total_seconds()
    horas = segundos // 3600
    if segundos % 3600 > 0: horas += 1
    return int(horas)