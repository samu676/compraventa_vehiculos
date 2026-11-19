-- =========================================================
-- Base de datos: compraventa_db
-- Script 2: carga de 10 registros por tabla
-- Ejecutar después de 01_creacion.sql
-- =========================================================

INSERT INTO marcas (nombre_marca, pais_origen) VALUES
('Chevrolet',  'Estados Unidos'),
('Renault',    'Francia'),
('Mazda',      'Japón'),
('Toyota',     'Japón'),
('Kia',        'Corea del Sur'),
('Nissan',     'Japón'),
('Ford',       'Estados Unidos'),
('Volkswagen', 'Alemania'),
('Hyundai',    'Corea del Sur'),
('Yamaha',     'Japón');

-- Las fotos están en static/fotos/ (créditos en docs/creditos_fotos.md)
INSERT INTO vehiculos (id_marca, linea, anio, placa, tipo, color, kilometraje, precio_venta, estado, foto) VALUES
( 1, 'Onix LTZ',            2021, 'JKL482', 'Automóvil',   'Blanco',  38000,  58900000.00, 'Disponible', 'jkl482.jpg'),
( 2, 'Duster Intens',       2019, 'HTR215', 'SUV',         'Gris',    72000,  62500000.00, 'Vendido',    'htr215.jpg'),
( 3, 'Mazda 3 Grand Touring',2022,'MZD903', 'Automóvil',   'Rojo',    21000,  98000000.00, 'Disponible', 'mzd903.jpg'),
( 4, 'Hilux 4x4',           2018, 'TYH118', 'Camioneta',   'Plata',  110000, 135000000.00, 'Vendido',    'tyh118.jpg'),
( 5, 'Picanto Vibrant',     2020, 'KPC774', 'Automóvil',   'Azul',    45000,  42000000.00, 'Reservado',  'kpc774.jpg'),
( 6, 'Frontier',            2017, 'NFR640', 'Camioneta',   'Negro',  128000,  95000000.00, 'Disponible', 'nfr640.jpg'),
( 7, 'Escape SE',           2019, 'FES331', 'SUV',         'Blanco',  64000,  88000000.00, 'Vendido',    'fes331.jpg'),
( 8, 'Gol Trendline',       2016, 'VWG557', 'Automóvil',   'Gris',    96000,  31500000.00, 'Disponible', 'vwg557.jpg'),
( 9, 'Tucson',              2021, 'HTC209', 'SUV',         'Negro',   33000, 118000000.00, 'Disponible', 'htc209.jpg'),
(10, 'FZ 2.0',              2022, 'YMF12G', 'Motocicleta', 'Azul',    15000,  11800000.00, 'Vendido',    'ymf12g.jpg');

INSERT INTO clientes (documento, nombre_cliente, telefono, email, ciudad) VALUES
('1075234567', 'Daniela Castro Ibarra',      '3104567890', 'daniela.castro@mail.com',   'Neiva'),
('1080456123', 'Juan Camilo Rojas',          '3157894561', 'juancrojas@mail.com',       'Neiva'),
('12198765',   'Luis Alberto Medina',        '3006543210', 'luis.medina@mail.com',      'Pitalito'),
('1077889900', 'Sofía Alejandra Tovar',      '3201122334', 'sofia.tovar@mail.com',      'Garzón'),
('36178452',   'Martha Lucía Díaz',          '3112233445', NULL,                         'Campoalegre'),
('1075998877', 'Andrés Mauricio Perdomo',    '3184455667', 'amperdomo@mail.com',        'Neiva'),
('7724519',    'Gustavo Adolfo Silva',       '3015566778', 'gustavo.silva@mail.com',    'Bogotá'),
('1083112233', 'Laura Valentina Ortiz',      '3166677889', 'lauravortiz@mail.com',      'La Plata'),
('1075665544', 'Felipe Andrés Cuenca',       '3127788990', 'felipe.cuenca@mail.com',    'Ibagué'),
('55163874',   'Gloria Inés Bermeo',         '3138899001', 'gloria.bermeo@mail.com',    'Florencia');

INSERT INTO asesores (nombre_asesor, telefono, email, porcentaje_comision) VALUES
('Carolina Muñoz Peña',     '3101239876', 'carolina.munoz@compraventa.co',   2.00),
('Esteban Ramírez Lugo',    '3152348765', 'esteban.ramirez@compraventa.co',  1.50),
('Natalia Quintero Rivas',  '3003457654', 'natalia.quintero@compraventa.co', 2.50),
('Mauricio Cerquera',       '3204566543', 'mauricio.cerquera@compraventa.co',1.75),
('Paula Andrea Salas',      '3115675432', 'paula.salas@compraventa.co',      2.00),
('Óscar Javier Trujillo',   '3186784321', 'oscar.trujillo@compraventa.co',   1.25),
('Isabel Cristina Vega',    '3017893210', 'isabel.vega@compraventa.co',      3.00),
('Diego Fernando Losada',   '3168902109', 'diego.losada@compraventa.co',     2.25),
('Mónica Patricia Arias',   '3129011098', 'monica.arias@compraventa.co',     1.50),
('Ricardo Andrés Polanco',  '3130120987', 'ricardo.polanco@compraventa.co',  2.00);

INSERT INTO operaciones (fecha, tipo_operacion, id_vehiculo, id_cliente, id_asesor, valor, forma_pago, observaciones) VALUES
('2026-08-04', 'Compra',  2, 3,  1,  55000000.00, 'Contado', 'Peritaje aprobado, papeles al día'),
('2026-08-11', 'Compra',  4, 6,  2, 120000000.00, 'Contado', NULL),
('2026-08-20', 'Venta',   2, 1,  3,  61000000.00, 'Crédito', 'Financiado a 48 meses'),
('2026-09-02', 'Compra',  7, 8,  4,  78000000.00, 'Permuta', 'Recibido como parte de pago'),
('2026-09-10', 'Venta',   4, 2,  5, 132000000.00, 'Contado', NULL),
('2026-09-18', 'Compra', 10, 9,  6,   9500000.00, 'Contado', 'SOAT vigente'),
('2026-09-25', 'Venta',   7, 4,  7,  86500000.00, 'Crédito', 'Cuota inicial del 30 %'),
('2026-10-03', 'Venta',  10, 10, 8,  11500000.00, 'Contado', NULL),
('2026-10-15', 'Compra',  9, 5,  9, 105000000.00, 'Permuta', 'Recibido como parte de pago'),
('2026-10-28', 'Compra',  3, 7, 10,  90000000.00, 'Contado', 'Único dueño');
