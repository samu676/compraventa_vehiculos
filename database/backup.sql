-- Backup de compraventa_db generado con pg_dump (PostgreSQL 17) --inserts
-- Restaurar: crear la base compraventa_db y ejecutar este archivo en el Query Tool de pgAdmin
-- o con:  psql -U postgres -d compraventa_db -f backup.sql

--
-- PostgreSQL database dump
--


-- Dumped from database version 17.11
-- Dumped by pg_dump version 17.11

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.vehiculos DROP CONSTRAINT IF EXISTS fk_vehiculos_marca;
ALTER TABLE IF EXISTS ONLY public.operaciones DROP CONSTRAINT IF EXISTS fk_operaciones_vehiculo;
ALTER TABLE IF EXISTS ONLY public.operaciones DROP CONSTRAINT IF EXISTS fk_operaciones_cliente;
ALTER TABLE IF EXISTS ONLY public.operaciones DROP CONSTRAINT IF EXISTS fk_operaciones_asesor;
DROP INDEX IF EXISTS public.idx_vehiculos_marca;
DROP INDEX IF EXISTS public.idx_operaciones_vehiculo;
DROP INDEX IF EXISTS public.idx_operaciones_fecha;
DROP INDEX IF EXISTS public.idx_operaciones_cliente;
DROP INDEX IF EXISTS public.idx_operaciones_asesor;
ALTER TABLE IF EXISTS ONLY public.vehiculos DROP CONSTRAINT IF EXISTS vehiculos_placa_key;
ALTER TABLE IF EXISTS ONLY public.vehiculos DROP CONSTRAINT IF EXISTS vehiculos_pkey;
ALTER TABLE IF EXISTS ONLY public.operaciones DROP CONSTRAINT IF EXISTS operaciones_pkey;
ALTER TABLE IF EXISTS ONLY public.marcas DROP CONSTRAINT IF EXISTS marcas_pkey;
ALTER TABLE IF EXISTS ONLY public.marcas DROP CONSTRAINT IF EXISTS marcas_nombre_marca_key;
ALTER TABLE IF EXISTS ONLY public.clientes DROP CONSTRAINT IF EXISTS clientes_pkey;
ALTER TABLE IF EXISTS ONLY public.clientes DROP CONSTRAINT IF EXISTS clientes_email_key;
ALTER TABLE IF EXISTS ONLY public.clientes DROP CONSTRAINT IF EXISTS clientes_documento_key;
ALTER TABLE IF EXISTS ONLY public.asesores DROP CONSTRAINT IF EXISTS asesores_pkey;
ALTER TABLE IF EXISTS ONLY public.asesores DROP CONSTRAINT IF EXISTS asesores_email_key;
ALTER TABLE IF EXISTS public.vehiculos ALTER COLUMN id_vehiculo DROP DEFAULT;
ALTER TABLE IF EXISTS public.operaciones ALTER COLUMN id_operacion DROP DEFAULT;
ALTER TABLE IF EXISTS public.marcas ALTER COLUMN id_marca DROP DEFAULT;
ALTER TABLE IF EXISTS public.clientes ALTER COLUMN id_cliente DROP DEFAULT;
ALTER TABLE IF EXISTS public.asesores ALTER COLUMN id_asesor DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.vehiculos_id_vehiculo_seq;
DROP TABLE IF EXISTS public.vehiculos;
DROP SEQUENCE IF EXISTS public.operaciones_id_operacion_seq;
DROP TABLE IF EXISTS public.operaciones;
DROP SEQUENCE IF EXISTS public.marcas_id_marca_seq;
DROP TABLE IF EXISTS public.marcas;
DROP SEQUENCE IF EXISTS public.clientes_id_cliente_seq;
DROP TABLE IF EXISTS public.clientes;
DROP SEQUENCE IF EXISTS public.asesores_id_asesor_seq;
DROP TABLE IF EXISTS public.asesores;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: asesores; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.asesores (
    id_asesor integer NOT NULL,
    nombre_asesor character varying(100) NOT NULL,
    telefono character varying(15) NOT NULL,
    email character varying(120) NOT NULL,
    porcentaje_comision numeric(4,2) DEFAULT 0 NOT NULL,
    CONSTRAINT asesores_porcentaje_comision_check CHECK (((porcentaje_comision >= (0)::numeric) AND (porcentaje_comision <= (10)::numeric)))
);


