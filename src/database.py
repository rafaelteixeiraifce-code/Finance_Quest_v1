import sqlite3
from pathlib import Path


# ============================================================
# CAMINHO DO BANCO
# ============================================================

# Pasta raiz do projeto:
# Finance_Quest_v1/
PASTA_PROJETO = Path(__file__).resolve().parent.parent

# Banco sempre ficará na raiz do projeto,
# independentemente de onde o programa for executado.
CAMINHO_BANCO = PASTA_PROJETO / "finance_quest.db"


def conectar_base():
    try:
        conexao = sqlite3.connect(
            CAMINHO_BANCO
        )

        print(
            "Conexão bem-sucedida ao banco de dados."
        )

        return conexao

    except sqlite3.Error as erro:

        print(
            f"Erro ao conectar ao banco de dados: {erro}"
        )

        raise


if __name__ == "__main__":

    print(
        f"Banco utilizado: {CAMINHO_BANCO}"
    )

    conexao = conectar_base()

    conexao.close()