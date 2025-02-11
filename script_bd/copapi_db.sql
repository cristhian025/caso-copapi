/* ============================== BASE DE DATOS COPAPI ==============================*/
-- DROP DATABASE copapi_db; -- comentar si es la primera vez creando la bd
CREATE DATABASE IF NOT EXISTS copapi_db;
Use copapi_db;

/* las siguientes variables son para poder realizar inserts que interactuan con la bitacora para evitar problemas, 
si no se quiere hacer uso de esto entonces no se podra insertar datos sin usar el sistema. otra opcion es quitar de momento los triggers que interactuan con la bitacora */
SET @nombre_personal = "Juan";
SET @rol_personal = "Administrador";

/* ======================== CREACION DE TABLAS =============================== */
CREATE TABLE Rol (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(250) NOT NULL
)engine = innodb;

CREATE TABLE Personal (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombres VARCHAR(60) NOT NULL,
    p_apellido VARCHAR(50) NOT NULL,
    s_apellido VARCHAR(50),
    telefono VARCHAR(15),
    nro_ci VARCHAR(15) NOT NULL UNIQUE
)engine = innodb;

CREATE TABLE Usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
	estado CHAR(1) NOT NULL CHECK (estado IN ('A', 'I')),
    id_personal INT NOT NULL,
    id_rol INT NOT NULL,
    FOREIGN KEY (id_personal) REFERENCES Personal(id),
    FOREIGN KEY (id_rol) REFERENCES Rol(id)
)engine = innodb;

CREATE TABLE Barrio (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    ubicacion VARCHAR(255) NOT NULL
)engine = innodb;

CREATE TABLE Servicio (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    estado CHAR(1) NOT NULL CHECK (estado IN ('A', 'I'))
)engine = innodb;

CREATE TABLE Proyecto (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	nombre VARCHAR(50) NOT NULL UNIQUE,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    estado CHAR(1) NOT NULL CHECK (estado IN ('A', 'C', 'F')), -- Activo, Cancelado, Finalizado
    id_barrio INT NOT NULL,
    FOREIGN KEY (id_barrio) REFERENCES Barrio(id)
)engine = innodb;

CREATE TABLE Proyecto_servicio (
    id_proyecto INT NOT NULL,
    id_servicio INT NOT NULL,
    PRIMARY KEY (id_proyecto, id_servicio),
    FOREIGN KEY (id_proyecto) REFERENCES Proyecto(id),
    FOREIGN KEY (id_servicio) REFERENCES Servicio(id)
)engine = innodb;

CREATE TABLE Encargado_deposito (
    id INT NOT NULL PRIMARY KEY,
    estado CHAR(1) NOT NULL CHECK (estado IN ('A', 'I')),
    FOREIGN KEY (id) REFERENCES Personal(id)
)engine = innodb;

CREATE TABLE Deposito (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    ubicacion VARCHAR(255) NOT NULL
)engine = innodb;

CREATE TABLE Tipo_material (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
)engine = innodb;

CREATE TABLE Material (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    estado CHAR(1) NOT NULL CHECK (estado IN ('A', 'I')),
    descripcion VARCHAR(255) NOT NULL,
    id_tipo_material INT NOT NULL,
    FOREIGN KEY (id_tipo_material) REFERENCES Tipo_material(id)
)engine = innodb;

CREATE TABLE Stock (
    id_deposito INT NOT NULL,
    id_material INT NOT NULL,
    cantidad_material INT NOT NULL,
    PRIMARY KEY (id_deposito, id_material),
    FOREIGN KEY (id_deposito) REFERENCES Deposito(id),
    FOREIGN KEY (id_material) REFERENCES Material(id)
)engine = innodb;

