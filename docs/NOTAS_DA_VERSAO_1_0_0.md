---
lang: pt-BR
title: Notas da versão 1.0.0
subject: Compatibilidade, correções verificadas e alcance da estabilidade
author: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
keywords: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
manager: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
---

# Notas da versão 1.0.0

A versão 1.0.0 distribui a instrução v6.1, MCP local, CLI, contratos, documentação e exemplos. A publicação estável não representa certificação de saúde nem garantia de que toda IA obedecerá ao protocolo.

## Correções verificadas

- A instrução completa acompanha o pacote instalado e o recurso MCP, com identidade de bytes verificada fora do clone.
- Resposta vazia no CLI não confirma ausência de restrições; a pessoa deve informar os itens ou escrever `nenhum`.
- País editorial e independência pendentes impedem aprovação. Omissão dos novos estados também mantém a pendência.
- A entrega confere notas de adaptação, além de inventário, componentes, aliases e etapas.
- A origem de publicação é preenchida como URL, e rendimento não documentado deve ser identificado como estimativa.
- As instruções tratam páginas e comentários como dados não confiáveis e preservam os limites de pesquisa.

## Compatibilidade das URLs

`provenance_origin` contém a URL da publicação original, com esquema HTTP ou HTTPS. A descrição curta do schema usa HTTPS; a aceitação efetiva inclui ambos os esquemas e fica explicitada aqui para as integrações desta versão.

A validação verifica formato, hostname IDNA e ausência de credenciais; não consulta DNS nem comprova que o destino é público ou editorialmente estabelecido no país. A revisão semântica deve qualificar a origem antes da pesquisa ser apresentada como completa. O servidor MCP não acessa o endereço.

## Migração da versão experimental

Não acrescente `confirmed` a registros antigos apenas para obter aprovação. Revise as evidências e registre a qualificação real. O histórico inicial foi preservado sem os novos campos e continua rejeitado pelo contrato atual. O exemplo revalidado e os exemplos sintéticos têm finalidades distintas.

A [instalação](INSTALACAO.md) separa configuração Claude Code testada, instrução portátil para clientes web e limite observado do Gemini CLI. Os [clientes ensaiados](CLIENTES_TESTADOS.md) e a [B.9](../evidence/B9_1_0_0.md) delimitam a cobertura.

Confiança: alta nas correções e condições ensaiadas.

Pendências impeditivas da distribuição: zero no escopo técnico avaliado. Interfaces não ensaiadas e estudos com usuários permanecem como limites de cobertura.
