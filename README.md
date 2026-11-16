# Tarefaz

Lista de tarefas para o dia a dia, feita como projeto da disciplina de Engenharia de Software. Cada usuário tem a sua conta e só enxerga as próprias tarefas.

## O que faz

- Cadastro, login e logout; troca de nome, e-mail e senha na página Conta.
- Adicionar tarefa só com o título (e a data, se quiser).
- Marcar como concluída com um clique.
- Lista separada em Atrasadas, Hoje, Próximas, Sem data e Concluídas.
- Tarefas marcadas com ★ aparecem primeiro dentro de cada grupo.
- Descrição e checklist em cada tarefa; o checklist também pode ser usado direto na lista.
- Editar o título clicando nele.
- Prazos como "Amanhã", "Sex" ou "há 3 dias".
- Busca por texto e modo escuro.

## Tecnologias

Python 3, Flask, SQLite, HTML/CSS/JavaScript sem frameworks e pytest.

## Como rodar

Necessário Python 3.10 ou superior.

```bash
python3 -m venv .venv
source .venv/bin/activate      # no Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Depois é só abrir http://127.0.0.1:5000. Fora do seu computador, defina a variável de ambiente `SECRET_KEY` com um valor próprio antes de subir o sistema. O banco (`instance/tarefaz.sqlite`) é criado sozinho na primeira execução. Para apagar tudo e começar do zero: `flask --app run init-db`.

## Testes

```bash
pytest
```

## Organização

```text
app/
  controllers/   rotas e validação dos formulários
  models/        consultas ao banco
  templates/     páginas HTML
  static/        CSS, JavaScript e fontes
  schema.sql     tabelas do banco
docs/            arquitetura e dicionário de dados
tests/           testes automatizados
run.py           ponto de entrada
```

## Licença

MIT. Veja o arquivo [LICENSE](LICENSE).
