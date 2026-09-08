import sqlite3

conexao = sqlite3.connect("finance_quest.db")
cursor = conexao.cursor()

cursor.execute("PRAGMA table_info(conta);")
print("CONTA:")
print(cursor.fetchall())

cursor.execute("SELECT * FROM conta;")
print("DADOS CONTA:")
print(cursor.fetchall())

cursor.execute("PRAGMA table_info(cartao);")
print("\nCARTAO:")
print(cursor.fetchall())

cursor.execute("SELECT * FROM cartao;")
print("DADOS CARTAO:")
print(cursor.fetchall())

conexao.close()