---
lang: pt-BR
title: "Verificação da versão 2.0.0"
subject: "Método de verificação e escopo das evidências da versão 2.0.0"
author: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
keywords: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
manager: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
version: "2.0.0"
status: versioned
---

# Verificação da versão 2.0.0

Os bytes 2.0.0 contêm a instrução v6.2, checklist inicial, contexto de cozinha e ficha operacional. A versão confere flexões regulares no bloqueio de ingredientes, pede confirmação de porções e utensílios ausentes, distingue vinagre de bebida e apresenta “a gosto” de forma coerente. A [revisão da jornada](REVISAO_JORNADA_2_0.md) preserva os achados e ensaios da candidata. A versão anterior está na tag v1.0.0; seu [relatório original de verificação](VERIFICACAO_1_0_0.md) tem escopo próprio.

O [registro da candidata](../evidence/JORNADA_2_0.json) separa testes locais, integração MCP e ensaios reais de conversa da 2.0.0-rc.1. Esses resultados não são testes dos bytes distribuídos. Resultados de testes, hashes e veredito da versão 2.0.0 constam no [parecer B.9](../evidence/B9_2_0_0.md). A CI avalia o commit indicado no próprio GitHub; teste local não é CI remota.

## Três resultados diferentes

- `ok` verifica os dados documentais e as correspondências de exclusões declaradas.
- `practical_ready` também exige ficha operacional completa e consistente com as condições registradas.
- `preparation_ready` considera as ações humanas aplicáveis antes de começar, sem certificar segurança individual.

Uma referência genérica que pode abranger uma exclusão específica pede identificação antes do preparo. O [suplemento de ingredientes genéricos](../evidence/RESTRICAO_GENERICA_2_0.md) descreve o caso reproduzido, a regra e seus limites. A aprovação dos bytes anteriores não cobre automaticamente essa correção: confira o escopo e os hashes do parecer independente correspondente antes da promoção.

A mudança de tratamento dos rótulos exige migração dos consumidores da 1.0.0. Registros antigos continuam legíveis; sua ausência de ficha não é preenchida nem promovida a prontidão prática.

O servidor não abre páginas, não chama modelos, não salva perfis nem executa a pesquisa. Estado confirmado de país e independência é declaração auditável do revisor, não prova obtida automaticamente pelo MCP. Leitura real, procedência, tradição, preço, rendimento e resultado culinário continuam exigindo evidência semântica.

## Integridade e portabilidade

O validador compara a instrução canônica, a cópia empacotada e o pacote instalado; os schemas são comparados aos modelos; o checklist humano e o portátil precisam corresponder à fonte determinística. O sincronizador preserva backups antes de escrever. Metadados, referências locais, conjunto público e hashes são conferidos em todos os arquivos distribuídos.

Os testes instalados incluem carregamento fora do clone, sem depender de `PYTHONPATH`, e comunicação MCP real por stdio. As quatro ferramentas permanecem locais e somente de leitura em relação ao ambiente externo. As anotações de ferramenta são informações ao cliente; o comportamento de menor acesso está na implementação, sem rede ou comandos nas tools.

`receitas iniciar` apresenta o checklist e `receitas mostrar` apresenta a ficha em texto humano, após validação. A apresentação determinística corrige pontuação no texto humano e conserva URLs; não altera o JSON recebido. Respostas livres da IA hospedeira ainda podem ter desvio tipográfico, como registrado no ensaio final.

## Revisão independente e estado da versão

O [parecer B.9 da versão 2.0.0](../evidence/B9_2_0_0.md) é a fonte para o veredito, os resultados e os hashes dos bytes distribuídos. A revisão da 1.0.0 tem escopo próprio e não é transferível. Ensaios funcionais no Claude Code registrados em `evidence/JORNADA_2_0.json` pertencem à candidata anterior.

A promoção estrita exige identidade e linhagem suficientes no envelope nativo. Se essa prova faltar, o estado permanece `INDEPENDENCE_UNPROVEN`. Não se deduz o modelo efetivamente servido de um seletor de interface, nem a família apenas do fornecedor. A tag estável só é criada com parecer aprovado.

## Fontes e limitações de cobertura

A [pesquisa de uso](PESQUISA_DE_USO_2026.md) distingue tendências brasileiras, estudos empíricos, relatos e exemplos de fornecedores. O [guia de sabor](SABOR_E_UMAMI.md) distingue umami, aroma, frescor, textura e equilíbrio, sem transformar presença de ingrediente em promessa de saúde. Ciência internacional não completa a contagem das sete receitas nacionais.

Foram consultadas as documentações oficiais de [MCP](https://github.com/modelcontextprotocol/python-sdk), [Claude Code](https://code.claude.com/docs/en/cli-reference), [arquivos de contexto Claude](https://code.claude.com/docs/en/memory) e [GEMINI.md](https://geminicli.com/docs/cli/gemini-md/). Os adapters são candidatos; não se presume homologação universal ou carregamento em todos os clientes.

Markdown contém idioma, título, assunto, autor, palavras-chave e gerente em frontmatter. Código, JSON, YAML, TOML e manifest usam [registro auxiliar por caminho](../ARTIFACT_METADATA.json), pois não possuem campos documentais nativos universais. O pacote usa autor e palavras-chave nativos, com gerente e idioma na tabela personalizada do projeto.

Confiança: alta nos cenários executados e na integridade conferida; média na generalização da experiência culinária e entre clientes.

Pendências: estudos com usuários, testes de cozinha e clientes ainda não ensaiados. O desvio tipográfico pontual nas respostas livres permanece declarado. Consulte o [parecer B.9](../evidence/B9_2_0_0.md) para pendências específicas da revisão dos bytes distribuídos.
