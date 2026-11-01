---
lang: pt-BR
title: Histórico de alterações do projeto
subject: Histórico de versões, correções e verificações
author: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
keywords: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
manager: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
version: "2.0.0"
status: versioned
---

# Histórico de alterações

## 2.0.0 - 01/11/2026

Corrigidas as flexões de número na conferência de exclusões, as ações para porções e utensílios não informados, as respostas “nenhum” e “não sei” no onboarding, a distinção entre vinagre e bebida e a exibição de quantidade “a gosto”. O guia de sabor agora limita o estudo de shiitake ao processo de secagem e descreve com precisão a afirmação da FSANZ. Os esquemas e o checklist acompanham os contratos 2.0.0.

**Mudanças incompatíveis adicionais:** `Profile.servings` ausente passa a `None`, sem assumir quatro pessoas; clientes devem perguntar pelas porções e tratar `porcoes_nao_confirmadas` antes de usar a ficha. Utensílios não informados geram `equipamento_nao_confirmado`; confirme a disponibilidade antes de tratar a receita como `practical_ready`. O planejamento da pesquisa continua aceitando essas lacunas.

Os ensaios funcionais preservados abaixo e em `evidence/JORNADA_2_0.json` pertencem à candidata 2.0.0-rc.1; não são ensaios dos bytes 2.0.0. Resultados de testes, hashes e veredito desta versão constam no [parecer B.9](evidence/B9_2_0_0.md). A tag estável só é criada com parecer aprovado.

## 2.0.0-rc.1 candidata - 31/10/2026

Instrução v6.2. O início agora apresenta um checklist alimentar com dez grupos e exemplos, sem preâmbulo técnico. A mesma fonte gera a pergunta do MCP, a instrução portátil e o documento humano. Acrescentados comando de início, guias de pedidos cotidianos, pesquisa atual de uso, sabor e umami, entradas para clientes e saída culinária legível no terminal.

O pedido passa a incluir contexto de tempo, ingredientes, orçamento e compras. A ficha exige medidas, rendimento explicado, utensílios e pontos observáveis. Foram corrigidos equivalência indevida de equipamento, quantidades inválidas, exclusões da CLI, padrões alimentares não operacionalizados e obrigatoriedade de inventar um detalhe especial. O validador também confere a igualdade dos esquemas e documentos gerados.

**Mudança incompatível:** `ok` deixa de bloquear a leitura do plano por conferências humanas pendentes. Clientes precisam interpretar também `practical_ready`, `preparation_ready` e `action_items`. A leitura de registros antigos foi preservada, mas registros sem ficha não recebem prontidão prática. Essa mudança de semântica justifica a versão principal 2.0.

Os ensaios reais encontraram e orientaram correções sobre dúvida de leite, tempo disponível, nomes de canjica e operação de liquidificador com líquido quente. A rodada final passou nos quatro critérios funcionais, mantendo um desvio tipográfico pontual fora da abertura. Resultados, hashes e limites estão na [revisão da jornada](docs/REVISAO_JORNADA_2_0.md). A candidata não herda B.9 nem promoção da versão anterior.

## 1.0.0 estável - 31/10/2026

Instrução v6.1 completa no pacote e no MCP, confirmação explícita de ausência no CLI, qualificação editorial pendente com bloqueio, notas de adaptação inspecionadas, origem descrita como URL e estimativa de rendimento identificada. Contratos, exemplos atuais e documentação foram atualizados; o histórico foi preservado.

Verificação: 52 testes locais, seis chamadas MCP reais após as correções e conversa portátil no Gemini web. A B.9 final foi confirmada com ressalvas por Google e xAI, com oito critérios sustentados pelas duas famílias. Pareceres, normalização de formato e triagem estão nos registros públicos. A [nota de compatibilidade](docs/NOTAS_DA_VERSAO_1_0_0.md) explicita a aceitação de HTTP e HTTPS na origem de publicação e os limites da análise de endereço.

## 0.1.0 experimental - 31/10/2026

Observação empírica: a v5.1 apresentava regras contraditórias de alergia, contagem de fontes e escolha de variante, além de dependências de uma plataforma. A pesquisa inicial de feijoada não encontrou o detalhe procurado. A exploração regional posterior encontrou seu uso culinário sem incluí-lo nas consultas e identificou uma republicação que não deveria contar como fonte independente.

Ajuste aplicado: instrução v6.0, onboarding inicial, desambiguação por ingredientes, sete receitas-fontes de grupos distintos do país, duas trajetórias de pesquisa, preservação de detalhes minoritários e contratos MCP locais. Foram acrescentados CLI, instalação isolada, testes de regressão, fontes de exemplo, metadados e manifest. A pesquisa histórica não foi promovida a aprovação integral: contadores não medidos permanecem desconhecidos e bloqueiam o gate correspondente.

Falsificação futura: em novos pratos com alvos ocultos, verificar se a trajetória doméstica/regional encontra detalhes verificáveis que a seleção inicial não encontra. Medir fontes rejeitadas, custo, retries, divergências e problemas de compreensão. Se apenas aumentar ruído ou não preservar detalhes minoritários, revisar o método e os critérios antes de promover uma versão estável. Um alvo não encontrado não autoriza inventá-lo.

Confiança: alta no registro das alterações e observações documentadas.

Pendências: avaliações externas e de uso descritas em [verificação](docs/VERIFICACAO.md).
