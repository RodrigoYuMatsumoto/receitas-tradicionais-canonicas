---
lang: pt-BR
title: Verificação e limites da versão inicial
subject: Evidências de pesquisa, testes de software e compatibilidade
author: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
keywords: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
manager: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
---

# Verificação e limites da versão inicial

A versão 0.1.0 reúne instrução portátil v6.0, papéis de pesquisa, código Python, servidor MCP local, testes e um ensaio documentado. Sua publicação é experimental. Aprovação estrutural não equivale a comprovação factual, segurança alimentar ou promoção estável.

## Evidência por requisito

| Requisito | Evidência disponível | Limite |
|---|---|---|
| Preservar a instrução original | Hash da v5.1 no diagnóstico; sucessora gravada em novo caminho | O original privado não é publicado. |
| Configurar preferências no primeiro uso | Prompt, ferramenta de perguntas e comando `onboarding` | A IA hospedeira deve iniciar a conversa e respeitar a escolha sobre persistência. |
| Não presumir prato ambíguo | Pergunta com nomes, regiões e ingredientes no prompt; gate de pedido pendente | O programa não conhece todas as homonímias e depende da identificação semântica do host. |
| Pesquisar sete receitas | Gate rejeita 6 ou 8 e exige sete IDs, grupos e origens distintos | Metadados falsos não se tornam verdadeiros por passarem no schema. |
| Usar sites do país | País e prova editorial obrigatórios; sete fontes reais identificadas no exemplo | Não é geolocalização automática nem verificação societária exaustiva. |
| Procurar saber doméstico | Duas trajetórias e ao menos uma fonte doméstica obrigatórias | O conteúdo da pesquisa exige leitura e revisão semântica. |
| Descobrir detalhes sem inseri-los nas buscas | Pesquisa separada, log de consultas e achado regional no ensaio | Um único prato, com direção regional explícita na segunda rodada; não prova cobertura universal. |
| Múltiplos agentes | Papéis, handoffs e pesquisa independente executada durante a construção | O servidor não fornece modelos; um host sem delegação executa etapas sequenciais e declara isso. |
| Impedir incompatibilidade alimentar explícita | Verificação de inventário, componentes, aliases e texto das etapas | Não detecta todos os ingredientes ocultos, sinônimos ou contato cruzado. |
| Conectar por MCP ou outro meio | Instrução copiável; pacote instalável; testes com cliente oficial por `stdio` | Sem endpoint remoto hospedado e sem instalação automática em aplicativos. |
| Copiar e adaptar com crédito | MIT para código, CC BY 4.0 para textos e aviso de origem | Materiais de terceiros mantêm seus direitos. |
| Pesquisa com limites | Tetos de 32 consultas, 40 páginas e três pesquisadores; contadores de reformulações | O host declara a execução. Contador desconhecido bloqueia a aprovação. |

## O que os testes exercitam

A suíte cobre contagem de fontes, URLs normalizadas, grupos editoriais, origem de republicação, país, datas, leitura de seções, trajetórias, teto de chamadas, contadores desconhecidos, onboarding, ambiguidade, restrições nas etapas e inventário, entrada inválida, limite de tamanho e saída JSON em UTF-8.

Os testes MCP iniciam o servidor como processo local e executam negociação, `initialize`, listagem de ferramentas, chamadas e leitura dos recursos de instruções e schemas. São chamadas reais ao servidor, com fontes inventadas e sem navegação externa. O teste do pacote fora do repositório verifica a instalação, não a experiência de uma interface comercial.

Uma revisão em contexto separado encontrou dois bypasses antes da publicação: marcação omitida de ingrediente proibido e ingrediente restrito escrito apenas em uma etapa. As correções acrescentam inspeção textual conservadora. Uma frase que mencione um ingrediente para negá-lo também pode ser rejeitada; nesse caso, reescreva a etapa com a alternativa permitida.

