-- 1. Crear la base de datos y seleccionarla
CREATE DATABASE IF NOT EXISTS estacionamiento_db;
USE estacionamiento_db;

-- 2. Tabla de Usuarios (Admin y Cobrador)
CREATE TABLE Usuarios (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    username VARCHAR(30) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, -- Ampliado para permitir hashing (seguridad)
    perfil VARCHAR(15) NOT NULL     -- 'admin' o 'cobrador'
);

-- 3. Tabla de Clientes
CREATE TABLE Clientes (
    cliente_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    telefono VARCHAR(15),
    email VARCHAR(50),
    usuario_id INT, 
    rfc VARCHAR(13),
    tipo_cliente VARCHAR(15) DEFAULT 'de_paso', -- 'de_paso' o 'frecuente'
    fecha_inicio_pension DATE,                  -- Clave para calcular el descuento de >2 años (Req. 6)
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id)
);

-- 4. Tabla de Vehículos
CREATE TABLE Vehiculos (
    matricula VARCHAR(10) PRIMARY KEY,
    modelo VARCHAR(20),
    marca VARCHAR(20),
    color VARCHAR(15),
    cliente_id INT NULL, -- Permite NULL para el "Registro Exprés" de nuevos vehículos
    FOREIGN KEY (cliente_id) REFERENCES Clientes(cliente_id)
);

-- 5. Tabla del Catálogo de Precios
CREATE TABLE Precios (
    folio_precio INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(15) NOT NULL,    -- 'cajon' o 'pension'
    precio DECIMAL(10,2) NOT NULL -- DECIMAL es ideal para manejar dinero
);

-- INSERCIÓN BASE: Agregamos los precios iniciales para que el sistema funcione
INSERT INTO Precios (tipo, precio) VALUES 
('cajon', 30.00), 
('pension', 1200.00);

-- 6. Tabla de Servicios (Entradas y Salidas Operativas)
CREATE TABLE Servicios (
    folio_servicio INT AUTO_INCREMENT PRIMARY KEY,
    matricula VARCHAR(10),
    fecha_entrada DATE NOT NULL,
    hora_entrada TIME NOT NULL,
    fecha_salida DATE,
    hora_salida TIME,
    folio_precio INT,
    tipo_servicio VARCHAR(10), -- 'cajon' o 'pension'
    FOREIGN KEY (matricula) REFERENCES Vehiculos(matricula),
    FOREIGN KEY (folio_precio) REFERENCES Precios(folio_precio)
);

-- 7. Tabla de Cobros (Registro Financiero)
CREATE TABLE Cobros (
    folio_cobro INT AUTO_INCREMENT PRIMARY KEY,
    folio_servicio INT NULL, -- Puede ser NULL si es un cobro directo de pensión mensual
    matricula VARCHAR(10),
    horas_estancia INT, 
    monto_total DECIMAL(10,2),
    usuario_id INT, -- Cobrador que procesó el pago
    FOREIGN KEY (folio_servicio) REFERENCES Servicios(folio_servicio),
    FOREIGN KEY (matricula) REFERENCES Vehiculos(matricula),
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id)
);