---
lang: pt-BR
title: Revisão independente do contexto de implementação
subject: Falhas reproduzidas, correções e limites da revisão técnica
author: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
keywords: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
manager: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
---

# Revisão da integração

Em 31/10/2026, um agente que não implementou o runtime revisou os contratos, a CLI, os testes e a documentação. A revisão ocorreu em contexto separado, na mesma família OpenAI. Ela não conclui B.9.

| Achado reproduzido | Correção | Rechecagem |
|---|---|---|
| Omissão de uma marcação permitia que um ingrediente de categoria proibida passasse na entrega. | Detecção conservadora de nomes conhecidos no inventário, componentes, aliases e etapas. | Casos conhecidos bloqueados no pacote instalado. |
| Um alérgeno podia aparecer só nas etapas, sem constar do inventário conferido. | Correspondência das restrições também no texto das etapas. | Caso com amendoim apenas na etapa foi bloqueado diante da alergia fictícia. |
| A documentação pedia leitura por seção e orçamento que ainda não tinham campos correspondentes. | Campos de seções, pesquisadores e reformulações, com bloqueio para contagem desconhecida. | Campos e rejeições por limites foram conferidos. |
| A entrada histórica não tinha contagem de retries após busca sem fonte elegível. | Valores desconhecidos preservados como `null`, com rejeição específica. | O registro real retorna `reformulacoes_nao_medidas`. |
| A revisão automática do PR encontrou hostname IDNA inválido que provocava exceção fora do relatório JSON. | Validação de codificação do hostname antes da normalização da URL, convertendo falha em erro de entrada. | Regressões para URL da receita, origem e prova editorial, nos dois comandos de validação. |

A revisão confirmou que `validate_delivery` revalida o lote incorporado e deriva dele o perfil. Não há segundo pedido operacional que permita trocar silenciosamente de prato ou perfil após validar a pesquisa.

A rechecagem usou o pacote instalado em `site-packages`, executado fora do repositório. O controle sintético válido permaneceu aprovado. Não houve reinstalação, edição de arquivos ou repetição da suíte completa pelo revisor. Os resultados da suíte coordenada estão em [TESTES.json](TESTES.json).

Depois dessa rechecagem, a revisão automática do [PR de publicação](https://github.com/RodrigoYuMatsumoto/receitas-tradicionais-canonicas/pull/1) identificou a falha IDNA adicional, reproduzida pelo coordenador e corrigida com testes. A aprovação anterior não foi tratada como prova de ausência de todos os defeitos. As restrições semânticas, a verificação de fontes reais, a segurança dos alimentos e as interfaces finais continuam com os limites descritos em [verificação](../docs/VERIFICACAO.md).

Confiança: alta nos controles rechecados, pois os cenários foram reproduzidos antes e depois das correções.

Pendências: B.9 por outra família e avaliações de uso fora do escopo desta revisão.
