from database import conectar_base


def inserir_compra(
    data,
    observacao,
    valor_total,
    id_categoria,
    id_item,
    id_pessoa_pagador,
    id_meio_pagamento,
    id_cartao,
    quantidade_parcelas
):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO compra (
            data,
            observacao,
            valor_total,
            id_categoria,
            id_item,
            id_pessoa_pagador,
            id_meio_pagamento,
            id_cartao,
            quantidade_parcelas
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        data,
        observacao,
        valor_total,
        id_categoria,
        id_item,
        id_pessoa_pagador,
        id_meio_pagamento,
        id_cartao,
        quantidade_parcelas
    ))

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

    cursor.execute("""
        INSERT INTO parcela (
            id_compra,
            numero_parcela,
            data_vencimento,
            valor
        )
        VALUES (?, ?, ?, ?);
    """, (
        id_compra,
        numero_parcela,
        data_vencimento,
        valor
    ))

    conexao.commit()
    conexao.close()


def listar_compras():
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            c.id_compra,
            c.data,
            c.observacao,
            c.valor_total,
            c.quantidade_parcelas,
            c.ativo
        FROM compra c
        ORDER BY c.data DESC,
                 c.id_compra DESC;
    """)

    dados = cursor.fetchall()

    conexao.close()
    return dados


def listar_parcelas_por_compra(id_compra):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id_parcela,
            numero_parcela,
            data_vencimento,
            valor,
            status
        FROM parcela
        WHERE id_compra = ?
        ORDER BY numero_parcela;
    """, (id_compra,))

    dados = cursor.fetchall()

    conexao.close()
    return dados