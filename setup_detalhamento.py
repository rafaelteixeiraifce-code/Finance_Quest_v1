import sqlite3

conexao = sqlite3.connect('finance_quest.db')
cursor = conexao.cursor()

comandos_sql = """
-- 1. A TABELA MESTRE (O Recibo da Compra)
CREATE TABLE IF NOT EXISTS compra (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    local TEXT NOT NULL, 
    valor_total REAL NOT NULL,
    id_categoria INTEGER NOT NULL,
    id_pessoa INTEGER NOT NULL,
    id_meio_pagamento INTEGER NOT NULL,
    ativo INTEGER DEFAULT 1,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id),
    FOREIGN KEY (id_pessoa) REFERENCES pessoa(id),
    FOREIGN KEY (id_meio_pagamento) REFERENCES meio_pagamento(id)
);

-- 2. OS DETALHES DOS ITENS
CREATE TABLE IF NOT EXISTS item_compra (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_compra INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    quantidade INTEGER DEFAULT 1,
    valor_unitario REAL NOT NULL,
    FOREIGN KEY (id_compra) REFERENCES compra(id) ON DELETE CASCADE
);

-- 3. A DILATAÇÃO DO TEMPO (Parcelas)
CREATE TABLE IF NOT EXISTS parcela (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_compra INTEGER NOT NULL,
    numero_parcela INTEGER NOT NULL,
    data_vencimento TEXT NOT NULL,
    valor REAL NOT NULL,
    pago INTEGER DEFAULT 0 CHECK (pago IN (0, 1)), -- 0 = Pendente, 1 = Pago
    FOREIGN KEY (id_compra) REFERENCES compra(id) ON DELETE CASCADE
);

-- ==========================================
-- INSERINDO DADOS DE TESTE (O LOOT DA GUILDA)
-- ==========================================

-- A) Registrando a compra geral (ID 1 gerado automaticamente)
-- Gastamos R$ 160.00 na Jambô Editora (Categoria 2, Pessoa 1, Cartão de Crédito ID 2)
INSERT INTO compra (data, local, valor_total, id_categoria, id_pessoa, id_meio_pagamento) 
VALUES ('2026-08-25', 'Jambô Editora', 160.00, 2, 1, 2);

-- B) Registrando os itens detalhados dessa compra (Ligados ao id_compra 1)
INSERT INTO item_compra (id_compra, descricao, quantidade, valor_unitario) 
VALUES (1, 'Livro A Lenda de Ruff Ghanor', 1, 90.00);

INSERT INTO item_compra (id_compra, descricao, quantidade, valor_unitario) 
VALUES (1, 'Conjunto de Dados D&D', 1, 70.00);

-- C) Registrando o parcelamento em 2x sem juros (Ligados ao id_compra 1)
INSERT INTO parcela (id_compra, numero_parcela, data_vencimento, valor, pago) 
VALUES (1, 1, '2026-09-10', 80.00, 0);

INSERT INTO parcela (id_compra, numero_parcela, data_vencimento, valor, pago) 
VALUES (1, 2, '2026-10-10', 80.00, 0);
"""

cursor.executescript(comandos_sql)
conexao.commit()
conexao.close()

print("As entidades Compra, Item e Parcela foram forjadas e o loot foi registrado com sucesso!")