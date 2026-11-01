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

**Candidata 2.0.0-rc.1, instrução v6.2.** A versão estável anterior é a [1.0.0](https://github.com/RodrigoYuMatsumoto/receitas-tradicionais-canonicas/releases/tag/v1.0.0). A candidata melhora a conversa inicial e a receita operacional; o alcance dos testes está na [revisão da jornada](docs/REVISAO_JORNADA_2_0.md).

## Comece pela conversa

1. Copie o [comando para começar](prompts/COMECE_AQUI.md) em uma nova conversa com sua IA. Também pode colar a [instrução completa](prompts/INSTRUCAO_PROJETO.md) no projeto.
2. A primeira resposta já traz uma lista de alimentos a evitar, com exemplos. Responda pelos nomes, números ou do seu jeito. Pode dizer “nenhum” ou “não sei”. Não precisa lembrar tudo de cabeça.
3. Conte só o que ainda falta: o que quer preparar ou aproveitar, pessoas, tempo, utensílios, compras e orçamento.

Exemplos de pedidos:

- “Tenho arroz, feijão e abóbora. Quero gastar pouco.”
- “Feijoada para seis pessoas; só tenho uma panela pequena.”
- “Um jantar de até meia hora, sem leite.”
- “Minha sopa está aguada. Me ajude uma etapa por vez.”

Veja [como pedir e cozinhar](docs/COMO_PEDIR.md). Você recebe quantidades, rendimento explicado, tempo ativo e total, utensílios, compras necessárias e passos com sinais de ponto. Pode pedir a receita inteira ou acompanhamento por etapas. A pesquisa sustenta a receita; os relatórios técnicos ficam disponíveis quando você quiser consultá-los.

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

## O toque que faz diferença

Uma ordem de preparo, um caldo bem extraído ou uma finalização podem mudar o resultado. A IA procura esses detalhes nas fontes domésticas e regionais, sem exigir que você já conheça o segredo.

O objetivo é sabor com ingredientes e técnicas, sem adicionar realçador comercial. Umami, aroma, frescor, textura e equilíbrio têm funções diferentes. A hortelã encontrada em uma feijoada regional é exemplo de aroma e frescor; não comprova umami ou efeito digestivo. O [guia de sabor](docs/SABOR_E_UMAMI.md) mostra exemplos japoneses, brasileiros e de outros contextos, com fontes e limites.

## Para conectar por MCP

O servidor local oferece perguntas iniciais, plano de pesquisa, esquemas e validadores. Ele não navega na internet nem chama outros modelos. A IA conectada realiza as buscas e a coordenação dos papéis com suas próprias ferramentas.

A instrução completa acompanha o pacote e é oferecida pelo MCP. Veja a [instalação e conexão](docs/INSTALACAO.md) e os [clientes efetivamente testados](docs/CLIENTES_TESTADOS.md). Também é possível usar apenas a instrução, sem instalar software.

Para imprimir apenas o checklist inicial depois de instalar:

```powershell
receitas iniciar
```

Para ver a saída humana de uma ficha já preenchida, use `receitas mostrar examples/entrega_pratica_sintetica.json`. É um exemplo de teste, sem pesquisa culinária real. A conversa com a IA preenche esses dados para você.

Os contratos distinguem pesquisa documentada (`ok`), cartão operacional completo (`practical_ready`) e conferências necessárias antes do preparo (`preparation_ready`). Uma conferência de rótulo pendente aparece como ação concreta, sem impedir a leitura do plano da receita. Esses estados não certificam segurança individual nem substituem as condições reais da cozinha.

## Ensaio de feijoada

A [pesquisa inicial](evidence/ENSAIO_FEIJOADA.md) registra o que funcionou e o que falhou. A primeira rodada não encontrou o detalhe procurado. A exploração de variantes regionais encontrou o uso culinário do ingrediente-alvo, sem inseri-lo nas consultas. Isso não comprova os efeitos fisiológicos atribuídos a ele.

Há um [lote real revalidado com sete fontes](examples/feijoada_revalidada.json), o [registro histórico da descoberta](examples/feijoada_pesquisa.json) e testes com casos sintéticos. A revalidação posterior passou no contrato documental com contadores medidos; ela reutiliza fontes conhecidas e não é outra descoberta cega. Nenhum exemplo é certificação de segurança ou receita clínica.

## Para contribuir ou reutilizar

Pode copiar, adaptar e distribuir. Preserve os créditos e cite o [repositório original](https://github.com/RodrigoYuMatsumoto/receitas-tradicionais-canonicas), indicando alterações. Consulte [licenças e atribuição](LICENSE.md), [como contribuir](CONTRIBUTING.md) e [limites da verificação](docs/VERIFICACAO.md).

Receitas e imagens dos sites consultados continuam sob os direitos de seus respectivos autores. Os exemplos contêm inventários factuais e resumos próprios, com links, sem reproduzir os textos integrais.

As mudanças de conversa foram informadas por [fontes atuais sobre uso culinário](docs/PESQUISA_DE_USO_2026.md), incluindo buscas brasileiras por utensílio e assistência durante o preparo. Exemplos de fornecedores e rankings de tendências não são uma medida representativa de todos os usuários.

Confiança: alta no código e nos cenários efetivamente registrados; a experiência em outras IAs depende das capacidades do cliente.

Pendências de cobertura: interfaces não ensaiadas, outros pratos e estudos com usuários. Consulte [verificação](docs/VERIFICACAO.md) e [clientes testados](docs/CLIENTES_TESTADOS.md) para o alcance das evidências.
