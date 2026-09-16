import json
import sqlite3
from pathlib import Path


# ============================================================
# CAMINHOS
# ============================================================

PASTA_PROJETO = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

CAMINHO_CONFIG = (
    PASTA_PROJETO
    / "finance_quest_config.json"
)


# ============================================================
# AMBIENTE
# ============================================================

def obter_ambiente():

    # Segurança:
    # se não houver configuração local,
    # o Finance Quest sempre inicia em DEV.
    if not CAMINHO_CONFIG.exists():
        return "dev"

    try:

        with open(
            CAMINHO_CONFIG,
            "r",
            encoding="utf-8"
        ) as arquivo:

            configuracao = json.load(
                arquivo
            )

        ambiente = configuracao.get(
            "ambiente",
            "dev"
        )

        if ambiente not in (
            "dev",
            "real"
        ):
            return "dev"

        return ambiente

    except Exception:
        return "dev"


AMBIENTE = obter_ambiente()


# ============================================================
# BANCO
# ============================================================

if AMBIENTE == "real":

    NOME_BANCO = (
        "finance_quest.db"
    )

else:

    NOME_BANCO = (
        "finance_quest_dev.db"
    )


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

    print(
        f"Ambiente: "
        f"{AMBIENTE.upper()}"
    )

    print(
        f"Banco: {CAMINHO_BANCO}"
    )

    conexao = conectar_base()

    conexao.close()

    print(
        "Conexão realizada com sucesso."
    )