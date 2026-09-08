import sqlite3

conexao = sqlite3.connect("finance_quest.db")
cursor = conexao.cursor()

cursor.executescript("""
DROP TABLE conta;
ALTER TABLE conta_nova RENAME TO conta;

DROP TABLE cartao;
ALTER TABLE cartao_novo RENAME TO cartao;
""")

conexao.commit()

cursor.execute("PRAGMA table_info(conta);")
print("ESTRUTURA CONTA:")
print(cursor.fetchall())

cursor.execute("SELECT * FROM conta;")
print("DADOS CONTA:")
print(cursor.fetchall())

cursor.execute("PRAGMA table_info(cartao);")
print("\nESTRUTURA CARTAO:")
print(cursor.fetchall())

cursor.execute("SELECT * FROM cartao;")
print("DADOS CARTAO:")
print(cursor.fetchall())

conexao.close()