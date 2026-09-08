from database import conectar_base


def listar_contas():
    conexao = conectar_base()
    cursor = conexao.cursor()

    comandos_sql = """
    SELECT
        c.id_conta,
        i.nome,
        c.nome,
        c.tipo,
        c.saldo_inicial,
        c.ativo
    FROM conta c
    JOIN instituicao i
        ON c.id_instituicao = i.id_instituicao;
    """

    cursor.execute(comandos_sql)
    dados = cursor.fetchall()

    conexao.close()

    return dados


def inserir_conta(id_instituicao, nome, tipo, saldo_inicial):
    conexao = conectar_base()
    cursor = conexao.cursor()

    comandos_sql = """
    INSERT INTO conta (
        id_instituicao,
        nome,
        tipo,
        saldo_inicial
    )
    VALUES (?, ?, ?, ?);
    """

    cursor.execute(
        comandos_sql,
        (id_instituicao, nome, tipo, saldo_inicial)
    )

    conexao.commit()
    conexao.close()


def desativar_conta(id_conta):
    conexao = conectar_base()
    cursor = conexao.cursor()

    comandos_sql = """
    UPDATE conta
    SET ativo = 0
    WHERE id_conta = ?;
    """

    cursor.execute(
        comandos_sql,
        (id_conta,)
    )

    linhas_afetadas = cursor.rowcount

    conexao.commit()
    conexao.close()

    return linhas_afetadas


def buscar_conta_por_nome(nome):
    conexao = conectar_base()
    cursor = conexao.cursor()

    comandos_sql = """
    SELECT id_conta, nome, ativo
    FROM conta
    WHERE nome = ?;
    """

    cursor.execute(
        comandos_sql,
        (nome,)
    )

    dado = cursor.fetchone()

    conexao.close()

    return dado


if __name__ == "__main__":
    print(listar_contas())