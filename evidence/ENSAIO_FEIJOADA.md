---
lang: pt-BR
title: Ensaio de pesquisa de feijoada brasileira
subject: Descoberta culinária sem o ingrediente-alvo nas consultas
author: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
keywords: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
manager: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
---

# Ensaio de pesquisa de feijoada brasileira

Em 31/10/2026, a pesquisa partiu do nome Feijoada Tradicional Brasileira. O objetivo foi verificar se a leitura de receitas locais encontraria um detalhe culinário conhecido pelo coordenador, sem informar esse detalhe ao pesquisador independente ou usá-lo nas consultas.

O resultado mudou com a exploração regional: a primeira rodada não encontrou o ingrediente-alvo; a segunda encontrou seu uso em receitas baianas. O ensaio é exploratório, com um único prato, sem teste de cozinha.

## O que foi separado

O coordenador conhecia o alvo porque ele constava do pedido. Por isso, sua própria busca não basta como prova de descoberta cega. Um pesquisador em contexto separado recebeu somente o nome do prato, país, requisitos de fontes e pedido genérico de detalhes domésticos.

Na primeira rodada, esse pesquisador executou 10 consultas e tentou 18 páginas únicas, incluindo falhas. Encontrou sete receitas-base de editores diferentes, além de registros regionais. Não encontrou o alvo. Duas consultas usaram nomes vistos em resultados antes da abertura das páginas; essa falha metodológica foi registrada, sem reclassificação retroativa.

O coordenador pesquisou em paralelo. Suas nove consultas culinárias foram:

1. `feijoada receita de família segredo`
2. `feijoada tempero segredo avó`
3. `feijoada tradicional dicas comentários`
4. `feijoada tradicional temperos ervas receita caseira`
5. `feijoada brasileira receitas regionais`
6. `feijoada receita tradicional depoimento cozinheira`
7. `feijoada baiana receita tradicional`
8. `feijoada pernambucana receita tradicional`
9. `feijoada brasileira toque especial ervas`

Essas consultas não continham o ingrediente-alvo. A sétima levou a páginas que o listam. O coordenador conhecia o resultado esperado; essa limitação permanece mesmo sem utilizar a palavra nas buscas.

Na segunda rodada independente, o coordenador indicou apenas a lacuna regional e pediu explorar receitas baianas fora do grupo Globo. Foram mais quatro consultas e seis páginas novas. A direção geográfica foi fornecida; o ingrediente continuou oculto. A primeira consulta dessa rodada foi `Feijoada Baiana`.

O log das 14 consultas do pesquisador separado e das 12 consultas do coordenador consta de [feijoada_pesquisa.json](../examples/feijoada_pesquisa.json): 26 consultas ao todo, incluindo três de qualificação editorial do coordenador. Os registros são agrupados por pesquisador e preservam a ordem interna, sem inventar uma cronologia global entre trabalhos paralelos. A [relação de páginas](PAGINAS_CONSULTADAS.json) registra 27 URLs culinárias e de procedência com conteúdo lido e seis URLs com falha ou conteúdo insuficiente. Consultas de documentação técnica são etapa separada. O campo `derived_from` explica o motivo declarado de cada refinamento; o software não certifica a cronologia real de abertura das páginas.

## As sete receitas selecionadas depois da exploração

O conjunto final é um panorama comparativo de preparações brasileiras, autorizado para este ensaio. Não representa uma escolha operacional de variante e não deve ser transformado em uma receita nacional única por mistura dos ingredientes.