CREATE TABLE Ingreso_material (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fecha_ingreso DATE NOT NULL, -- es la fecha donde llegara el material
    fecha_hora_registro DATETIME, -- es la fecha hora donde se registrara cuando llegue el material
    estado CHAR(1) NOT NULL CHECK (estado IN ('A', 'E', 'C')), -- Activo, Entregado, Cancelado
    observacion VARCHAR(255),
    id_encargado_deposito INT,
    id_deposito INT NOT NULL,
    FOREIGN KEY (id_encargado_deposito) REFERENCES Encargado_deposito(id),
    FOREIGN KEY (id_deposito) REFERENCES Deposito(id)
)engine = innodb;

CREATE TABLE Detalle_ingreso_mat (
    id_ingreso_material INT NOT NULL,
    id_material INT NOT NULL,
    cantidad_material INT NOT NULL,
    PRIMARY KEY (id_ingreso_material, id_material),
    FOREIGN KEY (id_ingreso_material) REFERENCES Ingreso_material(id),
    FOREIGN KEY (id_material) REFERENCES Material(id)
)engine = innodb;

CREATE TABLE Encargado_recepcion (
    id INT NOT NULL PRIMARY KEY,
    estado CHAR(1) NOT NULL CHECK (estado IN ('A', 'I')),
    FOREIGN KEY (id) REFERENCES Personal(id)
)engine = innodb;

CREATE TABLE Chofer (
    id INT NOT NULL PRIMARY KEY,
    estado CHAR(1) NOT NULL CHECK (estado IN ('A', 'I')),
    licencia_conducir VARCHAR(15) NOT NULL,
    FOREIGN KEY (id) REFERENCES Personal(id)
)engine = innodb;

CREATE TABLE Modelo_marca (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    modelo VARCHAR(50) NOT NULL,
    marca VARCHAR(50) NOT NULL
)engine = innodb;

CREATE TABLE Vehiculo (
    placa VARCHAR(10) NOT NULL PRIMARY KEY,
    tipo_vehiculo VARCHAR(50) NOT NULL,
    id_modelo_marca INT NOT NULL,
    FOREIGN KEY (id_modelo_marca) REFERENCES Modelo_marca(id)
)engine = innodb;

CREATE TABLE Transporte (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	fecha_salida DATE NOT NULL, -- fecha salida programada
    fecha_hora_registro DATETIME, -- fecha hora registro de salida del transporte cuando se envia
    observacion VARCHAR(255),
    estado CHAR(1) NOT NULL CHECK (estado IN ('A', 'E', 'C')), -- Activo, Entregado, Cancelado
    id_proyecto INT NOT NULL,
    placa_vehiculo VARCHAR(10),
    id_chofer INT,
    id_encargado_deposito INT,
    FOREIGN KEY (id_proyecto) REFERENCES Proyecto(id),
    FOREIGN KEY (placa_vehiculo) REFERENCES Vehiculo(placa),
    FOREIGN KEY (id_chofer) REFERENCES Chofer(id),
    FOREIGN KEY (id_encargado_deposito) REFERENCES Encargado_deposito(id)
)engine = innodb;

CREATE TABLE Detalle_transporte (
    id_transporte INT NOT NULL,
    id_deposito INT NOT NULL,
    id_material INT NOT NULL,
    cantidad_material INT NOT NULL,
    PRIMARY KEY (id_transporte, id_deposito, id_material),
    FOREIGN KEY (id_transporte) REFERENCES Transporte(id),
    FOREIGN KEY (id_deposito,id_material) REFERENCES Stock(id_deposito,id_material)
)engine = innodb;

CREATE TABLE Recepcion_transporte (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fechahora_entrega DATETIME NOT NULL,
    observacion VARCHAR(255),
    id_encargado_recepcion INT NOT NULL,
    id_transporte INT NOT NULL,
    FOREIGN KEY (id_encargado_recepcion) REFERENCES Encargado_recepcion(id),
    FOREIGN KEY (id_transporte) REFERENCES Transporte(id)
)engine = innodb;

