from database import conectar_base

# A função agora recebe os ingredientes exatos que a tabela 'movimentacao' exige
def inserir_nova_movimentacao(data, descricao, valor, id_categoria, id_pessoa, id_meio_pagamento):
    conexao = conectar_base()
    cursor = conexao.cursor()
    
    # Usamos interrogações para cada coluna que vamos preencher
    comando_sql = """
    INSERT INTO movimentacao (data, descricao, valor, id_categoria, id_pessoa, id_meio_pagamento)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    
    # Executamos o comando passando a tupla de ingredientes logo em seguida
    cursor.execute(comando_sql, (data, descricao, valor, id_categoria, id_pessoa, id_meio_pagamento))
    
    # O comando obrigatório para SALVAR a escrita no banco (muito importante!)
    conexao.commit()
    conexao.close()
    
 # 3. A arena de testes (O grande gatilho do jogo)
if __name__ == "__main__":
    # 1. Inserindo dados fictícios
    inserir_nova_movimentacao('2026-08-28', 'Teste de Forja', 150.00, 3, 1, 1)
    
    # 2. Imprimimos uma mensagem simples de sucesso
    print("Nova movimentação forjada com sucesso no banco de dados!")
    
def listar_movimentacoes():
    conexao = conectar_base()
    cursor = conexao.cursor()
    
    # A Mágica do JOIN: 
    # 'm' é o apelido de movimentacao, 'c' é o apelido de categoria.
    # Nós pedimos: traga a data(m), a descricao(m), o valor(m) e o nome da categoria(c).
    comando_sql = """
    SELECT m.data, m.descricao, m.valor, c.nome 
    FROM movimentacao m
    JOIN categoria c ON m.id_categoria = c.id;
    """
    
    cursor.execute(comando_sql)
    dados = cursor.fetchall()
    conexao.close()
    return dados