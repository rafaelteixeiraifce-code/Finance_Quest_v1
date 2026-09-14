import sqlite3


BANCO = "finance_quest.db"
ID_USUARIO_PRINCIPAL = 1


conexao = sqlite3.connect(BANCO)
cursor = conexao.cursor()


try:
    # As FKs serão temporariamente desligadas
    # durante esta migração estrutural.
    cursor.execute("PRAGMA foreign_keys = OFF;")

    conexao.execute("BEGIN;")


    # ========================================================
    # VERIFICAR SE AS CATEGORIAS NOVAS JÁ FORAM APLICADAS
    # ========================================================

    cursor.execute("""
        SELECT id, nome
        FROM categoria
        WHERE id IN (1, 2)
        ORDER BY id;
    """)

    categorias_atuais = cursor.fetchall()

    categorias_ja_migradas = (
        categorias_atuais == [
            (1, "Supermercado"),
            (2, "Moradia")
        ]
    )


    # ========================================================
    # 1. MOVIMENTAÇÃO: ENTRADA / SAÍDA
    # ========================================================

    cursor.execute(
        "PRAGMA table_info(movimentacao);"
    )

    colunas_movimentacao = [
        coluna[1]
        for coluna in cursor.fetchall()
    ]


    if "tipo" not in colunas_movimentacao:

        cursor.execute("""
            CREATE TABLE movimentacao_nova (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                data TEXT NOT NULL,

                tipo TEXT NOT NULL
                    CHECK (
                        tipo IN ('entrada', 'saida')
                    ),

                descricao TEXT NOT NULL,

                valor REAL NOT NULL
                    CHECK (valor > 0),

                id_categoria INTEGER,

                id_item INTEGER,

                id_pessoa INTEGER NOT NULL,

                id_meio_pagamento INTEGER,

                ativo INTEGER NOT NULL DEFAULT 1
                    CHECK (ativo IN (0,1)),

                FOREIGN KEY (id_categoria)
                    REFERENCES categoria(id),

                FOREIGN KEY (id_item)
                    REFERENCES item(id_item),

                FOREIGN KEY (id_pessoa)
                    REFERENCES pessoa(id),

                FOREIGN KEY (id_meio_pagamento)
                    REFERENCES meio_pagamento(id)
            );
        """)


        # ----------------------------------------------------
        # MODELO ANTIGO:
        #
        # Categoria 1 = Salário
        # Categoria 2 = Supermercado
        # Categoria 3 = Transporte
        #
        # TRANSFORMAÇÃO:
        #
        # Salário -> Entrada sem categoria
        # Supermercado antigo 2 -> novo 1
        # Transporte continua 3
        # ----------------------------------------------------

        cursor.execute("""
            INSERT INTO movimentacao_nova (
                id,
                data,
                tipo,
                descricao,
                valor,
                id_categoria,
                id_item,
                id_pessoa,
                id_meio_pagamento,
                ativo
            )

            SELECT
                id,
                data,

                CASE
                    WHEN id_categoria = 1
                    THEN 'entrada'
                    ELSE 'saida'
                END,

                descricao,
                valor,

                CASE
                    WHEN id_categoria = 1
                    THEN NULL

                    WHEN id_categoria = 2
                    THEN 1

                    ELSE id_categoria
                END,

                NULL,

                id_pessoa,

                CASE
                    WHEN id_categoria = 1
                    THEN NULL
                    ELSE id_meio_pagamento
                END,

                ativo

            FROM movimentacao;
        """)

        cursor.execute("""
            DROP TABLE movimentacao;
        """)

        cursor.execute("""
            ALTER TABLE movimentacao_nova
            RENAME TO movimentacao;
        """)

        print(
            "Movimentação convertida para Entrada/Saída."
        )

    else:
        print(
            "Movimentação já possui Entrada/Saída."
        )


    # ========================================================
    # 2. REMAPEAR REFERÊNCIAS DAS CATEGORIAS ANTIGAS
    # ========================================================

    if not categorias_ja_migradas:

        # ----------------------------------------------------
        # COMPRA
        # antigo 2 = Supermercado
        # novo   1 = Supermercado
        # ----------------------------------------------------

        cursor.execute("""
            UPDATE compra
            SET id_categoria = 1
            WHERE id_categoria = 2;
        """)


        # Itens antigos eram apenas de teste.
        cursor.execute("""
            UPDATE compra
            SET id_item = NULL;
        """)


        # ----------------------------------------------------
        # ORÇAMENTO
        # ----------------------------------------------------

        # Qualquer eventual orçamento de Salário
        # não faz sentido no novo modelo.
        cursor.execute("""
            DELETE FROM orcamento
            WHERE id_categoria = 1;
        """)

        cursor.execute("""
            UPDATE orcamento
            SET id_categoria = 1
            WHERE id_categoria = 2;
        """)


        # ====================================================
        # 3. RECRIAR CATEGORIAS DO MODELO REAL
        # ====================================================

        cursor.execute("""
            DELETE FROM categoria;
        """)

        categorias = [
            (1, "Supermercado"),
            (2, "Moradia"),
            (3, "Transporte"),
            (4, "Lazer"),
            (5, "Compras"),
            (6, "Contas"),
            (7, "Metas/Reservas"),
            (8, "Olívia"),
            (9, "Mãe"),
            (10, "Outros")
        ]

        cursor.executemany("""
            INSERT INTO categoria (
                id,
                nome,
                tipo,
                ativo
            )
            VALUES (?, ?, 'Despesa', 1);
        """, categorias)

        print(
            "Categorias atualizadas para o modelo da planilha."
        )

    else:
        print(
            "Categorias já estão no modelo novo."
        )


    # ========================================================
    # 4. RECRIAR ITENS
    # ========================================================

    cursor.execute("""
        UPDATE compra
        SET id_item = NULL;
    """)

    cursor.execute("""
        UPDATE movimentacao
        SET id_item = NULL;
    """)

    cursor.execute("""
        DELETE FROM item;
    """)


    # Estrutura baseada na planilha atual.
    itens = [

        # CAT001 - Supermercado
        (1, "Supermercado"),
        (1, "Delivery"),

        # CAT002 - Moradia
        (2, "IPTU"),
        (2, "Energia"),
        (2, "Condomínio"),

        # CAT003 - Transporte
        (3, "Kwid (gasolina)"),

        # CAT004 - Lazer
        (4, "Passeios"),
        (4, "Itapipoca"),

        # CAT005 - Compras
        (5, "Compras"),
        (5, "Roupas"),
        (5, "Clube Livelo"),
        (5, "Amazon"),
        (5, "Uber"),
        (5, "Presente"),
        (5, "Cartão"),

        # CAT006 - Contas
        (6, "Vivo"),
        (6, "Google One"),
        (6, "Greenlife"),
        (6, "Jangada Revisão Kwid"),
        (6, "Kwid (IPVA ou Revisão)"),
        (6, "Kwid (parcela+seguro)"),

        # CAT008 - Olívia
        (8, "Unimed Olívia"),
        (8, "Exame"),
        (8, "Carrinho"),
        (8, "Remédios/Vitaminas"),

        # CAT009 - Mãe
        (9, "Ajuda p Mãe"),
        (9, "Psi Mãe"),

        # CAT010 - Outros
        (10, "Restaurantes"),
        (10, "Barbearia"),
        (10, "Spotify")
    ]


    cursor.executemany("""
        INSERT INTO item (
            id_categoria,
            nome,
            ativo
        )
        VALUES (?, ?, 1);
    """, itens)

    print(
        "Itens atualizados para o modelo da planilha."
    )


    # ========================================================
    # 5. COMPRA: LOCAL -> OBSERVAÇÃO
    # ========================================================

    cursor.execute(
        "PRAGMA table_info(compra);"
    )

    colunas_compra = [
        coluna[1]
        for coluna in cursor.fetchall()
    ]


    if (
        "local" in colunas_compra
        and "observacao" not in colunas_compra
    ):

        cursor.execute("""
            ALTER TABLE compra
            RENAME COLUMN local TO observacao;
        """)

        print(
            "compra.local foi alterado para observacao."
        )

    else:
        print(
            "Compra já possui observacao."
        )


    # ========================================================
    # 6. TITULAR DO CARTÃO
    # ========================================================

    cursor.execute(
        "PRAGMA table_info(cartao);"
    )

    colunas_cartao = [
        coluna[1]
        for coluna in cursor.fetchall()
    ]


    if "id_pessoa_titular" not in colunas_cartao:

        cursor.execute("""
            ALTER TABLE cartao
            ADD COLUMN id_pessoa_titular INTEGER
            REFERENCES pessoa(id);
        """)

        print(
            "Titular adicionado ao cartão."
        )


    # Os cartões já cadastrados são considerados seus.
    cursor.execute("""
        UPDATE cartao
        SET id_pessoa_titular = ?
        WHERE id_pessoa_titular IS NULL;
    """, (
        ID_USUARIO_PRINCIPAL,
    ))


    # ========================================================
    # 7. COMMIT
    # ========================================================

    conexao.commit()

    print()
    print("=" * 50)
    print("AJUSTES DO MVP CONCLUÍDOS COM SUCESSO")
    print("=" * 50)


except Exception as erro:

    conexao.rollback()

    print()
    print("ERRO NA MIGRAÇÃO.")
    print(
        "Nenhuma alteração desta execução "
        "foi confirmada."
    )
    print(
        f"Detalhes: {erro}"
    )


finally:

    try:
        cursor.execute(
            "PRAGMA foreign_keys = ON;"
        )
    except Exception:
        pass

    conexao.close()