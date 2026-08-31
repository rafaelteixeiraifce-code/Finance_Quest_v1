import sqlite3
from sqlite3 import Error

def conectar_base():
    connection = None
    try:
        connection = sqlite3.connect("finance_quest.db")
        print("Conexão bem-sucedida ao banco de dados.")
        return connection
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise
if __name__ == "__main__":
    # Coloque seus testes aqui dentro!
    conectar_base()