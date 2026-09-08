from database import conectar_base


conexao = conectar_base()
cursor = conexao.cursor()

try:

    # ========================================================
    # ADICIONAR id_cartao À COMPRA
    # ========================================================

    cursor.execute(
        "PRAGMA table_info(compra);"
    )

    colunas = [
        coluna[1]
        for coluna in cursor.fetchall()
    ]

    if "id_cartao" not in colunas:

        cursor.execute("""
            ALTER TABLE compra
            ADD COLUMN id_cartao INTEGER
            REFERENCES cartao(id_cartao);
        """)

        print(
            "Coluna id_cartao adicionada à compra."
        )

    else:

        print(
            "Compra já possui id_cartao."
        )


    # ========================================================
    # CORRIGIR COMPRAS ANTIGAS
    # ========================================================
    #
    # As compras existentes foram feitas durante nossos testes
    # usando o Roxinho, cujo id_cartao é 1.
    #
    # Também corrigimos o novo meio de pagamento:
    #
    # 4 = Crédito à vista
    # 5 = Crédito parcelado
    # ========================================================

    cursor.execute("""
        UPDATE compra
        SET id_cartao = 1
        WHERE id_cartao IS NULL;
    """)

    cursor.execute("""
        UPDATE compra
        SET id_meio_pagamento =
            CASE
                WHEN quantidade_parcelas > 1
                THEN 5
                ELSE 4
            END;
    """)


    conexao.commit()


    # ========================================================
    # CONFERÊNCIA
    # ========================================================

    print(
        "\n=== COMPRAS ==="
    )

    cursor.execute("""
        SELECT
            id_compra,
            observacao,
            valor_total,
            quantidade_parcelas,
            id_meio_pagamento,
            id_cartao
        FROM compra
        ORDER BY id_compra;
    """)

    for compra in cursor.fetchall():
        print(compra)


    print(
        "\nCompra + Cartão ajustados com sucesso."
    )


except Exception as erro:

    conexao.rollback()

    print(
        "\nERRO NO AJUSTE."
    )

    print(
        f"Detalhes: {erro}"
    )


finally:

    conexao.close()