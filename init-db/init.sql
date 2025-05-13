CREATE DATABASE IF NOT EXISTS energia;
USE energia;

-- Tabla: Agente
CREATE TABLE Agente (
    id INT not null AUTO_INCREMENT PRIMARY KEY,
    NombreAgente VARCHAR(50) NOT NULL UNIQUE
);

-- Tabla: MedicionDemanda
CREATE TABLE MedicionDemanda (
    MedicionID INT not null AUTO_INCREMENT PRIMARY KEY,
    Fecha DATE NOT NULL,
    Hora VARCHAR(2) NOT NULL,
    Valor DECIMAL(14,2) NOT NULL Default 0,
    CodigoAgente VARCHAR(10) NOT NULL,
    AgenteID INT NOT NULL,
    FOREIGN KEY (AgenteID) REFERENCES Agente(id)
);

-- Tabla: DemandaComercial
CREATE TABLE DemandaComercial (
    DemandaComercialID INT not null AUTO_INCREMENT PRIMARY KEY,
    Fecha DATE NOT NULL,
    Hora VARCHAR(2) NOT NULL,
    Codigo VARCHAR(20) NOT NULL,
    Valor DECIMAL(14,2) NOT NULL
);

-- Tabla: CERE
CREATE TABLE Cere (
    CereID INT not null AUTO_INCREMENT PRIMARY KEY,
    Fecha DATE NOT NULL UNIQUE,
    Codigo VARCHAR(20) NOT NULL DEFAULT 'Sistema',
    Valor DECIMAL(14,5) NOT NULL
);

-- Cargar Agente
LOAD DATA INFILE '/var/lib/mysql-files/agentes.csv'
INTO TABLE Agente
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, NombreAgente);

-- Cargar DemandaComercial
LOAD DATA INFILE '/var/lib/mysql-files/demacome_transformado.csv'
INTO TABLE DemandaComercial
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Fecha, Codigo, Hora, Valor);

-- Cargar Cere
LOAD DATA INFILE '/var/lib/mysql-files/cere.csv'
INTO TABLE Cere
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Fecha, Codigo, Valor);

-- Cargar MedicionDemanda (requiere asociar AgenteID en código Python previamente)
LOAD DATA INFILE '/var/lib/mysql-files/demareal_transformado.csv'
INTO TABLE MedicionDemanda
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Fecha, AgenteID, CodigoAgente, Hora, Valor);
