console.log("Finance Quest iniciado!");


// ================================
// ELEMENTOS DO HTML
// ================================

const tipo =
    document.getElementById("tipo");

const categoria =
    document.getElementById("categoria");

const item =
    document.getElementById("item");

const campoCategoria =
    document.getElementById("campo-categoria");

const campoItem =
    document.getElementById("campo-item");

const campoPagamento =
    document.getElementById(
        "campo-pagamento"
    );


// ================================
// ITENS POR CATEGORIA
// ================================

const itensPorCategoria = {
    supermercado: [
        "Supermercado",
        "Delivery"
    ],

    moradia: [
        "IPTU",
        "Energia",
        "Condomínio"
    ],

    transporte: [
        "Kwid Gasolina",
        "Uber",
        "Ônibus"
    ],

    lazer: [
        "Restaurante",
        "Passeios",
        "Itapipoca"
    ],

    compras: [
        "Amazon",
        "Cartão",
        "Clube Livelo",
        "Compras",
        "Presente",
        "Roupas"
    ],

    contas: [
        "Vivo",
        "Google One",
        "Revisão Kwid",
        "IPVA Kwid",
        "Kwid (parcela+seguro)"
    ],

    aportes: [
        "Aporte"
    ],

    olivia: [
        "Unimed",
        "Exames",
        "Compras",
        "Remédios e Vitaminas"
    ],

    mae: [
        "Ajuda p/ mãe",
        "Psi mãe"
    ],

    outros: [
        "Barbearia",
        "Spotify"
    ]
};


// ================================
// EVENTO: TIPO
// ================================

tipo.addEventListener("change", function () {

    if (tipo.value === "entrada") {

        campoCategoria.classList.add(
            "oculto"
        );

        campoItem.classList.add(
            "oculto"
        );

        categoria.value = "";

        item.innerHTML = `
            <option value="">
                Selecione...
            </option>
        `;

    } else {

        campoCategoria.classList.remove(
            "oculto"
        );

        campoItem.classList.remove(
            "oculto"
        );
    }
});


// ================================
// EVENTO: CATEGORIA
// ================================

categoria.addEventListener(
    "change",
    function () {

        const categoriaSelecionada =
            categoria.value;

        // Primeiro limpa o campo Item
        item.innerHTML = `
            <option value="">
                Selecione...
            </option>
        `;

        // Se nenhuma categoria foi selecionada,
        // encerra a função.
        if (!categoriaSelecionada) {
            return;
        }

        const itens =
            itensPorCategoria[categoriaSelecionada];

        // Proteção caso a categoria não exista
        // no objeto itensPorCategoria.
        if (!itens) {
            return;
        }

        // Cria uma <option> para cada item.
        itens.forEach(function (nomeItem) {

            const opcao =
                document.createElement("option");

            opcao.value = nomeItem;
            opcao.textContent = nomeItem;

            item.appendChild(opcao);
        });

        console.log(
            "Categoria:",
            categoriaSelecionada
        );

        console.log(
            "Itens:",
            itens
        );

        console.log(
            "Meio de Pagamento",
            campoPagamento
        )
    }
);