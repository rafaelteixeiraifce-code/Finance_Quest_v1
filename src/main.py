import re
from datetime import datetime

from categoria_service import obter_resumo_categorias

from meio_pagamento_service import (
    obter_resumo_meios_pagamento
)

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

from item_service import (
    obter_itens,
    obter_itens_por_categoria,
    cadastrar_item,
    inativar_item
)

from participacao_service import (
    obter_compras_para_rateio,
    registrar_rateio,
    calcular_acerto_liquido
)

from orcamento_service import (
    cadastrar_orcamento,
    obter_execucao_orcamento
)


# ============================================================
# CONFIGURAÇÃO DO USUÁRIO
# ============================================================

ID_USUARIO_PRINCIPAL = 1


# ============================================================
# FORMATAÇÃO
# ============================================================

def obter_meses_consulta(
    quantidade=12
):
    hoje = datetime.now()

    meses = []

    ano = hoje.year
    mes = hoje.month

    for _ in range(quantidade):

        chave = (
            f"{ano}-"
            f"{mes:02d}"
        )

        nome = (
            f"{MESES[mes]}-"
            f"{str(ano)[2:]}"
        )

        meses.append(
            (
                chave,
                nome
            )
        )

        mes -= 1

        if mes == 0:
            mes = 12
            ano -= 1

    return meses

def selecionar_mes_orcamento(
    meses_futuros=12
):
    hoje = datetime.now()

    meses = []

    ano = hoje.year
    mes = hoje.month

    for _ in range(
        meses_futuros + 1
    ):
        chave = (
            f"{ano}-"
            f"{mes:02d}"
        )

        nome = (
            f"{MESES[mes]}-"
            f"{str(ano)[2:]}"
        )

        meses.append(
            (
                chave,
                nome
            )
        )

        mes += 1

        if mes == 13:
            mes = 1
            ano += 1

    print(
        "\n=== PERÍODO DO ORÇAMENTO ==="
    )

    for indice, (
        chave,
        nome
    ) in enumerate(
        meses,
        start=1
    ):

        if indice == 1:
            print(
                f"{indice}. "
                f"{nome} [atual]"
            )

        else:
            print(
                f"{indice}. {nome}"
            )

    escolha = input(
        "\nEscolha "
        "[Enter = mês atual]: "
    ).strip()

    if escolha == "":
        return meses[0]

    try:
        escolha = int(
            escolha
        )

    except ValueError:
        print(
            "Opção inválida."
        )
        return None

    if not 1 <= escolha <= len(
        meses
    ):
        print(
            "Opção inválida."
        )
        return None

    return meses[
        escolha - 1
    ]


def selecionar_mes_consulta():
    meses = obter_meses_consulta()

    print(
        "\n=== PERÍODO ==="
    )

    for indice, (
        chave,
        nome
    ) in enumerate(
        meses,
        start=1
    ):

        if indice == 1:
            print(
                f"{indice}. "
                f"{nome} [atual]"
            )

        else:
            print(
                f"{indice}. {nome}"
            )

    print(
        "0. Todos os lançamentos"
    )

    escolha = input(
        "\nEscolha "
        "[Enter = mês atual]: "
    ).strip()

    # Enter = mês corrente
    if escolha == "":
        return meses[0]

    try:
        escolha = int(
            escolha
        )

    except ValueError:
        print(
            "Opção inválida."
        )
        return None

    if escolha == 0:
        return (
            None,
            "Todos"
        )

    if not 1 <= escolha <= len(
        meses
    ):
        print(
            "Opção inválida."
        )
        return None

    return meses[
        escolha - 1
    ]

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

def selecionar_mes_execucao_orcamento():
    hoje = datetime.now()

    meses = []

    # 6 meses anteriores
    ano = hoje.year
    mes = hoje.month

    anteriores = []

    for _ in range(6):
        mes -= 1

        if mes == 0:
            mes = 12
            ano -= 1

        anteriores.append(
            (
                f"{ano}-{mes:02d}",
                f"{MESES[mes]}-{str(ano)[2:]}"
            )
        )

    anteriores.reverse()
    meses.extend(anteriores)

    # Mês atual + 12 meses futuros
    ano = hoje.year
    mes = hoje.month

    for _ in range(13):
        meses.append(
            (
                f"{ano}-{mes:02d}",
                f"{MESES[mes]}-{str(ano)[2:]}"
            )
        )

        mes += 1

        if mes == 13:
            mes = 1
            ano += 1

    indice_atual = len(anteriores)

    print("\n=== PERÍODO DO ORÇAMENTO ===")

    for indice, (chave, nome) in enumerate(
        meses,
        start=1
    ):
        if indice - 1 == indice_atual:
            print(
                f"{indice}. {nome} [atual]"
            )
        else:
            print(
                f"{indice}. {nome}"
            )

    escolha = input(
        "\nEscolha [Enter = mês atual]: "
    ).strip()

    if escolha == "":
        return meses[indice_atual]

    try:
        escolha = int(escolha)

    except ValueError:
        print("Opção inválida.")
        return None

    if not 1 <= escolha <= len(meses):
        print("Opção inválida.")
        return None

    return meses[escolha - 1]

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

        return (
            f"{data.day:02d}/"
            f"{MESES[data.month]}/"
            f"{str(data.year)[2:]}"
        )

    except (ValueError, TypeError):
        return data_iso


def converter_mes_usuario(mes_usuario):
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