CREATE TABLE Bitacora (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    personal VARCHAR(60) NOT NULL,
	rol VARCHAR(50) NOT NULL,
    operacion VARCHAR(10) NOT NULL,
    tabla VARCHAR(50) NOT NULL,
    fechahora DATETIME NOT NULL,
    detalles TEXT NOT NULL
)engine = innodb;

/* ====================================== PROCEDIMIENTOS ALMACENADOS ====================================== */

-- Verificar credenciales de usuario
DELIMITER //
CREATE PROCEDURE verificar_credencial(
    IN p_usuario VARCHAR(50),
    IN p_password VARCHAR(128)
)
BEGIN	
	SELECT p.nombres, p.p_apellido, p.s_apellido, r.nombre,u.id_personal, u.id, u.id_rol
		FROM personal p
		JOIN usuario u ON u.id_personal = p.id
		JOIN rol r ON r.id = u.id_rol
    WHERE u.usuario = p_usuario AND u.password = SHA2(p_password, 256);
END //
DELIMITER ;

-- Reporte Materiales Enviados
DELIMITER //
CREATE PROCEDURE ReporteMaterialesEnviados (
    IN fecha_inicio DATE,
    IN fecha_fin DATE,
    IN estado_transporte CHAR(1),
    IN minimo_material_total INT
)
BEGIN
    SELECT p.nombre AS proyecto,t.fecha_salida AS salida_programada,t.fecha_hora_registro AS registro_salida, t.estado as estado_transporte,
        tm.nombre AS tipo_material,m.nombre AS material,SUM(dt.cantidad_material) AS total_material
    FROM Proyecto p
        JOIN Transporte t ON p.id = t.id_proyecto
        JOIN Detalle_transporte dt ON t.id = dt.id_transporte
        JOIN Material m ON dt.id_material = m.id
        JOIN Tipo_material tm ON m.id_tipo_material = tm.id
    WHERE 
    	t.fecha_salida BETWEEN fecha_inicio AND fecha_fin
        AND (estado_transporte IS NULL OR t.estado = estado_transporte)
    GROUP BY p.nombre, tm.nombre
    HAVING SUM(dt.cantidad_material) >= minimo_material_total
	ORDER BY t.fecha_salida DESC;
END //
DELIMITER ;

-- Reporte de materiales ingresados a stock
DELIMITER //
CREATE PROCEDURE ReporteMaterialesIngresados (
    IN fecha_inicio DATE,
    IN fecha_fin DATE,
    IN estado_ingreso CHAR(1)
)
BEGIN
	SELECT im.fecha_ingreso as fecha_programada,im.fecha_hora_registro as fecha_hora_registro,im.estado,im.observacion,
		CONCAT(e.nombres,' ',e.p_apellido) AS encargado,d.nombre AS deposito,
		m.nombre AS material,dm.cantidad_material
	FROM Ingreso_material im
	JOIN Detalle_ingreso_mat dm ON im.id = dm.id_ingreso_material
	JOIN Encargado_deposito ed ON im.id_encargado_deposito = ed.id
	JOIN Personal e ON ed.id = e.id
	JOIN Deposito d ON im.id_deposito = d.id
	JOIN Material m ON dm.id_material = m.id
	WHERE 
    	im.fecha_ingreso BETWEEN fecha_inicio AND fecha_fin
        AND (estado_ingreso IS NULL OR im.estado = estado_ingreso)
    ORDER BY im.fecha_ingreso DESC;
END //
DELIMITER ;

-- ReporteStock
DELIMITER //
CREATE PROCEDURE ReporteStock (
    IN p_deposito VARCHAR(50),
    IN p_tipo_material VARCHAR(50)
)
BEGIN
	SELECT d.nombre AS deposito, tm.nombre as tipo_material, m.nombre AS material, m.descripcion, s.cantidad_material
	FROM Stock s
		JOIN Deposito d ON s.id_deposito = d.id
		JOIN Material m ON s.id_material = m.id
		JOIN tipo_material tm ON tm.id = m.id_tipo_material
	WHERE 
		m.estado = 'A'
		AND d.nombre LIKE CONCAT('%',p_deposito, '%')
		AND tm.nombre LIKE CONCAT('%',p_tipo_material, '%');
