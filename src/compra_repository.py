from database import conectar_base


def inserir_compra(
    data,
    local,
    valor_total,
    id_categoria,
    id_item,
    id_pessoa_pagador,
    id_meio_pagamento,
    quantidade_parcelas
):
    conexao = conectar_base()
    cursor = conexao.cursor()

    comandos_sql = """
    INSERT INTO compra (
        data,
        local,
        valor_total,
        id_categoria,
        id_item,
        id_pessoa_pagador,
        id_meio_pagamento,
        quantidade_parcelas
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
"""

    cursor.execute(
    comandos_sql,
    (
        data,
        local,
        valor_total,
        id_categoria,
        id_item,
        id_pessoa_pagador,
        id_meio_pagamento,
        quantidade_parcelas
    )
)

    id_compra = cursor.lastrowid

    conexao.commit()
    conexao.close()

    return id_compra


def inserir_parcela(
    id_compra,
    numero_parcela,
    data_vencimento,
    valor
):
    conexao = conectar_base()
    cursor = conexao.cursor()

    comandos_sql = """
    INSERT INTO parcela (
        id_compra,
        numero_parcela,
        data_vencimento,
        valor
    )
    VALUES (?, ?, ?, ?);
    """

    cursor.execute(
        comandos_sql,
        (
            id_compra,
            numero_parcela,
            data_vencimento,
            valor
        )
    )

    conexao.commit()
    conexao.close()


def listar_compras():
    conexao = conectar_base()
    cursor = conexao.cursor()

    comandos_sql = """
    SELECT
        c.id_compra,
        c.data,
        c.local,
        c.valor_total,
        c.quantidade_parcelas,
        c.ativo
    FROM compra c
    ORDER BY c.data;
    """

    cursor.execute(comandos_sql)
    dados = cursor.fetchall()

    conexao.close()

    return dados


def listar_parcelas_por_compra(id_compra):
    conexao = conectar_base()
    cursor = conexao.cursor()

    comandos_sql = """
    SELECT
        id_parcela,
        numero_parcela,
        data_vencimento,
        valor,
        status
    FROM parcela
    WHERE id_compra = ?
    ORDER BY numero_parcela;
    """

    cursor.execute(comandos_sql, (id_compra,))
    dados = cursor.fetchall()

    conexao.close()

    return dados

def buscar_cartao_por_meio_pagamento(id_meio_pagamento):
    conexao = conectar_base()
    cursor = conexao.cursor()

    comandos_sql = """
    SELECT
        c.id_cartao,
        c.nome,
        c.dia_fechamento,
        c.dia_vencimento
    FROM meio_pagamento mp
    JOIN cartao c
        ON mp.id_cartao = c.id_cartao
    WHERE mp.id = ?
      AND mp.tipo = 'cartao'
      AND c.ativo = 1;
    """

    cursor.execute(
        comandos_sql,
        (id_meio_pagamento,)
    )

    cartao = cursor.fetchone()

    conexao.close()

    return cartao