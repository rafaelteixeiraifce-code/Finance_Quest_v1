from participacao_repository import (
    listar_compras_para_rateio,
    buscar_compra_por_id,
    listar_participacoes_por_compra,
    substituir_rateio,
    listar_dividas_brutas
)


def obter_compras_para_rateio():
    return listar_compras_para_rateio()


def obter_participacoes(id_compra):
    return listar_participacoes_por_compra(
        id_compra
    )


def registrar_rateio(id_compra, cotas):
    """
    cotas:
    [
        (id_pessoa, valor),
        (id_pessoa, valor)
    ]
    """

    compra = buscar_compra_por_id(
        id_compra
    )

    if compra is None:
        return "Compra não encontrada."

    _, valor_total, _ = compra

    if not cotas:
        return "Informe pelo menos uma participação."

    pessoas = set()

    total_cotas = 0

    cotas_tratadas = []

    for id_pessoa, valor_cota in cotas:

        try:
            id_pessoa = int(id_pessoa)
            valor_cota = float(valor_cota)

        except (ValueError, TypeError):
            return "Existe uma participação com valor inválido."

        if id_pessoa in pessoas:
            return "Uma pessoa não pode aparecer duas vezes no mesmo rateio."

        if valor_cota <= 0:
            return "Todas as cotas devem ser maiores que zero."

        pessoas.add(id_pessoa)

        total_cotas += valor_cota

        cotas_tratadas.append(
            (id_pessoa, valor_cota)
        )

    # Trabalhamos com centavos para evitar diferenças
    # irrelevantes de ponto flutuante.
    if round(total_cotas, 2) != round(valor_total, 2):
        return (
            f"O rateio soma R$ {total_cotas:.2f}, "
            f"mas a compra possui valor de "
            f"R$ {valor_total:.2f}."
        )

    substituir_rateio(
        id_compra,
        cotas_tratadas
    )

    return "Rateio registrado com sucesso."


def calcular_acerto_liquido():
    dividas = listar_dividas_brutas()

    saldos = {}

    for (
        id_compra,
        id_pagador,
        nome_pagador,
        id_responsavel,
        nome_responsavel,
        valor
    ) in dividas:

        # A pessoa responsável deve ao pagador.
        chave = (
            id_responsavel,
            nome_responsavel,
            id_pagador,
            nome_pagador
        )

        saldos[chave] = (
            saldos.get(chave, 0)
            + valor
        )

    resultado = []

    pares_processados = set()

    for chave, valor in saldos.items():

        (
            id_devedor,
            nome_devedor,
            id_credor,
            nome_credor
        ) = chave

        par = frozenset(
            [id_devedor, id_credor]
        )

        if par in pares_processados:
            continue

        chave_inversa = (
            id_credor,
            nome_credor,
            id_devedor,
            nome_devedor
        )

        valor_inverso = saldos.get(
            chave_inversa,
            0
        )

        saldo = round(
            valor - valor_inverso,
            2
        )

        if saldo > 0:

            resultado.append({
                "devedor": nome_devedor,
                "credor": nome_credor,
                "valor": saldo
            })

        elif saldo < 0:

            resultado.append({
                "devedor": nome_credor,
                "credor": nome_devedor,
                "valor": abs(saldo)
            })

        pares_processados.add(par)

    return resultado


if __name__ == "__main__":

    print("ACERTO LÍQUIDO:")

    for acerto in calcular_acerto_liquido():

        print(
            f"{acerto['devedor']} deve "
            f"R$ {acerto['valor']:.2f} para "
            f"{acerto['credor']}"
        )