-- =========================================================
-- Base de datos: compraventa_db  (PostgreSQL)
-- Compra y venta de vehículos usados
-- Script 1: creación de las 5 tablas con PK, FK y restricciones
-- =========================================================

-- Antes de ejecutar este script:
--   CREATE DATABASE compraventa_db;
-- y conectarse a ella (en pgAdmin: clic derecho sobre compraventa_db > Query Tool).

DROP TABLE IF EXISTS operaciones;
DROP TABLE IF EXISTS vehiculos;
DROP TABLE IF EXISTS marcas;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS asesores;

-- ---------------------------------------------------------
-- marcas: fabricantes de los vehículos
-- ---------------------------------------------------------
CREATE TABLE marcas (
    id_marca     SERIAL      PRIMARY KEY,
    nombre_marca VARCHAR(50) NOT NULL UNIQUE,
    pais_origen  VARCHAR(50) NOT NULL
);

-- ---------------------------------------------------------
-- vehiculos: inventario del concesionario
-- ---------------------------------------------------------
CREATE TABLE vehiculos (
    id_vehiculo  SERIAL        PRIMARY KEY,
    id_marca     INTEGER       NOT NULL,
    linea        VARCHAR(60)   NOT NULL,
    anio         INTEGER       NOT NULL CHECK (anio BETWEEN 1980 AND 2027),
    placa        VARCHAR(6)    NOT NULL UNIQUE
        CHECK (placa ~ '^[A-Z]{3}[0-9]{2}[0-9A-Z]$'),   -- ABC123 (carro) o ABC12D (moto)
    tipo         VARCHAR(20)   NOT NULL
        CHECK (tipo IN ('Automóvil', 'SUV', 'Camioneta', 'Motocicleta')),
    color        VARCHAR(30)   NOT NULL,
    kilometraje  INTEGER       NOT NULL DEFAULT 0 CHECK (kilometraje >= 0),
    precio_venta NUMERIC(14,2) NOT NULL CHECK (precio_venta > 0),
    estado       VARCHAR(15)   NOT NULL DEFAULT 'Disponible'
        CHECK (estado IN ('Disponible', 'Reservado', 'Vendido')),
    CONSTRAINT fk_vehiculos_marca
        FOREIGN KEY (id_marca) REFERENCES marcas (id_marca)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- ---------------------------------------------------------
-- clientes: personas que le venden o le compran vehículos al concesionario
-- ---------------------------------------------------------
CREATE TABLE clientes (
    id_cliente     SERIAL       PRIMARY KEY,
    documento      VARCHAR(15)  NOT NULL UNIQUE CHECK (documento ~ '^[0-9]{6,15}$'),
    nombre_cliente VARCHAR(100) NOT NULL,
    telefono       VARCHAR(15)  NOT NULL,
    email          VARCHAR(120) UNIQUE,
    ciudad         VARCHAR(60)  NOT NULL
);

-- ---------------------------------------------------------
-- asesores: empleados que atienden cada negocio
-- ---------------------------------------------------------
CREATE TABLE asesores (
    id_asesor           SERIAL       PRIMARY KEY,
    nombre_asesor       VARCHAR(100) NOT NULL,
    telefono            VARCHAR(15)  NOT NULL,
    email               VARCHAR(120) NOT NULL UNIQUE,
    porcentaje_comision NUMERIC(4,2) NOT NULL DEFAULT 0
        CHECK (porcentaje_comision BETWEEN 0 AND 10)    -- 1.50 = 1,5 %
);

-- ---------------------------------------------------------
-- operaciones: cada compra o venta (tabla con 3 llaves foráneas)
--   Compra = el concesionario le compra el vehículo al cliente
--   Venta  = el concesionario le vende el vehículo al cliente
-- ---------------------------------------------------------
CREATE TABLE operaciones (
    id_operacion   SERIAL        PRIMARY KEY,
    fecha          DATE          NOT NULL,
    tipo_operacion VARCHAR(10)   NOT NULL CHECK (tipo_operacion IN ('Compra', 'Venta')),
    id_vehiculo    INTEGER       NOT NULL,
    id_cliente     INTEGER       NOT NULL,
    id_asesor      INTEGER       NOT NULL,
    valor          NUMERIC(14,2) NOT NULL CHECK (valor > 0),
    forma_pago     VARCHAR(15)   NOT NULL
        CHECK (forma_pago IN ('Contado', 'Crédito', 'Permuta')),
    observaciones  VARCHAR(200),
    CONSTRAINT fk_operaciones_vehiculo
        FOREIGN KEY (id_vehiculo) REFERENCES vehiculos (id_vehiculo)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_operaciones_cliente
        FOREIGN KEY (id_cliente)  REFERENCES clientes (id_cliente)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_operaciones_asesor
        FOREIGN KEY (id_asesor)   REFERENCES asesores (id_asesor)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE INDEX idx_vehiculos_marca       ON vehiculos (id_marca);
CREATE INDEX idx_operaciones_vehiculo  ON operaciones (id_vehiculo);
CREATE INDEX idx_operaciones_cliente   ON operaciones (id_cliente);
CREATE INDEX idx_operaciones_asesor    ON operaciones (id_asesor);
CREATE INDEX idx_operaciones_fecha     ON operaciones (fecha);