def selecionar_categoria():
    categorias = obter_resumo_categorias()

    if not categorias:
        print(
            "\nNenhuma categoria disponível."
        )
        return None

    print(
        "\n=== CATEGORIAS ==="
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

        return extrair_primeiro_numero(
            categorias[
                escolha - 1
            ]
        )

    except ValueError:
        print(
            "Digite uma opção numérica."
        )
        return None


def selecionar_item(id_categoria):

    itens = obter_itens_por_categoria(
        id_categoria
    )

    print(
        "\n=== ITENS ==="
    )

    for indice, item in enumerate(
        itens,
        start=1
    ):
        _, nome, _ = item

        print(
            f"{indice}. {nome}"
        )


    # ========================================================
    # OPÇÕES EXTRAS
    # ========================================================

    opcao_geral = len(itens) + 1
    opcao_novo = len(itens) + 2

    print(
        f"{opcao_geral}. Geral / Outro"
    )

    print(
        f"{opcao_novo}. Cadastrar novo item"
    )


    try:
        escolha = int(
            input(
                "Escolha o item: "
            )
        )

    except ValueError:

        print(
            "Opção inválida."
        )

        return None


    # ========================================================
    # ITEM EXISTENTE
    # ========================================================

    if 1 <= escolha <= len(itens):

        return itens[
            escolha - 1
        ][0]


    # ========================================================
    # GERAL / OUTRO
    # ========================================================

    if escolha == opcao_geral:

        nome_geral = "Geral"

        # Procura se já existe.
        for item in itens:

            id_item, nome, ativo = item

            if nome.lower() == (
                nome_geral.lower()
            ):
                return id_item


        # Se não existe, cria automaticamente.
        resultado = cadastrar_item(
            id_categoria,
            nome_geral
        )

        print(
            resultado
        )

        # Busca novamente para descobrir o ID.
        itens_atualizados = (
            obter_itens_por_categoria(
                id_categoria
            )
        )

        for item in itens_atualizados:

            id_item, nome, ativo = item

            if nome.lower() == (
                nome_geral.lower()
            ):
                return id_item

        return None


    # ========================================================
    # CADASTRAR NOVO ITEM
    # ========================================================

    if escolha == opcao_novo:

        nome = input(
            "Nome do novo item: "
        ).strip()

        if nome == "":

            print(
                "Nome inválido."
            )

            return None


        resultado = cadastrar_item(
            id_categoria,
            nome
        )

        print(
            resultado
        )


        # Busca novamente para recuperar o ID.
        itens_atualizados = (
            obter_itens_por_categoria(
                id_categoria
            )
        )

        for item in itens_atualizados:

            id_item, nome_item, ativo = item

            if nome_item.lower() == (
                nome.lower()
            ):
                return id_item


        return None


    print(
        "Opção inválida."
    )

    return None

def selecionar_ou_cadastrar_pessoa():
    pessoas = obter_pessoas()

    pessoas_ativas = [
        pessoa
        for pessoa in pessoas
        if pessoa[2] == 1
    ]

    print("\n=== PESSOAS ===")

    for indice, pessoa in enumerate(
        pessoas_ativas,
        start=1
    ):
        _, nome, _ = pessoa

        print(
            f"{indice}. {nome}"
        )

    opcao_nova = (
        len(pessoas_ativas) + 1
    )

    print(
        f"{opcao_nova}. Adicionar nova pessoa"
    )

    try:
        escolha = int(
            input(
                "Escolha a pessoa: "
            )
        )

    except ValueError:
        print(
            "Opção inválida."
        )
        return None

    # Nova pessoa
    if escolha == opcao_nova:

        nome = input(
            "Nome da nova pessoa: "
        ).strip()

        if nome == "":
            print(
                "Nome inválido."
            )
            return None

        resultado = cadastrar_pessoa(
            nome
        )

        print(
            resultado
        )

        # Busca novamente para obter o ID.
        pessoas = obter_pessoas()

        for pessoa in pessoas:

            (
                id_pessoa,
                nome_pessoa,
                ativo
            ) = pessoa

            if (
                ativo == 1
                and nome_pessoa.lower()
                == nome.lower()
            ):
                return id_pessoa

        return None

    # Pessoa existente
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

def selecionar_pessoa():
    pessoas = obter_pessoas()

    pessoas_ativas = [
        pessoa
        for pessoa in pessoas
        if pessoa[2] == 1
    ]

    if not pessoas_ativas:
        print(
            "\nNenhuma pessoa disponível."
        )
        return None

    print(
        "\n=== PESSOAS ==="
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
            "Digite uma opção numérica."
        )
        return None


def selecionar_instituicao():
    instituicoes = listar_instituicoes()

    ativas = [
        instituicao
        for instituicao in instituicoes
        if instituicao[2] == 1
    ]

    if not ativas:
        print(
            "\nNenhuma instituição disponível."
        )
        return None

    print(
        "\n=== INSTITUIÇÕES ==="
    )

    for indice, instituicao in enumerate(
        ativas,
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
            ativas
        ):
            return None

        return ativas[
            escolha - 1
        ][0]

    except ValueError:
        return None


def selecionar_conta():
    contas = listar_contas()

    ativas = [
        conta
        for conta in contas
        if conta[5] == 1
    ]

    if not ativas:
        return None

    print(
        "\n=== CONTAS ==="
    )

    for indice, conta in enumerate(
        ativas,
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
            ativas
        ):
            return None

        return ativas[
            escolha - 1
        ][0]

    except ValueError:
        return None


def selecionar_cartao_compra():

    print(
        "\n=== CARTÃO UTILIZADO ==="
    )

    print("1. Nubank")
    print("2. Bradesco")
    print("3. Inter")
    print("4. Cartão de outra pessoa")

    escolha = input(
        "Escolha: "
    ).strip()

    cartoes = obter_cartoes()

    instituicoes = {
        "1": "Nubank",
        "2": "Bradesco",
        "3": "Inter"
    }


    # ========================================================
    # CARTÃO PRÓPRIO
    # ========================================================

    if escolha in instituicoes:

        nome_instituicao = (
            instituicoes[
                escolha
            ]
        )

        encontrados = [
            cartao
            for cartao in cartoes

            if (
                cartao[6] == 1
                and cartao[7]
                == ID_USUARIO_PRINCIPAL
                and cartao[1].lower()
                == nome_instituicao.lower()
            )
        ]

        if not encontrados:

            print(
                f"Nenhum cartão ativo do "
                f"{nome_instituicao} encontrado."
            )

            return None

        return {
            "tipo": "proprio",
            "id_cartao":
                encontrados[0][0],
            "id_pagador":
                ID_USUARIO_PRINCIPAL
        }


    # ========================================================
    # CARTÃO DE OUTRA PESSOA
    # ========================================================

    if escolha == "4":

        print(
            "\nDe quem é o cartão?"
        )

        id_pessoa = (
            selecionar_ou_cadastrar_pessoa()
        )

        if id_pessoa is None:
            return None

        return {
            "tipo": "terceiro",
            "id_cartao": None,
            "id_pagador": id_pessoa
        }


    print(
        "Opção inválida."
    )

    return None


def selecionar_meio_pagamento():
    meios = (
        obter_resumo_meios_pagamento()
    )

    if not meios:
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
            return None

        return extrair_primeiro_numero(
            meios[
                escolha - 1
            ]
        )

    except ValueError:
        return None


def selecionar_meio_pagamento_cartao():
    meios = (
        obter_resumo_meios_pagamento()
    )

    meios_cartao = []

    for meio in meios:
        texto = meio.lower()

        if (
            "cart" in texto
            or "crédito" in texto
            or "credito" in texto
        ):
            meios_cartao.append(
                meio
            )

    if not meios_cartao:
        print(
            "\nNenhum cartão disponível."
        )
        return None

    print(
        "\n=== CARTÃO UTILIZADO ==="
    )

    for indice, meio in enumerate(
        meios_cartao,
        start=1
    ):
        print(
            f"{indice}. {meio}"
        )

    try:
        escolha = int(
            input(
                "Escolha o cartão: "
            )
        )

        if not 1 <= escolha <= len(
            meios_cartao
        ):
            return None

        return extrair_primeiro_numero(
            meios_cartao[
                escolha - 1
            ]
        )

    except ValueError:
        return None


# ============================================================
# MOVIMENTAÇÕES
# ============================================================

def fluxo_registrar_movimentacao():

    print(
        "\n" + "=" * 45
    )

    print(
        "         REGISTRAR MOVIMENTAÇÃO"
    )

    print(
        "=" * 45
    )

    print(
        "\n1. Entrada"
    )

    print(
        "2. Saída"
    )

    tipo_escolha = input(
        "\nEscolha [1/2]: "
    ).strip()


    # ========================================================
    # ENTRADA
    # ========================================================

    if tipo_escolha == "1":

        print(
            "\n=== ENTRADA ==="
        )

        print(
            "1. Salário"
        )

        print(
            "2. Gratificação"
        )

        print(
            "3. Reembolso"
        )

        print(
            "4. Outra entrada"
        )

        escolha = input(
            "\nTipo de entrada: "
        ).strip()

        tipos = {
            "1": "Salário",
            "2": "Gratificação",
            "3": "Reembolso"
        }

        if escolha in tipos:

            descricao = tipos[
                escolha
            ]

        elif escolha == "4":

            descricao = input(
                "Descrição: "
            )

        else:

            print(
                "Opção inválida."
            )

            return


        data = input(
            "Data (AAAA-MM-DD): "
        )

        valor = input(
            "Valor: "
        )


        resultado = registrar_movimentacao(
            tipo="entrada",
            data=data,
            descricao=descricao,
            valor=valor
        )


        print(
            f"\n{resultado}"
        )

        return


    # ========================================================
    # SAÍDA
    # ========================================================

    if tipo_escolha == "2":

        print(
            "\n=== SAÍDA ==="
        )

        data = input(
            "Data (AAAA-MM-DD): "
        )

        valor = input(
            "Valor: "
        )


        id_categoria = (
            selecionar_categoria()
        )

        if id_categoria is None:
            return


        id_item = selecionar_item(
            id_categoria
        )

        if id_item is None:
            return


        observacao = input(
            "Observação (opcional): "
        )


        id_meio_pagamento = (
            selecionar_meio_pagamento()
        )

        if id_meio_pagamento is None:
            return


        resultado = registrar_movimentacao(
            tipo="saida",
            data=data,
            descricao=observacao,
            valor=valor,
            id_categoria=id_categoria,
            id_item=id_item,
            id_meio_pagamento=
                id_meio_pagamento
        )


        print(
            f"\n{resultado}"
        )

        return


    print(
        "\nOpção inválida."
    )

def fluxo_registrar_compra():

    print(
        "\n" + "=" * 45
    )
    print(
        "         REGISTRAR MOVIMENTAÇÃO"
    )
    print(
        "=" * 45
    )

    print(
        "\n1. Entrada"
    )
    print(
        "2. Saída"
    )

    tipo_escolha = input(
        "\nEscolha [1/2]: "
    ).strip()


    # ========================================================
    # ENTRADA
    # ========================================================

    if tipo_escolha == "1":

        print(
            "\n=== ENTRADA ==="
        )

        print(
            "1. Salário"
        )
        print(
            "2. Gratificação"
        )
        print(
            "3. Reembolso"
        )
        print(
            "4. Outra entrada"
        )

        escolha = input(
            "\nTipo de entrada: "
        ).strip()

        tipos = {
            "1": "Salário",
            "2": "Gratificação",
            "3": "Reembolso"
        }

        if escolha in tipos:
            descricao = tipos[
                escolha
            ]

        elif escolha == "4":
            descricao = input(
                "Descrição: "
            )

        else:
            print(
                "Opção inválida."
            )
            return

        data = input(
            "Data (AAAA-MM-DD): "
        )

        valor = input(
            "Valor: "
        )

        resultado = registrar_movimentacao(
            tipo="entrada",
            data=data,
            descricao=descricao,
            valor=valor
        )

        print(
            f"\n{resultado}"
        )

        return


    # ========================================================
    # SAÍDA
    # ========================================================

    if tipo_escolha == "2":

        print(
            "\n=== SAÍDA ==="
        )

        data = input(
            "Data (AAAA-MM-DD): "
        )

        valor = input(
            "Valor: "
        )

        id_categoria = (
            selecionar_categoria()
        )

        if id_categoria is None:
            return

        id_item = selecionar_item(
            id_categoria
        )

        if id_item is None:
            return

        observacao = input(
            "Observação (opcional): "
        )

        id_meio_pagamento = (
            selecionar_meio_pagamento()
        )

        return


    print(
        "\nOpção inválida."
    )


# ============================================================
# COMPRA NO CARTÃO
# ============================================================

def montar_responsabilidades(
    valor_total,
    tipo_cartao="proprio"
):

    print(
        "\n=== RESPONSABILIDADE ==="
    )


    # ========================================================
    # CARTÃO DE OUTRA PESSOA
    # ========================================================

    if tipo_cartao == "terceiro":

        print(
            "1. Minha [padrão]"
        )

        print(
            "2. Compartilhada"
        )

        escolha = input(
            "Escolha [Enter = 1]: "
        ).strip()

        if escolha == "":
            escolha = "1"

        if escolha == "1":

            return [
                (
                    ID_USUARIO_PRINCIPAL,
                    valor_total
                )
            ]

        if escolha == "2":

            return (
                montar_rateio_compartilhado(
                    valor_total
                )
            )

        print(
            "Opção inválida."
        )

        return None


    # ========================================================
    # CARTÃO PRÓPRIO
    # ========================================================

    print(
        "1. Minha [padrão]"
    )

    print(
        "2. Outra pessoa"
    )

    print(
        "3. Compartilhada"
    )

    escolha = input(
        "Escolha [Enter = 1]: "
    ).strip()

    if escolha == "":
        escolha = "1"


    # Minha
    if escolha == "1":

        return [
            (
                ID_USUARIO_PRINCIPAL,
                valor_total
            )
        ]


    # Outra pessoa
    if escolha == "2":

        id_pessoa = (
            selecionar_ou_cadastrar_pessoa()
        )

        if id_pessoa is None:
            return None

        return [
            (
                id_pessoa,
                valor_total
            )
        ]


    # Compartilhada
    if escolha == "3":

        return (
            montar_rateio_compartilhado(
                valor_total
            )
        )


    print(
        "Opção inválida."
    )

    return None

def montar_rateio_compartilhado(
    valor_total
):

    try:
        quantidade = int(
            input(
                "Quantidade de participantes: "
            )
        )

    except ValueError:

        print(
            "Quantidade inválida."
        )

        return None

    if quantidade <= 0:
        return None

    cotas = []
    pessoas_usadas = set()

    for numero in range(
        1,
        quantidade + 1
    ):

        print(
            f"\nParticipante {numero}"
        )

        id_pessoa = (
            selecionar_ou_cadastrar_pessoa()
        )

        if id_pessoa is None:
            return None

        if id_pessoa in pessoas_usadas:

            print(
                "Pessoa repetida."
            )

            return None

        pessoas_usadas.add(
            id_pessoa
        )

        try:
            valor_cota = float(
                input(
                    "Valor da responsabilidade: "
                )
            )

        except ValueError:

            print(
                "Valor inválido."
            )

            return None

        cotas.append(
            (
                id_pessoa,
                valor_cota
            )
        )


    # Confere a soma
    total_cotas = round(
        sum(
            valor
            for _, valor in cotas
        ),
        2
    )

    if total_cotas != round(
        valor_total,
        2
    ):

        print(
            "\nA soma das responsabilidades "
            "precisa ser igual ao valor "
            "total da compra."
        )

        return None

    return cotas

def fluxo_registrar_compra():

    print(
        "\n" + "=" * 45
    )

    print(
        "      REGISTRAR COMPRA NO CARTÃO"
    )

    print(
        "=" * 45
    )


    # ========================================================
    # 1. CARTÃO
    # ========================================================

    contexto_cartao = (
        selecionar_cartao_compra()
    )

    if contexto_cartao is None:
        return

    id_cartao = (
        contexto_cartao[
            "id_cartao"
        ]
    )

    id_pagador = (
        contexto_cartao[
            "id_pagador"
        ]
    )

    tipo_cartao = (
        contexto_cartao[
            "tipo"
        ]
    )


    # ========================================================
    # 2. DATA
    # ========================================================

    data = input(
        "Data (AAAA-MM-DD): "
    )


    # ========================================================
    # 3. VALOR
    # ========================================================

    valor_texto = input(
        "Valor total: "
    )

    try:
        valor_total = float(
            valor_texto
        )

    except ValueError:

        print(
            "Valor inválido."
        )

        return


    # ========================================================
    # 4. CATEGORIA
    # ========================================================

    id_categoria = (
        selecionar_categoria()
    )

    if id_categoria is None:
        return


    # ========================================================
    # 5. ITEM
    # ========================================================

    id_item = selecionar_item(
        id_categoria
    )

    if id_item is None:
        return


    # ========================================================
    # 6. OBSERVAÇÃO
    # ========================================================

    observacao = input(
        "Observação (opcional): "
    )


    # ========================================================
    # 7. PARCELAS
    # ========================================================

    quantidade_parcelas = input(
        "Quantidade de parcelas [1]: "
    ).strip()

    if quantidade_parcelas == "":
        quantidade_parcelas = "1"


    # ========================================================
    # 8. RESPONSABILIDADE
    # ========================================================

    responsabilidades = (
        montar_responsabilidades(
            valor_total,
            tipo_cartao
        )
    )

    if responsabilidades is None:

        print(
            "\nResponsabilidade inválida."
        )

        return


    # ========================================================
    # 9. CADASTRAR
    # ========================================================

    resultado = cadastrar_compra(
        data=data,
        observacao=observacao,
        valor_total=valor_total,
        id_categoria=id_categoria,
        id_item=id_item,
        id_cartao=id_cartao,
        id_pessoa_pagador=id_pagador,
        quantidade_parcelas=
            quantidade_parcelas,
        responsabilidades=
            responsabilidades
    )

    print(
        f"\n{resultado}"
    )

# ============================================================
# ORÇAMENTO
# ============================================================

def menu_orcamento():

    while True:

        print("\n" + "=" * 50)
        print("                 ORÇAMENTO")
        print("=" * 50)

        print("1. Ver execução do mês")
        print("2. Definir orçamento")
        print("0. Voltar")

        opcao = input(
            "\nEscolha: "
        ).strip()


        # ====================================================
        # VER EXECUÇÃO
        # ====================================================

        if opcao == "1":

            periodo = selecionar_mes_execucao_orcamento()

            if periodo is None:
                continue

            mes_ano, nome_mes = periodo

            if mes_ano is None:
                print(
                    "\nEscolha um mês específico "
                    "para consultar o orçamento."
                )
                continue

            execucao = (
                obter_execucao_orcamento(
                    mes_ano
                )
            )

            print("\n" + "=" * 50)
            print(
                f"       EXECUÇÃO DO ORÇAMENTO — "
                f"{nome_mes.upper()}"
            )
            print("=" * 50)

            if not execucao:

                print(
                    "\nNenhum orçamento definido "
                    "para esse mês."
                )

                continue


            total_planejado = 0
            total_executado = 0

            for categoria in execucao:

                planejado = (
                    categoria["planejado"]
                )

                executado = (
                    categoria["executado"]
                )

                disponivel = (
                    categoria["disponivel"]
                )

                percentual = (
                    categoria[
                        "percentual_execucao"
                    ]
                )

                semaforo = (
                    categoria["semaforo"]
                )

                total_planejado += planejado
                total_executado += executado

                print(
                    "\n" + "-" * 50
                )

                print(
                    categoria[
                        "categoria"
                    ].upper()
                )

                print(
                    f"Planejado : "
                    f"{formatar_valor(planejado)}"
                )

                print(
                    f"Executado : "
                    f"{formatar_valor(executado)}"
                )

                print(
                    f"Disponível: "
                    f"{formatar_valor(disponivel)}"
                )

                print(
                    f"Execução  : "
                    f"{percentual:.1f}%"
                )

                print(
                    f"Semáforo  : "
                    f"{semaforo}"
                )


            # ================================================
            # RESUMO DO MÊS
            # ================================================

            total_disponivel = round(
                total_planejado
                - total_executado,
                2
            )

            if total_planejado > 0:

                percentual_total = round(
                    (
                        total_executado
                        / total_planejado
                    ) * 100,
                    1
                )

            else:
                percentual_total = 0


            print("\n" + "=" * 50)
            print("             RESUMO DO MÊS")
            print("=" * 50)

            print(
                f"Planejado total : "
                f"{formatar_valor(total_planejado)}"
            )

            print(
                f"Executado total : "
                f"{formatar_valor(total_executado)}"
            )

            print(
                f"Disponível total: "
                f"{formatar_valor(total_disponivel)}"
            )

            print(
                f"Execução total  : "
                f"{percentual_total:.1f}%"
            )


            # Ritmo temporal
            percentual_mes = (
                execucao[0][
                    "percentual_mes"
                ]
            )

            print(
                f"Mês transcorrido: "
                f"{percentual_mes:.1f}%"
            )

            print("=" * 50)


        # ====================================================
        # DEFINIR ORÇAMENTO
        # ====================================================

        elif opcao == "2":

            periodo = selecionar_mes_orcamento()

            if periodo is None:
                continue

            mes_ano, nome_mes = periodo

            if mes_ano is None:
                print(
                    "Escolha um mês específico."
                )
                continue


            print(
                f"\n=== ORÇAMENTO "
                f"{nome_mes.upper()} ==="
            )


            id_categoria = (
                selecionar_categoria()
            )

            if id_categoria is None:
                continue


            valor = input(
                "Valor planejado: "
            )


            resultado = (
                cadastrar_orcamento(
                    id_categoria,
                    mes_ano,
                    valor
                )
            )

            print(
                f"\n{resultado}"
            )


        elif opcao == "0":
            return


        else:
            print(
                "Opção inválida."
            )


# ============================================================
# CARTÕES
# ============================================================

def menu_cartoes():

    while True:

        print(
            "\n" + "=" * 45
        )

        print(
            "                CARTÕES"
        )

        print(
            "=" * 45
        )

        print(
            "1. Resumo do cartão"
        )

        print(
            "2. Ver cartões"
        )

        print(
            "0. Voltar"
        )

        escolha = input(
            "\nEscolha: "
        )


        if escolha == "1":

            contexto_cartao = selecionar_cartao_compra()

            if contexto_cartao is None:
                continue

            # Resumo só faz sentido para cartão
            # efetivamente cadastrado no sistema.
            if contexto_cartao["id_cartao"] is None:
                print(
                    "\nCartão de terceiro sem cadastro "
                    "não possui resumo de fatura."
                )
                continue

            id_cartao = contexto_cartao["id_cartao"]

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
                    "Mês inválido."
                )
                continue

            resumo = (
                obter_resumo_cartao(
                    id_cartao,
                    ano_mes
                )
            )

            if resumo is None:
                continue

            print(
                "\n" + "=" * 45
            )

            print(
                "          RESUMO DO CARTÃO"
            )

            print(
                "=" * 45
            )

            print(
                f"Cartão: "
                f"{resumo['cartao']}"
            )

            print(
                f"Fatura: "
                f"{mes_usuario.lower()}"
            )

            print(
                "\nLimite total: "
                f"{formatar_valor(resumo['limite_total'])}"
            )

            print(
                "Comprometido: "
                f"{formatar_valor(resumo['limite_comprometido'])}"
            )

            print(
                "Disponível: "
                f"{formatar_valor(resumo['limite_disponivel'])}"
            )

            print(
                "Fatura do mês: "
                f"{formatar_valor(resumo['fatura_mes'])}"
            )

            print(
                "Mana disponível: "
                f"{resumo['mana']:.1f}%"
            )


        elif escolha == "2":

            cartoes = obter_cartoes()

            if not cartoes:
                print(
                    "\nNenhum cartão cadastrado."
                )
                continue

            print(
                "\n=== CARTÕES CADASTRADOS ==="
            )

            for cartao in cartoes:

                id_cartao = cartao[0]
                instituicao = cartao[1]
                nome = cartao[2]
                limite_total = cartao[3]
                dia_fechamento = cartao[4]
                dia_vencimento = cartao[5]
                ativo = cartao[6]
                nome_titular = cartao[8]

                status = (
                    "Ativo"
                    if ativo == 1
                    else "Inativo"
                )

                print(
                    "\n" + "-" * 45
                )

                print(
                    f"{id_cartao}. "
                    f"{nome} | {instituicao}"
                )

                print(
                    f"Titular: {nome_titular}"
                )

                print(
                    f"Limite: "
                    f"{formatar_valor(limite_total)}"
                )

                print(
                    f"Fecha dia {dia_fechamento} "
                    f"| Vence dia {dia_vencimento}"
                )

                print(
                    f"Status: {status}"
                )

        elif escolha == "0":
                    return


        else:
            print("Opção inválida.")


