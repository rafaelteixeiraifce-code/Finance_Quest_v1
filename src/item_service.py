from item_repository import (
    listar_itens,
    listar_itens_por_categoria,
    inserir_item,
    buscar_item,
    desativar_item
)


def obter_itens():
    return listar_itens()


def obter_itens_por_categoria(id_categoria):
    return listar_itens_por_categoria(
        id_categoria
    )


def cadastrar_item(
    id_categoria,
    nome
):
    try:
        id_categoria = int(
            id_categoria
        )

    except ValueError:
        return "Categoria inválida."

    if id_categoria <= 0:
        return "Categoria inválida."

    if nome is None or nome.strip() == "":
        return "Nome do item não pode ser vazio."

    nome = nome.strip()

    if buscar_item(
        id_categoria,
        nome
    ):
        return (
            "Esse item já está cadastrado "
            "nessa categoria."
        )

    inserir_item(
        id_categoria,
        nome
    )

    return (
        f"Item '{nome}' cadastrado "
        "com sucesso."
    )


def inativar_item(id_item):
    try:
        id_item = int(
            id_item
        )

    except ValueError:
        return "Item inválido."

    if id_item <= 0:
        return "Item inválido."

    linhas_afetadas = (
        desativar_item(
            id_item
        )
    )

    if linhas_afetadas == 0:
        return "Item não encontrado."

    return "Item desativado com sucesso."


if __name__ == "__main__":
    print(
        obter_itens()
    )