END //
DELIMITER ;

/* ====================================== TRIGGERS ====================================== */

-- registro de detalle transporte
DELIMITER //
CREATE TRIGGER reg_detalle_transporte
AFTER INSERT ON detalle_transporte
FOR EACH ROW
BEGIN
    UPDATE stock
    SET cantidad_material = cantidad_material - NEW.cantidad_material
    WHERE id_deposito = NEW.id_deposito AND id_material = NEW.id_material;
END;
//
DELIMITER ;

-- TRIGGER DE BITACORA INSERT PROYECTO
DELIMITER //
CREATE TRIGGER after_insert_Proyecto
AFTER INSERT ON Proyecto
FOR EACH ROW
BEGIN
    DECLARE script TEXT;
    SET script = CONCAT(
        'INSERT INTO Proyecto (nombre, fecha_inicio, fecha_fin, estado, id_barrio) VALUES (',
        QUOTE(NEW.nombre), ', ',
        QUOTE(NEW.fecha_inicio), ', ',
        QUOTE(NEW.fecha_fin), ', ',
        QUOTE(NEW.estado), ', ',
        NEW.id_barrio, ');'
    );
    INSERT INTO Bitacora (personal, rol, operacion, tabla, fechahora,detalles)
    VALUES ( @nombre_personal, @rol_personal,'INSERT','Proyecto', NOW(), script);
END//
DELIMITER ;

-- TRIGGER DE BITACORA UPDATE PROYECTO
DELIMITER //
CREATE TRIGGER after_update_Proyecto
AFTER UPDATE ON Proyecto
FOR EACH ROW
BEGIN
    DECLARE script TEXT;
    SET script = CONCAT(
        'UPDATE Proyecto SET nombre = ', QUOTE(NEW.nombre),
        ', fecha_inicio = ', QUOTE(NEW.fecha_inicio),
        ', fecha_fin = ', QUOTE(NEW.fecha_fin),
        ', estado = ', QUOTE(NEW.estado),
        ', id_barrio = ', NEW.id_barrio,
        ' WHERE id = ', NEW.id, ';'
    );
    INSERT INTO Bitacora (personal, rol, operacion, tabla, fechahora, detalles)
    VALUES (@nombre_personal, @rol_personal, 'UPDATE', 'Proyecto', NOW(), script);
END//
DELIMITER ;

-- TRIGGER DE BITACORA INSERT Transporte
DELIMITER //
CREATE TRIGGER after_insert_Transporte
AFTER INSERT ON Transporte
FOR EACH ROW
BEGIN
    DECLARE script TEXT;
    SET script = CONCAT(
        'INSERT INTO Transporte (fecha_salida, fecha_hora_registro, observacion, estado, id_proyecto, 
		placa_vehiculo, id_chofer, id_encargado_deposito) VALUES (',
        QUOTE(NEW.fecha_salida), ', ',
        QUOTE(NEW.fecha_hora_registro), ', ',
        QUOTE(NEW.observacion), ', ',
        QUOTE(NEW.estado), ', ',
        NEW.id_proyecto, ', ',
        IFNULL(QUOTE(NEW.placa_vehiculo), 'NULL'), ', ',
        IFNULL(NEW.id_chofer, 'NULL'), ', ',
        IFNULL(NEW.id_encargado_deposito, 'NULL'), ');'
    );
    INSERT INTO Bitacora (personal, rol, operacion, tabla, fechahora, detalles)
    VALUES (@nombre_personal, @rol_personal, 'INSERT', 'Transporte', NOW(), script);
