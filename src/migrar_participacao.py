import sqlite3

conexao = sqlite3.connect("finance_quest.db")
cursor = conexao.cursor()

cursor.executescript("""
DROP TABLE participacao;

ALTER TABLE participacao_nova
RENAME TO participacao;
""")

conexao.commit()

cursor.execute("PRAGMA table_info(participacao);")
print("ESTRUTURA:")
print(cursor.fetchall())

cursor.execute("SELECT * FROM participacao;")
print("\nDADOS:")
print(cursor.fetchall())

conexao.close()