---
lang: pt-BR
title: Receitas Tradicionais Canônicas
subject: Pesquisa culinária com sete receitas do país de origem
author: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
keywords: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
manager: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
---

# Receitas Tradicionais Canônicas

Peça um prato à sua IA. Ela pesquisa sete receitas em sites do país de origem, compara o preparo e procura os detalhes que fazem diferença na cozinha de casa.

Você recebe ingredientes, passos curtos e sinais para reconhecer o ponto. Pode pedir uma etapa por vez, medidas caseiras ou uma explicação técnica mais detalhada.

**Distribuição 1.0.0, instrução v6.1.** A pesquisa depende de uma IA com acesso à internet. O projeto organiza e verifica o processo; não promete encontrar todo conhecimento culinário existente.

## Comece pela conversa

1. Abra a [instrução para sua IA](prompts/INSTRUCAO_PROJETO.md) e copie o conteúdo para as instruções do projeto ou para uma nova conversa.
2. Diga: “Vamos configurar minha cozinha”. A IA pergunta quais alimentos evitar, alergias, intolerâncias, preferências, porções e utensílios. Você pode responder uma pergunta por vez.
3. Peça, por exemplo: “Quero uma feijoada brasileira. Mostre as diferenças regionais antes de escolhermos”.

Se o mesmo nome indicar pratos diferentes, a IA apresenta os nomes comuns, o país ou região e os ingredientes básicos de cada opção. A escolha é sua.

O perfil vale para a conversa. Guardá-lo em memória ou arquivo depende de sua escolha. Não publique informações pessoais em issues, exemplos ou forks.

## O que orienta a pesquisa

- Sete receitas-fontes, de sete grupos editoriais distintos, com conteúdo efetivamente lido e evidência de atuação editorial no país. O endereço do site, sozinho, não comprova isso.
- Duas frentes: receitas de referência e receitas domésticas ou regionais. O saber de quem cozinha em casa tem lugar na pesquisa, com autoria e procedência.
- Ingredientes, preparo, observações e comentários são lidos antes da seleção. Detalhes minoritários não desaparecem por votação.
- As sete receitas são comparadas sem juntar, silenciosamente, versões regionais diferentes. Uma adaptação é identificada como adaptação.
- Quando faltarem fontes elegíveis ou a qualificação editorial estiver pendente, a IA explica o que faltou. O contrato rejeita a pendência; não inventa a sétima receita.
- Perguntas sobre alimentos evitados entram na configuração inicial. Avisos aparecem quando há uma questão concreta, sem repetir ressalvas genéricas a cada resposta.

O padrão deste projeto é preparo sem bebidas alcoólicas. As demais escolhas alimentares são configuráveis; instruções superiores da sua IA continuam aplicáveis.

## Para conectar por MCP

O servidor local oferece perguntas iniciais, plano de pesquisa, esquemas e validadores. Ele não navega na internet nem chama outros modelos. A IA conectada realiza as buscas e a coordenação dos papéis com suas próprias ferramentas.

A instrução completa acompanha o pacote e é oferecida pelo MCP. Veja a [instalação e conexão](docs/INSTALACAO.md) e os [clientes efetivamente testados](docs/CLIENTES_TESTADOS.md). Também é possível usar apenas a instrução, sem instalar software.

## Ensaio de feijoada

A [pesquisa inicial](evidence/ENSAIO_FEIJOADA.md) registra o que funcionou e o que falhou. A primeira rodada não encontrou o detalhe procurado. A exploração de variantes regionais encontrou o uso culinário do ingrediente-alvo, sem inseri-lo nas consultas. Isso não comprova os efeitos fisiológicos atribuídos a ele.

Há um [lote real revalidado com sete fontes](examples/feijoada_revalidada.json), o [registro histórico da descoberta](examples/feijoada_pesquisa.json) e testes com casos sintéticos. A revalidação posterior passou no contrato documental com contadores medidos; ela reutiliza fontes conhecidas e não é outra descoberta cega. Nenhum exemplo é certificação de segurança ou receita clínica.

## Para contribuir ou reutilizar

Pode copiar, adaptar e distribuir. Preserve os créditos e cite o [repositório original](https://github.com/RodrigoYuMatsumoto/receitas-tradicionais-canonicas), indicando alterações. Consulte [licenças e atribuição](LICENSE.md), [como contribuir](CONTRIBUTING.md) e [limites da verificação](docs/VERIFICACAO.md).

Receitas e imagens dos sites consultados continuam sob os direitos de seus respectivos autores. Os exemplos contêm inventários factuais e resumos próprios, com links, sem reproduzir os textos integrais.

Confiança: alta nos contratos e cenários ensaiados; a experiência em outras IAs depende das capacidades do cliente.

Pendências de cobertura: interfaces não ensaiadas, outros pratos e estudos com usuários. Consulte [verificação](docs/VERIFICACAO.md) e [clientes testados](docs/CLIENTES_TESTADOS.md) para o alcance das evidências.
