# 1. Importar a função que busca os dados do repository
from categoria_repository import listar_categorias

# 2. Definir a função de negócio
def obter_resumo_categorias():
 
    # A) Pedir os dados brutos para o repository
    dados_brutos = listar_categorias()

    # B) Criar uma lista vazia para guardar os textos formatados
    categorias_formatadas = []
    
    # C) Fazer um loop 'for' passando pela lista de dados brutos
    for id, nome, tipo in dados_brutos:
    
        # D) Dentro do loop, usar uma f-string para montar um texto amigável. Ex: "Categoria 2: Supermercado (Despesa)"
        texto_amigavel = f"Categoria {id}: {nome} ({tipo})"

        # E) Adicionar esse texto na lista vazia usando o método .append()
        categorias_formatadas.append(texto_amigavel)

    # F) Retornar a lista formatada
    return categorias_formatadas

# 3. A arena de testes
if __name__ == "__main__":
    # Chamar a função, guardar numa variável e imprimir usando um loop para vermos a mágica!
    resultado = obter_resumo_categorias()
    print("--- RELATÓRIO DE CATEGORIAS ---")
    for linha in resultado:
        print(linha)