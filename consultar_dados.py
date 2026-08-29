import sqlite3

conexao = sqlite3.connect('finance_quest.db')
cursor = conexao.cursor()

print("=== INSTITUIÇÕES CADASTRADAS ===")
cursor.execute("SELECT id, nome, ativo FROM instituicao;")
# O comando fetchall() pega todas as linhas que o SELECT encontrou e traz para o Python
instituicoes = cursor.fetchall() 
for linha in instituicoes:
    print(linha)

print("\n=== CONTAS E SEUS BANCOS (O Poder do JOIN) ===")
consulta_contas = """
SELECT conta.nome, conta.tipo, instituicao.nome 
FROM conta
JOIN instituicao ON conta.id_instituicao = instituicao.id;
"""
cursor.execute(consulta_contas)
contas = cursor.fetchall()
for linha in contas:
    # Acessando as colunas pelo índice (0 = nome da conta, 1 = tipo, 2 = nome do banco)
    print(f"Conta: {linha[0]} | Tipo: {linha[1]} | Banco: {linha[2]}")

conexao.close()