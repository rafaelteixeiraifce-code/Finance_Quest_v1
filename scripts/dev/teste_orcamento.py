import sqlite3

conexao = sqlite3.connect("finance_quest.db")
cursor = conexao.cursor()

cursor.execute("PRAGMA table_info(orcamento);")
print("ESTRUTURA:")
print(cursor.fetchall())

cursor.execute("SELECT * FROM orcamento;")
print("\nDADOS:")
print(cursor.fetchall())

conexao.close()