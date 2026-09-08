from database import conectar_base


def listar_itens():
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            i.id_item,
            i.id_categoria,
            c.nome,
            i.nome,
            i.ativo
        FROM item i

        JOIN categoria c
            ON i.id_categoria = c.id

        ORDER BY c.nome, i.nome;
    """)

    dados = cursor.fetchall()

    conexao.close()

    return dados


def listar_itens_por_categoria(id_categoria):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id_item,
            nome,
            ativo
        FROM item
        WHERE id_categoria = ?
          AND ativo = 1
        ORDER BY nome;
    """, (id_categoria,))

    dados = cursor.fetchall()

    conexao.close()

    return dados


def inserir_item(
    id_categoria,
    nome
):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO item (
            id_categoria,
            nome
        )
        VALUES (?, ?);
    """, (
        id_categoria,
        nome
    ))

    conexao.commit()
    conexao.close()


def buscar_item(
    id_categoria,
    nome
):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id_item,
            id_categoria,
            nome,
            ativo
        FROM item
        WHERE id_categoria = ?
          AND nome = ?;
    """, (
        id_categoria,
        nome
    ))

    item = cursor.fetchone()

    conexao.close()

    return item


def desativar_item(id_item):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE item
        SET ativo = 0
        WHERE id_item = ?;
    """, (id_item,))

    linhas_afetadas = cursor.rowcount

    conexao.commit()
    conexao.close()

    return linhas_afetadas