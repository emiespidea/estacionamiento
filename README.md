# 🚗 Sistema de Estacionamiento Público

El Sistema de Estacionamiento Público es una aplicación web transaccional diseñada para administrar de manera eficiente el flujo de vehículos, control de clientes y finanzas de un estacionamiento. El proyecto fue realizado como actividad final del curso de Bases de Datos (a cargo del PHD. MCC. Ramiro Luperco Coronel) para la carrera de Ingeniería Informática en el Centro Universitario de Ciencias Exactas e Ingenierías (CUCEI) de la Universidad de Guadalajara. 

Está construido utilizando el patrón MVC con Python y Flask para el backend, Bootstrap para el frontend y MySQL para la persistencia de datos.

## ✨ Tecnologías 
* <kbd>Python 3</kbd>
* <kbd>Flask</kbd>
* <kbd>MySQL</kbd>
* <kbd>HTML5</kbd> & <kbd>Bootstrap 5</kbd>
* <kbd>Jinja2</kbd>

## 🚀 Características 
* **Autenticación Segura:** El sistema cuenta con inicio de sesión seguro que encripta las contraseñas en la base de datos mediante *hashes*.
* **Control de Acceso Basado en Roles (RBAC):** Diferencia entre el rol de **Administrador** (acceso total a finanzas y reportes) y **Cobrador** (acceso exclusivo a la operación diaria).
* **Monitor en Tiempo Real:** Interfaz dinámica que muestra una tabla y un menú desplegable de los vehículos que se encuentran físicamente dentro del estacionamiento para evitar errores de captura.
* **Cálculo de Tarifas Dinámico:** El precio por hora disminuye automáticamente a partir de la quinta hora de estancia, aplicando tarifas especiales para clientes frecuentes.
* **Módulo de Pensiones:** Sistema de lealtad que cobra una tarifa mensual fija y aplica un 15% de descuento automático a clientes con más de 2 años de antigüedad.
* **Registro Exprés:** Capacidad de registrar entradas de vehículos nuevos en la base de datos en milisegundos sin interrumpir el flujo vehicular.
* **Inteligencia Financiera:** Panel de control que calcula horas pico, meses de mayor demanda, ingresos históricos consolidados y una bitácora detallada de los últimos 100 movimientos en el estacionamiento.

---

## 📂 Estructura del Proyecto

```text
estacionamiento/
│
├── database/
│   └── schema.sql           # Script principal para crear la BD
│
├── app/
│   ├── templates/           # Vistas HTML (Frontend)
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── reportes.html
│   │   └── cambiar_password.html
│   │
│   ├── __init__.py          # Configuración inicial y conexión a MySQL
│   ├── auth.py              # Lógica de seguridad y roles
│   ├── logic.py             # Motor de cálculos matemáticos de tarifas
│   └── routes.py            # Controladores principales
│
├── crear_admin.py           # Script instalador del primer usuario
├── run.py                   # Archivo raíz para levantar el servidor
├── .gitignore               # Archivos ocultos para GitHub
└── README.md                # Documentación principal