import sqlite3
from pathlib import Path


# ============================================================
# CONFIGURAÇÃO DO AMBIENTE
# ============================================================

# True  = banco de desenvolvimento/testes
# False = banco de uso real
MODO_DEV = True


# ============================================================
# CAMINHOS
# ============================================================

PASTA_PROJETO = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

if MODO_DEV:
    NOME_BANCO = "finance_quest_dev.db"
else:
    NOME_BANCO = "finance_quest.db"

CAMINHO_BANCO = (
    PASTA_PROJETO
    / NOME_BANCO
)


# ============================================================
# CONEXÃO
# ============================================================

def conectar_base():

    try:

        conexao = sqlite3.connect(
            CAMINHO_BANCO
        )

        conexao.execute(
            "PRAGMA foreign_keys = ON;"
        )

        return conexao

    except sqlite3.Error as erro:

        print(
            f"Erro ao conectar ao banco: "
            f"{erro}"
        )

        raise


# ============================================================
# TESTE DIRETO
# ============================================================

if __name__ == "__main__":

    ambiente = (
        "DESENVOLVIMENTO"
        if MODO_DEV
        else "USO REAL"
    )

    print(
        f"Ambiente: {ambiente}"
    )

    print(
        f"Banco: {CAMINHO_BANCO}"
    )

    conexao = conectar_base()
    conexao.close()

    print(
        "Conexão realizada com sucesso."
    )