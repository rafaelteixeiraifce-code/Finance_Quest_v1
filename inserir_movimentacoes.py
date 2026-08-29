import sqlite3

conexao = sqlite3.connect('finance_quest.db')
cursor = conexao.cursor()

comandos_sql = """
-- 1. CADASTRANDO OS MEIOS DE PAGAMENTO
-- Aqui deixamos o id_cartao vazio (NULL) automaticamente, pois só passamos o id_conta
INSERT INTO meio_pagamento (nome, tipo, id_conta) 
VALUES ('Débito Bradesco', 'conta', 1);

-- Aqui fazemos o inverso: deixamos o id_conta vazio e preenchemos o id_cartao
INSERT INTO meio_pagamento (nome, tipo, id_cartao) 
VALUES ('Crédito Roxinho', 'cartao', 1);


-- 2. CADASTRANDO AS MOVIMENTAÇÕES (O Log de Batalha)
-- O Loot: Receita (id_categoria 1 = Salário), feita por Rafael (id_pessoa 1), caindo no Débito (id_meio_pagamento 1)
INSERT INTO movimentacao (data, descricao, valor, id_categoria, id_pessoa, id_meio_pagamento) 
VALUES ('2026-08-01', 'Salário ALCE', 5500.00, 1, 1, 1);

-- Gasto de Gold: Despesa (id_categoria 2 = Supermercado), feita por Bruna (id_pessoa 3), no Crédito (id_meio_pagamento 2)
INSERT INTO movimentacao (data, descricao, valor, id_categoria, id_pessoa, id_meio_pagamento) 
VALUES ('2026-08-05', 'Compras do Mês', 850.50, 2, 3, 2);

-- Gasto de Gold: Despesa (id_categoria 3 = Transporte), feita por Rafael (id_pessoa 1), no Crédito (id_meio_pagamento 2)
INSERT INTO movimentacao (data, descricao, valor, id_categoria, id_pessoa, id_meio_pagamento) 
VALUES ('2026-08-10', 'Gasolina Honda Civic', 250.00, 3, 1, 2);
"""

cursor.executescript(comandos_sql)
conexao.commit()
conexao.close()

print("Meios de pagamento e movimentações inseridos com sucesso!")