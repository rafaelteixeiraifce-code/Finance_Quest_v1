import sqlite3

conexao = sqlite3.connect('finance_quest.db')
cursor = conexao.cursor()

comandos_sql = """
-- 1. O TABULEIRO DO JOGO: Orçamento (Budget Mensal)
CREATE TABLE IF NOT EXISTS orcamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_categoria INTEGER NOT NULL,
    mes_ano TEXT NOT NULL, -- Ex: '2026-08'
    valor_limite REAL NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id)
);

-- 2. O TABULEIRO DO JOGO: Meta (O Grande Loot)
CREATE TABLE IF NOT EXISTS meta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    valor_alvo REAL NOT NULL,
    data_limite TEXT
);

-- 3. O MODO MULTIPLAYER: Participação (Rateio da Conta)
CREATE TABLE IF NOT EXISTS participacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_compra INTEGER NOT NULL,
    id_pessoa INTEGER NOT NULL,
    valor_cota REAL NOT NULL,
    FOREIGN KEY (id_compra) REFERENCES compra(id) ON DELETE CASCADE,
    FOREIGN KEY (id_pessoa) REFERENCES pessoa(id)
);

-- ==========================================
-- INSERINDO DADOS DE TESTE (CENÁRIOS REAIS)
-- ==========================================

-- A) Definindo o Orçamento de Agosto/2026 para Supermercado (Categoria 2)
INSERT INTO orcamento (id_categoria, mes_ano, valor_limite) 
VALUES (2, '2026-08', 1200.00);

-- B) Definindo uma Meta de longo prazo
INSERT INTO meta (nome, valor_alvo, data_limite) 
VALUES ('Fundo de Emergência', 10000.00, '2027-12-31');

-- C) Registrando uma nova Compra (O evento do rateio)
-- Compra ID 2: Um café da manhã no Café Zinn (assumindo Categoria 2 provisoriamente)
INSERT INTO compra (data, local, valor_total, id_categoria, id_pessoa, id_meio_pagamento) 
VALUES ('2026-08-12', 'Café Zinn', 90.00, 2, 1, 2);

-- D) Dividindo a conta do café (Compra ID 2): Rafael (Pessoa 1) e Bruna (Pessoa 3) pagam R$ 45 cada
INSERT INTO participacao (id_compra, id_pessoa, valor_cota) 
VALUES (2, 1, 45.00);

INSERT INTO participacao (id_compra, id_pessoa, valor_cota) 
VALUES (2, 3, 45.00);
"""

cursor.executescript(comandos_sql)
conexao.commit()
conexao.close()

print("Módulos de Orçamento, Meta e Participação forjados com sucesso!")