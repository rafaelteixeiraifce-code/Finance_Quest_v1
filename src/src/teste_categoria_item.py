import sqlite3

conexao = sqlite3.connect("finance_quest.db")
cursor = conexao.cursor()


print("\n=== ESTRUTURA CATEGORIA ===")

cursor.execute("PRAGMA table_info(categoria);")

for coluna in cursor.fetchall():
    print(coluna)


print("\n=== DADOS CATEGORIA ===")

cursor.execute("SELECT * FROM categoria;")

for registro in cursor.fetchall():
    print(registro)


print("\n=== ESTRUTURA ITEM_COMPRA ===")

cursor.execute("PRAGMA table_info(item_compra);")

for coluna in cursor.fetchall():
    print(coluna)


print("\n=== DADOS ITEM_COMPRA ===")

cursor.execute("SELECT * FROM item_compra;")

for registro in cursor.fetchall():
    print(registro)


conexao.close()