# ============================================================
# ACERTO DE CONTAS
# ============================================================

def menu_acerto():

    while True:

        print(
            "\n" + "=" * 45
        )

        print(
            "          ACERTO DE CONTAS"
        )

        print(
            "=" * 45
        )

        print(
            "1. Ver acerto"
        )

        print(
            "2. Editar rateio de compra"
        )

        print(
            "0. Voltar"
        )

        escolha = input(
            "\nEscolha: "
        )


        if escolha == "1":

            acertos = (
                calcular_acerto_liquido()
            )

            print(
                "\n" + "=" * 45
            )

            print(
                "          ACERTO DE CONTAS"
            )

            print(
                "=" * 45
            )

            if not acertos:

                print(
                    "\nNenhum valor pendente."
                )

                continue

            for acerto in acertos:

                print(
                    "\n"
                    f"{acerto['devedor']} "
                    f"deve pagar para "
                    f"{acerto['credor']}:"
                )

                print(
                    formatar_valor(
                        acerto[
                            "valor"
                        ]
                    )
                )


        elif escolha == "2":

            compras = (
                obter_compras_para_rateio()
            )

            if not compras:
                continue

            print(
                "\n=== COMPRAS ==="
            )

            for indice, compra in enumerate(
                compras,
                start=1
            ):

                (
                    _,
                    data,
                    observacao,
                    valor,
                    _,
                    pagador
                ) = compra

                descricao = (
                    observacao
                    if observacao
                    else "Sem observação"
                )

                print(
                    f"{indice}. "
                    f"{descricao} | "
                    f"{formatar_valor(valor)} | "
                    f"{formatar_data(data)} | "
                    f"Pagador: {pagador}"
                )

            try:
                indice = int(
                    input(
                        "Escolha a compra: "
                    )
                )

            except ValueError:
                continue

            if not 1 <= indice <= len(
                compras
            ):
                continue

            compra = compras[
                indice - 1
            ]

            id_compra = compra[0]
            valor_total = compra[3]

            responsabilidades = (
                montar_responsabilidades(
                    valor_total
                )
            )

            if responsabilidades is None:
                continue

            print(
                registrar_rateio(
                    id_compra,
                    responsabilidades
                )
            )


        elif escolha == "0":
            return


