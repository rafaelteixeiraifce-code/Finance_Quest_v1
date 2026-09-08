from database import conectar_base

conexao = conectar_base()
cursor = conexao.cursor()

# Primeiro removemos as parcelas vinculadas às compras de teste.
cursor.execute("""
DELETE FROM parcela
WHERE id_compra IN (
    SELECT id_compra
    FROM compra
    WHERE local IN (
        'Livraria Teste',
        'Teste Parcelamento',
        'Teste Parcelamento Final',
        'Teste Antes Fechamento',
        'Teste Depois Fechamento'
    )
);
""")

# Depois removemos as próprias compras.
cursor.execute("""
DELETE FROM compra
WHERE local IN (
    'Livraria Teste',
    'Teste Parcelamento',
    'Teste Parcelamento Final',
    'Teste Antes Fechamento',
    'Teste Depois Fechamento'
);
""")

conexao.commit()

cursor.execute("""
SELECT id_compra, data, local, valor_total
FROM compra;
""")

print("\nCOMPRAS RESTANTES:")
for compra in cursor.fetchall():
    print(compra)

cursor.execute("""
SELECT id_parcela, id_compra, numero_parcela,
       data_vencimento, valor, status
FROM parcela;
""")

print("\nPARCELAS RESTANTES:")
for parcela in cursor.fetchall():
    print(parcela)

conexao.close()