END//
DELIMITER ;

-- TRIGGER DE BITACORA INSERT Transporte
DELIMITER //
CREATE TRIGGER after_update_Transporte
AFTER UPDATE ON Transporte
FOR EACH ROW
BEGIN
    DECLARE script TEXT;
    SET script = CONCAT(
        'UPDATE Transporte SET fecha_salida = ', QUOTE(NEW.fecha_salida),
        ', fecha_hora_registro = ', IFNULL(QUOTE(NEW.fecha_hora_registro), 'NULL'),
        ', observacion = ', IFNULL(QUOTE(NEW.observacion), 'NULL'),
        ', estado = ', QUOTE(NEW.estado),
        ', id_proyecto = ', NEW.id_proyecto,
        ', placa_vehiculo = ', IFNULL(QUOTE(NEW.placa_vehiculo), 'NULL'),
        ', id_chofer = ', IFNULL(NEW.id_chofer, 'NULL'),
        ', id_encargado_deposito = ', IFNULL(NEW.id_encargado_deposito, 'NULL'),
        ' WHERE id = ', NEW.id, ';'
    );
    INSERT INTO Bitacora (personal, rol, operacion, tabla, fechahora, detalles)
    VALUES (@nombre_personal, @rol_personal, 'UPDATE', 'Transporte', NOW(), script);
END//
DELIMITER ;

/* ====================================== INSERTS ======================================*/
INSERT INTO Rol (nombre, descripcion) VALUES
('Administrador', 'Rol con acceso total al sistema'),
('Encargado de Inventario', 'Responsable del manejo de inventarios'),
('Encargado de Recepción', 'Responsable de recibir materiales en los proyectos');

INSERT INTO Personal (nombres, p_apellido, s_apellido, telefono, nro_ci) VALUES
('Juan', 'Pérez', 'González', '123456789', '1234567'),
('María', 'López', 'Gutiérrez', '987654321', '7654321'),
('Pedro', 'García', 'Martínez', '77733346', '3334446'),
('Luis', 'Peralta', 'Jimenez', '66655511', '4446665'),
('Paco', 'Soto', 'Montes', '456789123', '3334449'),
('Favian', 'Lotore', 'Aguilar', '88899987', '5555889'),
('Aldru', 'Martínez', 'Rodríguez', '321654987', '8765432');

INSERT INTO Usuario (usuario, password, estado, id_personal, id_rol) VALUES
('admin', SHA2('password123', 256), 'A', 1, 1),  -- Usuario administrador
('enc_inv_1', SHA2('password123', 256), 'A', 2, 2),  -- Encargado de Inventario
('enc_inv_2', SHA2('password123', 256), 'A', 3, 2),  -- Encargado de Inventario
('enc_rec_1', SHA2('password123', 256), 'A', 4, 3),  -- Encargado de Recepción
('enc_rec_2', SHA2('password123', 256), 'A', 5, 3);  -- Encargado de Recepción

INSERT INTO Barrio (nombre, ubicacion) VALUES
('Barrio A', 'Noreste de la ciudad, zona de la pampa'),
('Barrio B', 'Av. Lujan, zona urbana');

INSERT INTO Servicio (nombre, estado) VALUES
('Agua Potable', 'A'),
('Alcantarillado Sanitario', 'A');

INSERT INTO Modelo_marca (modelo, marca) VALUES
('Modelo 1', 'Marca A'),
('Modelo 2', 'Marca B');

INSERT INTO Vehiculo (placa, tipo_vehiculo, id_modelo_marca) VALUES
('3004YNG', 'Camion volqueta', 1),
('4003GNY', 'Camion carga', 2);

INSERT INTO Deposito (nombre, ubicacion) VALUES
('Depósito Principal', 'Av. Central 123'),
('Depósito Norte', 'Zona Norte');

INSERT INTO Tipo_material (nombre) VALUES
('Fierro'),
('Cemento'),
('Alquitrán');

