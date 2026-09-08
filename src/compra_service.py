from datetime import datetime
import calendar

from compra_repository import (
    inserir_compra,
    inserir_parcela,
    listar_compras,
    listar_parcelas_por_compra,
    buscar_cartao_por_meio_pagamento
)


def adicionar_meses(data_base, meses):
    ano = data_base.year
    mes = data_base.month + meses

    while mes > 12:
        mes -= 12
        ano += 1

    ultimo_dia = calendar.monthrange(ano, mes)[1]
    dia = min(data_base.day, ultimo_dia)

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

    # Compra passou do fechamento:
    # vai para a próxima fatura.
    if data_compra.day > dia_fechamento:
        mes += 1

        if mes > 12:
            mes = 1
            ano += 1

    # Evita datas impossíveis, como dia 31 em fevereiro.
    ultimo_dia = calendar.monthrange(ano, mes)[1]
    dia = min(dia_vencimento, ultimo_dia)

    return datetime(
        ano,
        mes,
        dia
    )

def cadastrar_compra(
    data,
    local,
    valor_total,
    id_categoria,
    id_item,
    id_pessoa_pagador,
    id_meio_pagamento,
    quantidade_parcelas
):
    if local is None or local.strip() == "":
        return "Local da compra não pode ser vazio."

    local = local.strip()

    try:
        valor_total = float(valor_total)
        id_categoria = int(id_categoria)
        id_item = int(id_item)
        id_pessoa_pagador = int(id_pessoa_pagador)
        id_meio_pagamento = int(id_meio_pagamento)
        quantidade_parcelas = int(quantidade_parcelas)

    except ValueError:
        return "Existem valores numéricos inválidos."

    if valor_total <= 0:
        return "O valor da compra deve ser maior que zero."

    if quantidade_parcelas <= 0:
        return "A quantidade de parcelas deve ser maior que zero."

    try:
        data_compra = datetime.strptime(data, "%Y-%m-%d")

    except ValueError:
        return "Data inválida. Use YYYY-MM-DD."
    
    cartao = buscar_cartao_por_meio_pagamento(
        id_meio_pagamento
    )

    if cartao is None:
        return "O meio de pagamento informado não está vinculado a um cartão ativo."

    id_cartao, nome_cartao, dia_fechamento, dia_vencimento = cartao

    primeiro_vencimento = calcular_primeiro_vencimento(
        data_compra,
        dia_fechamento,
        dia_vencimento
    )

    id_compra = inserir_compra(
        data,
        local,
        valor_total,
        id_categoria,
        id_item,
        id_pessoa_pagador,
        id_meio_pagamento,
        quantidade_parcelas
    )

    valor_parcela = round(
        valor_total / quantidade_parcelas,
        2
    )

    for numero in range(1, quantidade_parcelas + 1):
        data_parcela = adicionar_meses(
            primeiro_vencimento,
            numero - 1
        )

        inserir_parcela(
            id_compra,
            numero,
            data_parcela.strftime("%Y-%m-%d"),
            valor_parcela
        )

    return f"Compra cadastrada com sucesso. ID: {id_compra}"


def obter_compras():
    return listar_compras()


def obter_parcelas(id_compra):
    return listar_parcelas_por_compra(id_compra)


if __name__ == "__main__":
    resultado = cadastrar_compra(
        "2026-09-04",
        "Teste Depois Fechamento",
        300,
        2,
        1,
        2,
        3
    )

    print(resultado)

    if resultado.startswith("Compra cadastrada com sucesso"):
        id_compra = int(resultado.split(":")[-1].strip())

        print("\nPARCELAS GERADAS:")

        parcelas = obter_parcelas(id_compra)

        for parcela in parcelas:
            print(parcela)