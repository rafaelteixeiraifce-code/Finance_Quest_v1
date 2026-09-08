from item_service import obter_itens_por_categoria
import re
from datetime import datetime

from categoria_service import obter_resumo_categorias

from meio_pagamento_service import obter_resumo_meios_pagamento

from movimentacao_service import (
    registrar_movimentacao,
    obter_resumo_movimentacoes
)

from instituicao_service import (
    listar_instituicoes,
    cadastrar_instituicao,
    inativar_instituicao
)

from conta_service import (
    listar_contas,
    cadastrar_conta,
    desativar_conta
)

from cartao_service import (
    obter_cartoes,
    cadastrar_cartao,
    inativar_cartao,
    obter_resumo_cartao
)

from compra_service import (
    cadastrar_compra,
    obter_compras,
    obter_parcelas
)

from pessoa_service import (
    obter_pessoas,
    cadastrar_pessoa,
    inativar_pessoa
)

from participacao_service import (
    obter_compras_para_rateio,
    registrar_rateio,
    calcular_acerto_liquido
)

from orcamento_service import (
    cadastrar_orcamento,
    obter_resumo_orcamento
)


# ============================================================
# FORMATAÇÃO
# ============================================================

MESES = {
    1: "jan",
    2: "fev",
    3: "mar",
    4: "abr",
    5: "mai",
    6: "jun",
    7: "jul",
    8: "ago",
    9: "set",
    10: "out",
    11: "nov",
    12: "dez"
}


def formatar_valor(valor):
    valor_formatado = f"{valor:,.2f}"

    valor_formatado = (
        valor_formatado
        .replace(",", "TEMP")
        .replace(".", ",")
        .replace("TEMP", ".")
    )

    return f"R$ {valor_formatado}"


def formatar_data(data_iso):
    try:
        data = datetime.strptime(
            data_iso,
            "%Y-%m-%d"
        )

        mes = MESES[data.month]

        return (
            f"{data.day:02d}/"
            f"{mes}/"
            f"{str(data.year)[2:]}"
        )

    except (ValueError, TypeError):
        return data_iso


def converter_mes_usuario(mes_usuario):
    """
    Exemplo:
    set-26 -> 2026-09
    """

    meses = {
        "jan": "01",
        "fev": "02",
        "mar": "03",
        "abr": "04",
        "mai": "05",
        "jun": "06",
        "jul": "07",
        "ago": "08",
        "set": "09",
        "out": "10",
        "nov": "11",
        "dez": "12"
    }

    try:
        mes_texto, ano_curto = (
            mes_usuario
            .strip()
            .lower()
            .split("-")
        )

        if mes_texto not in meses:
            return None

        if len(ano_curto) != 2:
            return None

        int(ano_curto)

        return (
            f"20{ano_curto}-"
            f"{meses[mes_texto]}"
        )

    except ValueError:
        return None


def extrair_primeiro_numero(texto):
    resultado = re.search(
        r"\d+",
        texto
    )

    if resultado:
        return int(
            resultado.group()
        )

    return None


# ============================================================
# SELETORES
# ============================================================

def selecionar_item(id_categoria):
    itens = obter_itens_por_categoria(
        id_categoria
    )

    if not itens:
        print(
            "Nenhum item cadastrado para essa categoria."
        )
        return None

    print(
        "\n=== ITENS DISPONÍVEIS ==="
    )

    for indice, item in enumerate(
        itens,
        start=1
    ):
        id_item, nome, ativo = item

        print(
            f"{indice}. {nome}"
        )

    try:
        escolha = int(
            input(
                "Escolha o item: "
            )
        )

        if not 1 <= escolha <= len(itens):
            print(
                "Opção inválida."
            )
            return None

        return itens[
            escolha - 1
        ][0]

    except ValueError:
        print(
            "Digite uma opção numérica válida."
        )
        return None

def selecionar_instituicao():
    instituicoes = listar_instituicoes()

    instituicoes_ativas = [
        instituicao
        for instituicao in instituicoes
        if instituicao[2] == 1
    ]

    if not instituicoes_ativas:
        print(
            "Nenhuma instituição ativa encontrada."
        )
        return None

    print(
        "\n=== INSTITUIÇÕES DISPONÍVEIS ==="
    )

    for indice, instituicao in enumerate(
        instituicoes_ativas,
        start=1
    ):
        _, nome, _ = instituicao

        print(
            f"{indice}. {nome}"
        )

    try:
        escolha = int(
            input(
                "Escolha a instituição: "
            )
        )

        if not 1 <= escolha <= len(
            instituicoes_ativas
        ):
            print(
                "Opção inválida."
            )
            return None

        return instituicoes_ativas[
            escolha - 1
        ][0]

    except ValueError:
        print(
            "Digite uma opção numérica válida."
        )
        return None


