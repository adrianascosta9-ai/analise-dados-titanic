CREATE TABLE IF NOT EXISTS classe (
    classe_id INTEGER PRIMARY KEY,
    descricao TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS passageiro (
    passenger_id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    sexo TEXT NOT NULL,
    idade REAL,
    sobrevivente INTEGER NOT NULL,
    classe_id INTEGER NOT NULL,
    sib_sp INTEGER,
    parch INTEGER,
    ticket TEXT,
    fare REAL,
    embarked TEXT,
    FOREIGN KEY (classe_id) REFERENCES classe(classe_id)
);

INSERT OR IGNORE INTO classe (classe_id, descricao)
VALUES
(1, 'Primeira classe'),
(2, 'Segunda classe'),
(3, 'Terceira classe');