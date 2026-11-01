---
lang: pt-BR
title: "Revisão prática da jornada de receitas, versão 2.0"
subject: "Entrada, pesquisa, saída humana, correções e limites da candidata"
author: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
keywords: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
manager: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
version: "2.0.0-rc.1"
status: candidate
---

# A conversa começa pela comida

A candidata substitui a pergunta vaga e o relatório de instalação por um checklist com dez grupos e exemplos. Depois aproveita os dados já informados sobre pessoas, tempo, ingredientes, compras e utensílios. A receita passa a ter uma ficha operacional, acompanhada por sinais de ponto e pelas sete fontes. [Copie o comando de início](../prompts/COMECE_AQUI.md) ou consulte [o checklist completo](CHECKLIST_INICIAL.md).

O núcleo da pesquisa permanece: exatamente sete receitas-fontes de sete grupos editoriais distintos, estabelecidos no país do prato, com leitura e procedência declaradas; duas trajetórias, de referência e doméstica/regional; primeira consulta somente pelo nome confirmado do prato. A procura pelo detalhe culinário não começa por um ingrediente secreto conhecido de antemão.

## O que foi examinado

A base foi a distribuição 1.0.0, commit `4f7b39cb7fffa6fb245384e4a145c8466d3977d9`. Seus 55 arquivos rastreados foram enumerados e preservados em backup local com a identificação Git. A revisão semântica abrangeu os módulos do runtime, testes, instrução, papéis, esquemas, exemplos e documentos de uso; os registros históricos permaneceram preservados. A verificação final percorre todos os arquivos públicos para conferir integridade, referências e metadados. Isso não equivale a refazer cada pesquisa histórica ou comprovar novamente toda fonte externa.

Foram aplicadas as especializações de ecossistema, agente, instrução, prompt, MCP, multiagente, pipeline e arquitetura humano-IA. O repositório não contém uma skill própria instalável a ser descoberta; não foi criada uma cópia adicional da instrução apenas para preencher esse formato. As entradas portáteis, os arquivos de contexto e o MCP atendem aos meios de uso existentes.

## Achados e correções

Contagem: **16 candidatos; 14 achados mantidos e corrigidos; 2 rebaixados a ampliação de escopo ou limitação; zero descartados**. As etapas abaixo distinguem problemas da base e problemas encontrados durante a construção da candidata.

| Achado | Origem observável | Correção e verificação |
|---|---|---|
| 1. Abertura técnica e pergunta que depende da memória do usuário. | Respostas reais fornecidas pelo operador; instrução, comando e `onboarding_questions`. | Checklist com exemplos na primeira resposta; reprodução da mesma fonte no MCP, terminal e instrução portátil. |
| 2. Despensa, tempo, compras e orçamento não tinham contrato. | `Profile` e `Request` da 1.0.0. | `Request.kitchen`; condições do preparo separadas de preferências duráveis. |
| 3. Uma entrega sem quantidades ou sinais de ponto podia ser aprovada. | `Delivery` da 1.0.0 e fixture mínima. | `recipe_card`, rendimento explicado, tempos, utensílios, quantidades e pontos observáveis. |
| 4. Toda receita exigia atestado de rótulos antes de ser mostrada. | `validate_delivery`, `labels_reviewed`. | Separação entre plano consultável e conferências necessárias antes de preparar. |
| 5. Endereços locais passavam como URLs públicas. | `validate_http_url`; casos locais reproduzidos sem rede. | Recusa sintática de endereços locais e IPs literais não globais; limite de DNS explicitado. |
| 6. O schema distribuído podia divergir dos modelos. | `validate_repository.py`. | Comparação com `model_json_schema`, instrução instalada e checklist gerado. |
| 7. Panela genérica era aceita como panela de pressão. | Revisão do novo `validate_delivery`. | Equivalência conservadora de equipamento; o tipo e a capacidade não são presumidos. |
| 8. Quantidades como uma palavra sem medida ou divisão por zero passavam. | Revisão do novo cartão operacional. | Gramática de quantidades positivas e ajustes qualitativos com instrução observável. |
| 9. Rejeições informadas na CLI ficavam só em preferências. | `interactive_onboarding`. | Ingredientes rejeitados também entram em `excluded_ingredients`. |
| 10. Padrão alimentar podia ser ignorado pela prontidão. | `dietary_patterns`, novo na candidata. | Revisão culinária declarada e exclusões concretas; ausência impede prontidão prática. |
| 11. Campo obrigatório podia pressionar a inventar um toque especial. | `RecipeCard.flavor_detail`, durante a implementação. | Detalhe opcional, com nota de busca quando não houve achado específico. |
| 12. A IA avançou sobre dúvida de leite e sugeriu observar mal-estar. | Primeira rodada real no Claude Code. | Pergunta somente pelo alcance da exclusão provisória; não sugere experimentar ou inferir diagnóstico. |
| 13. Desambiguação omitiu nomes comuns ou generalizou ingrediente opcional. | Rodadas reais sobre canjica. | Exemplos por nomes, regiões e ingredientes distintivos; sem generalização de amendoim. |
| 14. Correção de sopa recomendou liquidificador quente sem verificar o modelo. | Primeira rodada real de acompanhamento. | Alternativa sem bater quente ou consulta ao manual específico antes dessa operação. |

Confiança dos achados: alta nos cenários reproduzidos. O falsificador de cada correção é a repetição do cenário original produzindo novamente a conduta descrita; os testes estruturais não substituem a observação semântica das respostas.

