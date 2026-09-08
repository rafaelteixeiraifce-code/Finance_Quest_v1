from cartao_repository import (
    listar_cartoes,
    inserir_cartao,
    desativar_cartao,
    buscar_cartao_por_nome,
    buscar_cartao_por_id,
    calcular_limite_comprometido,
    calcular_fatura_mes
)

def obter_cartoes():
    return listar_cartoes()


def cadastrar_cartao(
    id_instituicao,
    nome,
    limite_total,
    dia_fechamento,
    dia_vencimento
):
    if id_instituicao <= 0:
        return "ID da instituição inválido."

    if nome is None or nome.strip() == "":
        return "Nome do cartão não pode ser vazio."

    nome = nome.strip()

    if buscar_cartao_por_nome(nome):
        return "Esse cartão já está cadastrado."

    try:
        limite_total = float(limite_total)
        dia_fechamento = int(dia_fechamento)
        dia_vencimento = int(dia_vencimento)

    except ValueError:
        return "Limite, fechamento e vencimento devem ser números."

    if limite_total <= 0:
        return "O limite total deve ser maior que zero."

    if dia_fechamento < 1 or dia_fechamento > 31:
        return "Dia de fechamento inválido."

    if dia_vencimento < 1 or dia_vencimento > 31:
        return "Dia de vencimento inválido."

    inserir_cartao(
        id_instituicao,
        nome,
        limite_total,
        dia_fechamento,
        dia_vencimento
    )

    return f"Cartão '{nome}' cadastrado com sucesso."


def inativar_cartao(id_cartao):
    if id_cartao <= 0:
        return "ID do cartão inválido."

    linhas_afetadas = desativar_cartao(id_cartao)

    if linhas_afetadas == 0:
        return "Cartão não encontrado."

    return "Cartão desativado com sucesso."


if __name__ == "__main__":
    print(
        cadastrar_cartao(
            3,
            "Inter Gold",
            3000,
            10,
            17
        )
    )

    print(obter_cartoes())
    
def obter_resumo_cartao(id_cartao, ano_mes):
    cartao = buscar_cartao_por_id(id_cartao)

    if cartao is None:
        return None

    (
        id_cartao,
        nome,
        limite_total,
        dia_fechamento,
        dia_vencimento,
        ativo
    ) = cartao

    limite_comprometido = calcular_limite_comprometido(
        id_cartao
    )

    limite_disponivel = (
        limite_total - limite_comprometido
    )

    if limite_disponivel < 0:
        limite_disponivel = 0

    fatura_mes = calcular_fatura_mes(
        id_cartao,
        ano_mes
    )

    mana_percentual = round(
        (limite_disponivel / limite_total) * 100,
        1
    )

    return {
        "cartao": nome,
        "limite_total": limite_total,
        "limite_comprometido": limite_comprometido,
        "limite_disponivel": limite_disponivel,
        "fatura_mes": fatura_mes,
        "mana": mana_percentual
    }
    
if __name__ == "__main__":
        resumo = obter_resumo_cartao(
            1,
            "2026-10"
        )

        print("\n=== RESUMO DO CARTÃO ===")
        print(f"Cartão: {resumo['cartao']}")
        print(f"Limite total: R$ {resumo['limite_total']:.2f}")
        print(f"Limite comprometido: R$ {resumo['limite_comprometido']:.2f}")
        print(f"Limite disponível: R$ {resumo['limite_disponivel']:.2f}")
        print(f"Fatura do mês: R$ {resumo['fatura_mes']:.2f}")
        print(f"Mana: {resumo['mana']:.1f}%")