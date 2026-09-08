from database import conectar_base


def salvar_orcamento(
    id_categoria,
    mes_ano,
    valor_planejado
):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO orcamento (
            id_categoria,
            mes_ano,
            valor_planejado
        )
        VALUES (?, ?, ?)

        ON CONFLICT(id_categoria, mes_ano)
        DO UPDATE SET
            valor_planejado = excluded.valor_planejado;
    """, (
        id_categoria,
        mes_ano,
        valor_planejado
    ))

    conexao.commit()
    conexao.close()


def listar_orcamentos_mes(mes_ano):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            o.id_orcamento,
            o.id_categoria,
            c.nome,
            o.valor_planejado
        FROM orcamento o

        JOIN categoria c
            ON o.id_categoria = c.id

        WHERE o.mes_ano = ?

        ORDER BY c.nome;
    """, (mes_ano,))

    dados = cursor.fetchall()

    conexao.close()

    return dados


def calcular_executado_categoria(
    id_categoria,
    mes_ano,
    id_pessoa_usuario
):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            COALESCE(
                SUM(
                    CASE

                        -- Se a compra possui rateio,
                        -- usamos somente a cota do usuário.
                        WHEN EXISTS (
                            SELECT 1
                            FROM participacao part
                            WHERE part.id_compra = c.id_compra
                        )
                        THEN COALESCE(
                            (
                                SELECT part.valor_cota
                                FROM participacao part
                                WHERE part.id_compra = c.id_compra
                                  AND part.id_pessoa = ?
                            ),
                            0
                        )

                        -- Sem rateio, consideramos o valor
                        -- integral se o usuário for o pagador.
                        WHEN c.id_pessoa_pagador = ?
                        THEN c.valor_total

                        ELSE 0

                    END
                ),
                0
            )

        FROM compra c

        WHERE c.id_categoria = ?
          AND substr(c.data, 1, 7) = ?
          AND c.ativo = 1;
    """, (
        id_pessoa_usuario,
        id_pessoa_usuario,
        id_categoria,
        mes_ano
    ))

    valor = cursor.fetchone()[0]

    conexao.close()

    return valor

if __name__ == "__main__":

    print("ORÇAMENTOS:")
    print(
        listar_orcamentos_mes(
            "2026-08"
        )
    )

    print("\nEXECUTADO CATEGORIA 2:")
    print(
        calcular_executado_categoria(
            2,
            "2026-08"
        )
    )