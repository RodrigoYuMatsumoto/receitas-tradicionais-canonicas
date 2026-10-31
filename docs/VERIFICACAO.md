---
lang: pt-BR
title: Verificação da distribuição 1.0.0
subject: Escopo da estabilidade, evidências técnicas e revisão independente
author: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
keywords: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
manager: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
---

# Verificação da distribuição 1.0.0

A distribuição reúne instrução portátil v6.1, papéis de pesquisa, CLI e servidor MCP local. A estabilidade publicada é identificada pela release correspondente no GitHub. Os rótulos de versão não certificam leitura de páginas, identidade editorial, tradição ou segurança alimentar.

## Contratos e evidências

O lote exige exatamente sete fontes de grupos e origens distintos, país do pedido, ingredientes e preparo lidos, duas trajetórias e pelo menos uma prática doméstica. Qualificação de país e independência têm estados explícitos: `pending` impede aprovação. Campos omitidos não recebem confirmação automática. Mesmo `confirmed` é uma declaração do revisor, que deve confrontar a prova com o conteúdo lido.

A entrega incorpora o lote e seu único perfil. Inventário, componentes, aliases, etapas e notas de adaptação são comparados com as restrições explícitas. Aprovação não certifica ingredientes ocultos, contato cruzado ou segurança individual. Revisão de rótulos e, quando aplicável, contato cruzado dependem da pessoa responsável.

A primeira consulta é exatamente o nome confirmado do prato. O host executa busca e papéis com teto global de 32 consultas, 40 páginas lidas, três pesquisadores e duas reformulações por trajetória. O servidor confere declarações e não mede nem executa a navegação do host.

## Portabilidade e regressões

A instrução completa é dado do pacote e precisa ser idêntica ao prompt canônico. Testes leem o recurso instalado fora do clone, sem `PYTHONPATH`, e verificam a instrução na inicialização MCP. O contrato é exercitado por negociação, listagem das quatro ferramentas, chamadas e leitura de recursos.

A suíte cobre contagem, países, qualificação pendente, URLs, grupos, origem de republicação, datas, leitura de seções, limites, ambiguidade, onboarding, inventário, etapas e notas incompatíveis, JSON malformado e erros sem eco de dados privados. Os resultados finais desta distribuição constam em [testes 1.0.0](../evidence/TESTES_1_0_0.json); o registro experimental de 42 testes permanece histórico.

Os [clientes ensaiados](CLIENTES_TESTADOS.md) separam chamadas funcionais, comportamento da conversa e pesquisa real. A aprovação documental de uma IA não foi tratada como sucesso semântico quando suas próprias notas reconheciam prova insuficiente.

## Estudo culinário inicial

O [ensaio de feijoada](../evidence/ENSAIO_FEIJOADA.md) preserva a sequência original: primeira exploração sem o detalhe procurado; descoberta posterior na ampliação regional, sem incluir o ingrediente-alvo nas consultas. Presença culinária não confirma infusão, remoção de gordura ou efeito digestivo.

O [lote revalidado](../examples/feijoada_revalidada.json) reúne sete fontes já qualificadas e contadores medidos; seus estados explícitos registram a revisão documental anterior. Reutiliza URLs conhecidas e não é outra descoberta cega. O [registro histórico](../examples/feijoada_pesquisa.json) não foi reescrito: além dos retries não medidos, não contém os novos estados de qualificação. Deve ser rejeitado pelo contrato atual, sem retropreencher confirmações.

## Revisão B.9 e publicação

A B.9 avalia um conjunto funcional congelado, com critérios fixados antes das respostas, gerador identificado como OpenAI e verificadores de outras famílias pelo navegador. Relatórios, objeções e triagem ficam em [revisão B.9](../evidence/B9_1_0_0.md). A revisão cobre os arquivos e hashes indicados, não alterações futuras ou todos os dados factuais da internet.

A publicação estável depende do resultado conclusivo da rodada final, da resolução das objeções materiais, das regressões e da CI sobre a alteração integrada. Um parecer do próprio gerador ou teste técnico não substitui esse requisito. Não há promoção por simples troca de número de versão.

## Fontes técnicas e limites

Foram consultados o [SDK oficial MCP](https://github.com/modelcontextprotocol/python-sdk), sua [documentação](https://py.sdk.modelcontextprotocol.io/), o [CLI oficial Claude Code](https://code.claude.com/docs/en/cli-reference) e a [documentação MCP do Gemini CLI](https://geminicli.com/docs/tools/mcp-server/). A configuração foi confrontada com as versões locais efetivamente executadas.

Markdown registra idioma, título, assunto, autor, palavras-chave e gerente no frontmatter. Código e JSON usam [registro auxiliar](../ARTIFACT_METADATA.json), pois não possuem propriedades documentais nativas universais. Não há serviço remoto hospedado, persistência automática de perfis ou instalação global.

Confiança: alta nos contratos e execuções cobertos pelas evidências; média na generalização do método culinário, avaliado em poucos cenários.

Pendências de cobertura: pesquisa comparativa com outros pratos, interfaces não ensaiadas e estudos com usuários. Não se promete descoberta universal de saber não publicado.
