from database import conectar_base


conexao = conectar_base()
cursor = conexao.cursor()


try:
    # ========================================================
    # CONFERIR ESTRUTURA
    # ========================================================

    cursor.execute(
        "PRAGMA table_info(meio_pagamento);"
    )

    colunas = [
        coluna[1]
        for coluna in cursor.fetchall()
    ]

    print(
        "Colunas atuais:",
        colunas
    )


    # ========================================================
    # SUBSTITUIR MEIOS DE PAGAMENTO
    # ========================================================

    cursor.execute("""
        DELETE FROM meio_pagamento;
    """)


    meios = [
        (1, "PIX", "conta"),
        (2, "Débito", "conta"),
        (3, "Transferência", "conta"),
        (4, "Crédito à vista", "cartao"),
        (5, "Crédito parcelado", "cartao")
    ]


    for (
        id_meio,
        nome,
        tipo
    ) in meios:

        cursor.execute("""
            INSERT INTO meio_pagamento (
                id,
                nome,
                tipo,
                id_conta,
                id_cartao,
                ativo
            )
            VALUES (?, ?, ?, NULL, NULL, 1);
        """, (
            id_meio,
            nome,
            tipo
        ))


    conexao.commit()


    # ========================================================
    # CONFERÊNCIA
    # ========================================================

    print(
        "\n=== MEIOS DE PAGAMENTO ==="
    )

    cursor.execute("""
        SELECT
            id,
            nome,
            tipo,
            ativo
        FROM meio_pagamento
        ORDER BY id;
    """)

    for meio in cursor.fetchall():
        print(meio)


    print(
        "\nMeios de pagamento atualizados com sucesso."
    )


except Exception as erro:

    conexao.rollback()

    print(
        "\nERRO AO ATUALIZAR MEIOS DE PAGAMENTO."
    )

    print(
        f"Detalhes: {erro}"
    )


finally:
    conexao.close()