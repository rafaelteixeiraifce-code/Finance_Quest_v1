from database import conectar_base


# ============================================================
# ORÇAMENTO PLANEJADO
# ============================================================

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
    """, (
        mes_ano,
    ))

    dados = cursor.fetchall()

    conexao.close()

    return dados


# ============================================================
# SAÍDAS DIRETAS
# PIX / DÉBITO / TRANSFERÊNCIA
# ============================================================

def calcular_saidas_diretas(
    id_categoria,
    mes_ano,
    id_pessoa_usuario
):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            COALESCE(
                SUM(m.valor),
                0
            )

        FROM movimentacao m

        WHERE m.tipo = 'saida'

          AND m.id_categoria = ?

          AND m.id_pessoa = ?

          AND substr(
                m.data,
                1,
                7
              ) = ?

          AND m.ativo = 1;
    """, (
        id_categoria,
        id_pessoa_usuario,
        mes_ano
    ))

    valor = cursor.fetchone()[0]

    conexao.close()

    return valor


# ============================================================
# PARCELAS DE CARTÃO DO MÊS
# ============================================================

def calcular_parcelas_responsabilidade(
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

                        -- Existe rateio/responsabilidade
                        -- registrada para essa pessoa.
                        WHEN part.valor_cota IS NOT NULL

                        THEN
                            p.valor
                            *
                            (
                                part.valor_cota
                                / c.valor_total
                            )


                        -- Fallback para compras antigas:
                        -- sem participação registrada,
                        -- mas pagas pelo próprio usuário.
                        WHEN NOT EXISTS (
                            SELECT 1
                            FROM participacao px
                            WHERE px.id_compra = c.id_compra
                        )
                        AND c.id_pessoa_pagador = ?

                        THEN p.valor


                        ELSE 0

                    END
                ),
                0
            )

        FROM parcela p

        JOIN compra c
            ON p.id_compra = c.id_compra

        LEFT JOIN participacao part
            ON part.id_compra = c.id_compra
           AND part.id_pessoa = ?

        WHERE c.id_categoria = ?

          AND substr(
                p.data_vencimento,
                1,
                7
              ) = ?

          AND c.ativo = 1

          AND p.status = 'pendente';
    """, (
        id_pessoa_usuario,
        id_pessoa_usuario,
        id_categoria,
        mes_ano
    ))

    valor = cursor.fetchone()[0]

    conexao.close()

    return round(
        valor,
        2
    )


# ============================================================
# EXECUTADO TOTAL
# ============================================================

def calcular_executado_categoria(
    id_categoria,
    mes_ano,
    id_pessoa_usuario
):
    saidas_diretas = calcular_saidas_diretas(
        id_categoria,
        mes_ano,
        id_pessoa_usuario
    )

    parcelas_cartao = (
        calcular_parcelas_responsabilidade(
            id_categoria,
            mes_ano,
            id_pessoa_usuario
        )
    )

    executado = (
        saidas_diretas
        + parcelas_cartao
    )

    return round(
        executado,
        2
    )