| Fonte | Procedência editorial | Detalhe documentado |
|---|---|---|
| [Panelinha: feijoada na pressão](https://panelinha.com.br/receita/feijoada-na-pressao) | Editora Panelinha; termos e operação locais | Parte do caldo das carnes cozinha o feijão; grãos amassados entram no refogado. |
| [Delci Gomes: feijoada](https://receitas.globo.com/receitas-da-tv/e-de-casa/feijoada-e-de-casa.ghtml) | Globo; cozinheira da Mangueira identificada | Carnes cozinham inteiras, são cortadas depois e servidas separadas do feijão. |
| [Camil: feijoada](https://www.camil.com.br/receitas/feijoada) | Operação brasileira da Camil, conforme história institucional | Laranja sem casca entra quando o caldo engrossa e é retirada depois. |
| [Receiteria: feijoada](https://www.receiteria.com.br/receita/feijoada/) | Grupo Contteudo, Maringá/PR, conforme página institucional | A capa do bacon acompanha o cozimento e depois é retirada. |
| [Receita da Boa: feijoada](https://jc.uol.com.br/receitadaboa/aprenda-como-fazer-feijoada-receita-tradicional-brasileira-para-reunir-a-familia-a-mesa.html) | SJCC/Grupo JCPM, conforme página institucional | Prepara inicialmente feijão e refogado de carnes em separado. |
| [Salvador Cordovil: feijoada da família](https://www.band.com.br/entretenimento/realities/masterchef/ritmista-da-portela-salvador-ensina-feijoada-perfeita-para-preparar-ouvindo-samba-veja-a-receita-16310456) | Band; relato familiar atribuído à avó Lídia | Engrossa refogado separado com feijão batido e descreve cortes após cozinhar carnes inteiras. |
| [André Albuquerque: feijoada baiana](https://www.tudogostoso.com.br/receita/296211-feijoada-baiana.html) | Webedia Internet Brasil, conforme política da plataforma | A erva fresca procurada aparece no inventário e é batida com os demais temperos. |

São sete grupos editoriais declarados distintos. Os endereços de qualificação e os inventários factuais estão no JSON. Isso comprova a seleção documentada, sem demonstrar que nenhuma receita influenciou intelectualmente outra. O domínio UOL que hospeda Receita da Boa não foi confundido com seu responsável editorial SJCC/JCPM.

## O que o achado permite afirmar

O [TudoGostoso, na receita de André Albuquerque](https://www.tudogostoso.com.br/receita/296211-feijoada-baiana.html), lista hortelã fresca e a inclui no preparo batido dos temperos. O [iBahia, na receita atribuída a Dadá](https://www.ibahia.com/diversao/gastronomia/aprenda-a-fazer-uma-deliciosa-feijoada-baiana), registra nomes populares diferentes para a erva em sua lista. Esses nomes não autorizam presumir identidade botânica ou intercambiar espécies.

O [Delicioso](https://www.delicioso.com.br/receitas/feijoada-baiana-como-fazer) também apresenta a erva em ramos. Sua responsabilidade editorial local não foi suficientemente qualificada para incluí-lo entre as sete fontes. A página cita livros e instituições, mas essa referência não comprova que cada ingrediente tenha sido conferido nos originais.

O [TudoReceitas](https://www.tudoreceitas.com/receita-de-feijoada-baiana-9730.html) a apresenta como opcional. O rodapé identifica empresa estrangeira; por isso essa receita não foi contada como site editorial brasileiro. Uma [republicação no Efuxico](https://efuxico.com/domingo-e-dia-do-e-de-cumer-no-efuxico-feijoada-baiana-de-jorge-da-unipres/) declara essa origem e usa suas imagens. Não são duas confirmações independentes.

Uma [receita também intitulada baiana na Band](https://receitas.band.com.br/dia-dia/receita/feijoada-baiana-band-receitas-id-10258) usa feijão preto e não lista essa erva. A página contém a quantidade anômala de costelinha `3001 grama(s)` e menciona ingredientes de farofa fora da lista principal. Esses problemas impedem copiar seus números automaticamente. O nome regional, sozinho, não resolve todas as diferenças.

**Presença culinária confirmada não é comprovação fisiológica.** Não foi demonstrado neste ensaio que a erva retire gordura, melhore a digestão ou reduza gases. Também não foi encontrada confirmação da versão em infusão ou chá forte. O resultado documentado são folhas ou ramos como tempero em algumas preparações regionais. Não foi definida uma dose para adicionar a outra receita.

## Por que a instrução foi alterada

| Observação | Alteração | Como pode ser refutada ou melhorada |
|---|---|---|
| As sete receitas mais fáceis de selecionar não revelaram o alvo. | Explorar uma frente doméstica/regional antes de fechar as sete. | Repetir com pratos e detalhes desconhecidos do coordenador e medir cobertura. |
| A ampliação geográfica revelou ingredientes minoritários. | Registrar variantes e detalhes antes de aplicar síntese ou maioria. | Um conjunto em que a expansão só traga ruído pede ajuste da seleção, sem apagar a diferença. |
| Uma página local republicava fonte estrangeira. | Registrar grupo editorial e origem de republicação, além do país do site. | Encontrar duplicatas não detectadas demonstra necessidade de revisão semântica adicional. |
| Fontes culinárias faziam afirmações de saúde sem prova. | Separar uso culinário, explicação sensorial e efeito fisiológico. | Uma fonte primária aplicável pode sustentar uma afirmação específica, sem validar todas as demais. |
| A instrução original excluía relatos domésticos sem institucionalidade. | Admitir autoria doméstica identificável e data ausente declarada. | Fonte sem procedência ou receita sem conteúdo lido continua inelegível. |

A pesquisa inicial e a descoberta do coordenador precederam a instalação do pacote. A segunda rodada independente foi uma replicação posterior. O repositório não foi conectado às IAs pessoais do operador.

O ensaio não mediu o número de reformulações feitas após uma busca sem fonte elegível em cada trajetória. O pesquisador confirmou que os logs não permitem reconstruir esse número rigorosamente. Por isso os dois contadores permanecem desconhecidos no JSON e o validador novo deve retornar `reformulacoes_nao_medidas`, impedindo uma aprovação integral retroativa. Refinamento exploratório bem-sucedido não equivale automaticamente a retry de fracasso. A descoberta documental permanece válida com essa limitação metodológica explícita.

Depois da implementação e da correção das URLs, uma rodada separada de [revalidação assistida](REVALIDACAO_DOCUMENTAL.json) leu novamente as sete receitas e suas provas editoriais: uma consulta com o nome do prato, 12 URLs distintas, dois contextos de pesquisa, zero falhas e zero reformulações. O [novo lote](../examples/feijoada_revalidada.json) passou no contrato documental. Os endereços foram reaproveitados do registro anterior; isso não constitui nova descoberta cega. O histórico permanece intacto e reprovado quanto aos seus contadores desconhecidos.

Confiança: alta na presença do ingrediente nas páginas lidas e na identificação da republicação; média na caracterização das variantes e na generalização do método, pois houve um único prato e direção regional explícita na segunda rodada.

Pendências: contagem retrospectiva de retries desconhecida; teste de cozinha; confirmação da infusão e dos efeitos fisiológicos; revisão dos livros citados por fontes secundárias; investigação completa de dependência intelectual; avaliação cega com outros pratos; revisão por outra família de modelos.
