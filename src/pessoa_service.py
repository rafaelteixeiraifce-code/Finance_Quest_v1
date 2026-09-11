from pessoa_repository import (
    listar_pessoas,
    inserir_pessoa,
    buscar_pessoa_por_nome,
    desativar_pessoa
)


def obter_pessoas():
    return listar_pessoas()


def cadastrar_pessoa(nome):
    if nome is None or nome.strip() == "":
        return "Nome da pessoa não pode ser vazio."

    nome = nome.strip()

    if buscar_pessoa_por_nome(nome):
        return "Essa pessoa já está cadastrada."

    inserir_pessoa(nome)

    return f"Pessoa '{nome}' cadastrada com sucesso."


def inativar_pessoa(id_pessoa):
    if id_pessoa <= 0:
        return "Pessoa inválida."

    linhas_afetadas = desativar_pessoa(id_pessoa)

    if linhas_afetadas == 0:
        return "Pessoa não encontrada."

    return "Pessoa desativada com sucesso."
