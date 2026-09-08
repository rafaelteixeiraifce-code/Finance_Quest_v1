import sqlite3

conexao = sqlite3.connect("finance_quest.db")
cursor = conexao.cursor()

cursor.execute("PRAGMA table_info(compra);")
print("ESTRUTURA COMPRA:")
print(cursor.fetchall())

cursor.execute("SELECT * FROM compra;")
print("\nDADOS COMPRA:")
print(cursor.fetchall())

cursor.execute("PRAGMA table_info(parcela);")
print("\nESTRUTURA PARCELA:")
print(cursor.fetchall())

cursor.execute("SELECT * FROM parcela;")
print("\nDADOS PARCELA:")
print(cursor.fetchall())

conexao.close()