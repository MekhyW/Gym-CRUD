DROP DATABASE IF EXISTS academia;
CREATE DATABASE academia;
USE academia;

CREATE TABLE membros (
    id_membro INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(30) NOT NULL,
    sobrenome VARCHAR(30) NOT NULL,
    celular BIGINT,
    PRIMARY KEY (id_membro)
);

CREATE TABLE planos (
    id_plano INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(30) NOT NULL,
    preco VARCHAR(30) NOT NULL,
    PRIMARY KEY (id_plano)
);

CREATE TABLE assinaturas (
	id_assinatura INT NOT NULL AUTO_INCREMENT,
	id_membro INT NOT NULL,
    id_plano INT NOT NULL,
    data_ativacao DATETIME NOT NULL,
    ativo TINYINT NOT NULL,
    PRIMARY KEY (id_assinatura),
    FOREIGN KEY (id_membro) REFERENCES membros(id_membro),
    FOREIGN KEY (id_plano) REFERENCES planos(id_plano)
);


INSERT INTO membros(nome, sobrenome,celular) VALUES ('Micah','Zassim', 55554433), ('Flip','Liporg', 6942314), ('Adin', 'Samura', 119926183);
INSERT INTO planos(nome, preco) VALUES ('diario',50), ('mensal',150), ('semestral', 600);
INSERT INTO assinaturas(id_membro, id_plano,data_ativacao, ativo) VALUES (1,2,'2001-12-12 00:00:00',1),(2,1,'2001-12-12 00:00:00',1),(3,3,'2001-12-12 00:00:00',0);
Select * from planos;