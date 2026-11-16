# Visão Geral e Requisitos do Tarefaz

## 1. Apresentação

O Tarefaz é uma aplicação web de organização de tarefas pessoais. O sistema permite que cada usuário crie uma conta, registre suas tarefas e acompanhe o que precisa ser feito no dia a dia.

As tarefas são organizadas por prazo em grupos como atrasadas, hoje, próximas e sem data. Além disso, o usuário pode marcar tarefas como importantes, adicionar descrições e checklists, pesquisar informações e concluir atividades.

## 2. Problema abordado

Muitas tarefas pessoais ficam distribuídas em anotações, mensagens ou são esquecidas por não terem um prazo ou uma forma simples de acompanhamento. O Tarefaz foi desenvolvido para reunir essas informações em um ambiente único, simples e acessível pelo navegador.

## 3. Objetivo

Disponibilizar uma aplicação web que ajude pessoas a registrar, priorizar e acompanhar tarefas pessoais de forma organizada.

## 4. Público-alvo

O sistema é voltado para pessoas que desejam organizar tarefas de estudo, trabalho ou rotina pessoal sem utilizar ferramentas complexas.

## 5. Escopo da solução

Nesta versão, o Tarefaz disponibiliza:

- Cadastro, login e logout de usuários.
- Alteração de nome, e-mail e senha na página de conta.
- Criação de tarefas com título e prazo opcional.
- Edição de título, descrição, prazo e indicação de tarefa importante.
- Organização das tarefas em atrasadas, hoje, próximas, sem data e concluídas.
- Conclusão e reabertura de tarefas.
- Checklist vinculado a cada tarefa.
- Busca por título ou descrição.
- Tema claro e escuro.
- Isolamento das informações: cada usuário visualiza somente as próprias tarefas.

## 6. Requisitos funcionais

| Código | Requisito |
|---|---|
| RF01 | O sistema deve permitir o cadastro de novos usuários. |
| RF02 | O sistema deve permitir login e logout. |
| RF03 | O usuário deve poder alterar seus dados de conta e senha. |
| RF04 | O usuário deve poder criar uma tarefa com título obrigatório e prazo opcional. |
| RF05 | O usuário deve poder editar e excluir uma tarefa própria. |
| RF06 | O usuário deve poder marcar uma tarefa como concluída ou reabri-la. |
| RF07 | O sistema deve separar as tarefas de acordo com prazo e situação. |
| RF08 | O usuário deve poder marcar uma tarefa como importante. |
| RF09 | O usuário deve poder adicionar, concluir e excluir itens de checklist. |
| RF10 | O sistema deve permitir busca por título ou descrição. |
| RF11 | O usuário deve visualizar somente os dados vinculados à sua conta. |
| RF12 | O sistema deve oferecer alternância entre tema claro e escuro. |

## 7. Requisitos não funcionais

| Código | Requisito |
|---|---|
| RNF01 | A aplicação deve ser acessível por navegador em computador ou celular. |
| RNF02 | As senhas devem ser armazenadas com hash, e não em texto puro. |
| RNF03 | Os dados devem permanecer disponíveis após reinicializações do serviço de hospedagem. |
| RNF04 | A interface deve apresentar mensagens claras para dados inválidos. |
| RNF05 | O código deve seguir uma organização baseada no padrão MVC. |
| RNF06 | O sistema deve possuir testes automatizados para funcionalidades principais. |

## 8. Regras de negócio

- Uma tarefa não pode ser criada sem título.
- Uma tarefa pertence a apenas um usuário.
- Um usuário não pode acessar, editar ou excluir tarefas de outra conta.
- Um item de checklist pertence a uma única tarefa.
- Tarefas com prazo anterior à data atual e ainda não concluídas são apresentadas como atrasadas.
- Tarefas importantes recebem destaque visual e são exibidas antes das demais dentro de cada grupo.

## 9. Itens fora do escopo

Esta versão não inclui colaboração entre usuários, compartilhamento de tarefas, notificações por e-mail, integração com calendário ou aplicativo para instalação em celular.