--
-- Name: asesores_id_asesor_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.asesores_id_asesor_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: asesores_id_asesor_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.asesores_id_asesor_seq OWNED BY public.asesores.id_asesor;


--
-- Name: clientes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.clientes (
    id_cliente integer NOT NULL,
    documento character varying(15) NOT NULL,
    nombre_cliente character varying(100) NOT NULL,
    telefono character varying(15) NOT NULL,
    email character varying(120),
    ciudad character varying(60) NOT NULL,
    CONSTRAINT clientes_documento_check CHECK (((documento)::text ~ '^[0-9]{6,15}$'::text))
);


--
-- Name: clientes_id_cliente_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.clientes_id_cliente_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: clientes_id_cliente_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.clientes_id_cliente_seq OWNED BY public.clientes.id_cliente;


--
-- Name: marcas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.marcas (
    id_marca integer NOT NULL,
    nombre_marca character varying(50) NOT NULL,
    pais_origen character varying(50) NOT NULL
);


--
-- Name: marcas_id_marca_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.marcas_id_marca_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: marcas_id_marca_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.marcas_id_marca_seq OWNED BY public.marcas.id_marca;


--
-- Name: operaciones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.operaciones (
    id_operacion integer NOT NULL,
    fecha date NOT NULL,
    tipo_operacion character varying(10) NOT NULL,
    id_vehiculo integer NOT NULL,
    id_cliente integer NOT NULL,
    id_asesor integer NOT NULL,
    valor numeric(14,2) NOT NULL,
    forma_pago character varying(15) NOT NULL,
    observaciones character varying(200),
    CONSTRAINT operaciones_forma_pago_check CHECK (((forma_pago)::text = ANY ((ARRAY['Contado'::character varying, 'Crédito'::character varying, 'Permuta'::character varying])::text[]))),
    CONSTRAINT operaciones_tipo_operacion_check CHECK (((tipo_operacion)::text = ANY ((ARRAY['Compra'::character varying, 'Venta'::character varying])::text[]))),
    CONSTRAINT operaciones_valor_check CHECK ((valor > (0)::numeric))
);


--
-- Name: operaciones_id_operacion_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.operaciones_id_operacion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: operaciones_id_operacion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.operaciones_id_operacion_seq OWNED BY public.operaciones.id_operacion;


--
-- Name: vehiculos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.vehiculos (
    id_vehiculo integer NOT NULL,
    id_marca integer NOT NULL,
    linea character varying(60) NOT NULL,
    anio integer NOT NULL,
    placa character varying(6) NOT NULL,
    tipo character varying(20) NOT NULL,
    color character varying(30) NOT NULL,
    kilometraje integer DEFAULT 0 NOT NULL,
    precio_venta numeric(14,2) NOT NULL,
    estado character varying(15) DEFAULT 'Disponible'::character varying NOT NULL,
    CONSTRAINT vehiculos_anio_check CHECK (((anio >= 1980) AND (anio <= 2027))),
    CONSTRAINT vehiculos_estado_check CHECK (((estado)::text = ANY ((ARRAY['Disponible'::character varying, 'Reservado'::character varying, 'Vendido'::character varying])::text[]))),
    CONSTRAINT vehiculos_kilometraje_check CHECK ((kilometraje >= 0)),
    CONSTRAINT vehiculos_placa_check CHECK (((placa)::text ~ '^[A-Z]{3}[0-9]{2}[0-9A-Z]$'::text)),
    CONSTRAINT vehiculos_precio_venta_check CHECK ((precio_venta > (0)::numeric)),
    CONSTRAINT vehiculos_tipo_check CHECK (((tipo)::text = ANY ((ARRAY['Automóvil'::character varying, 'SUV'::character varying, 'Camioneta'::character varying, 'Motocicleta'::character varying])::text[])))
);


