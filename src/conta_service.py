from conta_repository import (
    listar_contas,
    inserir_conta,
    desativar_conta,
    buscar_conta_por_nome
)
from instituicao_repository import buscar_instituicao_por_nome, desativar_instituicao

def cadastrar_conta(id_instituicao, nome, tipo, saldo_inicial):
    if nome is None:
        return "Nome da conta não pode ser vazio."

    nome = nome.strip()

    if nome == "":
        return "Nome da conta não pode ser vazio."

    if buscar_conta_por_nome(nome):
        return "Essa conta já está cadastrada."

    inserir_conta(id_instituicao, nome, tipo, saldo_inicial)

    return f"Conta '{nome}' cadastrada com sucesso."

    if tipo not in ("corrente", "poupança"):
        return "Tipo de conta inválido."
    
    try:
        saldo_inicial = float(saldo_inicial)
    except ValueError:
        return "Saldo inicial deve ser um número."
    
    if id_instituicao <= 0:
        return "ID da instituição inválido."