As duas observações rebaixadas são: a classificação de umami, incorporada como ampliação fundamentada do guia, e a tipografia de respostas livres do modelo, que continua sujeita a desvio pontual. O checklist determinístico preserva a tipografia; o ensaio final da pergunta sobre canjica ainda exibiu aspas incompatíveis fora da abertura. Esse resultado foi preservado, sem normalizar a evidência original ou afirmar conformidade tipográfica universal.

## Entrada, elaboração e saída

| Momento | Trabalho da pessoa | Trabalho da IA ou ferramenta |
|---|---|---|
| Configurar a comida | Marcar nomes ou números; pode dizer “nenhum” ou “não sei”. | Oferecer exemplos, confirmar só a dúvida relevante, não diagnosticar nem persistir sem escolha. |
| Escolher o preparo | Informar o prato ou ingredientes; escolher entre variantes. | Aproveitar contexto, apresentar até três opções viáveis, desambiguar antes de pesquisar. |
| Pesquisar | Aguardar ou ajustar o pedido se faltar evidência. | Duas trajetórias, orçamento global, sete grupos editoriais do país, preservação de detalhes minoritários. |
| Cozinhar | Conferir condições reais e seguir uma etapa ou a receita inteira. | Quantidades, sinais de ponto, compras, detalhe documentado e sete links. |
| Ajustar | Contar o estado do preparo ou ingrediente que faltou. | Ajudar sem repetir cadastro nem reiniciar a pesquisa por dúvida de execução. |

O MCP mantém quatro ferramentas. A navegação e os papéis pertencem à IA hospedeira; o servidor local não chama modelos, não salva perfil nem executa a pesquisa. Sem subagentes, os papéis podem ser sequenciais. Essa coordenação não prova independência arquitetural.

## Migração: por que 2.0

Há mudança de semântica: na 1.0.0, rótulos não conferidos impediam `ok`; nesta candidata, conferências humanas aplicáveis ficam em `action_items` e afetam `preparation_ready`. Por isso foi escolhida uma versão principal nova, mesmo preservando a leitura dos JSON antigos.

- `ok`: consistência documental e de exclusões declaradas; não é autorização para cozinhar.
- `practical_ready`: além do resultado documental, a ficha contém os dados operacionais e cabe nas condições declaradas.
- `preparation_ready`: também foram declaradas as conferências aplicáveis antes de começar. Não é certificação de segurança individual.

Registros antigos sem `recipe_card` continuam legíveis, mas não recebem prontidão prática. Clientes devem ler os três campos e `action_items`; não devem tratar somente `ok` como receita pronta.

`Request.kitchen` contém ingredientes disponíveis, tempo total, orçamento textual, possibilidade de compras, objetivo de sabor e apresentação completa ou passo a passo. Valores desconhecidos não são inventados. Preço, capacidade de aparelho e rendimento exigem fundamento ou indicação explícita de estimativa.

Quando houver `Profile.dietary_patterns`, o host registra `Delivery.dietary_pattern_review` com padrão, exclusões concretas, revisão de compatibilidade e nota. O host faz a revisão culinária e pergunta só por ambiguidade material; não transfere ao usuário a tarefa de listar uma ontologia de alimentos. A declaração não prova compatibilidade clínica nem substitui conferência das evidências.

`RecipeCard.flavor_detail` pode ser ausente. Nesse caso, `detail_search_note` registra a busca sem achado específico. Isso evita inventar um segredo para completar um campo. A nota não dispensa a exploração e os detalhes documentais exigidos nas sete fontes.

## Como conferir e usar

Depois da instalação, estes comandos usam dados públicos ou sintéticos:

```powershell
receitas iniciar
receitas mostrar examples/entrega_pratica_sintetica.json
python scripts/sincronizar_checklist.py
python -m unittest discover -s tests -v
python scripts/validate_repository.py
```

`iniciar` mostra só a primeira pergunta. `mostrar` apresenta a receita declarada em texto humano, depois das validações, sem salvar arquivo. O exemplo é sintético e não é uma receita tradicional qualificada. O sincronizador, sem `--write`, somente confere; a gravação explícita preserva backups e relê os destinos. Atualizar metadados e manifest é a última etapa da montagem, com `scripts/validate_repository.py --refresh`.

Os resultados executados e as respostas reais resumidas constam em [evidência da jornada](../evidence/JORNADA_2_0.json). A nova pesquisa de uso está [documentada com fontes e limites](PESQUISA_DE_USO_2026.md); as explicações sensoriais estão no [guia de sabor](SABOR_E_UMAMI.md).

## Estado real e limites

Esta é uma candidata, sem nova promoção estável. A release 1.0.0 e seus registros permanecem preservados. A revisão B.9 daquela versão não cobre os novos bytes. Ensaios funcionais no Claude Code e revisão por subagentes OpenAI não concluem B.9. A verificação arquitetural exige identidade e linhagem suficientes do gerador e do verificador; rótulo de interface ou fornecedor diferente não prova isso sozinho.

Não houve estudo com usuários finais, teste de cozinha, homologação de todos os clientes ou nova pesquisa cega de sete receitas para cada prato citado nos guias. O Gemini CLI continuou fora dos testes funcionais desta candidata; o impedimento histórico não foi contornado por alterações de autenticação. As entradas `CLAUDE.md` e `GEMINI.md` são adapters locais e não provam, por existirem, carregamento em cada versão desses produtos.

Confiança: alta nas correções reproduzidas e verificações efetivamente registradas; média na generalização para outros modelos e situações de cozinha.

Pendências: B.9 específica com linhagem comprovada, decisão de promoção estável, testes com usuários e cobertura adicional de clientes; desvio tipográfico pontual em resposta livre do modelo.
