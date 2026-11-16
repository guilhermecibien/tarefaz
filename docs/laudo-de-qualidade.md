# Laudo de Qualidade do Tarefaz

## 1. Objetivo

Este laudo registra os resultados dos testes de aceitação realizados por cinco avaliadores convidados e as melhorias aplicadas à versão publicada do Tarefaz.

## 2. Evidências utilizadas

- [Registros dos testes de aceitação](testes-de-aceitacao.md)
- [Plano e registro de testes automatizados](plano-de-testes.md)
- Sistema publicado: https://tarefaz-production.up.railway.app/login

Os testes automatizados da versão atual também foram executados com sucesso, totalizando 19 testes aprovados.

## 3. Resumo da avaliação

| Item avaliado | Resultado |
|---|---|
| Cadastro e login | Funcionamento confirmado pelos avaliadores. |
| Criação de tarefas e definição de prazo | Funcionamento confirmado pelos avaliadores. |
| Organização visual das tarefas | Avaliada como simples, direta e intuitiva. |
| Checklist | Funcionamento confirmado. |
| Busca | Funcionamento confirmado. |
| Troca de senha, logout e novo login | Funcionamento confirmado. |
| Tema escuro | Funcionamento confirmado. |

Os avaliadores não relataram falhas críticas nas funcionalidades utilizadas.

## 4. Melhoria identificada

| Identificação | Descrição |
|---|---|
| LQ-01 | A avaliadora Cassia Nascimentos dos Santos sugeriu maior diferenciação visual para tarefas urgentes. |

A sugestão foi considerada pertinente, pois tarefas com prazo para o dia atual ou vencido precisam chamar mais atenção na lista.

## 5. Correção aplicada

Foi aplicada uma diferenciação visual com cores leves nas seções:

- **Hoje:** destaque visual para tarefas com prazo no dia atual.
- **Atrasadas:** destaque visual para tarefas com prazo vencido.

A implementação utiliza cores e uma borda lateral discreta para melhorar a identificação das prioridades, sem comprometer a simplicidade da interface.

## 6. Resultado após a correção

A melhoria torna a visualização das tarefas urgentes mais clara e atende à sugestão recebida durante os testes. A correção foi incorporada ao código publicado e será demonstrada no vídeo final do projeto.

## 7. Conclusão

Com base nos testes automatizados e nos cinco testes de aceitação, o Tarefaz apresentou comportamento adequado para as funcionalidades avaliadas. A única melhoria registrada foi implementada e documentada, demonstrando o uso do feedback para evolução da solução.
