import sqlite3

#1. Importar a sua função de conexão do arquivo database.py
from database import conectar_base

#2. Definir a função que vai buscar os dados
def listar_meios_pagamento():
    
    # A) Chamar a função conectar_base() e guardar a conexão
    conexao = conectar_base()

    # B) Criar o cursor
    cursor = conexao.cursor()
    
    # C) Executar o comando SQL: SELECT id, nome, tipo FROM categoria;
    comandos_sql = """    
    SELECT id, nome, tipo FROM meio_pagamento;
""" 
    
    # C.1) Executando o script SQL
    cursor.execute(comandos_sql)

    # D) Guardar o resultado com fetchall()
    dados = cursor.fetchall()
    
    # E) Fechar a conexão
    conexao.close()
    
    # F) Retornar o resultado (return)
    return dados

# 3. A arena de testes
if __name__ == "__main__":
    # Chamar a função listar_meios_pagamento(), guardar o retorno em uma variável e imprimir (print) para testar!
    resultado = listar_meios_pagamento()
    print(resultado)