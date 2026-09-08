from database import conectar_base


def listar_compras_para_rateio():
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            c.id_compra,
            c.data,
            c.observacao,
            c.valor_total,
            c.id_pessoa_pagador,
            p.nome

        FROM compra c

        JOIN pessoa p
            ON c.id_pessoa_pagador = p.id

        WHERE c.ativo = 1

        ORDER BY c.data DESC,
                 c.id_compra DESC;
    """)

    dados = cursor.fetchall()

    conexao.close()
    return dados


def buscar_compra_por_id(id_compra):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id_compra,
            valor_total,
            id_pessoa_pagador

        FROM compra

        WHERE id_compra = ?
          AND ativo = 1;
    """, (
        id_compra,
    ))

    compra = cursor.fetchone()

    conexao.close()
    return compra


def listar_participacoes_por_compra(
    id_compra
):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            part.id_participacao,
            part.id_pessoa,
            p.nome,
            part.valor_cota

        FROM participacao part

        JOIN pessoa p
            ON part.id_pessoa = p.id

        WHERE part.id_compra = ?

        ORDER BY p.nome;
    """, (
        id_compra,
    ))

    dados = cursor.fetchall()

    conexao.close()
    return dados


def substituir_rateio(
    id_compra,
    cotas
):
    conexao = conectar_base()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            DELETE FROM participacao
            WHERE id_compra = ?;
        """, (
            id_compra,
        ))

        for (
            id_pessoa,
            valor_cota
        ) in cotas:

            cursor.execute("""
                INSERT INTO participacao (
                    id_compra,
                    id_pessoa,
                    valor_cota
                )
                VALUES (?, ?, ?);
            """, (
                id_compra,
                id_pessoa,
                valor_cota
            ))

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


def listar_dividas_brutas():
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            c.id_compra,

            pagador.id,
            pagador.nome,

            responsavel.id,
            responsavel.nome,

            part.valor_cota

        FROM participacao part

        JOIN compra c
            ON part.id_compra = c.id_compra

        JOIN pessoa pagador
            ON c.id_pessoa_pagador = pagador.id

        JOIN pessoa responsavel
            ON part.id_pessoa = responsavel.id

        WHERE c.ativo = 1
          AND part.id_pessoa
              != c.id_pessoa_pagador;
    """)

    dados = cursor.fetchall()

    conexao.close()
    return dados