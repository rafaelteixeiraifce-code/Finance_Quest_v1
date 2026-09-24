# 🎮 Finance Quest

**Seu dinheiro. Sua jornada.**

Finance Quest é um projeto de controle financeiro pessoal desenvolvido com o objetivo de unir organização financeira, análise de dados e aprendizado prático de desenvolvimento de software.

O projeto começou como uma solução para controle das finanças pessoais e também funciona como um projeto de aprendizagem: cada nova funcionalidade é utilizada para estudar e aplicar conceitos de Python, SQL, bancos de dados, arquitetura de software e, atualmente, desenvolvimento web com HTML e CSS.

A proposta futura é transformar o controle financeiro em uma experiência visual inspirada em jogos de RPG e pixel art.

---

## 🎯 Objetivo

O Finance Quest busca permitir o acompanhamento das finanças pessoais de forma simples, estruturada e progressivamente mais visual.

Entre os objetivos do projeto estão:

* registrar entradas e saídas;
* acompanhar compras e parcelas;
* controlar cartões de crédito;
* organizar categorias e itens;
* criar e acompanhar orçamentos;
* dividir despesas entre pessoas;
* acompanhar compromissos financeiros futuros;
* desenvolver indicadores e dashboards;
* auxiliar na tomada de decisões financeiras.

Além da aplicação em si, o projeto é utilizado como ambiente prático de aprendizagem de desenvolvimento de software.

---

## 🚧 Estado atual

O Finance Quest está em desenvolvimento.

A primeira versão utilizável foi construída em **Python**, utilizando **SQLite** como banco de dados e uma interface executada pelo terminal.

Essa versão já permite trabalhar com diferentes partes do controle financeiro, incluindo:

* movimentações financeiras;
* compras;
* parcelas;
* cartões;
* contas e instituições financeiras;
* pessoas;
* categorias e itens;
* meios de pagamento;
* orçamento;
* rateio e acerto de contas.

Atualmente, o projeto também iniciou uma nova etapa: a construção de uma **interface web com HTML e CSS**.

Essa interface ainda está em desenvolvimento e representa também o primeiro contato prático do autor do projeto com desenvolvimento web.

---

## 🧱 Arquitetura

A aplicação Python utiliza uma separação de responsabilidades inspirada em uma arquitetura em camadas:

`Interface → Service → Repository → Database → SQLite`

### Interface

Responsável pela interação com o usuário.

Na versão atual em Python, essa função está principalmente concentrada em `main.py`, através da interface de terminal.

### Service

Contém validações, transformações e regras de negócio.

Exemplo:

`categoria_service.py`

### Repository

Responsável pelo acesso aos dados e pela execução das operações SQL.

Exemplo:

`categoria_repository.py`

### Database

Centraliza a conexão com o banco SQLite.

Exemplo:

`database.py`

Essa separação busca evitar que interface, regras de negócio e acesso ao banco de dados fiquem misturados no mesmo código.

---

## 🗃️ Modelagem de dados

O Finance Quest utiliza um banco de dados relacional em SQLite.

A modelagem contempla entidades relacionadas ao domínio financeiro, como:

* instituições;
* contas;
* cartões;
* pessoas;
* categorias;
* itens;
* meios de pagamento;
* movimentações;
* compras;
* parcelas;
* participações em despesas;
* orçamentos;
* metas.

O banco utiliza conceitos como:

* chaves primárias (PK);
* chaves estrangeiras (FK);
* relacionamentos entre tabelas;
* restrições `UNIQUE`;
* restrições `CHECK`;
* integridade referencial.

A evolução da estrutura do banco também é registrada através de migrations.

---

## 📁 Estrutura do projeto

De forma simplificada:

```text
Finance_Quest_v1/
│
├── migrations/
│   └── evolução da estrutura do banco
│
├── scripts/
│   └── scripts auxiliares e ambiente de desenvolvimento
│
├── src/
│   ├── main.py
│   ├── database.py
│   ├── *_service.py
│   └── *_repository.py
│
└── README.md
```

À medida que a interface web evoluir, os arquivos relacionados ao frontend também passarão a fazer parte dessa estrutura.

---

## 🌐 Interface web

O desenvolvimento da interface web representa a etapa atual do projeto.

As primeiras tecnologias utilizadas são:

**HTML**

Responsável pela estrutura e pelo significado do conteúdo apresentado na página.

**CSS**

Responsável pela apresentação visual, layout e estilização da interface.

Nesta etapa, o objetivo também é aprender os fundamentos dessas tecnologias através da construção real da interface do Finance Quest.

A evolução posterior poderá conectar essa interface às regras de negócio e aos dados já existentes na aplicação.

---

## 🧰 Tecnologias

Atualmente, o projeto envolve:

* **Python** — regras de negócio e aplicação;
* **SQLite** — banco de dados;
* **SQL** — manipulação e consulta dos dados;
* **HTML** — estrutura da interface web;
* **CSS** — apresentação da interface web;
* **Git e GitHub** — versionamento e documentação do desenvolvimento.

---

## 🎮 Identidade do Finance Quest

A visão de longo prazo é combinar controle financeiro com uma identidade inspirada em RPG e pi
