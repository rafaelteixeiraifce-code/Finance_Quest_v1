import sqlite3

# 1. Abrindo a porta da taverna (conectando ao banco que você acabou de criar)
conexao = sqlite3.connect('finance_quest.db')
cursor = conexao.cursor()

# 2. Preparando os feitiços de inserção
comandos_insert = """
-- Inserindo as Instituições
INSERT INTO instituicao (nome) VALUES ('Bradesco');
INSERT INTO instituicao (nome) VALUES ('Nubank');
INSERT INTO instituicao (nome) VALUES ('Inter');

-- Como o Bradesco foi o primeiro, o banco deu a ele o ID 1 automaticamente.
-- O Nubank recebeu o ID 2, e o Inter o ID 3.

-- Inserindo uma Conta ligada ao Bradesco (ID 1)
INSERT INTO conta (id_instituicao, nome, tipo, saldo_inicial) 
VALUES (1, 'Conta Corrente Principal', 'corrente', 2500.50);

-- Inserindo uma Conta ligada ao Nubank (ID 2)
INSERT INTO conta (id_instituicao, nome, tipo, saldo_inicial) 
VALUES (2, 'Reserva (Caixinhas)', 'poupança', 500.00);
"""

# 3. Executando e salvando
cursor.executescript(comandos_insert)
conexao.commit()
conexao.close()

print("Instituições e Contas criadas com sucesso!")