INSERT INTO Material (nombre, estado, descripcion, id_tipo_material) VALUES
('Fierro corrugado', 'A', 'Material para estructuras', 1),
('Cemento Portland', 'A', 'Material para construcción', 2),
('Alquitrán líquido', 'A', 'Material para asfaltado', 3);

INSERT INTO Encargado_deposito (id, estado) VALUES
(2, 'A'),
(3, 'A');

INSERT INTO Encargado_recepcion (id, estado) VALUES
(4, 'A'),
(5, 'A');

INSERT INTO Chofer (id, estado, licencia_conducir) VALUES
(6, 'A', '1112227'),
(7, 'A', '2223338');

/* ----------------------------------------- */
INSERT INTO Encargado_deposito (id, estado) VALUES
(1, 'A');

INSERT INTO Encargado_recepcion (id, estado) VALUES
(1, 'A');

INSERT INTO Barrio (nombre, ubicacion) VALUES
('Barrio C', 'Zona C plan 3000'),
('Barrio D', 'Zona D plan 4000'),
('Barrio F', 'Barrio nuevo dia'),
('Barrio G', 'Barrio lindo');
/* ------------------------ INSERTS IMPORTANTES ------------------------------- */
-- Insertar registros en la tabla Stock
INSERT INTO Stock (id_deposito, id_material, cantidad_material) VALUES
(1, 1, 100),
(1, 2, 200),
(1, 3, 150),
(2, 1, 120),
(2, 2, 220),
(2, 3, 180);

-- Insertar registros en la tabla Ingreso_material
INSERT INTO Ingreso_material (fecha_ingreso, fecha_hora_registro, estado, observacion, id_encargado_deposito, id_deposito) VALUES
('2024-01-10', '2024-01-10 10:00:00', 'A', 'Ingreso de fierro', 2, 1),
('2024-01-15', '2024-01-15 11:00:00', 'E', 'Ingreso de cemento', 3, 2),
('2024-02-10', '2024-02-10 12:00:00', 'C', 'Ingreso de alquitrán', 2, 1),
('2024-02-15', '2024-02-15 13:00:00', 'A', 'Ingreso de fierro', 3, 2),
('2024-03-10', '2024-03-10 14:00:00', 'E', 'Ingreso de cemento', 2, 1),
('2024-03-15', '2024-03-15 15:00:00', 'C', 'Ingreso de alquitrán', 3, 2);

-- Insertar registros en la tabla Detalle_ingreso_mat
INSERT INTO Detalle_ingreso_mat (id_ingreso_material, id_material, cantidad_material) VALUES
(1, 1, 50),
(1, 2, 30),
(2, 3, 40),
(2, 1, 20),
(3, 2, 60),
(3, 3, 70),
(4, 1, 50),
(4, 2, 30),
(5, 3, 40),
(5, 1, 20),
(6, 2, 60),
(6, 3, 70);

-- Insertar registros en la tabla Proyecto
INSERT INTO Proyecto (nombre, fecha_inicio, fecha_fin, estado, id_barrio) VALUES
('Proyecto Agua Potable Barrio A', '2023-01-01', '2023-12-31', 'F', 1),
('Proyecto Alcantarillado Barrio B', '2023-02-01', '2023-11-30', 'F', 2),
('Proyecto Renovación Barrio C', '2023-03-01', '2023-09-30', 'F', 3),
('Proyecto Mejoras Barrio D', '2024-01-01', NULL, 'A', 4),
('Proyecto Ampliación Barrio F', '2023-04-01', '2023-10-31', 'F', 5),
('Proyecto Nuevas Conexiones Barrio G', '2024-02-01', NULL, 'A', 6),
('Proyecto Rehabilitación Barrio A', '2023-05-01', '2023-12-15', 'F', 1),
('Proyecto Saneamiento Barrio B', '2023-06-01', NULL, 'C', 2),
('Proyecto Modernización Barrio C', '2024-03-01', NULL, 'A', 3),
('Proyecto Construcción Barrio D', '2023-07-01', '2023-12-31', 'F', 4);