--
-- Name: vehiculos_id_vehiculo_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.vehiculos_id_vehiculo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: vehiculos_id_vehiculo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.vehiculos_id_vehiculo_seq OWNED BY public.vehiculos.id_vehiculo;


--
-- Name: asesores id_asesor; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asesores ALTER COLUMN id_asesor SET DEFAULT nextval('public.asesores_id_asesor_seq'::regclass);


--
-- Name: clientes id_cliente; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clientes ALTER COLUMN id_cliente SET DEFAULT nextval('public.clientes_id_cliente_seq'::regclass);


--
-- Name: marcas id_marca; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.marcas ALTER COLUMN id_marca SET DEFAULT nextval('public.marcas_id_marca_seq'::regclass);


--
-- Name: operaciones id_operacion; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.operaciones ALTER COLUMN id_operacion SET DEFAULT nextval('public.operaciones_id_operacion_seq'::regclass);


--
-- Name: vehiculos id_vehiculo; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehiculos ALTER COLUMN id_vehiculo SET DEFAULT nextval('public.vehiculos_id_vehiculo_seq'::regclass);


--
-- Data for Name: asesores; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.asesores VALUES (1, 'Carolina Muñoz Peña', '3101239876', 'carolina.munoz@compraventa.co', 2.00);
INSERT INTO public.asesores VALUES (2, 'Esteban Ramírez Lugo', '3152348765', 'esteban.ramirez@compraventa.co', 1.50);
INSERT INTO public.asesores VALUES (3, 'Natalia Quintero Rivas', '3003457654', 'natalia.quintero@compraventa.co', 2.50);
INSERT INTO public.asesores VALUES (4, 'Mauricio Cerquera', '3204566543', 'mauricio.cerquera@compraventa.co', 1.75);
INSERT INTO public.asesores VALUES (5, 'Paula Andrea Salas', '3115675432', 'paula.salas@compraventa.co', 2.00);
INSERT INTO public.asesores VALUES (6, 'Óscar Javier Trujillo', '3186784321', 'oscar.trujillo@compraventa.co', 1.25);
INSERT INTO public.asesores VALUES (7, 'Isabel Cristina Vega', '3017893210', 'isabel.vega@compraventa.co', 3.00);
INSERT INTO public.asesores VALUES (8, 'Diego Fernando Losada', '3168902109', 'diego.losada@compraventa.co', 2.25);
INSERT INTO public.asesores VALUES (9, 'Mónica Patricia Arias', '3129011098', 'monica.arias@compraventa.co', 1.50);
INSERT INTO public.asesores VALUES (10, 'Ricardo Andrés Polanco', '3130120987', 'ricardo.polanco@compraventa.co', 2.00);


--
-- Data for Name: clientes; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.clientes VALUES (1, '1075234567', 'Daniela Castro Ibarra', '3104567890', 'daniela.castro@mail.com', 'Neiva');
INSERT INTO public.clientes VALUES (2, '1080456123', 'Juan Camilo Rojas', '3157894561', 'juancrojas@mail.com', 'Neiva');
INSERT INTO public.clientes VALUES (3, '12198765', 'Luis Alberto Medina', '3006543210', 'luis.medina@mail.com', 'Pitalito');
INSERT INTO public.clientes VALUES (4, '1077889900', 'Sofía Alejandra Tovar', '3201122334', 'sofia.tovar@mail.com', 'Garzón');
INSERT INTO public.clientes VALUES (5, '36178452', 'Martha Lucía Díaz', '3112233445', NULL, 'Campoalegre');
INSERT INTO public.clientes VALUES (6, '1075998877', 'Andrés Mauricio Perdomo', '3184455667', 'amperdomo@mail.com', 'Neiva');
INSERT INTO public.clientes VALUES (7, '7724519', 'Gustavo Adolfo Silva', '3015566778', 'gustavo.silva@mail.com', 'Bogotá');
INSERT INTO public.clientes VALUES (8, '1083112233', 'Laura Valentina Ortiz', '3166677889', 'lauravortiz@mail.com', 'La Plata');
INSERT INTO public.clientes VALUES (9, '1075665544', 'Felipe Andrés Cuenca', '3127788990', 'felipe.cuenca@mail.com', 'Ibagué');
INSERT INTO public.clientes VALUES (10, '55163874', 'Gloria Inés Bermeo', '3138899001', 'gloria.bermeo@mail.com', 'Florencia');


