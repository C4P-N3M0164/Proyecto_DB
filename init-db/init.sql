-- CREATE DATABASE energia;
USE energia;

CREATE TABLE Sistema_Energetico (
    id_sistema INT AUTO_INCREMENT PRIMARY KEY,
    nombre_sistema VARCHAR(100) NOT NULL,
    region VARCHAR(100)
);

CREATE TABLE Agente_Mercado (
    id_agente INT AUTO_INCREMENT PRIMARY KEY,
    nombre_agente VARCHAR(100) NOT NULL,
    tipo_agente VARCHAR(50)
);

CREATE TABLE Precio_Energia (
    id_precio INT AUTO_INCREMENT PRIMARY KEY,
    id_sistema INT,
    fecha DATE NOT NULL,
    valor_cop_kwh DECIMAL(10,5),
    FOREIGN KEY (id_sistema) REFERENCES Sistema_Energetico(id_sistema)
);

CREATE TABLE Demanda_Energetica (
    id_demanda INT AUTO_INCREMENT PRIMARY KEY,
    id_agente INT,
    fecha DATE NOT NULL,
    hora INT NOT NULL,
    valor_kwh DECIMAL(10,2),
    FOREIGN KEY (id_agente) REFERENCES Agente_Mercado(id_agente)
);

CREATE TABLE Transaccion_Energetica (
    id_transaccion INT AUTO_INCREMENT PRIMARY KEY,
    id_agente INT,
    fecha DATE NOT NULL,
    hora INT NOT NULL,
    volumen_kwh DECIMAL(10,2),
    FOREIGN KEY (id_agente) REFERENCES Agente_Mercado(id_agente)
);

-- datos

CREATE TABLE Sistema_Energetico (
    id_sistema INT AUTO_INCREMENT PRIMARY KEY,
    nombre_sistema VARCHAR(100) NOT NULL,
    region VARCHAR(100)
);

CREATE TABLE Agente_Mercado (
    id_agente INT AUTO_INCREMENT PRIMARY KEY,
    nombre_agente VARCHAR(100) NOT NULL,
    tipo_agente VARCHAR(50)
);

CREATE TABLE Precio_Energia (
    id_precio INT AUTO_INCREMENT PRIMARY KEY,
    id_sistema INT NOT NULL,
    fecha DATE NOT NULL,
    valor_cop_kwh DECIMAL(10,5),
    FOREIGN KEY (id_sistema) REFERENCES Sistema_Energetico(id_sistema)
);

CREATE TABLE Demanda_Energetica (
    id_demanda INT AUTO_INCREMENT PRIMARY KEY,
    id_agente INT NOT NULL,
    fecha DATE NOT NULL,
    hora INT NOT NULL CHECK (hora BETWEEN 0 AND 23),
    valor_kwh DECIMAL(10,2),
    FOREIGN KEY (id_agente) REFERENCES Agente_Mercado(id_agente)
);

CREATE TABLE Transaccion_Energetica (
    id_transaccion INT AUTO_INCREMENT PRIMARY KEY,
    id_agente INT NOT NULL,
    fecha DATE NOT NULL,
    hora INT NOT NULL CHECK (hora BETWEEN 0 AND 23),
    volumen_kwh DECIMAL(10,2),
    FOREIGN KEY (id_agente) REFERENCES Agente_Mercado(id_agente)
);

-- Insertar sistemas energéticos
INSERT INTO Sistema_Energetico (nombre_sistema, region) VALUES
('Sistema Nacional Interconectado', 'Centro'),
('Sistema Aislado', 'Norte');

-- Insertar agentes de mercado
INSERT INTO Agente_Mercado (nombre_agente, tipo_agente) VALUES
('Empresa Energética S.A.', 'Distribuidor'),
('Generadora Solar Ltda.', 'Generador');

-- Insertar precios de energía
INSERT INTO Precio_Energia (id_sistema, fecha, valor_cop_kwh) VALUES
(1, '2025-04-28', 320.54321),
(2, '2025-04-28', 350.12345);

-- Insertar demanda energética
INSERT INTO Demanda_Energetica (id_agente, fecha, hora, valor_kwh) VALUES
(1, '2025-04-28', 10, 5000.50),
(1, '2025-04-28', 11, 4800.75),
(2, '2025-04-28', 10, 3000.00);

-- Insertar transacciones energéticas
INSERT INTO Transaccion_Energetica (id_agente, fecha, hora, volumen_kwh) VALUES
(2, '2025-04-28', 10, 1500.25),
(2, '2025-04-28', 11, 1450.00);


-- Para cargar los agentes
LOAD DATA INFILE 'agentes.csv' 
INTO TABLE Agente_Mercado 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 LINES 
(nombre_agente, tipo_agente);

-- Para cargar la demanda
LOAD DATA INFILE 'demanda.csv' 
INTO TABLE Demanda_Energetica 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 LINES 
(nombre_agente, fecha, hora, valor_kwh);

-- Para cargar los precios
LOAD DATA INFILE 'precios.csv' 
INTO TABLE Precio_Energia 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 LINES 
(nombre_sistema, fecha, valor_cop_kwh);

LOAD DATA INFILE 'transacciones.csv' 
INTO TABLE Transaccion_Energetica 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 LINES 
(nombre_agente, fecha, hora, volumen_kwh);