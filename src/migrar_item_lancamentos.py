from database import conectar_base


conexao = conectar_base()
cursor = conexao.cursor()


# ============================================================
# COMPRA
# ============================================================

cursor.execute("PRAGMA table_info(compra);")
colunas_compra = [
    coluna[1]
    for coluna in cursor.fetchall()
]

if "id_item" not in colunas_compra:

    cursor.execute("""
        ALTER TABLE compra
        ADD COLUMN id_item INTEGER
        REFERENCES item(id_item);
    """)

    print("Coluna id_item adicionada à tabela compra.")

else:
    print("Compra já possui id_item.")


# ============================================================
# MOVIMENTAÇÃO
# ============================================================

cursor.execute("PRAGMA table_info(movimentacao);")
colunas_movimentacao = [
    coluna[1]
    for coluna in cursor.fetchall()
]

if "id_item" not in colunas_movimentacao:

    cursor.execute("""
        ALTER TABLE movimentacao
        ADD COLUMN id_item INTEGER
        REFERENCES item(id_item);
    """)

    print("Coluna id_item adicionada à tabela movimentacao.")

else:
    print("Movimentação já possui id_item.")


conexao.commit()


# ============================================================
# CONFERÊNCIA
# ============================================================

print("\n=== COMPRA ===")

cursor.execute("PRAGMA table_info(compra);")

for coluna in cursor.fetchall():
    print(coluna)


print("\n=== MOVIMENTAÇÃO ===")

cursor.execute("PRAGMA table_info(movimentacao);")

for coluna in cursor.fetchall():
    print(coluna)


conexao.close()