--
-- Data for Name: marcas; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.marcas VALUES (1, 'Chevrolet', 'Estados Unidos');
INSERT INTO public.marcas VALUES (2, 'Renault', 'Francia');
INSERT INTO public.marcas VALUES (3, 'Mazda', 'Japón');
INSERT INTO public.marcas VALUES (4, 'Toyota', 'Japón');
INSERT INTO public.marcas VALUES (5, 'Kia', 'Corea del Sur');
INSERT INTO public.marcas VALUES (6, 'Nissan', 'Japón');
INSERT INTO public.marcas VALUES (7, 'Ford', 'Estados Unidos');
INSERT INTO public.marcas VALUES (8, 'Volkswagen', 'Alemania');
INSERT INTO public.marcas VALUES (9, 'Hyundai', 'Corea del Sur');
INSERT INTO public.marcas VALUES (10, 'Yamaha', 'Japón');


--
-- Data for Name: operaciones; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.operaciones VALUES (1, '2026-08-04', 'Compra', 2, 3, 1, 55000000.00, 'Contado', 'Peritaje aprobado, papeles al día');
INSERT INTO public.operaciones VALUES (2, '2026-08-11', 'Compra', 4, 6, 2, 120000000.00, 'Contado', NULL);
INSERT INTO public.operaciones VALUES (3, '2026-08-20', 'Venta', 2, 1, 3, 61000000.00, 'Crédito', 'Financiado a 48 meses');
INSERT INTO public.operaciones VALUES (4, '2026-09-02', 'Compra', 7, 8, 4, 78000000.00, 'Permuta', 'Recibido como parte de pago');
INSERT INTO public.operaciones VALUES (5, '2026-09-10', 'Venta', 4, 2, 5, 132000000.00, 'Contado', NULL);
INSERT INTO public.operaciones VALUES (6, '2026-09-18', 'Compra', 10, 9, 6, 9500000.00, 'Contado', 'SOAT vigente');
INSERT INTO public.operaciones VALUES (7, '2026-09-25', 'Venta', 7, 4, 7, 86500000.00, 'Crédito', 'Cuota inicial del 30 %');
INSERT INTO public.operaciones VALUES (8, '2026-10-03', 'Venta', 10, 10, 8, 11500000.00, 'Contado', NULL);
INSERT INTO public.operaciones VALUES (9, '2026-10-15', 'Compra', 9, 5, 9, 105000000.00, 'Permuta', 'Recibido como parte de pago');
INSERT INTO public.operaciones VALUES (10, '2026-10-28', 'Compra', 3, 7, 10, 90000000.00, 'Contado', 'Único dueño');


--
-- Data for Name: vehiculos; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.vehiculos VALUES (1, 1, 'Onix LTZ', 2021, 'JKL482', 'Automóvil', 'Blanco', 38000, 58900000.00, 'Disponible');
INSERT INTO public.vehiculos VALUES (2, 2, 'Duster Intens', 2019, 'HTR215', 'SUV', 'Gris', 72000, 62500000.00, 'Vendido');
INSERT INTO public.vehiculos VALUES (3, 3, 'Mazda 3 Grand Touring', 2022, 'MZD903', 'Automóvil', 'Rojo', 21000, 98000000.00, 'Disponible');
INSERT INTO public.vehiculos VALUES (4, 4, 'Hilux 4x4', 2018, 'TYH118', 'Camioneta', 'Plata', 110000, 135000000.00, 'Vendido');
INSERT INTO public.vehiculos VALUES (5, 5, 'Picanto Vibrant', 2020, 'KPC774', 'Automóvil', 'Azul', 45000, 42000000.00, 'Reservado');
INSERT INTO public.vehiculos VALUES (6, 6, 'Frontier', 2017, 'NFR640', 'Camioneta', 'Negro', 128000, 95000000.00, 'Disponible');
INSERT INTO public.vehiculos VALUES (7, 7, 'Escape SE', 2019, 'FES331', 'SUV', 'Blanco', 64000, 88000000.00, 'Vendido');
INSERT INTO public.vehiculos VALUES (8, 8, 'Gol Trendline', 2016, 'VWG557', 'Automóvil', 'Gris', 96000, 31500000.00, 'Disponible');
INSERT INTO public.vehiculos VALUES (9, 9, 'Tucson', 2021, 'HTC209', 'SUV', 'Negro', 33000, 118000000.00, 'Disponible');
INSERT INTO public.vehiculos VALUES (10, 10, 'FZ 2.0', 2022, 'YMF12G', 'Motocicleta', 'Azul', 15000, 11800000.00, 'Vendido');


