from datetime import datetime
import calendar

from orcamento_repository import (
    salvar_orcamento,
    listar_orcamentos_mes,
    calcular_executado_categoria
)


def cadastrar_orcamento(
    id_categoria,
    mes_ano,
    valor_planejado
):
    try:
        id_categoria = int(id_categoria)
        valor_planejado = float(valor_planejado)

    except ValueError:
        return "Categoria ou valor inválido."

    if id_categoria <= 0:
        return "Categoria inválida."

    if valor_planejado < 0:
        return "O valor planejado não pode ser negativo."

    try:
        datetime.strptime(
            mes_ano,
            "%Y-%m"
        )

    except ValueError:
        return "Mês inválido."

    salvar_orcamento(
        id_categoria,
        mes_ano,
        valor_planejado
    )

    return "Orçamento salvo com sucesso."


def calcular_percentual_mes(mes_ano):
    ano, mes = map(
        int,
        mes_ano.split("-")
    )

    hoje = datetime.now()

    # Mês passado = 100%
    if (ano, mes) < (hoje.year, hoje.month):
        return 100.0

    # Mês futuro = 0%
    if (ano, mes) > (hoje.year, hoje.month):
        return 0.0

    # Mês atual
    total_dias = calendar.monthrange(
        ano,
        mes
    )[1]

    percentual = (
        hoje.day / total_dias
    ) * 100

    return round(
        percentual,
        1
    )


def calcular_semaforo(
    percentual_execucao,
    percentual_mes
):
    diferenca = (
        percentual_execucao
        - percentual_mes
    )

    if diferenca <= 5:
        return "VERDE"

    if diferenca <= 15:
        return "AMARELO"

    return "VERMELHO"


def obter_resumo_orcamento(
    mes_ano,
    id_pessoa_usuario
):
    orcamentos = listar_orcamentos_mes(
        mes_ano
    )

    percentual_mes = calcular_percentual_mes(
        mes_ano
    )

    resultado = []

    for (
        id_orcamento,
        id_categoria,
        nome_categoria,
        valor_planejado
    ) in orcamentos:

        executado = calcular_executado_categoria(
            id_categoria,
            mes_ano,
            id_pessoa_usuario
        )

        disponivel = (
            valor_planejado - executado
        )

        if valor_planejado > 0:
            percentual_execucao = (
                executado / valor_planejado
            ) * 100

        else:
            percentual_execucao = 0

        percentual_execucao = round(
            percentual_execucao,
            1
        )

        semaforo = calcular_semaforo(
            percentual_execucao,
            percentual_mes
        )

        resultado.append({
            "categoria": nome_categoria,
            "planejado": valor_planejado,
            "executado": executado,
            "disponivel": disponivel,
            "percentual_execucao": percentual_execucao,
            "percentual_mes": percentual_mes,
            "semaforo": semaforo
        })

    return resultado


if __name__ == "__main__":

    resumo = obter_resumo_orcamento(
        "2026-08",
        1
    )

    for item in resumo:
        print(item)