---
lang: pt-BR
title: "Como os pedidos culinários orientam a experiência do projeto"
subject: "Fontes primárias sobre buscas, conversação culinária e decisões de interface"
author: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
keywords: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
manager: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
version: "2.0.0"
status: versioned
verified_at: "2026-10-31"
---

# Pedidos reais e exemplos atuais de uso culinário

A revisão encontrou três tipos diferentes de evidência: tendências de buscas, estudos empíricos e exemplos ou relatos publicados por fornecedores. Eles ajudam a desenhar a experiência, mas não demonstram que todos os públicos fazem os mesmos pedidos.

## O que foi consultado

| Fonte primária | Data | Evidência observada | Limite da conclusão |
|---|---|---|---|
| [Google Brasil: Buscas do Ano 2025](https://blog.google/intl/pt-br/produtos/as-buscas-do-ano-o-que-os-brasileiros-mais-pesquisaram-no-google-em-2025/) | 04/12/2025 | A lista de receitas inclui seis entradas com air fryer: batata frita, pudim, batata-doce, bolo, pastel e peixe. | Tendências não medem a participação de cada intenção em todas as buscas nem representam uma pesquisa de preferências. |
| [Google: tarefas domésticas com Gemini](https://blog.google/innovation-and-ai/products/gemini-app/household-chores-tips/) | 15/09/2026 | Demonstra planejamento por restrições e preferências, compras e aproveitamento de ingredientes mostrados pela câmera. | Os exemplos culinários são demonstrações do fornecedor. Dados gerais de uso doméstico citados no artigo não quantificam cada formato de pedido de receita. |
| [OpenAI Academy: experiência de Ram Pillai](https://academy.openai.com/public/blogs/ram-pillai-chatgpt-cooking-family) | 05/08/2026 | Relato de uso doméstico para lidar com ingrediente ausente, molho que não fica bom e ingredientes disponíveis. | Um relato individual publicado pelo fornecedor não permite estimar prevalência ou eficácia. |
| [ChatGPT: receitas e cozinha](https://chatgpt.com/use-cases/recipes-cooking/) | Sem data editorial; consulta em 31/10/2026 | Exemplos de pedidos por despensa, sobras, tempo, orçamento, substituição, porções, preparo antecipado e correção de sabor. | Exemplos promocionais de interação, sem frequência de uso ou avaliação independente. |
| [Google Search: planejamento de jantar](https://blog.google/products-and-platforms/products/search/dinner-party-hosting-tips/) | 28/07/2026 | Relata buscas sobre tarefas de servir, como manter uma massa aquecida para o jantar. | Não apresenta metodologia suficiente para extrapolar o exemplo para toda a população. |
| [Frummet e colaboradores: Cooking with conversation](https://eprints.gla.ac.uk/326038/) | Publicação em 29/04/2024 | Questionário com 200 participantes e estudo de acompanhamento com 48. Encontrou expectativa por instruções sobre etapas e processos; a assistência ativa aumentou a interação e as perguntas de conhecimento culinário. | Estudo de assistentes conversacionais em condições próprias; não representa todos os usuários de LLMs nem valida este checklist. |

As páginas foram consultadas em 31/10/2026. Para o estudo acadêmico, foram conferidos o registro e o resumo disponibilizados pelo repositório da Universidade de Glasgow; não se declara leitura integral do artigo.

## Decisões de produto derivadas da pesquisa

As decisões abaixo são interpretações de projeto. Ainda precisam ser avaliadas em uso humano:

1. **Aceitar a necessidade antes de exigir o nome do prato.** A pessoa pode começar por ingredientes disponíveis, tempo, gasto ou utensílio. A IA oferece poucas opções viáveis e confirma a escolha antes da pesquisa completa.
2. **Dar exemplos no checklist.** Mostrar grupos de alimentos reduz o trabalho de lembrar de cabeça. “Nenhum”, “não sei” e resposta livre devem continuar disponíveis. Um item marcado não determina uma condição médica.
3. **Separar perfil e pedido do dia.** Uma exclusão confirmada pode acompanhar a conversa; o tempo disponível, os ingredientes e o orçamento daquele preparo podem mudar.
4. **Aproveitar informação já dada.** “Para quatro pessoas, em meia hora, só na panela” deve preencher essas condições, sem obrigar a responder novamente.
5. **Entregar instruções executáveis.** Quantidades, rendimento explicado, tempos, utensílios e sinais de ponto ajudam a preparar e servir. As referências continuam acessíveis em um bloco compacto.
6. **Continuar ajudando durante o preparo.** Substituições e correções do mesmo prato não devem reiniciar o cadastro. A pessoa pode pedir uma etapa de cada vez.
7. **Usar foto e voz somente quando disponíveis.** A IA confirma ingredientes reconhecidos e lacunas; imagem não comprova composição, frescor ou segurança.

Os dois relatos fornecidos pelo operador nesta revisão mostram uma falha concreta da versão anterior: a conversa começava por versão, ferramentas e validação, terminando em pergunta genérica sem exemplos. Esse material orienta a correção do início da conversa; não foi tratado como pesquisa representativa de usuários.

## Como avaliar se a mudança ajuda

Um teste de uso pode pedir que pessoas realizem tarefas como escolher uma receita com o que possuem, declarar uma exclusão, resolver um nome ambíguo e acompanhar três etapas do preparo. Devem ser observados:

- se entendem como responder ao checklist sem ajuda;
- se conseguem informar um item ausente da lista;
- se “não sei” permanece uma lacuna, sem virar ausência de restrição;
- se a IA aproveita dados anteriores e evita perguntas repetidas;
- se a receita permite identificar o que usar, quanto usar e qual é a próxima ação;
- se as conferências humanas pendentes aparecem como ações claras.

Este documento especifica essa avaliação; não registra teste humano executado, taxa de adoção, satisfação ou redução de erros. Também não foi localizado um levantamento representativo atual que quantifique todos esses formatos de pedido entre brasileiros. A pesquisa disponível sustenta exemplos e hipóteses de interface, com esses limites.

Para usar o projeto, consulte [como pedir e cozinhar](COMO_PEDIR.md). Para a distinção entre umami e outros efeitos sensoriais, consulte [sabor e umami](SABOR_E_UMAMI.md).
