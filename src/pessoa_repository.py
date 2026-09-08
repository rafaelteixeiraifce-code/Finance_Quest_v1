from database import conectar_base


def listar_pessoas():
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, ativo
        FROM pessoa
        ORDER BY nome;
    """)

    dados = cursor.fetchall()

    conexao.close()

    return dados


def inserir_pessoa(nome):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO pessoa (nome)
        VALUES (?);
    """, (nome,))

    conexao.commit()
    conexao.close()


def buscar_pessoa_por_nome(nome):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, ativo
        FROM pessoa
        WHERE nome = ?;
    """, (nome,))

    pessoa = cursor.fetchone()

    conexao.close()

    return pessoa


def desativar_pessoa(id_pessoa):
    conexao = conectar_base()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE pessoa
        SET ativo = 0
        WHERE id = ?;
    """, (id_pessoa,))

    linhas_afetadas = cursor.rowcount

    conexao.commit()
    conexao.close()

    return linhas_afetadas