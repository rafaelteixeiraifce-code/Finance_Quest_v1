from cartao_repository import (
    listar_cartoes,
    inserir_cartao,
    desativar_cartao,
    buscar_cartao_por_nome,
    buscar_cartao_por_id,
    listar_cartoes_por_titular,
    calcular_limite_comprometido,
    calcular_fatura_mes
)


ID_USUARIO_PRINCIPAL = 1


def obter_cartoes():
    return listar_cartoes()


def obter_cartoes_por_titular(
    id_pessoa
):
    return listar_cartoes_por_titular(
        id_pessoa
    )


def cadastrar_cartao(
    id_instituicao,
    nome,
    limite_total,
    dia_fechamento,
    dia_vencimento,
    id_pessoa_titular=ID_USUARIO_PRINCIPAL
):
    if nome is None or nome.strip() == "":
        return (
            "Nome do cartão não pode ser vazio."
        )

    nome = nome.strip()

    try:
        id_instituicao = int(
            id_instituicao
        )

        limite_total = float(
            limite_total
        )

        dia_fechamento = int(
            dia_fechamento
        )

        dia_vencimento = int(
            dia_vencimento
        )

        id_pessoa_titular = int(
            id_pessoa_titular
        )

    except (ValueError, TypeError):
        return (
            "Existem valores inválidos."
        )

    if limite_total <= 0:
        return (
            "O limite deve ser maior que zero."
        )

    if not 1 <= dia_fechamento <= 31:
        return (
            "Dia de fechamento inválido."
        )

    if not 1 <= dia_vencimento <= 31:
        return (
            "Dia de vencimento inválido."
        )

    if buscar_cartao_por_nome(
        nome
    ):
        return (
            "Esse cartão já está cadastrado."
        )

    inserir_cartao(
        id_instituicao,
        nome,
        limite_total,
        dia_fechamento,
        dia_vencimento,
        id_pessoa_titular
    )

    return (
        f"Cartão '{nome}' "
        "cadastrado com sucesso."
    )


def inativar_cartao(id_cartao):
    try:
        id_cartao = int(
            id_cartao
        )

    except (ValueError, TypeError):
        return "Cartão inválido."

    linhas = desativar_cartao(
        id_cartao
    )

    if linhas == 0:
        return (
            "Cartão não encontrado."
        )

    return (
        "Cartão desativado com sucesso."
    )


def obter_resumo_cartao(
    id_cartao,
    ano_mes
):
    cartao = buscar_cartao_por_id(
        id_cartao
    )

    if cartao is None:
        return None

    (
        id_cartao,
        nome,
        limite_total,
        dia_fechamento,
        dia_vencimento,
        ativo,
        id_pessoa_titular
    ) = cartao

    limite_comprometido = (
        calcular_limite_comprometido(
            id_cartao
        )
    )

    limite_disponivel = (
        limite_total
        - limite_comprometido
    )

    if limite_disponivel < 0:
        limite_disponivel = 0

    fatura_mes = calcular_fatura_mes(
        id_cartao,
        ano_mes
    )

    if limite_total > 0:

        mana = round(
            (
                limite_disponivel
                / limite_total
            ) * 100,
            1
        )

    else:
        mana = 0

    return {
        "cartao": nome,
        "limite_total": limite_total,
        "limite_comprometido":
            limite_comprometido,
        "limite_disponivel":
            limite_disponivel,
        "fatura_mes": fatura_mes,
        "mana": mana
    }