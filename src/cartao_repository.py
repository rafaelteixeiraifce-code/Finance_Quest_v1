from database import conectar_base


def listar_cartoes():
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            c.id_cartao,
            i.nome,
            c.nome,
            c.limite_total,
            c.dia_fechamento,
            c.dia_vencimento,
            c.ativo,
            c.id_pessoa_titular,
            COALESCE(p.nome, '-')

        FROM cartao c

        JOIN instituicao i
            ON c.id_instituicao = i.id_instituicao

        LEFT JOIN pessoa p
            ON c.id_pessoa_titular = p.id

        ORDER BY i.nome, c.nome;
    """)

    dados = cursor.fetchall()

    conexao.close()
    return dados


def inserir_cartao(
    id_instituicao,
    nome,
    limite_total,
    dia_fechamento,
    dia_vencimento,
    id_pessoa_titular
):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO cartao (
            id_instituicao,
            nome,
            limite_total,
            dia_fechamento,
            dia_vencimento,
            id_pessoa_titular
        )
        VALUES (?, ?, ?, ?, ?, ?);
    """, (
        id_instituicao,
        nome,
        limite_total,
        dia_fechamento,
        dia_vencimento,
        id_pessoa_titular
    ))

    conexao.commit()
    conexao.close()


def desativar_cartao(id_cartao):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE cartao
        SET ativo = 0
        WHERE id_cartao = ?;
    """, (id_cartao,))

    linhas_afetadas = cursor.rowcount

    conexao.commit()
    conexao.close()

    return linhas_afetadas


def buscar_cartao_por_nome(nome):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id_cartao,
            nome,
            ativo
        FROM cartao
        WHERE nome = ?;
    """, (nome,))

    cartao = cursor.fetchone()

    conexao.close()
    return cartao


def buscar_cartao_por_id(id_cartao):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id_cartao,
            nome,
            limite_total,
            dia_fechamento,
            dia_vencimento,
            ativo,
            id_pessoa_titular
        FROM cartao
        WHERE id_cartao = ?;
    """, (id_cartao,))

    cartao = cursor.fetchone()

    conexao.close()
    return cartao


def listar_cartoes_por_titular(id_pessoa):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            c.id_cartao,
            i.nome,
            c.nome,
            c.limite_total,
            c.dia_fechamento,
            c.dia_vencimento,
            c.ativo,
            c.id_pessoa_titular,
            p.nome

        FROM cartao c

        JOIN instituicao i
            ON c.id_instituicao = i.id_instituicao

        JOIN pessoa p
            ON c.id_pessoa_titular = p.id

        WHERE c.id_pessoa_titular = ?
          AND c.ativo = 1

        ORDER BY c.nome;
    """, (id_pessoa,))

    dados = cursor.fetchall()

    conexao.close()
    return dados


def calcular_limite_comprometido(id_cartao):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            COALESCE(SUM(p.valor), 0)

        FROM parcela p

        JOIN compra c
            ON p.id_compra = c.id_compra

        WHERE c.id_cartao = ?
          AND p.status = 'pendente'
          AND c.ativo = 1;
    """, (id_cartao,))

    total = cursor.fetchone()[0]

    conexao.close()
    return total


def calcular_fatura_mes(
    id_cartao,
    ano_mes
):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            COALESCE(SUM(p.valor), 0)

        FROM parcela p

        JOIN compra c
            ON p.id_compra = c.id_compra

        WHERE c.id_cartao = ?
          AND substr(
                p.data_vencimento,
                1,
                7
              ) = ?
          AND p.status = 'pendente'
          AND c.ativo = 1;
    """, (
        id_cartao,
        ano_mes
    ))

    total = cursor.fetchone()[0]

    conexao.close()
    return total