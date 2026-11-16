# Plano e Registro de Testes

## 1. Objetivo

Os testes verificam se as principais funcionalidades do Tarefaz atendem ao comportamento esperado e se os dados de cada usuário permanecem protegidos.

## 2. Testes automatizados

Os testes automatizados foram implementados com **pytest** no arquivo [tests/test_tarefaz.py](../tests/test_tarefaz.py).

Para executá-los localmente:

```bash
pytest
```

Na validação da versão atual, foram executados **19 testes com sucesso**.

| Grupo | Funcionalidades verificadas |
|---|---|
| Autenticação | Cadastro, login, regras de senha e troca de senha. |
| Conta | Alteração de nome e e-mail, validação da senha atual e bloqueio de e-mail duplicado. |
| Tarefas | Criação, validação de título obrigatório, edição, exclusão, conclusão e reabertura. |
| Organização | Agrupamento de tarefas atrasadas e busca por texto. |
| Segurança de dados | Impedimento de acesso, edição e exclusão de tarefas de outra conta. |
| Checklist | Inclusão, conclusão, exclusão e visualização de itens vinculados a uma tarefa. |
| Prazos | Exibição dos rótulos Hoje, Amanhã, data futura e data atrasada. |

## 3. Critérios de aprovação

Uma funcionalidade é considerada aprovada quando:

- Produz o resultado esperado.
- Apresenta mensagem adequada para dados inválidos.
- Não permite que uma conta acesse dados de outra conta.
- Mantém o banco de dados consistente após a operação.

## 4. Testes de aceitação por usuários

A etapa seguinte será realizada com cinco avaliadores reais. Cada pessoa deverá criar uma conta e testar o sistema publicado.

Sugestão de distribuição dos testes:

| Avaliador | Funcionalidades sugeridas |
|---|---|
| 1 | Cadastro, login e alteração de senha. |
| 2 | Criação de tarefa, prazo e organização por data. |
| 3 | Edição de tarefa, marcação como importante e busca. |
| 4 | Inclusão, conclusão e exclusão de itens de checklist. |
| 5 | Conclusão e reabertura de tarefa, tema e página de conta. |

Para cada avaliação, serão registrados nome, data, funcionalidades que funcionaram, problemas encontrados, sugestão de correção e funcionalidades que não foram testadas. Os registros serão inseridos no template oficial da disciplina.

## 5. Registro de melhorias

Qualquer problema ou sugestão pertinente identificado pelos avaliadores será registrado no laudo de qualidade. As correções realizadas serão publicadas no repositório com um commit descritivo.
