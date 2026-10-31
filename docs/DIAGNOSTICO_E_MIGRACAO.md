---
lang: pt-BR
title: "Diagnóstico e migração da instrução de receitas tradicionais"
subject: "Quatorze achados da v5.1 e critérios de aceitação da sucessora v6.0"
author: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
keywords: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
manager: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
version: "0.1.0"
status: experimental
---

# Diagnóstico e migração

A instrução sucessora v6.0 foi preparada para o Receitas Tradicionais Canônicas, versão 0.1.0 experimental. A migração preserva a intenção de pesquisar tradições culinárias e atribuir fontes, substituindo dependências de provedor, regras contraditórias e garantias que apenas um prompt não consegue executar.

O objetivo é pesquisar exatamente 7 receitas-fontes, de 7 grupos editoriais distintos e estabelecidos no país associado ao prato. A entrega pode ser uma receita redigida com palavras próprias, da variante escolhida, acompanhada de comparação breve e 7 links. Não significa entregar 7 receitas integrais nem fundir variantes. Repositório público: [receitas-tradicionais-canonicas](https://github.com/RodrigoYuMatsumoto/receitas-tradicionais-canonicas).

## Base e método

Foi auditado o texto da instrução v5.1. O original externo foi preservado. Sua identificação de integridade é SHA-256 `FAE612BC1E392F29E3A25269B905F8FED2C9ECEB114139287EE7636A616E312E`. Este relatório não publica caminhos pessoais nem reproduz o acervo privado de origem.

A análise é textual, com referências às linhas dessa versão. Foram levantados 14 candidatos e mantidos 14 achados, sem consolidação ou descarte. Os exemplos de suposta oficialidade presentes no original não foram tratados como fatos. Esta auditoria não pesquisou receitas nem validou externamente instituições, URLs, história ou números de segurança. O ensaio de pesquisa e seus limites pertencem à evidência específica registrada separadamente no repositório.

## Achados e critérios de aceitação

| Nº | Linhas da v5.1 | Achado mantido | Migração e aceitação |
|---|---|---|---|
| 1 | 24, 277 e 311 | Palavras de alergia e intolerância acionam bloqueio, embora a lista de ingredientes deva oferecer alternativas. | Onboarding registra ingredientes evitados sem recusa lexical. Somente a avaliação individual fora do escopo requer encaminhamento. Testar aceitação de perfil com alergia declarada. |
| 2 | 297 | A descrição de zona de perigo contém uma inversão textual nas desigualdades. | Remover a tabela do prompt. Orientação concreta exige fonte oficial aplicável à técnica e local. Não promover números memorizados como regra validada. |
| 3 | 297 e 322 | Regras gerais de tempo, temperatura, conservação e um pacote fixo de altitude são aplicados sem contexto suficiente. | Exigir contexto e evidência aplicável. Ausência de informação crítica vira pendência específica, sem interpolação automática de segurança ou altitude. |
| 4 | 227-229 e 426-435 | Exemplos alegam acesso, oficialidade e convergência; há URLs ilustrativas ou incompletas. | Não transportar as alegações como fatos ou fontes reais. Exemplos de teste devem ser sintéticos e inequivocamente rotulados. |
| 5 | 131 e 133-144 | Institucionalidade, diploma implícito e data visível podem excluir saber doméstico documentado. | Exigir responsabilidade editorial demonstrável no país, sem exigir diploma nem inventar data. Publicação doméstica/regional legítima é elegível. |
| 6 | 36-37, 144-146 e 199 | Hierarquia e maioria podem transformar uma variante em autoridade exclusiva. | Explorar antes de selecionar; registrar divergências e detalhes incomuns. Não resolver diferença cultural material por votação automática. |
| 7 | 87-97 e 199 | A desambiguação inicial pode ser contornada pela escolha automática posterior. | Confirmar nome, país/região e ingredientes distintivos antes da pesquisa. Ambiguidade material bloqueia a navegação até esclarecimento. |
| 8 | 138-140 e 269 | Não há contrato de 7 receitas-fontes; há recomendação de trocar de conversa acima de 6 receitas. | Seleção final exatamente 7, de 7 grupos editoriais distintos. Mais candidatas são permitidas no teto. Menos de 7 implica insuficiência, sem fonte inventada. |
| 9 | 47-49 e 77-79 | Persona com credenciais alegadas e formatos longos dificultam a linguagem inicial simples. | Competências funcionais, sem biografia fictícia; explicação simples por padrão e opção técnica. Não exigir escolha adicional de versão para todo pedido. |
| 10 | 20, 131, 209-215 e 493 | Há contratos de fonte diferentes e ambiguidade entre busca e leitura. | Separar descoberta de acesso e leitura. Esquemas registram metadados, seções lidas e evidências; busca não comprova conteúdo integral. |
| 11 | 60-71, 265, 347 e 410 | Modelo, widget, memória e ferramentas específicos limitam a portabilidade. | Prompt independente de provedor; host fornece pesquisa e delegação; MCP local oferece contratos. Sem subagentes, papéis sequenciais declarados. |
| 12 | 7, 110, 207 e 384 | O texto chama regras de mecânicas ou bloqueantes sem demonstrar execução externa. | Implementar validação determinística, declarar execução real e distinguir aprovação estrutural de revisão semântica. Campos preenchidos não provam veracidade. |
| 13 | 16 e 281 | Substituições e proporções universais podem implicar equivalência culinária não demonstrada. | Adaptar por caso, com rótulo e consequência sustentada. Entrega operacional respeita o perfil; pesquisa histórica não equivale a recomendação de execução. |
| 14 | 243, 349 e 380 | As condições de verificação externa variam e podem ser confundidas com mera separação de papéis. | Informar o que foi revisado e por quem. Revisão da mesma família não conclui B.9; manter pendência para promoção estável. |

Não foi encontrada uma promessa literal de descobrir todos os segredos culinários. Ainda assim, persona extraordinária, canonicidade singular e entrega declarada final podem sugerir completude excessiva. A v6.0 limita a promessa a práticas publicadas e verificáveis. Nenhum prompt ou pesquisa demonstra que nada relevante permaneceu fora da web.

## Arquitetura mínima útil

O [prompt portátil](../prompts/INSTRUCAO_PROJETO.md) conduz onboarding, desambiguação, exploração, comparação e redação. Os [papéis](../agents/PAPEIS.md) separam responsabilidades de coordenação, pesquisa-base, pesquisa doméstica/regional, redação e revisão. Essa separação organiza trabalho, mas não comprova independência.

O host executa busca e delegação. O MCP local oferece `onboarding_questions`, `plan_research`, `validate_research` e `validate_delivery`, com esquemas tipados. Ele não navega, não chama modelos e não é um orquestrador de LLM. A integração deve usar seus esquemas reais.

Os validadores verificam campos declarados, contagens, limites, duplicação e compatibilidade com o perfil. Não provam sozinhos leitura real, país, tradição, independência editorial ou segurança. A documentação e o resultado devem preservar essa diferença.

A pesquisa exige ao menos 2 trajetórias, receita-base e doméstica/regional, antes da seleção. A primeira consulta contém exatamente o nome confirmado do prato (`dish`); o país delimita a elegibilidade editorial, sem ser acrescentado automaticamente à consulta inicial. A pesquisa lê ingredientes, preparo, notas e comentários existentes, registra detalhes incomuns e busca corroboração. Comentários com autoria identificável são pistas, não prova automática. O orçamento global é de 32 consultas, 40 páginas lidas, até 3 pesquisadores e 2 reformulações por trajetória, incluindo coordenação e qualificação editorial. Falhas de acesso são registradas separadamente e não equivalem a páginas lidas.

Os registros usam `research_track` por receita-fonte (`base` ou `domestic_regional`), `completed_tracks` e `pages_read` no lote. Esses campos são declarações verificáveis quanto à estrutura, sem constituir prova autônoma de leitura ou exploração suficiente. O perfil admite equipamentos e região ampla opcional, sem exigir endereço pessoal.

## Verificação da migração

Os testes devem cobrir onboarding sem bloqueio lexical, ausência de persistência implícita, ambiguidade pendente, contagem diferente de 7, grupos duplicados, país sem evidência, orçamento excedido, trajetória ausente, seções inacessíveis mal declaradas, detalhe incomum omitido, adaptação incompatível com o perfil e aprovação não executada. Casos sintéticos não devem ser apresentados como pesquisa culinária real.

Os testes comprovam apenas as condições executadas. Uma palavra ausente do texto não comprova segurança para alergias; um domínio não comprova país; duas URLs não comprovam independência; um campo de leitura não comprova que a página foi realmente lida. A revisão semântica e as evidências consultadas continuam necessárias.

O original v5.1 permanece preservado, sem migração retroativa do acervo privado. Perfis pessoais não entram no repositório público. A publicação da versão experimental é distinta da promoção estável e não representa declaração de B.9 concluído.

Confiança: alta no diagnóstico textual e na correspondência entre os 14 achados e os critérios propostos, pois as contradições e dependências foram localizadas na versão auditada. A eficácia operacional depende do runtime, dos testes executados e da qualidade da pesquisa concreta.

Pendências: verificação externa dos exemplos e dos números de segurança do legado não realizada; comprovação de eficácia por uso real ainda necessária; leitura real, país, tradição e independência editorial exigem revisão de evidência a cada pesquisa; B.9 não concluído e pendente para promoção estável. Este relatório não substitui os resultados de testes e ensaios registrados em seus próprios arquivos.
