import sqlite3
from pathlib import Path


PASTA_PROJETO = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent
)

CAMINHO_BANCO = (
    PASTA_PROJETO
    / "finance_quest.db"
)


# ============================================================
# PROTEÇÃO
# ============================================================

if CAMINHO_BANCO.exists():

    print(
        "\nATENÇÃO:"
    )

    print(
        "Já existe um banco REAL:"
    )

    print(
        CAMINHO_BANCO
    )

    print(
        "\nPor segurança, nenhuma alteração foi feita."
    )

    raise SystemExit


conexao = sqlite3.connect(
    CAMINHO_BANCO
)

cursor = conexao.cursor()


try:

    cursor.execute(
        "PRAGMA foreign_keys = ON;"
    )


    # ========================================================
    # PESSOA
    # ========================================================

    cursor.execute("""
        CREATE TABLE pessoa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            ativo INTEGER NOT NULL DEFAULT 1
                CHECK (ativo IN (0,1))
        );
    """)


    # ========================================================
    # INSTITUIÇÃO
    # ========================================================

    cursor.execute("""
        CREATE TABLE instituicao (
            id_instituicao INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            ativo INTEGER NOT NULL DEFAULT 1
                CHECK (ativo IN (0,1))
        );
    """)


    # ========================================================
    # CONTA
    # ========================================================

    cursor.execute("""
        CREATE TABLE conta (
            id_conta INTEGER PRIMARY KEY AUTOINCREMENT,
            id_instituicao INTEGER NOT NULL,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL
                CHECK (
                    tipo IN (
                        'corrente',
                        'poupança'
                    )
                ),
            saldo_inicial REAL NOT NULL DEFAULT 0,
            ativo INTEGER NOT NULL DEFAULT 1
                CHECK (ativo IN (0,1)),

            FOREIGN KEY (id_instituicao)
                REFERENCES instituicao(
                    id_instituicao
                )
        );
    """)


    # ========================================================
    # CARTÃO
    # ========================================================

    cursor.execute("""
        CREATE TABLE cartao (
            id_cartao INTEGER PRIMARY KEY AUTOINCREMENT,
            id_instituicao INTEGER NOT NULL,
            nome TEXT NOT NULL UNIQUE,
            limite_total REAL NOT NULL,
            dia_fechamento INTEGER NOT NULL,
            dia_vencimento INTEGER NOT NULL,
            ativo INTEGER NOT NULL DEFAULT 1
                CHECK (ativo IN (0,1)),
            id_pessoa_titular INTEGER,

            FOREIGN KEY (id_instituicao)
                REFERENCES instituicao(
                    id_instituicao
                ),

            FOREIGN KEY (id_pessoa_titular)
                REFERENCES pessoa(id)
        );
    """)


    # ========================================================
    # CATEGORIA
    # ========================================================

    cursor.execute("""
        CREATE TABLE categoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            tipo TEXT NOT NULL DEFAULT 'Despesa',
            ativo INTEGER NOT NULL DEFAULT 1
                CHECK (ativo IN (0,1))
        );
    """)


    # ========================================================
    # ITEM
    # ========================================================

    cursor.execute("""
        CREATE TABLE item (
            id_item INTEGER PRIMARY KEY AUTOINCREMENT,
            id_categoria INTEGER NOT NULL,
            nome TEXT NOT NULL,
            ativo INTEGER NOT NULL DEFAULT 1
                CHECK (ativo IN (0,1)),

            FOREIGN KEY (id_categoria)
                REFERENCES categoria(id)
        );
    """)


    # ========================================================
    # MEIO DE PAGAMENTO
    # ========================================================

    cursor.execute("""
        CREATE TABLE meio_pagamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            tipo TEXT NOT NULL
                CHECK (
                    tipo IN (
                        'conta',
                        'cartao',
                        'dinheiro',
                        'outros'
                    )
                ),
            id_conta INTEGER,
            id_cartao INTEGER,
            ativo INTEGER NOT NULL DEFAULT 1
                CHECK (ativo IN (0,1)),

            FOREIGN KEY (id_conta)
                REFERENCES conta(id_conta),

            FOREIGN KEY (id_cartao)
                REFERENCES cartao(id_cartao)
        );
    """)


    # ========================================================
    # MOVIMENTAÇÃO
    # ========================================================

    cursor.execute("""
        CREATE TABLE movimentacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            tipo TEXT NOT NULL
                CHECK (
                    tipo IN (
                        'entrada',
                        'saida'
                    )
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


    # ========================================================
    # COMPRA
    # ========================================================

    cursor.execute("""
        CREATE TABLE compra (
            id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            observacao TEXT,
            valor_total REAL NOT NULL
                CHECK (valor_total > 0),
            id_categoria INTEGER NOT NULL,
            id_item INTEGER,
            id_pessoa_pagador INTEGER NOT NULL,
            id_meio_pagamento INTEGER NOT NULL,
            id_cartao INTEGER,
            quantidade_parcelas INTEGER NOT NULL DEFAULT 1,
            ativo INTEGER NOT NULL DEFAULT 1
                CHECK (ativo IN (0,1)),

            FOREIGN KEY (id_categoria)
                REFERENCES categoria(id),

            FOREIGN KEY (id_item)
                REFERENCES item(id_item),

            FOREIGN KEY (id_pessoa_pagador)
                REFERENCES pessoa(id),

            FOREIGN KEY (id_meio_pagamento)
                REFERENCES meio_pagamento(id),

            FOREIGN KEY (id_cartao)
                REFERENCES cartao(id_cartao)
        );
    """)


    # ========================================================
    # PARCELA
    # ========================================================

    cursor.execute("""
        CREATE TABLE parcela (
            id_parcela INTEGER PRIMARY KEY AUTOINCREMENT,
            id_compra INTEGER NOT NULL,
            numero_parcela INTEGER NOT NULL,
            data_vencimento TEXT NOT NULL,
            valor REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'pendente',

            FOREIGN KEY (id_compra)
                REFERENCES compra(id_compra)
        );
    """)


    # ========================================================
    # PARTICIPAÇÃO
    # ========================================================

    cursor.execute("""
        CREATE TABLE participacao (
            id_participacao INTEGER PRIMARY KEY AUTOINCREMENT,
            id_compra INTEGER NOT NULL,
            id_pessoa INTEGER NOT NULL,
            valor_cota REAL NOT NULL
                CHECK (valor_cota > 0),

            FOREIGN KEY (id_compra)
                REFERENCES compra(id_compra),

            FOREIGN KEY (id_pessoa)
                REFERENCES pessoa(id),

            UNIQUE (
                id_compra,
                id_pessoa
            )
        );
    """)


    # ========================================================
    # ORÇAMENTO
    # ========================================================

    cursor.execute("""
        CREATE TABLE orcamento (
            id_orcamento INTEGER PRIMARY KEY AUTOINCREMENT,
            id_categoria INTEGER NOT NULL,
            mes_ano TEXT NOT NULL,
            valor_planejado REAL NOT NULL
                CHECK (
                    valor_planejado >= 0
                ),

            FOREIGN KEY (id_categoria)
                REFERENCES categoria(id),

            UNIQUE (
                id_categoria,
                mes_ano
            )
        );
    """)


    # ========================================================
    # META
    # ========================================================

    cursor.execute("""
        CREATE TABLE meta (
            id_meta INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            valor_alvo REAL NOT NULL,
            valor_acumulado REAL NOT NULL DEFAULT 0,
            ativo INTEGER NOT NULL DEFAULT 1
                CHECK (ativo IN (0,1))
        );
    """)


    # ========================================================
    # DADOS INICIAIS REAIS
    # ========================================================

    # Usuário principal
    cursor.execute("""
        INSERT INTO pessoa (
            id,
            nome,
            ativo
        )
        VALUES (
            1,
            'Rafael',
            1
        );
    """)


    # Instituições
    cursor.execute("""
        INSERT INTO instituicao (
            id_instituicao,
            nome,
            ativo
        )
        VALUES
            (1, 'Nubank', 1),
            (2, 'Bradesco', 1),
            (3, 'Inter', 1);
    """)


    # Categorias
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


    # Itens
    itens = [
        (1, "Supermercado"),
        (1, "Delivery"),

        (2, "IPTU"),
        (2, "Energia"),
        (2, "Condomínio"),

        (3, "Kwid (gasolina)"),

        (4, "Passeios"),
        (4, "Itapipoca"),

        (5, "Compras"),
        (5, "Roupas"),
        (5, "Clube Livelo"),
        (5, "Amazon"),
        (5, "Uber"),
        (5, "Presente"),
        (5, "Cartão"),

        (6, "Vivo"),
        (6, "Google One"),
        (6, "Greenlife"),
        (6, "Jangada Revisão Kwid"),
        (6, "Kwid (IPVA ou Revisão)"),
        (6, "Kwid (parcela+seguro)"),

        (8, "Unimed Olívia"),
        (8, "Exame"),
        (8, "Carrinho"),
        (8, "Remédios/Vitaminas"),

        (9, "Ajuda p Mãe"),
        (9, "Psi Mãe"),

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


    # Meios de pagamento
    cursor.execute("""
        INSERT INTO meio_pagamento (
            id,
            nome,
            tipo,
            ativo
        )
        VALUES
            (1, 'PIX', 'conta', 1),
            (2, 'Débito', 'conta', 1),
            (3, 'Transferência', 'conta', 1),
            (4, 'Crédito à vista', 'cartao', 1),
            (5, 'Crédito parcelado', 'cartao', 1);
    """)


    conexao.commit()


    print()
    print("=" * 55)
    print("BANCO REAL CRIADO COM SUCESSO")
    print("=" * 55)

    print(
        f"Banco: {CAMINHO_BANCO}"
    )

    print()
    print(
        "Nenhuma movimentação, compra, parcela "
        "ou orçamento fictício foi criado."
    )


except Exception as erro:

    conexao.rollback()

    print(
        f"\nErro ao criar banco REAL: "
        f"{erro}"
    )


finally:

    conexao.close()