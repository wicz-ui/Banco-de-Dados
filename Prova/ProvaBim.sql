CREATE DATABASE ProvaBim;

USE ProvaBim;

CREATE TABLE Disciplinas (
  codDisciplina INT AUTO_INCREMENT PRIMARY KEY,
  descricao VARCHAR(80) NOT NULL,
  cargaHoraria VARCHAR(6),
  nomeProfessor VARCHAR(80)
);

-- 3 registros
INSERT INTO Disciplinas (descricao, cargaHoraria, nomeProfessor) VALUES
("Banco de Dados", "80", "Carlos"),
("Algoritmos", "60", "Ana"),
("Estrutura de Dados", "100", "Marcos");
