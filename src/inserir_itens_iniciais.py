from item_service import cadastrar_item


itens = [
    # Categoria 1 - Salário / Receita
    # normalmente não precisa de item agora

    # Categoria 2 - Supermercado
    (2, "Mercado"),
    (2, "Feira"),
    (2, "Produtos de limpeza"),

    # Categoria 3 - Transporte
    (3, "Gasolina"),
    (3, "Uber"),
    (3, "Estacionamento")
]


for id_categoria, nome in itens:
    resultado = cadastrar_item(
        id_categoria,
        nome
    )

    print(resultado)