# 1. Importar a função do repositório
from movimentacao_repository import inserir_nova_movimentacao
from movimentacao_repository import listar_movimentacoes

# 2. Definir a função do Service exigindo os mesmos ingredientes
def registrar_movimentacao(data, descricao, valor, id_categoria, id_pessoa, id_meio_pagamento):
    
    # A) Tenta converter o valor digitado para número decimal
    try:
        valor_float = float(valor)
    except ValueError:
        # Se falhar (ex: digitou letras), o escudo ativa e devolve o erro para a Taverna
        return "Falha Crítica: O valor precisa ser um número válido (ex: 15.50)!"
        
    # B) Continua com as outras validações que você já construiu perfeitamente
    if valor_float <= 0:
        return "Falha Crítica: O valor da movimentação precisa ser maior que zero!"
        
    # C) Se passou pelos escudos de validação, chama o repositório para salvar
    inserir_nova_movimentacao(data, descricao, valor_float, id_categoria, id_pessoa, id_meio_pagamento)
    
    # D) Retorna uma mensagem de sucesso para a Taverna
    return f"Sucesso: Movimentação '{descricao}' de R$ {valor_float} forjada no pergaminho!"

# 3. A Arena de Testes
if __name__ == "__main__":
    # Teste 1: Um loot inválido (valor negativo)
    resultado_erro = registrar_movimentacao('2026-08-28', 'Poção de Vida', -50.00, 2, 1, 1)
    print(resultado_erro)
    
    # Teste 2: Um loot válido
    resultado_sucesso = registrar_movimentacao('2026-08-28', 'Poção de Mana', 75.00, 2, 1, 1)
    print(resultado_sucesso)
    
def obter_resumo_movimentacoes():
    # A) Chama o repositório para buscar os dados
    dados_brutos = listar_movimentacoes()

    # B) Criar uma lista vazia para guardar os textos formatados
    movimentacoes_formatadas = []
    
    # C) Fazer um loop 'for' passando pela lista de dados brutos
    for data, desc, valor, categoria in dados_brutos:
    
        # D) Dentro do loop, usar uma f-string para montar um texto amigável.           
        texto_amigavel = f"'{data}' - {desc} R$ {valor} {categoria}"

        # E) Adicionar esse texto na lista vazia usando o método .append()
        movimentacoes_formatadas.append(texto_amigavel)

    # B) Retorna os dados para a Taverna
    return movimentacoes_formatadas