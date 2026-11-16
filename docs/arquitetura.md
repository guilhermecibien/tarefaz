# Arquitetura MVC

O Tarefaz usa uma organização baseada em MVC (Model-View-Controller) para separar as responsabilidades do sistema.

- **Models** (`app/models`): concentram o acesso ao SQLite e as consultas ligadas a usuários, tarefas e itens do checklist. Por exemplo, `task.py` busca tarefas apenas pelo `usuario_id` da sessão.
- **Views** (`app/templates`): são as páginas HTML renderizadas para o usuário. O CSS e o JavaScript de apoio ficam em `app/static`.
- **Controllers** (`app/controllers`): recebem requisições, validam dados, chamam os models e escolhem a view ou redirecionamento adequado.

O arquivo `app/__init__.py` funciona como fábrica da aplicação: configura Flask e banco de dados, depois registra os controllers.
