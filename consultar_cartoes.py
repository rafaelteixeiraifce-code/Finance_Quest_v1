import sqlite3

conexao = sqlite3.connect('finance_quest.db')
cursor = conexao.cursor()

print("=== MEUS CARTÕES E SEUS BANCOS ===")
consulta_cartoes = """
SELECT cartao.nome, cartao.limite_total, instituicao.nome 
FROM cartao
JOIN instituicao ON cartao.id_instituicao = instituicao.id;
"""

cursor.execute(consulta_cartoes)
cartoes = cursor.fetchall() # Guardamos na variável 'cartoes'

for linha in cartoes: # Lemos a variável 'cartoes'
    # linha[0] = nome do cartão | linha[1] = limite | linha[2] = nome da instituição
    print(f"Cartão: {linha[0]} | Limite (Mana): R$ {linha[1]} | Banco: {linha[2]}")

conexao.close()