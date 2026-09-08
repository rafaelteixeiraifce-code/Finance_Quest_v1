# Importar a sua função de conexão do arquivo database.py
from database import conectar_base

# Definir a função que vai buscar os dados
def listar_instituicoes():
    
    # A) Chamar a função conectar_base() e guardar a conexão
    conexao = conectar_base()

    # B) Criar o cursor
    cursor = conexao.cursor()
    
    # C) Executar o comando SQL: SELECT id, nome, tipo FROM instituicao;
    comandos_sql = """    
SELECT id_instituicao, nome, ativo
FROM instituicao;
""" 
    
    # C.1) Executando o script SQL
    cursor.execute(comandos_sql)

    # D) Guardar o resultado com fetchall()
    dados = cursor.fetchall()
    
    # E) Fechar a conexão
    conexao.close()
    
    # F) Retornar o resultado (return)
    return dados

    
# Definir a função que vai inserir nome de instituição
def inserir_instituicao(nome):
    conexao = conectar_base()
    cursor = conexao.cursor()
    
    comandos_sql = """    
INSERT INTO instituicao (nome) 
VALUES (?);
""" 

    cursor.execute(comandos_sql, (nome,))
    conexao.commit()
    conexao.close()

    
 # Definir a função que vai desativar uma instituição
def desativar_instituicao(id_instituicao):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE instituicao
        SET ativo = 0
        WHERE id_instituicao = ?;
    """, (id_instituicao,))

    linhas_afetadas = cursor.rowcount

    conexao.commit()
    conexao.close()

    return linhas_afetadas

def buscar_instituicao_por_nome(nome):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_instituicao, nome, ativo
        FROM instituicao
        WHERE nome = ?;
    """, (nome,))

    dado = cursor.fetchone()

    conexao.close()
    return dado