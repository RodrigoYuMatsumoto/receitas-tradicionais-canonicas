---
lang: pt-BR
title: Clientes de IA ensaiados
subject: Execuções reais, compatibilidade e problemas encontrados
author: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
keywords: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
manager: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
version: "2.0.0"
status: versioned
---

# Clientes de IA ensaiados

Os ensaios funcionais da candidata 2.0.0-rc.1 constam na [revisão da jornada](REVISAO_JORNADA_2_0.md) e no [registro de evidências](../evidence/JORNADA_2_0.json). Esses ensaios não cobrem os bytes distribuídos da 2.0.0. A seção abaixo preserva os ensaios históricos da 1.0.0; suas aprovações não são transferidas. Resultados de testes, hashes e veredito da 2.0.0 constam no [parecer B.9](../evidence/B9_2_0_0.md). A tag estável só é criada com parecer aprovado.

Os ensaios de 31/10/2026 usam perfis fictícios, configurações temporárias fora do clone e instrução integral. Não são estudo de usabilidade com pessoas nem revisão B.9. Nenhuma configuração global ou credencial foi alterada.

| Cliente e modo | Resultado observado | Limite |
|---|---|---|
| Claude Code 2.1.304, modelo claude-sonnet-5-5, MCP local | Conexão confirmada, cinco chamadas reais com argumentos idênticos às fixtures e respostas esperadas | Lote conhecido e perfis fictícios; sem nova descoberta nesse caso |
| Claude Code, conversa com nome ambíguo | Apresentou canjica de milho verde e de milho branco com regiões e ingredientes, pediu escolha, não iniciou pesquisa | Opções foram hipóteses, não descobertas verificadas |
| Gemini web, modo Pro mostrado na interface, instrução anexa | Perguntou por ingredientes a evitar; após perfil fictício, distinguiu duas canjicas e pediu escolha antes de pesquisar | Sem conexão MCP local; o identificador exato do modelo não é exposto pelo seletor Pro |
| Gemini CLI 0.61.0 | Provedor recusou a conta antes de qualquer chamada MCP ou evento de modelo | IneligibleTierError / UNSUPPORTED_CLIENT; não homologado neste ambiente |

## Chamadas reais no Claude Code

O cliente chamou `onboarding_questions`, `plan_research`, `validate_research` com sete fontes, `validate_research` com seis fontes e `validate_delivery` com um ingrediente explicitamente excluído. As duas primeiras validações de pesquisa retornaram, respectivamente, aprovação documental e rejeição por contagem. A entrega incompatível foi rejeitada no inventário e nas etapas. As respostas mantiveram `semantic_review_required: true`.

O segundo cenário usou apenas “Quero fazer canjica”. A resposta apresentou nomes, regiões e ingredientes básicos e pediu decisão. Não forneceu receita operacional. O custo informado das duas sessões foi US$ 0,3699895.

## Pesquisa nova de ponta a ponta

Em sessão separada, o Claude Code pesquisou “Pão de queijo mineiro tradicional”: sete consultas, 24 URLs de leitura distintas, 16 acessos com conteúdo e oito falhas registradas. Papéis foram sequenciais no mesmo modelo. A execução durou 317,97 segundos, com 38 turnos e custo informado de US$ 0,9929396.

O cliente emitiu dois argumentos JSON não analisáveis, rejeitados antes do servidor. Em seguida, o servidor rejeitou `provenance_origin` preenchido com prosa; a IA corrigiu para URLs e obteve aprovação documental. A entrega foi rejeitada por revisão humana de rótulos ainda não realizada.

A execução não demonstrou sete fontes plenamente qualificadas. A própria IA reconheceu evidência editorial apoiada apenas em resumo de busca e independência não verificada de uma republicação, mas concluiu que faltava somente conferir rótulos. Também apresentou porções sem rendimento informado pela fonte. Essas conclusões não foram adotadas pelo coordenador.

O contrato foi corrigido: qualificações pendentes têm estados estruturados e impedem aprovação; origem é descrita como URL no schema; porções sem rendimento documentado recebem identificação de estimativa. A revisão não transformou páginas bloqueadas em lidas nem completou evidência por inferência.

## Reprodução e privacidade

A configuração testada do Claude Code está em [instalação](INSTALACAO.md). O MCP foi instalado em ambiente virtual e chamado fora do clone. A instrução integral foi fornecida ao sistema da sessão; o servidor também a oferece na inicialização e no recurso `receitas://project/instructions`.

Os registros brutos de clientes ficam locais porque incluem detalhes operacionais da máquina e da conta. O resumo público registra versões, contagens, hashes e resultados em [evidências dos clientes](../evidence/CLIENTES_1_0_0.json). A sessão web foi preservada por leitura do DOM; os detalhes das citações ao anexo não foram confundidos com pesquisa na internet.

Os ensaios de conversa ocorreram antes da explicitação final dos estados de qualificação. A regressão do contrato corrigido e os hashes das instruções usadas ficam separados no registro; não se alega que um resultado antigo cobriu bytes posteriores.

Confiança: alta nos comportamentos registrados; limitada à experiência dos clientes e cenários descritos.

Pendências: interfaces e versões não ensaiadas; compreensão e acessibilidade com usuários reais. São limites de cobertura, não homologação de todos os clientes.
