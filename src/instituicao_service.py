from instituicao_repository import (
    listar_instituicoes,
    inserir_instituicao,
    desativar_instituicao,
    buscar_instituicao_por_nome
)


def cadastrar_instituicao(nome):
    if nome is None:
        return "Nome da instituição não pode ser vazio."

    nome = nome.strip()

    if nome == "":
        return "Nome da instituição não pode ser vazio."

    if buscar_instituicao_por_nome(nome):
        return "Essa instituição já está cadastrada."

    inserir_instituicao(nome)

    return f"Instituição '{nome}' cadastrada com sucesso."


def inativar_instituicao(id_instituicao):
    if id_instituicao <= 0:
        return "ID da instituição inválido."

    linhas_afetadas = desativar_instituicao(id_instituicao)

    if linhas_afetadas == 0:
        return "Instituição não encontrada."

    return "Instituição desativada com sucesso."