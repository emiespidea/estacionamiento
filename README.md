# 🚗 Sistema de Estacionamiento Público

El Sistema de Estacionamiento Público es una aplicación web transaccional diseñada para administrar de manera eficiente el flujo de vehículos, control de clientes y finanzas de un estacionamiento. El proyecto fue realizado como actividad final del curso de Bases de Datos para la carrera de Ingeniería Informática en el Centro Universitario de Ciencias Exactas e Ingenierías (CUCEI) de la Universidad de Guadalajara.

## ✨ Tecnologías 
* <kbd>Python 3</kbd>
* <kbd>Flask</kbd>
* <kbd>MySQL</kbd>
* <kbd>HTML5</kbd> & <kbd>Bootstrap 5</kbd>

## 🚀 Características 
* **Autenticación Segura:** Encriptación de contraseñas mediante hashing.
* **Control de Roles:** Diferenciación entre Administrador (Reportes y Finanzas) y Cobrador (Operación).
* **Monitor en Tiempo Real:** Visualización de vehículos activos y selección mediante menús desplegables para evitar errores humanos.
* **Cálculo de Tarifas Automático:** Lógica escalonada (cambio de precio tras la 5ta hora) y distinción entre clientes ocasionales y frecuentes.
* **Módulo de Pensiones:** Cobro mensual con aplicación de descuento del 15% por antigüedad (> 2 años).
* **Reportes Avanzados:** Top 5 de horas pico, meses de mayor demanda, ingresos anuales y bitácora detallada de los últimos 100 movimientos.

## 🛠️ Instalación Local
1. **Clonar el repo e instalar dependencias:**
   ```bash
   pip install flask mysql-connector-python werkzeug