# Frascos

    Frascos é uma rede social semelhante ao X/Twitter

# Descrição

    Frascos é um projeto que eu fiz para estudar melhor o Flask e Web application
    em geral. Essencialmente ele é uma rede social inspirada no X/Twitter

# Tecnologias Usadas

- Backend: Flask
- Database: PostgreSQL
- Frontend: HTML,CSS,JavaScript

# Como Rodar o Projeto

- Abra a pasta do projeto no terminal
- Ative o ambiente virtual

```bash
# Criando...
python -m venv venv

# Linux
. venv/bin/activate

# Windows
. venv\Scripts\Activate
```

- Instale as dependências

```bash
pip install -r requirements.txt
```

- Crie um usuário no PostgreSQL chamado frascos_db com senha postgres
- Rode os scripts do arquivo DDL_SQL.md

- Rode o programa

```bash
flask --app frascos.py run
```
