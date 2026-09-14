from database import conectar_base, CAMINHO_BANCO


print("\nBANCO USADO PELO SISTEMA:")
print(CAMINHO_BANCO)


conexao = conectar_base()
cursor = conexao.cursor()


cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name;
""")

print("\nTABELAS ENCONTRADAS:")

tabelas = cursor.fetchall()

for tabela in tabelas:
    print(tabela[0])


conexao.close()