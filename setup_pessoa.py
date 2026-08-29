import sqlite3

#1. Abrindo a porta da taverna
conexao = sqlite3.connect('finance_quest.db')
cursor = conexao.cursor()

#2. Escrevendo o comando SQL
comandos_sql = """
CREATE TABLE IF NOT EXISTS pessoa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    ativo INTEGER DEFAULT 1
);

INSERT INTO pessoa (nome) 
VALUES ('Rafael');

INSERT INTO pessoa (nome) 
VALUES ('Mãe');

INSERT INTO pessoa (nome) 
VALUES ('Bruna');

"""
#3. Executando o script SQL
cursor.executescript(comandos_sql)

#4. Confirmando as alterações e fechando
conexao.commit()
conexao.close()

print("A entidade 'pessoa' foi criada e os dados inseridos com sucesso!")