# ============================================================
# CONSULTAR LANÇAMENTOS
# ============================================================

def menu_consultas():

    while True:

        print(
            "\n" + "=" * 45
        )

        print(
            "         CONSULTAR LANÇAMENTOS"
        )

        print(
            "=" * 45
        )

        print(
            "1. Movimentações"
        )

        print(
            "2. Compras no cartão"
        )

        print(
            "0. Voltar"
        )

        escolha = input(
            "\nEscolha: "
        )


        # ====================================================
        # MOVIMENTAÇÕES
        # ====================================================

        if escolha == "1":

            periodo = (
                selecionar_mes_consulta()
            )

            if periodo is None:
                continue

            mes_ano, nome_mes = periodo

            movimentacoes = (
                obter_resumo_movimentacoes()
            )

            # Se mes_ano for None,
            # significa "Todos".
            if mes_ano is not None:

                movimentacoes = [
                    movimentacao
                    for movimentacao
                    in movimentacoes

                    if movimentacao[1][
                        :7
                    ] == mes_ano
                ]


            print(
                "\n" + "=" * 45
            )

            print(
                "           MOVIMENTAÇÕES"
            )

            print(
                f"             {nome_mes}"
            )

            print(
                "=" * 45
            )


            if not movimentacoes:

                print(
                    "\nNenhuma movimentação "
                    "encontrada nesse período."
                )

                continue


            for movimentacao in movimentacoes:

                (
                    _,
                    data,
                    tipo,
                    descricao,
                    valor,
                    categoria,
                    item,
                    ativo
                ) = movimentacao


                print(
                    "\n" + "-" * 40
                )

                print(
                    f"{formatar_data(data)} "
                    f"| {tipo.upper()}"
                )


                # Entrada não possui categoria/item.
                if tipo == "saida":

                    print(
                        f"{categoria} / {item}"
                    )


                if descricao:

                    print(
                        f"Obs.: {descricao}"
                    )


                print(
                    formatar_valor(
                        valor
                    )
                )


        # ====================================================
        # COMPRAS NO CARTÃO
        # ====================================================

        elif escolha == "2":

            periodo = (
                selecionar_mes_consulta()
            )

            if periodo is None:
                continue

            mes_ano, nome_mes = periodo

            compras = obter_compras()


            if mes_ano is not None:

                compras = [
                    compra
                    for compra in compras

                    if compra[1][
                        :7
                    ] == mes_ano
                ]


            print(
                "\n" + "=" * 45
            )

            print(
                "        COMPRAS NO CARTÃO"
            )

            print(
                f"             {nome_mes}"
            )

            print(
                "=" * 45
            )


            if not compras:

                print(
                    "\nNenhuma compra encontrada "
                    "nesse período."
                )

                continue


            for compra in compras:

                (
                    id_compra,
                    data,
                    observacao,
                    valor_total,
                    quantidade_parcelas,
                    ativo
                ) = compra


                print(
                    "\n" + "-" * 40
                )

                print(
                    f"Data: "
                    f"{formatar_data(data)}"
                )

                print(
                    f"Valor: "
                    f"{formatar_valor(valor_total)}"
                )


                if observacao:

                    print(
                        f"Obs.: {observacao}"
                    )


                print(
                    f"Parcelas: "
                    f"{quantidade_parcelas}x"
                )


                parcelas = obter_parcelas(
                    id_compra
                )


                for parcela in parcelas:

                    (
                        _,
                        numero,
                        vencimento,
                        valor,
                        status
                    ) = parcela


                    print(
                        f"  "
                        f"{numero}/"
                        f"{quantidade_parcelas}"
                        f" | "
                        f"{formatar_data(vencimento)}"
                        f" | "
                        f"{formatar_valor(valor)}"
                        f" | "
                        f"{status}"
                    )


        # ====================================================
        # VOLTAR
        # ====================================================

        elif escolha == "0":
            return


        else:

            print(
                "Opção inválida."
            )


