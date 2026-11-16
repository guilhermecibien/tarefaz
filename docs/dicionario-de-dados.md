# Dicionário de dados

## Tabela `usuarios`

| Campo | Tipo | Finalidade |
|---|---|---|
| id | INTEGER | Identificador único do usuário (chave primária). |
| nome | TEXT | Nome exibido no sistema. |
| email | TEXT | E-mail de login; único por usuário. |
| senha_hash | TEXT | Senha armazenada de forma protegida por hash. |
| data_criacao | TIMESTAMP | Momento de criação da conta. |

## Tabela `tarefas`

| Campo | Tipo | Finalidade |
|---|---|---|
| id | INTEGER | Identificador único da tarefa (chave primária). |
| titulo | TEXT | Título obrigatório da tarefa. |
| descricao | TEXT | Detalhes opcionais da tarefa. |
| prioridade | TEXT | `alta` marca a tarefa como importante (★); `media` é o padrão. |
| prazo | DATE | Data limite opcional. |
| status | TEXT | `a_fazer` ou `concluido`. |
| usuario_id | INTEGER | Usuário proprietário da tarefa (chave estrangeira). |
| data_criacao | TIMESTAMP | Momento de criação da tarefa. |
| data_atualizacao | TIMESTAMP | Última atualização da tarefa. |

A coluna `tarefas.usuario_id` referencia `usuarios.id`, garantindo que cada tarefa esteja ligada a uma conta existente.

## Tabela `itens`

Itens do checklist de uma tarefa.

| Campo | Tipo | Finalidade |
|---|---|---|
| id | INTEGER | Identificador único do item (chave primária). |
| tarefa_id | INTEGER | Tarefa à qual o item pertence (chave estrangeira, com exclusão em cascata). |
| texto | TEXT | Texto do item; não pode ser vazio. |
| feito | INTEGER | 0 = pendente, 1 = concluído. |