-- Insertar registros en la tabla Proyecto_servicio
INSERT INTO Proyecto_servicio (id_proyecto, id_servicio) VALUES
(1, 1), -- Proyecto Agua Potable Barrio A con servicio de Agua Potable
(2, 2), -- Proyecto Alcantarillado Barrio B con servicio de Alcantarillado Sanitario
(3, 1), -- Proyecto Renovación Barrio C con servicio de Agua Potable
(4, 2), -- Proyecto Mejoras Barrio D con servicio de Alcantarillado Sanitario
(5, 1), -- Proyecto Ampliación Barrio F con servicio de Agua Potable
(6, 2), -- Proyecto Nuevas Conexiones Barrio G con servicio de Alcantarillado Sanitario
(7, 1), -- Proyecto Rehabilitación Barrio A con servicio de Agua Potable
(8, 2), -- Proyecto Saneamiento Barrio B con servicio de Alcantarillado Sanitario
(9, 1), -- Proyecto Modernización Barrio C con servicio de Agua Potable
(10, 2); -- Proyecto Construcción Barrio D con servicio de Alcantarillado Sanitario

-- Insertar registros en la tabla transporte
INSERT INTO `transporte` (`id`, `fecha_salida`, `fecha_hora_registro`, `observacion`, `estado`, `id_proyecto`, `placa_vehiculo`, `id_chofer`, `id_encargado_deposito`) VALUES
(1, '2025-02-11', '2025-02-11 16:31:21', 'prueba 1', 'E', 9, '3004YNG', 6, 1),
(2, '2025-02-11', '2025-02-11 16:31:39', 'prueba 2', 'E', 6, '4003GNY', 7, 1),
(3, '2025-02-11', '2025-02-11 16:33:46', 'prueba 3', 'E', 4, '3004YNG', 6, 1),
(4, '2025-02-11', '2025-02-11 16:34:26', 'prueba 4', 'C', 6, '3004YNG', 6, 1),
(5, '2025-02-12', '2025-02-11 16:36:24', 'prueba 5', 'E', 6, '3004YNG', 6, 1),
(6, '2025-02-10', '2025-02-11 16:38:31', 'prueba 6', 'A', 6, '3004YNG', 6, 1),
(7, '2025-02-11', NULL, NULL, 'A', 9, NULL, NULL, NULL);

-- Insertar registros en la tabla Detalle_transporte
INSERT INTO `detalle_transporte` (`id_transporte`, `id_deposito`, `id_material`, `cantidad_material`) VALUES
(1, 2, 1, 10),
(1, 2, 2, 10),
(1, 2, 3, 10),
(2, 2, 1, 10),
(2, 2, 2, 10),
(2, 2, 3, 10),
(3, 2, 2, 10),
(3, 2, 3, 10),
(4, 1, 1, 10),
(4, 1, 2, 10),
(4, 1, 3, 10),
(5, 1, 2, 5),
(5, 1, 3, 10),
(5, 2, 1, 5),
(6, 1, 2, 30),
(6, 1, 3, 15),
(7, 1, 2, 20),
(7, 2, 2, 30);

-- Insertar registros en la tabla Recepcion_transporte
INSERT INTO `recepcion_transporte` (`id`, `fechahora_entrega`, `observacion`, `id_encargado_recepcion`, `id_transporte`) VALUES
(1, '2025-02-11 16:32:05', 'prueba 1', 1, 1),
(2, '2025-02-11 16:32:14', 'prueba 2', 1, 2),
(3, '2025-02-11 16:34:11', 'prueba 3', 1, 3),
(4, '2025-02-11 16:36:37', 'prueba 5', 1, 5);