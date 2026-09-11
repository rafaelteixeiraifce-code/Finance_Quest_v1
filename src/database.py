import sqlite3
from pathlib import Path


PASTA_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_BANCO = PASTA_PROJETO / "finance_quest.db"


def conectar_base():
    try:
        return sqlite3.connect(
            CAMINHO_BANCO
        )

    except sqlite3.Error as erro:
        print(
            f"Erro ao conectar ao banco de dados: {erro}"
        )
        raise


if __name__ == "__main__":
    print(
        f"Banco utilizado: {CAMINHO_BANCO}"
    )