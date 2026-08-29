# 1. Importar a função que busca os dados do repository
from meio_pagamento_repository import listar_meios_pagamento

# 2. Definir a função de negócio
def obter_resumo_meios_pagamento():
 
    # A) Pedir os dados brutos para o repository
    dados_brutos = listar_meios_pagamento()

    # B) Criar uma lista vazia para guardar os textos formatados
    meios_pagamento_formatados = []
    
    # C) Fazer um loop 'for' passando pela lista de dados brutos
    for id, nome, tipo in dados_brutos:
    
        # D) Dentro do loop, usar uma f-string para montar um texto amigável.           
        texto_amigavel = f"Os meios de pagamento são {id}: {nome} ({tipo})"

        # E) Adicionar esse texto na lista vazia usando o método .append()
        meios_pagamento_formatados.append(texto_amigavel)

    # F) Retornar a lista formatada
    return meios_pagamento_formatados

# 3. A arena de testes
if __name__ == "__main__":
    # Chamar a função, guardar numa variável e imprimir usando um loop para vermos a mágica!
    resultado = obter_resumo_meios_pagamento()
    print("--- RELATÓRIO DE MEIOS DE PAGAMENTO ---")
    for linha in resultado:
        print(linha)
