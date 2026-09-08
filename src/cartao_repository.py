from database import conectar_base


def listar_cartoes():
    conexao = conectar_base()
    cursor = conexao.cursor()

    comandos_sql = """
    SELECT
        c.id_cartao,
        i.nome,
        c.nome,
        c.limite_total,
        c.dia_fechamento,
        c.dia_vencimento,
        c.ativo
    FROM cartao c
    JOIN instituicao i
        ON c.id_instituicao = i.id_instituicao;
    """

    cursor.execute(comandos_sql)
    dados = cursor.fetchall()

    conexao.close()
    return dados


def inserir_cartao(
    id_instituicao,
    nome,
    limite_total,
    dia_fechamento,
    dia_vencimento
):
    conexao = conectar_base()
    cursor = conexao.cursor()

    comandos_sql = """
    INSERT INTO cartao (
        id_instituicao,
        nome,
        limite_total,
        dia_fechamento,
        dia_vencimento
    )
    VALUES (?, ?, ?, ?, ?);
    """

    cursor.execute(
        comandos_sql,
        (
            id_instituicao,
            nome,
            limite_total,
            dia_fechamento,
            dia_vencimento
        )
    )

    conexao.commit()
    conexao.close()


def desativar_cartao(id_cartao):
    conexao = conectar_base()
    cursor = conexao.cursor()

    comandos_sql = """
    UPDATE cartao
    SET ativo = 0
    WHERE id_cartao = ?;
    """

    cursor.execute(comandos_sql, (id_cartao,))

    linhas_afetadas = cursor.rowcount

    conexao.commit()
    conexao.close()

    return linhas_afetadas


def buscar_cartao_por_nome(nome):
    conexao = conectar_base()
    cursor = conexao.cursor()

    comandos_sql = """
    SELECT id_cartao, nome, ativo
    FROM cartao
    WHERE nome = ?;
    """

    cursor.execute(comandos_sql, (nome,))
    dado = cursor.fetchone()

    conexao.close()
    return dado


if __name__ == "__main__":
    print(listar_cartoes())
    
def buscar_cartao_por_id(id_cartao):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id_cartao,
            nome,
            limite_total,
            dia_fechamento,
            dia_vencimento,
            ativo
        FROM cartao
        WHERE id_cartao = ?;
    """, (id_cartao,))

    cartao = cursor.fetchone()

    conexao.close()
    return cartao


def calcular_limite_comprometido(id_cartao):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(p.valor), 0)
        FROM parcela p

        JOIN compra c
            ON p.id_compra = c.id_compra

        JOIN meio_pagamento mp
            ON c.id_meio_pagamento = mp.id

        WHERE mp.id_cartao = ?
          AND p.status = 'pendente'
          AND c.ativo = 1;
    """, (id_cartao,))

    total = cursor.fetchone()[0]

    conexao.close()
    return total


def calcular_fatura_mes(id_cartao, ano_mes):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(p.valor), 0)
        FROM parcela p

        JOIN compra c
            ON p.id_compra = c.id_compra

        JOIN meio_pagamento mp
            ON c.id_meio_pagamento = mp.id

        WHERE mp.id_cartao = ?
          AND substr(p.data_vencimento, 1, 7) = ?
          AND p.status = 'pendente'
          AND c.ativo = 1;
    """, (id_cartao, ano_mes))

    total = cursor.fetchone()[0]

    conexao.close()
    return total