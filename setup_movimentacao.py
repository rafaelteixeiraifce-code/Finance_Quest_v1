import sqlite3

#1. Abrindo a porta da taverna
conexao = sqlite3.connect('finance_quest.db')
cursor = conexao.cursor()

#2. Escrevendo o comando SQL
comandos_sql = """
CREATE TABLE IF NOT EXISTS meio_pagamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE, 
    tipo TEXT NOT NULL CHECK (tipo IN ('conta', 'cartao', 'dinheiro', 'outros')),
    id_conta INTEGER,  
    id_cartao INTEGER,
    ativo INTEGER DEFAULT 1,
    FOREIGN KEY (id_conta) REFERENCES conta(id),
    FOREIGN KEY (id_cartao) REFERENCES cartao(id)
);

CREATE TABLE IF NOT EXISTS movimentacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    descricao TEXT NOT NULL,
    valor REAL NOT NULL,
    id_categoria INTEGER NOT NULL,
    id_pessoa INTEGER NOT NULL,
    id_meio_pagamento INTEGER NOT NULL,
    ativo INTEGER DEFAULT 1,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id),
    FOREIGN KEY (id_pessoa) REFERENCES pessoa(id),
    FOREIGN KEY (id_meio_pagamento) REFERENCES meio_pagamento(id)
);
"""

#3. Executando o script SQL
cursor.executescript(comandos_sql)

#4. Confirmando as alterações e fechando
conexao.commit()
conexao.close()

print("As entidades 'meio_pagamento' e 'movimentacao' foram criadas e os dados inseridos com sucesso!")