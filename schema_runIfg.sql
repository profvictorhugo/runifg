
CREATE DATABASE run_ifg;

USE run_ifg;

CREATE TABLE Modalidade (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

CREATE TABLE Corrida (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    modalidade_id INT NOT NULL,
    data DATE NOT NULL,
    horario TIME NOT NULL,
    local VARCHAR(250) NOT NULL,
    status VARCHAR(100) NOT NULL,
    FOREIGN KEY (modalidade_id) REFERENCES Modalidade(id)
);

CREATE TABLE Provas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    distancia_km DECIMAL(5,2) NOT NULL
);

CREATE TABLE FaixaEtaria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    faixa_etaria VARCHAR(50) NOT NULL
);

CREATE TABLE Categoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    corrida_id INT NOT NULL,
    prova_id INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    previsao_hora_largada TIME NOT NULL,
    faixa_etaria_id INT NOT NULL,
    FOREIGN KEY (corrida_id) REFERENCES Corrida(id),
    FOREIGN KEY (prova_id) REFERENCES Provas(id),
    FOREIGN KEY (faixa_etaria_id) REFERENCES FaixaEtaria(id),
    UNIQUE (corrida_id, prova_id, faixa_etaria_id)
);

CREATE TABLE Atleta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE,
    sexo ENUM('M', 'F') NOT NULL,
    data_nasc DATE NOT NULL,
    email VARCHAR(100)
);

CREATE TABLE Inscricao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    atleta_id INT NOT NULL,
    corrida_id INT NOT NULL,
    categoria_id INT NOT NULL,
    numero INT,
    hora_largada TIME,
    hora_chegada TIME,
    classificacao INT,
    status VARCHAR(100) NOT NULL,
    FOREIGN KEY (atleta_id) REFERENCES Atleta(id),
    FOREIGN KEY (corrida_id) REFERENCES Corrida(id),
    FOREIGN KEY (categoria_id) REFERENCES Categoria(id),
    UNIQUE (corrida_id, numero),
    UNIQUE (atleta_id, corrida_id)
);
