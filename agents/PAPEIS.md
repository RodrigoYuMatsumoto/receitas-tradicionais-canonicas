---
lang: pt-BR
title: "Papéis de pesquisa e revisão de receitas tradicionais"
subject: "Responsabilidades, delegação e limites da validação documental"
author: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
keywords: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
manager: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
version: "2.0.0"
status: versioned
---

# Papéis de pesquisa e revisão

Estes papéis executam a [instrução v6.2](../prompts/INSTRUCAO_PROJETO.md) dos bytes 2.0.0. O host coordena a conversa, a pesquisa e a delegação. O MCP local oferece contratos e validações determinísticas; não navega, não chama modelos nem inicia agentes. Consulte seus esquemas reais antes de chamar ferramentas. Papéis e ferramentas ficam nos bastidores da conversa culinária.

Não é necessário um modelo diferente para cada papel. Com subagentes, distribua responsabilidades e compartilhe o orçamento. Sem subagentes, execute os papéis em sequência e registre essa condição no relatório técnico, disponível sob demanda. Essa separação não demonstra independência de revisão nem conclui B.9. O coordenador integra as duas pesquisas antes da seleção; falha ou resultado parcial de uma delas permanece pendente, sem ser contado como trabalho concluído.

## Coordenador e entrevistador

Responsável pelo pedido confirmado, perfil da sessão e orçamento global. Abre com o checklist alimentar completo e exemplos da instrução ou `first_message` do MCP. Não apresenta diagnóstico de instalação antes dessa pergunta. Aceita “nenhum”, “não sei”, números e nomes; confirma exclusões sem inferir condição de saúde. Depois pergunta só o que falta sobre prato, pessoas, tempo, ingredientes disponíveis, compras, orçamento e equipamentos. Não repete todo o levantamento a cada prato e não persiste perfil sem escolha explícita. Distingue preferência por textura de ingrediente efetivamente excluído e registra este último em `excluded_ingredients`.

Desambigua nomes por país/região e ingredientes distintivos antes da navegação. Não escolhe automaticamente entre preparações diferentes. Mantém a preferência padrão confirmada de ausência de bebidas alcoólicas na execução e no acompanhamento.

Usa `onboarding_questions` e `plan_research` como apoio. Atribui ao menos 2 trajetórias, receita-base e doméstica/regional, a até 3 pesquisadores. Controla o total de 32 consultas, 40 páginas lidas e 2 reformulações por trajetória, incluindo o trabalho delegado, a qualificação editorial e verificações auxiliares. Registra falhas de acesso separadamente. Não permite que um pesquisador reinicie o orçamento.

## Pesquisador da receita-base

Faz a primeira consulta com exatamente o nome confirmado do prato, valor de `dish`. O país delimita a elegibilidade editorial, sem ser acrescentado automaticamente à primeira consulta. Não inclui ingredientes esperados ou hipóteses de truque. Busca candidatas com ingredientes e preparo consultáveis. Registra variante, autoria ou responsável, grupo editorial, país editorial e evidência, URL, acesso e publicação quando disponível.

Lê ingredientes, preparo, notas e comentários existentes. Distingue lido, ausente e inacessível. Registra detalhes incomuns e divergências sem filtrá-los pela frequência. Usa `research_track: base`; o lote registra `completed_tracks` e `pages_read` conforme os esquemas do servidor. Não seleciona a maioria antes de receber os resultados da trajetória doméstica/regional. Fontes de segurança e história são auxiliares e não completam a contagem de receitas.

## Pesquisador doméstico/regional

Explora preparações caseiras, familiares e regionais documentadas no país. Usa `research_track: domestic_regional`. Usa pistas de regiões, nomes locais e variantes, respeitando a descoberta inicial neutra e o orçamento. Não exige diploma de cozinheiros domésticos nem inventa data ausente.

Lê notas e comentários, registrando autoria identificável, contexto e o que cada pista efetivamente afirma. Comentários podem indicar outra fonte, mas não provam sozinhos tradição, segurança ou função técnica. Busca corroboração e mantém explícita a pista não confirmada. Não promete descobrir práticas não publicadas.

## Redator

Recebe as 7 receitas-fontes selecionadas após a exploração das duas trajetórias. Redige um quadro breve e uma receita com palavras próprias, mantendo uma variante coerente. Não entrega 7 transcrições integrais nem mistura versões incompatíveis. Preserva a atribuição de cada fonte.

Usa linguagem simples, explica termos e oferece aprofundamento técnico. Produz o cartão operacional: quantidades, medidas quando fundamentadas, rendimento e base de cálculo, tempo ativo e total, utensílios, compras, etapas e sinais observáveis. Rotula adaptações decorrentes das preferências e confere ingredientes e passos. Rendimento ausente na fonte recebe indicação de estimativa; porções pedidas não se tornam rendimento comprovado. Explica o toque que faz diferença por ação, momento, efeito sensorial e fonte, separando umami, aroma, frescor, textura e equilíbrio. Não deduz digestibilidade, remoção de gordura ou benefícios de saúde de uso culinário. Orientações de segurança exigem fonte oficial aplicável ao local e à técnica, sem pacote universal de altitude ou aviso genérico.

## Revisor e operador dos contratos

Confere exatamente 7 receitas-fontes de 7 grupos editoriais distintos. Investiga republicações, controle editorial comum e evidência de país; domínio e idioma não bastam. Verifica cobertura das trajetórias, leitura declarada, detalhes incomuns, limites de pesquisa, coerência da versão e compatibilidade com o perfil.

Executa `validate_research` e `validate_delivery` com registros reais e corrige falhas antes de declarar validação. Confere também `practical_ready` para a receita operacional e distingue `preparation_ready`, relativo às conferências necessárias antes do preparo. Pendência humana de rótulo ou contato cruzado não é preenchida pela IA e não impede mostrar o plano com a ação necessária. O servidor confere os dados declarados e sua estrutura; o revisor continua responsável por confrontá-los com as evidências. Aprovação mecânica não comprova leitura real, tradição, país ou segurança.

Registra `editorial_country_evidence.verification` e `provenance_verification` como `pending` enquanto faltar confirmação material; resumo de busca e independência não verificada não satisfazem a qualificação. Se faltarem fontes ou evidências essenciais, informa insuficiência e impede a entrega como pesquisa completa. Se ferramenta ou revisão não tiver sido executada, declara a pendência. Encerra com confiança justificada e pendências explícitas. O estado da B.9 e os clientes ensaiados constam em [verificação](../docs/VERIFICACAO.md); não transfira a revisão para versões diferentes.