# ============================================================
# CONFIGURAÇÕES
# ============================================================


def menu_configuracoes():

    while True:

        print(
            "\n" + "=" * 45
        )

        print(
            "             CONFIGURAÇÕES"
        )

        print(
            "=" * 45
        )

        print(
            "1. Instituições"
        )

        print(
            "2. Contas"
        )

        print(
            "3. Cartões"
        )

        print(
            "4. Pessoas"
        )

        print(
            "5. Categorias e Itens"
        )

        print(
            "6. Meios de pagamento"
        )

        print(
            "0. Voltar"
        )

        escolha = input(
            "\nEscolha: "
        )


        # ====================================================
        # INSTITUIÇÕES
        # ====================================================

        if escolha == "1":

            print(
                "\n1. Ver"
            )
            print(
                "2. Cadastrar"
            )
            print(
                "3. Desativar"
            )

            acao = input(
                "Escolha: "
            )

            if acao == "1":

                for instituicao in (
                    listar_instituicoes()
                ):

                    _, nome, ativo = (
                        instituicao
                    )

                    print(
                        f"{nome} | "
                        f"{'Ativa' if ativo else 'Inativa'}"
                    )


            elif acao == "2":

                nome = input(
                    "Nome: "
                )

                print(
                    cadastrar_instituicao(
                        nome
                    )
                )


            elif acao == "3":

                id_instituicao = (
                    selecionar_instituicao()
                )

                if id_instituicao:

                    print(
                        inativar_instituicao(
                            id_instituicao
                        )
                    )


        # ====================================================
        # CONTAS
        # ====================================================

        elif escolha == "2":

            print(
                "\n1. Ver"
            )
            print(
                "2. Cadastrar"
            )
            print(
                "3. Desativar"
            )

            acao = input(
                "Escolha: "
            )

            if acao == "1":

                for conta in listar_contas():

                    print(
                        conta
                    )


            elif acao == "2":

                id_instituicao = (
                    selecionar_instituicao()
                )

                if id_instituicao is None:
                    continue

                nome = input(
                    "Nome da conta: "
                )

                tipo = input(
                    "Tipo "
                    "(corrente/poupança): "
                )

                saldo = input(
                    "Saldo inicial: "
                )

                print(
                    cadastrar_conta(
                        id_instituicao,
                        nome,
                        tipo,
                        saldo
                    )
                )


            elif acao == "3":

                id_conta = (
                    selecionar_conta()
                )

                if id_conta:

                    print(
                        desativar_conta(
                            id_conta
                        )
                    )


        # ====================================================
        # CARTÕES
        # ====================================================

        elif escolha == "3":

            print(
                "\n1. Ver"
            )
            print(
                "2. Cadastrar"
            )
            print(
                "3. Desativar"
            )

            acao = input(
                "Escolha: "
            )

            if acao == "1":

                for cartao in obter_cartoes():
                    print(
                        cartao
                    )


            elif acao == "2":

                id_instituicao = (
                    selecionar_instituicao()
                )

                if id_instituicao is None:
                    continue

                nome = input(
                    "Nome do cartão: "
                )

                limite = input(
                    "Limite: "
                )

                fechamento = input(
                    "Dia de fechamento: "
                )

                vencimento = input(
                    "Dia de vencimento: "
                )

                print(
                    "\nTitular do cartão:"
                )

                print(
                    "1. Eu [padrão]"
                )

                print(
                    "2. Outra pessoa"
                )

                titular_opcao = input(
                    "Escolha [Enter = 1]: "
                ).strip()

                if titular_opcao in (
                    "",
                    "1"
                ):
                    id_pessoa_titular = (
                        ID_USUARIO_PRINCIPAL
                    )

                elif titular_opcao == "2":

                    id_pessoa_titular = (
                        selecionar_pessoa()
                    )

                    if id_pessoa_titular is None:
                        continue

                else:

                    print(
                        "Opção inválida."
                    )

                    continue

                print(
                    cadastrar_cartao(
                        id_instituicao,
                        nome,
                        limite,
                        fechamento,
                        vencimento,
                        id_pessoa_titular
                    )
                )


            elif acao == "3":

                id_cartao = (
                    selecionar_cartao_compra()
                )

                if id_cartao:

                    print(
                        inativar_cartao(
                            id_cartao
                        )
                    )


        # ====================================================
        # PESSOAS
        # ====================================================

        elif escolha == "4":

            print(
                "\n1. Ver"
            )
            print(
                "2. Cadastrar"
            )
            print(
                "3. Desativar"
            )

            acao = input(
                "Escolha: "
            )

            if acao == "1":

                for pessoa in obter_pessoas():
                    print(
                        pessoa
                    )


            elif acao == "2":

                nome = input(
                    "Nome: "
                )

                print(
                    cadastrar_pessoa(
                        nome
                    )
                )


            elif acao == "3":

                id_pessoa = (
                    selecionar_pessoa()
                )

                if id_pessoa:

                    print(
                        inativar_pessoa(
                            id_pessoa
                        )
                    )


        # ====================================================
        # CATEGORIAS / ITENS
        # ====================================================

        elif escolha == "5":

            print(
                "\n=== CATEGORIAS ==="
            )

            for categoria in (
                obter_resumo_categorias()
            ):
                print(
                    categoria
                )

            print(
                "\n=== ITENS ==="
            )

            for item in obter_itens():
                print(
                    item
                )

            print(
                "\n1. Cadastrar item"
            )
            print(
                "2. Desativar item"
            )
            print(
                "0. Voltar"
            )

            acao = input(
                "Escolha: "
            )

            if acao == "1":

                id_categoria = (
                    selecionar_categoria()
                )

                if id_categoria is None:
                    continue

                nome = input(
                    "Nome do item: "
                )

                print(
                    cadastrar_item(
                        id_categoria,
                        nome
                    )
                )


            elif acao == "2":

                try:
                    id_item = int(
                        input(
                            "ID do item: "
                        )
                    )

                except ValueError:
                    continue

                print(
                    inativar_item(
                        id_item
                    )
                )


        # ====================================================
        # MEIOS DE PAGAMENTO
        # ====================================================

        elif escolha == "6":

            print(
                "\n=== MEIOS DE PAGAMENTO ==="
            )

            for meio in (
                obter_resumo_meios_pagamento()
            ):
                print(
                    meio
                )


        elif escolha == "0":
            return


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
            "\n1. Registrar movimentação"
        )

        print(
            "2. Registrar compra no cartão"
        )

        print(
            "3. Orçamento"
        )

        print(
            "4. Cartões"
        )

        print(
            "5. Acerto de contas"
        )

        print(
            "6. Consultar lançamentos"
        )

        print(
            "7. Configurações"
        )

        print(
            "\n0. Sair"
        )

        escolha = input(
            "\nDigite sua opção: "
        )


        if escolha == "1":
            fluxo_registrar_movimentacao()


        elif escolha == "2":
            fluxo_registrar_compra()


        elif escolha == "3":
            menu_orcamento()


        elif escolha == "4":
            menu_cartoes()


        elif escolha == "5":
            menu_acerto()


        elif escolha == "6":
            menu_consultas()


        elif escolha == "7":
            menu_configuracoes()


        elif escolha == "0":

            print(
                "\nAté a próxima aventura!"
            )

            break


        else:

            print(
                "\nOpção inválida."
            )


# ============================================================
# INÍCIO
# ============================================================

if __name__ == "__main__":
    iniciar_taverna()