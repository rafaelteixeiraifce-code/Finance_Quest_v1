import sqlite3

conexao = sqlite3.connect('finance_quest.db')
cursor = conexao.cursor()

# O feitiço para derrubar a tabela errada
cursor.execute("DROP TABLE movimentacao;")

conexao.commit()
conexao.close()

print("A tabela 'movimentacao' foi destruída!")