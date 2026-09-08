from database import conectar_base


def inserir_movimentacao(
    data,
    tipo,
    descricao,
    valor,
    id_pessoa,
    id_categoria=None,
    id_item=None,
    id_meio_pagamento=None
):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO movimentacao (
            data,
            tipo,
            descricao,
            valor,
            id_categoria,
            id_item,
            id_pessoa,
            id_meio_pagamento
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        data,
        tipo,
        descricao,
        valor,
        id_categoria,
        id_item,
        id_pessoa,
        id_meio_pagamento
    ))

    conexao.commit()
    conexao.close()


def listar_movimentacoes():
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            m.id,
            m.data,
            m.tipo,
            m.descricao,
            m.valor,
            COALESCE(c.nome, '-'),
            COALESCE(i.nome, '-'),
            m.ativo

        FROM movimentacao m

        LEFT JOIN categoria c
            ON m.id_categoria = c.id

        LEFT JOIN item i
            ON m.id_item = i.id_item

        ORDER BY m.data DESC,
                 m.id DESC;
    """)

    dados = cursor.fetchall()

    conexao.close()
    return dados