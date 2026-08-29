import sqlite3

# 1. Conectando ao banco
conexao = sqlite3.connect('finance_quest.db')
cursor = conexao.cursor()

# 2. Inserindo uma Categoria
comando_sql = """

INSERT INTO categoria (nome, tipo) 
VALUES ('Salário', 'Receita');

INSERT INTO categoria (nome, tipo) 
VALUES ('Supermercado', 'Despesa');

INSERT INTO categoria (nome, tipo) 
VALUES ('Transporte', 'Despesa');
"""

# 3. Executando e salvando
cursor.executescript(comando_sql)
conexao.commit()
conexao.close()

print("Categorias criadas com sucesso!")