import sqlite3

conexao = sqlite3.connect('finance_quest.db')
cursor = conexao.cursor()

# Inserindo apenas o cartão
comando_sql = """
INSERT INTO cartao (id_instituicao, nome, limite_total, dia_fechamento, dia_vencimento) 
VALUES (2, 'Roxinho', 1500.00, 5, 10);
"""

cursor.execute(comando_sql)
conexao.commit()
conexao.close()

print("Cartão Roxinho forjado com sucesso!")