def selecionar_conta():
    contas = listar_contas()

    contas_ativas = [
        conta
        for conta in contas
        if conta[5] == 1
    ]

    if not contas_ativas:
        print(
            "Nenhuma conta ativa encontrada."
        )
        return None

    print(
        "\n=== CONTAS DISPONÍVEIS ==="
    )

    for indice, conta in enumerate(
        contas_ativas,
        start=1
    ):
        (
            _,
            instituicao,
            nome,
            tipo,
            _,
            _
        ) = conta

        print(
            f"{indice}. "
            f"{nome} | "
            f"{instituicao} | "
            f"{tipo}"
        )

    try:
        escolha = int(
            input(
                "Escolha a conta: "
            )
        )

        if not 1 <= escolha <= len(
            contas_ativas
        ):
            print(
                "Opção inválida."
            )
            return None

        return contas_ativas[
            escolha - 1
        ][0]

    except ValueError:
        print(
            "Digite uma opção numérica válida."
        )
        return None


def selecionar_cartao():
    cartoes = obter_cartoes()

    cartoes_ativos = [
        cartao
        for cartao in cartoes
        if cartao[6] == 1
    ]

    if not cartoes_ativos:
        print(
            "Nenhum cartão ativo encontrado."
        )
        return None

    print(
        "\n=== CARTÕES DISPONÍVEIS ==="
    )

    for indice, cartao in enumerate(
        cartoes_ativos,
        start=1
    ):
        (
            _,
            instituicao,
            nome,
            _,
            _,
            _,
            _
        ) = cartao

        print(
            f"{indice}. "
            f"{nome} | "
            f"{instituicao}"
        )

    try:
        escolha = int(
            input(
                "Escolha o cartão: "
            )
        )

        if not 1 <= escolha <= len(
            cartoes_ativos
        ):
            print(
                "Opção inválida."
            )
            return None

        return cartoes_ativos[
            escolha - 1
        ][0]

    except ValueError:
        print(
            "Digite uma opção numérica válida."
        )
        return None


def selecionar_categoria():
    categorias = obter_resumo_categorias()

    if not categorias:
        print(
            "Nenhuma categoria encontrada."
        )
        return None

    print(
        "\n=== CATEGORIAS DISPONÍVEIS ==="
    )

    for indice, categoria in enumerate(
        categorias,
        start=1
    ):
        print(
            f"{indice}. {categoria}"
        )

    try:
        escolha = int(
            input(
                "Escolha a categoria: "
            )
        )

        if not 1 <= escolha <= len(
            categorias
        ):
            print(
                "Opção inválida."
            )
            return None

        categoria_escolhida = categorias[
            escolha - 1
        ]

        return extrair_primeiro_numero(
            categoria_escolhida
        )

    except ValueError:
        print(
            "Digite uma opção numérica válida."
        )
        return None


def selecionar_pessoa():
    pessoas = obter_pessoas()

    pessoas_ativas = [
        pessoa
        for pessoa in pessoas
        if pessoa[2] == 1
    ]

    if not pessoas_ativas:
        print(
            "Nenhuma pessoa ativa encontrada."
        )
        return None

    print(
        "\n=== PESSOAS DISPONÍVEIS ==="
    )

    for indice, pessoa in enumerate(
        pessoas_ativas,
        start=1
    ):
        _, nome, _ = pessoa

        print(
            f"{indice}. {nome}"
        )

    try:
        escolha = int(
            input(
                "Escolha a pessoa: "
            )
        )

        if not 1 <= escolha <= len(
            pessoas_ativas
        ):
            print(
                "Opção inválida."
            )
            return None

        return pessoas_ativas[
            escolha - 1
        ][0]

    except ValueError:
        print(
            "Digite uma opção numérica válida."
        )
        return None


