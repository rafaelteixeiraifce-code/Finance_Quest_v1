from datetime import datetime

from movimentacao_repository import (
    inserir_movimentacao,
    listar_movimentacoes
)


ID_USUARIO_PRINCIPAL = 1


def registrar_movimentacao(
    tipo,
    data,
    descricao,
    valor,
    id_categoria=None,
    id_item=None,
    id_meio_pagamento=None
):
    tipo = (
        tipo
        .strip()
        .lower()
    )

    if tipo not in (
        "entrada",
        "saida"
    ):
        return (
            "Tipo de movimentação inválido."
        )

    descricao = (
        descricao.strip()
        if descricao
        else ""
    )

    try:
        valor = float(valor)

    except (ValueError, TypeError):
        return "Valor inválido."

    if valor <= 0:
        return (
            "O valor deve ser maior que zero."
        )

    try:
        datetime.strptime(
            data,
            "%Y-%m-%d"
        )

    except ValueError:
        return (
            "Data inválida. "
            "Use AAAA-MM-DD."
        )

    # ========================================================
    # ENTRADA
    # ========================================================

    if tipo == "entrada":

        inserir_movimentacao(
            data=data,
            tipo="entrada",
            descricao=descricao,
            valor=valor,
            id_pessoa=ID_USUARIO_PRINCIPAL
        )

        return (
            "Entrada registrada com sucesso."
        )


    # ========================================================
    # SAÍDA
    # ========================================================

    if (
        id_categoria is None
        or id_item is None
    ):
        return (
            "Saída precisa de Categoria "
            "e Item."
        )

    try:
        id_categoria = int(
            id_categoria
        )

        id_item = int(
            id_item
        )

        if id_meio_pagamento is not None:
            id_meio_pagamento = int(
                id_meio_pagamento
            )

    except (ValueError, TypeError):
        return (
            "Categoria, Item ou meio "
            "de pagamento inválido."
        )

    inserir_movimentacao(
        data=data,
        tipo="saida",
        descricao=descricao,
        valor=valor,
        id_pessoa=ID_USUARIO_PRINCIPAL,
        id_categoria=id_categoria,
        id_item=id_item,
        id_meio_pagamento=id_meio_pagamento
    )

    return (
        "Saída registrada com sucesso."
    )


def obter_resumo_movimentacoes():
    return listar_movimentacoes()