from datetime import datetime

from orcamento_repository import (
    salvar_orcamento,
    listar_orcamentos_mes,
    calcular_executado_categoria
)


ID_USUARIO_PRINCIPAL = 1


# ============================================================
# CADASTRAR / ATUALIZAR ORÇAMENTO
# ============================================================

def cadastrar_orcamento(
    id_categoria,
    mes_ano,
    valor_planejado
):
    try:
        id_categoria = int(
            id_categoria
        )

        valor_planejado = float(
            valor_planejado
        )

    except (ValueError, TypeError):
        return "Valores inválidos."

    if valor_planejado < 0:
        return (
            "O valor planejado não pode "
            "ser negativo."
        )

    try:
        datetime.strptime(
            mes_ano,
            "%Y-%m"
        )

    except ValueError:
        return (
            "Mês inválido. "
            "Use AAAA-MM."
        )

    salvar_orcamento(
        id_categoria,
        mes_ano,
        valor_planejado
    )

    return (
        "Orçamento salvo com sucesso."
    )


# ============================================================
# SEMÁFORO
# ============================================================

def calcular_semaforo(
    percentual_execucao,
    percentual_mes
):

    # Mês futuro:
    # ainda não existe ritmo de execução.
    if percentual_mes == 0:
        return "PROJEÇÃO"

    diferenca = (
        percentual_execucao
        - percentual_mes
    )

    if percentual_execucao >= 100:
        return "VERMELHO"

    if diferenca > 15:
        return "VERMELHO"

    if diferenca > 5:
        return "AMARELO"

    return "VERDE"


# ============================================================
# PERCENTUAL DO MÊS
# ============================================================

def calcular_percentual_mes(
    mes_ano
):
    hoje = datetime.now()

    ano, mes = map(
        int,
        mes_ano.split("-")
    )

    # Mês passado:
    # já consideramos 100% transcorrido.
    if (
        ano < hoje.year
        or (
            ano == hoje.year
            and mes < hoje.month
        )
    ):
        return 100.0

    # Mês futuro:
    if (
        ano > hoje.year
        or (
            ano == hoje.year
            and mes > hoje.month
        )
    ):
        return 0.0

    # Mês atual
    import calendar

    dias_mes = calendar.monthrange(
        ano,
        mes
    )[1]

    percentual = (
        hoje.day
        / dias_mes
    ) * 100

    return round(
        percentual,
        1
    )


# ============================================================
# EXECUÇÃO COMPLETA DO MÊS
# ============================================================

def obter_execucao_orcamento(
    mes_ano,
    id_pessoa_usuario=ID_USUARIO_PRINCIPAL
):
    orcamentos = listar_orcamentos_mes(
        mes_ano
    )

    percentual_mes = (
        calcular_percentual_mes(
            mes_ano
        )
    )

    resultado = []

    for (
        id_orcamento,
        id_categoria,
        categoria,
        planejado
    ) in orcamentos:

        executado = (
            calcular_executado_categoria(
                id_categoria,
                mes_ano,
                id_pessoa_usuario
            )
        )

        disponivel = round(
            planejado - executado,
            2
        )

        if planejado > 0:
            percentual_execucao = round(
                (
                    executado
                    / planejado
                ) * 100,
                1
            )

        else:
            percentual_execucao = 0.0

        semaforo = calcular_semaforo(
            percentual_execucao,
            percentual_mes
        )

        resultado.append({
            "id_categoria": id_categoria,
            "categoria": categoria,
            "planejado": planejado,
            "executado": executado,
            "disponivel": disponivel,
            "percentual_execucao":
                percentual_execucao,
            "percentual_mes":
                percentual_mes,
            "semaforo": semaforo
        })

    return resultado