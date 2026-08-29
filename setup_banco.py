import sqlite3

# 1. Conectando ao banco de dados (se o arquivo não existir, o Python o cria automaticamente)
conexao = sqlite3.connect('finance_quest.db')

# 2. Criando um cursor (o "mensageiro" que leva nossos comandos SQL para o banco)
cursor = conexao.cursor()

# 3. Escrevendo nossos comandos SQL
comandos_sql = """
CREATE TABLE IF NOT EXISTS instituicao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
    ativo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS conta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_instituicao INTEGER NOT NULL,
    nome TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('corrente', 'poupança')),
    saldo_inicial REAL DEFAULT 0.0,
    ativo INTEGER DEFAULT 1,
    FOREIGN KEY (id_instituicao) REFERENCES instituicao(id)
);

CREATE TABLE IF NOT EXISTS cartao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_instituicao INTEGER NOT NULL,
    nome TEXT NOT NULL,
    limite_total REAL NOT NULL,
    dia_fechamento INTEGER NOT NULL CHECK (dia_fechamento >= 1 AND dia_fechamento <= 31),
    dia_vencimento INTEGER NOT NULL CHECK (dia_vencimento >= 1 AND dia_vencimento <= 31),
    ativo INTEGER DEFAULT 1,
    FOREIGN KEY (id_instituicao) REFERENCES instituicao(id)
);
"""

# 4. Executando o script SQL inteiro
cursor.executescript(comandos_sql)

# 5. Confirmando as alterações (salvando) e fechando a conexão
conexao.commit()
conexao.close()

print("Banco de dados 'finance_quest.db' criado com sucesso! As tabelas estão prontas.")