--
-- Name: asesores_id_asesor_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.asesores_id_asesor_seq', 10, true);


--
-- Name: clientes_id_cliente_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.clientes_id_cliente_seq', 10, true);


--
-- Name: marcas_id_marca_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.marcas_id_marca_seq', 10, true);


--
-- Name: operaciones_id_operacion_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.operaciones_id_operacion_seq', 10, true);


--
-- Name: vehiculos_id_vehiculo_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.vehiculos_id_vehiculo_seq', 10, true);


--
-- Name: asesores asesores_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asesores
    ADD CONSTRAINT asesores_email_key UNIQUE (email);


--
-- Name: asesores asesores_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.asesores
    ADD CONSTRAINT asesores_pkey PRIMARY KEY (id_asesor);


--
-- Name: clientes clientes_documento_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_documento_key UNIQUE (documento);


--
-- Name: clientes clientes_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_email_key UNIQUE (email);


--
-- Name: clientes clientes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_pkey PRIMARY KEY (id_cliente);


--
-- Name: marcas marcas_nombre_marca_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.marcas
    ADD CONSTRAINT marcas_nombre_marca_key UNIQUE (nombre_marca);


--
-- Name: marcas marcas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.marcas
    ADD CONSTRAINT marcas_pkey PRIMARY KEY (id_marca);


--
-- Name: operaciones operaciones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.operaciones
    ADD CONSTRAINT operaciones_pkey PRIMARY KEY (id_operacion);


--
-- Name: vehiculos vehiculos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehiculos
    ADD CONSTRAINT vehiculos_pkey PRIMARY KEY (id_vehiculo);


--
-- Name: vehiculos vehiculos_placa_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehiculos
    ADD CONSTRAINT vehiculos_placa_key UNIQUE (placa);


--
-- Name: idx_operaciones_asesor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_operaciones_asesor ON public.operaciones USING btree (id_asesor);


--
-- Name: idx_operaciones_cliente; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_operaciones_cliente ON public.operaciones USING btree (id_cliente);


--
-- Name: idx_operaciones_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_operaciones_fecha ON public.operaciones USING btree (fecha);


--
-- Name: idx_operaciones_vehiculo; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_operaciones_vehiculo ON public.operaciones USING btree (id_vehiculo);


--
-- Name: idx_vehiculos_marca; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_vehiculos_marca ON public.vehiculos USING btree (id_marca);


--
-- Name: operaciones fk_operaciones_asesor; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.operaciones
    ADD CONSTRAINT fk_operaciones_asesor FOREIGN KEY (id_asesor) REFERENCES public.asesores(id_asesor) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: operaciones fk_operaciones_cliente; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.operaciones
    ADD CONSTRAINT fk_operaciones_cliente FOREIGN KEY (id_cliente) REFERENCES public.clientes(id_cliente) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: operaciones fk_operaciones_vehiculo; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.operaciones
    ADD CONSTRAINT fk_operaciones_vehiculo FOREIGN KEY (id_vehiculo) REFERENCES public.vehiculos(id_vehiculo) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: vehiculos fk_vehiculos_marca; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehiculos
    ADD CONSTRAINT fk_vehiculos_marca FOREIGN KEY (id_marca) REFERENCES public.marcas(id_marca) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--