def selecionar_meio_pagamento():
    meios = obter_resumo_meios_pagamento()

    if not meios:
        print(
            "Nenhum meio de pagamento encontrado."
        )
        return None

    print(
        "\n=== MEIOS DE PAGAMENTO ==="
    )

    for indice, meio in enumerate(
        meios,
        start=1
    ):
        print(
            f"{indice}. {meio}"
        )

    try:
        escolha = int(
            input(
                "Escolha o meio de pagamento: "
            )
        )

        if not 1 <= escolha <= len(
            meios
        ):
            print(
                "Opção inválida."
            )
            return None

        meio_escolhido = meios[
            escolha - 1
        ]

        return extrair_primeiro_numero(
            meio_escolhido
        )

    except ValueError:
        print(
            "Digite uma opção numérica válida."
        )
        return None


def selecionar_compra_para_rateio():
    compras = obter_compras_para_rateio()

    if not compras:
        print(
            "Nenhuma compra disponível para rateio."
        )
        return None

    print(
        "\n=== COMPRAS DISPONÍVEIS ==="
    )

    for indice, compra in enumerate(
        compras,
        start=1
    ):
        (
            _,
            data,
            local,
            valor_total,
            _,
            nome_pagador
        ) = compra

        print(
            f"{indice}. "
            f"{local} | "
            f"{formatar_valor(valor_total)} | "
            f"{formatar_data(data)} | "
            f"Pagador: {nome_pagador}"
        )

    try:
        escolha = int(
            input(
                "Escolha a compra: "
            )
        )

        if not 1 <= escolha <= len(
            compras
        ):
            print(
                "Opção inválida."
            )
            return None

        return compras[
            escolha - 1
        ]

    except ValueError:
        print(
            "Digite uma opção numérica válida."
        )
        return None


# ============================================================
# MENU PRINCIPAL
# ============================================================

