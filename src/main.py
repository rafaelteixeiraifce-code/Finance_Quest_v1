# 1. Importar o Service que acabamos de criar
from categoria_service import obter_resumo_categorias
from meio_pagamento_service import obter_resumo_meios_pagamento
from movimentacao_service import registrar_movimentacao
from movimentacao_service import obter_resumo_movimentacoes

# 2. Definir a função do Menu Principal
def iniciar_taverna():

    # A) Iniciar o loop infinito
    while True:

        # B) Mostrar as opções com print() (Ex: 1. Ver categorias, 0. Sair)
        print('Escolha uma das opções válidas: 1. Ver categorias, 2. Ver meios de pagamento, 3. Nova Movimentação, 4. Ver Movimentações, 0. Sair')

        # C) Capturar a escolha do usuário com input()
        escolha = input("Digite sua opção: ")

        # D) Fazer as checagens com if/elif/else:
        # Se a escolha for '1':
        if escolha == '1':
            # Chama o obter_resumo_categorias(), guarda o resultado e faz o loop for para imprimir na tela
            resultado = obter_resumo_categorias()          
            for linha in resultado:
                    print(linha)

        # Se a escolha for '2':
        elif escolha == '2':
            # Chama o obter_resumo_meios_pagamento(), guarda o resultado e faz o loop for para imprimir na tela
            resultado = obter_resumo_meios_pagamento()          
            for linha in resultado:
                    print(linha)

        # Se a escolha for '3':
        elif escolha == '3':
            print("\n--- FORJANDO NOVA MOVIMENTAÇÃO ---")
            
            # A) Faça as perguntas e guarde as respostas
            data_mov = input("Data (YYYY-MM-DD): ")
            desc_mov = input("Descrição: ")
            valor_mov = input("Valor (Ex: 150.50): ")
            cat_id = input("ID da Categoria (1-Salário, 2-Supermercado, 3-Transporte): ")
            pes_id = input("ID da Pessoa (1-Rafael, 2-Fulano...): ")
            pag_id = input("ID do Meio de Pagamento (1-Débito, 2-Crédito): ")
            
            # B) Mande os dados capturados para o Service e guarde a resposta (sucesso ou erro)
            mensagem_retorno = registrar_movimentacao(data_mov, desc_mov, valor_mov, cat_id, pes_id, pag_id)
            
            # C) Imprima a resposta para o usuário ver
            print(mensagem_retorno)
            print("----------------------------------\n")

        # Se a escolha for '4':
        elif escolha == '4':
            # Chama o obter_resumo_movimentacoes(), guarda o resultado e faz o loop for para imprimir na tela
            resumo = obter_resumo_movimentacoes()
            for linha in resumo:
                    print(linha)

        # Se a escolha for '0':
        elif escolha == '0':
            # Imprime uma mensagem de despedida e usa o comando 'break' para encerrar
            print('Vlw, flw!')
            break


        # Se for qualquer outra coisa (else):
        else:
            # Imprime "Opção inválida!"
            print('Opção inválida!')


# 3. A arena de testes (O grande gatilho do jogo)
if __name__ == "__main__":
    iniciar_taverna()