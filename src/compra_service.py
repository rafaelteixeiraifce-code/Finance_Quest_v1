from datetime import datetime
import calendar

from compra_repository import (
    inserir_compra,
    inserir_parcela,
    listar_compras,
    listar_parcelas_por_compra
)

from cartao_repository import (
    buscar_cartao_por_id
)

from participacao_service import (
    registrar_rateio
)


ID_USUARIO_PRINCIPAL = 1


def adicionar_meses(
    data_base,
    meses
):
    ano = data_base.year
    mes = data_base.month + meses

    while mes > 12:
        mes -= 12
        ano += 1

    ultimo_dia = calendar.monthrange(
        ano,
        mes
    )[1]

    dia = min(
        data_base.day,
        ultimo_dia
    )

    return data_base.replace(
        year=ano,
        month=mes,
        day=dia
    )


def calcular_primeiro_vencimento(
    data_compra,
    dia_fechamento,
    dia_vencimento
):
    ano = data_compra.year
    mes = data_compra.month

    if data_compra.day > dia_fechamento:
        mes += 1

        if mes > 12:
            mes = 1
            ano += 1

    ultimo_dia = calendar.monthrange(
        ano,
        mes
    )[1]

    dia = min(
        dia_vencimento,
        ultimo_dia
    )

    return datetime(
        ano,
        mes,
        dia
    )


def cadastrar_compra(
    data,
    observacao,
    valor_total,
    id_categoria,
    id_item,
    id_cartao,
    id_pessoa_pagador,
    quantidade_parcelas,
    responsabilidades=None
):
    observacao = (
        observacao.strip()
        if observacao
        else ""
    )

    try:
        valor_total = float(
            valor_total
        )

        id_categoria = int(
            id_categoria
        )

        id_item = int(
            id_item
        )

        id_pessoa_pagador = int(
            id_pessoa_pagador
        )

        quantidade_parcelas = int(
            quantidade_parcelas
        )

        if id_cartao is not None:
            id_cartao = int(
                id_cartao
            )

    except (ValueError, TypeError):
        return "Existem valores inválidos."

    if valor_total <= 0:
        return (
            "O valor precisa ser maior que zero."
        )

    if quantidade_parcelas <= 0:
        return (
            "Quantidade de parcelas inválida."
        )

    try:
        data_compra = datetime.strptime(
            data,
            "%Y-%m-%d"
        )

    except ValueError:
        return (
            "Data inválida. Use AAAA-MM-DD."
        )


    # ========================================================
    # CARTÃO PRÓPRIO
    # ========================================================

    if id_cartao is not None:

        cartao = buscar_cartao_por_id(
            id_cartao
        )

        if cartao is None:
            return "Cartão não encontrado."

        (
            id_cartao,
            nome_cartao,
            limite_total,
            dia_fechamento,
            dia_vencimento,
            ativo,
            _
        ) = cartao

        if ativo != 1:
            return (
                "O cartão escolhido está inativo."
            )


    # ========================================================
    # CARTÃO DE TERCEIRO
    # ========================================================

    else:

        # Simplificação do MVP.
        # Posteriormente poderemos cadastrar
        # fechamento/vencimento por cartão de terceiro.
        dia_fechamento = 5
        dia_vencimento = 10


    # ========================================================
    # MEIO DE PAGAMENTO
    # ========================================================

    if quantidade_parcelas == 1:
        id_meio_pagamento = 4

    else:
        id_meio_pagamento = 5


    # ========================================================
    # PRIMEIRO VENCIMENTO
    # ========================================================

    primeiro_vencimento = (
        calcular_primeiro_vencimento(
            data_compra,
            dia_fechamento,
            dia_vencimento
        )
    )


    # ========================================================
    # COMPRA
    # ========================================================

    id_compra = inserir_compra(
        data,
        observacao,
        valor_total,
        id_categoria,
        id_item,
        id_pessoa_pagador,
        id_meio_pagamento,
        id_cartao,
        quantidade_parcelas
    )


    # ========================================================
    # PARCELAS
    # ========================================================

    valor_base = round(
        valor_total
        / quantidade_parcelas,
        2
    )

    for numero in range(
        1,
        quantidade_parcelas + 1
    ):

        if numero < quantidade_parcelas:

            valor_parcela = valor_base

        else:

            valor_parcela = round(
                valor_total
                - (
                    valor_base
                    * (
                        quantidade_parcelas - 1
                    )
                ),
                2
            )

        data_parcela = adicionar_meses(
            primeiro_vencimento,
            numero - 1
        )

        inserir_parcela(
            id_compra,
            numero,
            data_parcela.strftime(
                "%Y-%m-%d"
            ),
            valor_parcela
        )


    # ========================================================
    # RESPONSABILIDADE
    # ========================================================

    if responsabilidades is None:

        responsabilidades = [
            (
                ID_USUARIO_PRINCIPAL,
                valor_total
            )
        ]

    resultado_rateio = registrar_rateio(
        id_compra,
        responsabilidades
    )

    if resultado_rateio != (
        "Rateio registrado com sucesso."
    ):

        return (
            "Compra cadastrada, mas houve "
            "problema na responsabilidade: "
            f"{resultado_rateio}"
        )

    return (
        "Compra cadastrada com sucesso. "
        f"ID: {id_compra}"
    )


def obter_compras():
    return listar_compras()


def obter_parcelas(
    id_compra
):
    return listar_parcelas_por_compra(
        id_compra
    )