def iniciar_taverna():

    while True:

        print(
            "\n" + "=" * 55
        )
        print(
            "                  FINANCE QUEST"
        )
        print(
            "=" * 55
        )

        print(
            "\n--- MOVIMENTAÇÕES ---"
        )
        print("1. Ver categorias")
        print("2. Ver meios de pagamento")
        print("3. Nova movimentação")
        print("4. Ver movimentações")

        print(
            "\n--- INSTITUIÇÕES ---"
        )
        print("5. Ver instituições")
        print("6. Cadastrar instituição")
        print("7. Desativar instituição")

        print(
            "\n--- CONTAS ---"
        )
        print("8. Ver contas")
        print("9. Cadastrar conta")
        print("10. Desativar conta")

        print(
            "\n--- CARTÕES ---"
        )
        print("11. Ver cartões")
        print("12. Cadastrar cartão")
        print("13. Desativar cartão")
        print("14. Resumo do cartão")

        print(
            "\n--- COMPRAS ---"
        )
        print("15. Cadastrar compra")
        print("16. Ver compras")

        print(
            "\n--- PESSOAS ---"
        )
        print("17. Ver pessoas")
        print("18. Cadastrar pessoa")
        print("19. Desativar pessoa")

        print(
            "\n--- ACERTO DE CONTAS ---"
        )
        print("20. Ratear compra")
        print("21. Ver acerto de contas")

        print(
            "\n--- ORÇAMENTO ---"
        )
        print("22. Definir orçamento")
        print("23. Ver execução do orçamento")

        print(
            "\n0. Sair"
        )

        escolha = input(
            "\nDigite sua opção: "
        )


        # ====================================================
        # 1 - CATEGORIAS
        # ====================================================

        if escolha == "1":

            categorias = (
                obter_resumo_categorias()
            )

            print(
                "\n=== CATEGORIAS ==="
            )

            for categoria in categorias:
                print(categoria)


        # ====================================================
        # 2 - MEIOS DE PAGAMENTO
        # ====================================================

        elif escolha == "2":

            meios = (
                obter_resumo_meios_pagamento()
            )

            print(
                "\n=== MEIOS DE PAGAMENTO ==="
            )

            for meio in meios:
                print(meio)


        # ====================================================
        # 3 - NOVA MOVIMENTAÇÃO
        # ====================================================

        elif escolha == "3":

            print(
                "\n=== NOVA MOVIMENTAÇÃO ==="
            )

            data = input(
                "Data (AAAA-MM-DD): "
            )

            descricao = input(
                "Descrição: "
            )

            valor = input(
                "Valor: "
            )

            id_categoria = (
                selecionar_categoria()
            )

            if id_categoria is None:
                continue

            id_item = selecionar_item(
                id_categoria
            )

            if id_item is None:
                continue

            id_pessoa = (
                selecionar_pessoa()
            )

            if id_pessoa is None:
                continue

            id_meio_pagamento = (
                selecionar_meio_pagamento()
            )

            if id_meio_pagamento is None:
                continue

            resultado = registrar_movimentacao(
                data,
                descricao,
                valor,
                id_categoria,
                id_item,
                id_pessoa,
                id_meio_pagamento
            )

            print(resultado)


        # ====================================================
        # 4 - VER MOVIMENTAÇÕES
        # ====================================================

        elif escolha == "4":

            movimentacoes = (
                obter_resumo_movimentacoes()
            )

            print(
                "\n=== MOVIMENTAÇÕES ==="
            )

            for movimentacao in movimentacoes:
                print(movimentacao)


        # ====================================================
        # 5 - VER INSTITUIÇÕES
        # ====================================================

        elif escolha == "5":

            instituicoes = (
                listar_instituicoes()
            )

            print(
                "\n=== INSTITUIÇÕES ==="
            )

            for (
                _,
                nome,
                ativo
            ) in instituicoes:

                status = (
                    "Ativa"
                    if ativo == 1
                    else "Inativa"
                )

                print(
                    f"{nome} | {status}"
                )


        # ====================================================
        # 6 - CADASTRAR INSTITUIÇÃO
        # ====================================================

        elif escolha == "6":

            print(
                "\n=== CADASTRAR INSTITUIÇÃO ==="
            )

            nome = input(
                "Nome da instituição: "
            )

            resultado = (
                cadastrar_instituicao(
                    nome
                )
            )

            print(resultado)


        # ====================================================
        # 7 - DESATIVAR INSTITUIÇÃO
        # ====================================================

        elif escolha == "7":

            print(
                "\n=== DESATIVAR INSTITUIÇÃO ==="
            )

            id_instituicao = (
                selecionar_instituicao()
            )

            if id_instituicao is not None:

                resultado = (
                    inativar_instituicao(
                        id_instituicao
                    )
                )

                print(resultado)


        # ====================================================
        # 8 - VER CONTAS
        # ====================================================

        elif escolha == "8":

            contas = listar_contas()

            print(
                "\n=== CONTAS ==="
            )

            for (
                _,
                instituicao,
                nome,
                tipo,
                saldo_inicial,
                ativo
            ) in contas:

                status = (
                    "Ativa"
                    if ativo == 1
                    else "Inativa"
                )

                print(
                    "\n" + "-" * 40
                )

                print(
                    f"Conta: {nome}"
                )

                print(
                    f"Instituição: {instituicao}"
                )

                print(
                    f"Tipo: {tipo}"
                )

                print(
                    "Saldo inicial: "
                    f"{formatar_valor(saldo_inicial)}"
                )

                print(
                    f"Status: {status}"
                )


        # ====================================================
        # 9 - CADASTRAR CONTA
        # ====================================================

        elif escolha == "9":

            print(
                "\n=== CADASTRAR CONTA ==="
            )

            id_instituicao = (
                selecionar_instituicao()
            )

            if id_instituicao is None:
                continue

            nome = input(
                "Nome da conta: "
            )

            tipo = input(
                "Tipo (corrente/poupança): "
            )

            saldo_inicial = input(
                "Saldo inicial: "
            )

            resultado = cadastrar_conta(
                id_instituicao,
                nome,
                tipo,
                saldo_inicial
            )

            print(resultado)


        # ====================================================
        # 10 - DESATIVAR CONTA
        # ====================================================

        elif escolha == "10":

            print(
                "\n=== DESATIVAR CONTA ==="
            )

            id_conta = (
                selecionar_conta()
            )

            if id_conta is not None:

                resultado = (
                    desativar_conta(
                        id_conta
                    )
                )

                print(resultado)


        # ====================================================
        # 11 - VER CARTÕES
        # ====================================================

        elif escolha == "11":

            cartoes = obter_cartoes()

            print(
                "\n=== CARTÕES ==="
            )

            for (
                _,
                instituicao,
                nome,
                limite_total,
                dia_fechamento,
                dia_vencimento,
                ativo
            ) in cartoes:

                status = (
                    "Ativo"
                    if ativo == 1
                    else "Inativo"
                )

                print(
                    "\n" + "-" * 40
                )

                print(
                    f"Cartão: {nome}"
                )

                print(
                    f"Instituição: {instituicao}"
                )

                print(
                    "Limite: "
                    f"{formatar_valor(limite_total)}"
                )

                print(
                    "Fechamento: "
                    f"dia {dia_fechamento}"
                )

                print(
                    "Vencimento: "
                    f"dia {dia_vencimento}"
                )

                print(
                    f"Status: {status}"
                )


        # ====================================================
        # 12 - CADASTRAR CARTÃO
        # ====================================================

        elif escolha == "12":

            print(
                "\n=== CADASTRAR CARTÃO ==="
            )

            id_instituicao = (
                selecionar_instituicao()
            )

            if id_instituicao is None:
                continue

            nome = input(
                "Nome do cartão: "
            )

            limite_total = input(
                "Limite total: "
            )

            dia_fechamento = input(
                "Dia de fechamento: "
            )

            dia_vencimento = input(
                "Dia de vencimento: "
            )

            resultado = cadastrar_cartao(
                id_instituicao,
                nome,
                limite_total,
                dia_fechamento,
                dia_vencimento
            )

            print(resultado)


        # ====================================================
        # 13 - DESATIVAR CARTÃO
        # ====================================================

        elif escolha == "13":

            print(
                "\n=== DESATIVAR CARTÃO ==="
            )

            id_cartao = (
                selecionar_cartao()
            )

            if id_cartao is not None:

                resultado = (
                    inativar_cartao(
                        id_cartao
                    )
                )

                print(resultado)


        # ====================================================
        # 14 - RESUMO DO CARTÃO
        # ====================================================

        elif escolha == "14":

            print(
                "\n=== RESUMO DO CARTÃO ==="
            )

            id_cartao = (
                selecionar_cartao()
            )

            if id_cartao is None:
                continue

            mes_usuario = input(
                "Mês da fatura "
                "(ex.: set-26): "
            )

            ano_mes = (
                converter_mes_usuario(
                    mes_usuario
                )
            )

            if ano_mes is None:

                print(
                    "Mês inválido. "
                    "Use o formato set-26."
                )

                continue

            resumo = obter_resumo_cartao(
                id_cartao,
                ano_mes
            )

            if resumo is None:

                print(
                    "Cartão não encontrado."
                )

                continue

            print(
                "\n" + "=" * 42
            )
            print(
                "          RESUMO DO CARTÃO"
            )
            print(
                "=" * 42
            )

            print(
                f"Cartão: {resumo['cartao']}"
            )

            print(
                f"Fatura: {mes_usuario.lower()}"
            )

            print(
                "Limite total: "
                f"{formatar_valor(resumo['limite_total'])}"
            )

            print(
                "Limite comprometido: "
                f"{formatar_valor(resumo['limite_comprometido'])}"
            )

            print(
                "Limite disponível: "
                f"{formatar_valor(resumo['limite_disponivel'])}"
            )

            print(
                "Valor da fatura: "
                f"{formatar_valor(resumo['fatura_mes'])}"
            )

            print(
                "Mana disponível: "
                f"{resumo['mana']:.1f}%"
            )

            print(
                "=" * 42
            )


        # ====================================================
        # 15 - CADASTRAR COMPRA
        # ====================================================

        elif escolha == "15":

            print(
                "\n=== CADASTRAR COMPRA ==="
            )

            data = input(
                "Data da compra (AAAA-MM-DD): "
            )

            local = input(
                "Local da compra: "
            )

            valor_total = input(
                "Valor total: "
            )

            id_categoria = (
                selecionar_categoria()
            )

            if id_categoria is None:
                continue
            
            id_item = selecionar_item(
                id_categoria
            )

            if id_item is None:
                continue

            id_pessoa_pagador = (
                selecionar_pessoa()
            )

            if id_pessoa_pagador is None:
                continue

            id_meio_pagamento = (
                selecionar_meio_pagamento()
            )

            if id_meio_pagamento is None:
                continue

            quantidade_parcelas = input(
                "Quantidade de parcelas: "
            )

            resultado = cadastrar_compra(
                    data,
                    local,
                    valor_total,
                    id_categoria,
                    id_item,
                    id_pessoa_pagador,
                    id_meio_pagamento,
                    quantidade_parcelas
                )

            print(resultado)


        # ====================================================
        # 16 - VER COMPRAS
        # ====================================================

        elif escolha == "16":

            compras = obter_compras()

            print(
                "\n=== COMPRAS ==="
            )

            if not compras:
                print(
                    "Nenhuma compra encontrada."
                )
                continue

            for compra in compras:

                (
                    id_compra,
                    data,
                    local,
                    valor_total,
                    quantidade_parcelas,
                    ativo
                ) = compra

                status = (
                    "Ativa"
                    if ativo == 1
                    else "Inativa"
                )

                print(
                    "\n" + "-" * 45
                )

                print(
                    f"Compra: {local}"
                )

                print(
                    "Data: "
                    f"{formatar_data(data)}"
                )

                print(
                    "Valor total: "
                    f"{formatar_valor(valor_total)}"
                )

                print(
                    "Parcelamento: "
                    f"{quantidade_parcelas}x"
                )

                print(
                    f"Status: {status}"
                )

                parcelas = obter_parcelas(
                    id_compra
                )

                if parcelas:

                    print(
                        "\nParcelas:"
                    )

                    for (
                        _,
                        numero_parcela,
                        data_vencimento,
                        valor,
                        status_parcela
                    ) in parcelas:

                        print(
                            f"  "
                            f"{numero_parcela}/"
                            f"{quantidade_parcelas}"
                            f" | "
                            f"{formatar_data(data_vencimento)}"
                            f" | "
                            f"{formatar_valor(valor)}"
                            f" | "
                            f"{status_parcela}"
                        )


        # ====================================================
        # 17 - VER PESSOAS
        # ====================================================

        elif escolha == "17":

            pessoas = obter_pessoas()

            print(
                "\n=== PESSOAS ==="
            )

            if not pessoas:
                print(
                    "Nenhuma pessoa cadastrada."
                )
                continue

            for (
                _,
                nome,
                ativo
            ) in pessoas:

                status = (
                    "Ativa"
                    if ativo == 1
                    else "Inativa"
                )

                print(
                    f"{nome} | {status}"
                )


        # ====================================================
        # 18 - CADASTRAR PESSOA
        # ====================================================

        elif escolha == "18":

            print(
                "\n=== CADASTRAR PESSOA ==="
            )

            nome = input(
                "Nome da pessoa: "
            )

            resultado = (
                cadastrar_pessoa(
                    nome
                )
            )

            print(resultado)


        # ====================================================
        # 19 - DESATIVAR PESSOA
        # ====================================================

        elif escolha == "19":

            print(
                "\n=== DESATIVAR PESSOA ==="
            )

            id_pessoa = (
                selecionar_pessoa()
            )

            if id_pessoa is not None:

                resultado = (
                    inativar_pessoa(
                        id_pessoa
                    )
                )

                print(resultado)


        # ====================================================
        # 20 - RATEAR COMPRA
        # ====================================================

        elif escolha == "20":

            print(
                "\n=== RATEAR COMPRA ==="
            )

            compra = (
                selecionar_compra_para_rateio()
            )

            if compra is None:
                continue

            (
                id_compra,
                data,
                local,
                valor_total,
                id_pessoa_pagador,
                nome_pagador
            ) = compra

            print(
                "\n" + "-" * 45
            )

            print(
                f"Compra: {local}"
            )

            print(
                f"Data: {formatar_data(data)}"
            )

            print(
                "Valor total: "
                f"{formatar_valor(valor_total)}"
            )

            print(
                f"Pagador: {nome_pagador}"
            )

            print(
                "-" * 45
            )

            try:
                quantidade_pessoas = int(
                    input(
                        "\nQuantas pessoas participarão "
                        "do rateio? "
                    )
                )

                if quantidade_pessoas <= 0:

                    print(
                        "A quantidade deve ser "
                        "maior que zero."
                    )

                    continue

            except ValueError:

                print(
                    "Digite uma quantidade válida."
                )

                continue

            cotas = []
            pessoas_usadas = set()

            for numero in range(
                1,
                quantidade_pessoas + 1
            ):

                print(
                    f"\n--- PARTICIPANTE {numero} ---"
                )

                id_pessoa = (
                    selecionar_pessoa()
                )

                if id_pessoa is None:
                    cotas = []
                    break

                if id_pessoa in pessoas_usadas:

                    print(
                        "Essa pessoa já foi "
                        "adicionada ao rateio."
                    )

                    cotas = []
                    break

                pessoas_usadas.add(
                    id_pessoa
                )

                valor_cota = input(
                    "Valor da responsabilidade: "
                )

                cotas.append(
                    (
                        id_pessoa,
                        valor_cota
                    )
                )

            if not cotas:

                print(
                    "Rateio cancelado."
                )

                continue

            resultado = registrar_rateio(
                id_compra,
                cotas
            )

            print(
                f"\n{resultado}"
            )


        # ====================================================
        # 21 - VER ACERTO DE CONTAS
        # ====================================================

        elif escolha == "21":

            print(
                "\n" + "=" * 42
            )

            print(
                "          ACERTO DE CONTAS"
            )

            print(
                "=" * 42
            )

            acertos = (
                calcular_acerto_liquido()
            )

            if not acertos:

                print(
                    "\nNenhum valor pendente "
                    "entre as pessoas."
                )

            else:

                for acerto in acertos:

                    print(
                        "\n" + "-" * 42
                    )

                    print(
                        f"{acerto['devedor']} "
                        f"deve pagar para "
                        f"{acerto['credor']}:"
                    )

                    print(
                        formatar_valor(
                            acerto["valor"]
                        )
                    )

            print(
                "\n" + "=" * 42
            )


        # ====================================================
        # 22 - DEFINIR ORÇAMENTO
        # ====================================================

        elif escolha == "22":

            print(
                "\n" + "=" * 42
            )

            print(
                "          DEFINIR ORÇAMENTO"
            )

            print(
                "=" * 42
            )

            id_categoria = (
                selecionar_categoria()
            )

            if id_categoria is None:
                continue

            mes_usuario = input(
                "Mês do orçamento "
                "(ex.: set-26): "
            )

            mes_ano = (
                converter_mes_usuario(
                    mes_usuario
                )
            )

            if mes_ano is None:

                print(
                    "Mês inválido. "
                    "Use o formato set-26."
                )

                continue

            valor_planejado = input(
                "Valor planejado: "
            )

            resultado = cadastrar_orcamento(
                id_categoria,
                mes_ano,
                valor_planejado
            )

            print(
                f"\n{resultado}"
            )


        # ====================================================
        # 23 - VER EXECUÇÃO DO ORÇAMENTO
        # ====================================================

        elif escolha == "23":

            print(
                "\n" + "=" * 42
            )

            print(
                "       EXECUÇÃO DO ORÇAMENTO"
            )

            print(
                "=" * 42
            )

            mes_usuario = input(
                "Mês do orçamento "
                "(ex.: set-26): "
            )

            mes_ano = (
                converter_mes_usuario(
                    mes_usuario
                )
            )

            if mes_ano is None:

                print(
                    "Mês inválido. "
                    "Use o formato set-26."
                )

                continue

            print(
                "\nDe quem é o orçamento?"
            )

            id_pessoa_usuario = (
                selecionar_pessoa()
            )

            if id_pessoa_usuario is None:
                continue

            resumo = obter_resumo_orcamento(
                mes_ano,
                id_pessoa_usuario
            )

            print(
                "\n" + "=" * 42
            )

            print(
                "     ORÇAMENTO | "
                f"{mes_usuario.lower()}"
            )

            print(
                "=" * 42
            )

            if not resumo:

                print(
                    "\nNenhum orçamento definido "
                    "para esse mês."
                )

            else:

                for item in resumo:

                    print(
                        "\n" + "-" * 42
                    )

                    print(
                        f"CATEGORIA: "
                        f"{item['categoria']}"
                    )

                    print(
                        "\nPlanejado:  "
                        f"{formatar_valor(item['planejado'])}"
                    )

                    print(
                        "Executado:  "
                        f"{formatar_valor(item['executado'])}"
                    )

                    print(
                        "Disponível: "
                        f"{formatar_valor(item['disponivel'])}"
                    )

                    print(
                        "\nExecução:   "
                        f"{item['percentual_execucao']:.1f}%"
                    )

                    print(
                        "Ritmo mês:  "
                        f"{item['percentual_mes']:.1f}%"
                    )

                    print(
                        "\nSemáforo: "
                        f"{item['semaforo']}"
                    )

            print(
                "\n" + "=" * 42
            )


        # ====================================================
        # 0 - SAIR
        # ====================================================

        elif escolha == "0":

            print(
                "\nAté a próxima aventura!"
            )

            break


        # ====================================================
        # OPÇÃO INVÁLIDA
        # ====================================================

        else:

            print(
                "\nOpção inválida. "
                "Escolha uma opção do menu."
            )


# ============================================================
# INÍCIO
# ============================================================

if __name__ == "__main__":
    iniciar_taverna()