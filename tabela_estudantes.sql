USE DBCOMERCIAL;

DROP TABLE IF EXISTS estudantes;

CREATE TABLE estudantes (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  data_nascimento DATE NULL,
  regiao VARCHAR(30) NOT NULL,
  possui_veiculo ENUM('Sim', 'Não') NOT NULL DEFAULT 'Não',
  ocupacao VARCHAR(100) NOT NULL,
  PRIMARY KEY (id),
  INDEX idx_regiao (regiao),
  INDEX idx_ativo (possui_veiculo),
  INDEX idx_data_evento (data_nascimento)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO estudantes (data_nascimento, regiao, possui_veiculo, ocupacao) VALUES
('2006-10-10', 'Leste', 'Não', 'analista de suporte'),
('2026-09-06', 'Sul',   'Sim', 'Produção'),
('1993-05-01', 'Oeste', 'Não', 'Estoquista'),
('1998-01-30', 'Oeste', 'Sim', 'Estudante'),
('2003-12-13', 'Oeste', 'Não', 'Auxiliar Financeiro'),
('2000-05-19', 'Oeste', 'Não', 'Assistente de TI'),
('1976-05-03', 'Oeste', 'Não', 'Estudante'),
('1977-05-16', 'Norte', 'Não', 'Organização'),
('2002-08-30', 'Cambé', 'Não', 'Estudante');

select * from estudantes;

-- 1. 
SELECT * FROM estudantes
WHERE data_nascimento IS NOT NULL AND data_nascimento > DATE_SUB(CURDATE(), INTERVAL 18 YEAR);
-- 2. 
SELECT * FROM estudantes
WHERE data_nascimento IS NOT NULL AND data_nascimento <= DATE_SUB(CURDATE(), INTERVAL 18 YEAR);
-- 3. 
SELECT * FROM estudantes WHERE possui_veiculo = 'Sim';
-- 4. 
SELECT regiao FROM estudantes;
-- 5. 
SELECT * FROM estudantes WHERE ocupacao LIKE '%TI%';
-- 6. 
SELECT * FROM estudantes WHERE ocupacao + 'Estudante' AND possui_veiculo = 'Sim';
-- 7.
-- A maioria não tem carro, mora na região oeste, quase todos tem ocupação e tinha uma inconsistência na data (id = 2)
--
UPDATE estudantes SET data_nascimento = '2008-05-20' WHERE id = 2;
