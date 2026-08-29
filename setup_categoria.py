import sqlite3

#1. Abrindo a porta da taverna
conexao = sqlite3.connect('finance_quest.db')
cursor = conexao.cursor()

#2. Escrevendo o comando SQL
comandos_sql = """
CREATE TABLE IF NOT EXISTS categoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    tipo TEXT NOT NULL CHECK (tipo IN ('Receita', 'Despesa')),
    ativo INTEGER DEFAULT 1
);
"""
#3. Executando o script SQL
cursor.executescript(comandos_sql)

#4. Confirmando as alterações e fechando
conexao.commit()
conexao.close()

print("A entidade 'categoria' foi criada com sucesso!")