Os 42 testes locais passaram, sem falhas, erros ou testes ignorados, em Windows com Python 3.14.3, MCP 2.3.0 e Pydantic 2.14.2, incluindo as regressões de URLs IDNA inválidas. Também foram executados fora do repositório os comandos de plano, pesquisa sintética, entrega sintética e pesquisa histórica com rejeição esperada. O resultado está em [TESTES.json](../evidence/TESTES.json) e a [rechecagem independente](../evidence/REVISAO_INDEPENDENTE.md) documenta os controles corrigidos. A matriz de CI cobre Windows e Linux, Python 3.11 e 3.14; só o estado efetivo dos jobs permite afirmar aprovação em cada combinação. O workflow não publica pacotes nem faz deploy.

## Pesquisa real e dados sintéticos

O registro real tem sete receitas e identifica a presença culinária do ingrediente-alvo em uma variante. Seus contadores de reformulações após fracasso não foram medidos. Por isso a CLI retorna rejeição documental específica nesse registro, preservando o resultado e a lacuna, sem inventar zero. O [ensaio](../evidence/ENSAIO_FEIJOADA.md) explica esse limite.

Uma rodada posterior revalidou as sete fontes em dois contextos de pesquisa: uma consulta neutra, 12 URLs distintas abertas sem falha e nenhum retry. O [registro dessa rodada](../evidence/REVALIDACAO_DOCUMENTAL.json) e o [lote real aprovado](../examples/feijoada_revalidada.json) demonstram a passagem pelo contrato corrigido, também chamado pelo cliente MCP real com o servidor instalado e executado fora do repositório. Os endereços eram conhecidos; essa rodada não demonstra nova descoberta cega nem apaga a lacuna histórica. Os inventários resumidos do registro anterior foram complementados na nova rodada.

O exemplo sintético tem contadores conhecidos e deve passar nos controles estruturais. Ele não comprova a existência de fonte, tradição, país ou segurança. Os três exemplos têm funções diferentes e não devem ser apresentados como equivalentes.

## Fontes técnicas consultadas

Em 31/10/2026 foram conferidos o [SDK oficial MCP](https://github.com/modelcontextprotocol/python-sdk), a [documentação de execução](https://py.sdk.modelcontextprotocol.io/run/), a [versão no PyPI](https://pypi.org/project/mcp/2.3.0/), o [checkout do GitHub Actions](https://github.com/actions/checkout) e o [setup-python](https://github.com/actions/setup-python). As Actions foram fixadas por SHA dos respectivos rótulos v7 consultados. O pacote fixa MCP 2.3.0 e Pydantic 2.14.2, versões efetivamente instaladas no ensaio técnico.

A revisão removeu tabelas universais de segurança e altitude do prompt original. Não as substituiu por números memorizados. Uma orientação concreta de risco exige fonte oficial aplicável à técnica e ao local de preparo.

## Próximas avaliações

Antes de promover uma versão estável, submeter o conjunto congelado por hash a uma família de modelos distinta da do gerador, resolver objeções e ensaiar a experiência em clientes finais. Repetir o estudo culinário com outros pratos e medir retries desde o início. Não houve diagnóstico nem prescrição nutricional neste trabalho.

Os perfis dos exemplos são fictícios. Não foram instaladas rotinas recorrentes, salvos perfis pessoais ou alteradas configurações globais de IA. Markdown registra propriedades no frontmatter; código e JSON usam [registro auxiliar de metadados](../ARTIFACT_METADATA.json), pois esses formatos não possuem campos documentais nativos universais. No pacote Python, gerente e idioma ficam em campos personalizados.

Confiança: alta nas condições cobertas pelos testes efetivamente aprovados; média na portabilidade de ponta a ponta, que depende das ferramentas e do comportamento do host.

Pendências: B.9 por outra família antes da promoção estável; ensaios em clientes finais e com usuários; ampliação da avaliação culinária para outros pratos. As lacunas específicas do ensaio histórico permanecem em seu registro.
