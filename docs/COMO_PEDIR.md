---
lang: pt-BR
title: "Como pedir uma receita e cozinhar com a sua IA"
subject: "Pedidos cotidianos, checklist alimentar e acompanhamento do preparo"
author: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
keywords: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
manager: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
version: "2.0.0-rc.1"
status: candidate
---

# Peça do seu jeito

Você pode dizer o nome de um prato, contar o que tem em casa ou pedir ajuda com uma comida que já está no fogo. Pode escrever ou falar, se a sua IA aceitar áudio. Não precisa conhecer nomes de técnicas nem descobrir sozinho todos os ingredientes de uma receita.

## Primeiro, confira o que evitar

A IA começa com uma lista de ingredientes e exemplos. Você pode responder pelos nomes, pelos números apresentados ou dizer “nenhum” ou “não sei”. Não é necessário contar informações pessoais.

Abra [o checklist completo, com todos os grupos e exemplos](CHECKLIST_INICIAL.md). Ele é gerado pela mesma fonte usada no terminal, no MCP e na instrução portátil. Assim os números apresentados correspondem aos mesmos grupos em cada meio de uso.

A lista ajuda a lembrar; você pode acrescentar qualquer item. Marcar leite não significa excluir automaticamente todo o grupo. Se você disser apenas um número, a IA confirma quais ingredientes daquele grupo quer evitar. Se já souber, diga se é alergia, intolerância, outra restrição ou preferência. A IA não decide isso por você.

Exemplo de resposta: “Não gosto de coentro. Evito amendoim por alergia. Leite eu ainda não sei; preciso conferir.”

A formulação exibida no início vem de `onboarding_questions`, disponível também pelo comando `receitas iniciar`. Este guia explica o uso; os exemplos e as opções efetivamente apresentados pela ferramenta acompanham a versão instalada.

## Depois, conte somente o que faltar

Para adaptar a receita, a IA aproveita o que você já disse e pergunta pelos dados necessários:

- **Quantidade:** para quantas pessoas ou porções.
- **Tempo:** quanto tempo há até servir; diga se algum ingrediente já está cozido ou de molho.
- **Cozinha:** panela comum ou de pressão, forno, air fryer, liquidificador e tamanho aproximado, quando relevante.
- **Ingredientes e compras:** o que já tem, se pode comprar e quanto pretende gastar.
- **Ajuda desejada:** receita completa ou uma etapa por vez.

“Para quatro pessoas, em meia hora, sem comprar nada e só com uma panela” já responde a várias perguntas. Você não precisa preencher um formulário técnico nem repetir todo o checklist em cada prato.

## Dez pedidos que você pode fazer

| Você diz | Como a IA deve ajudar |
|---|---|
| “Quero feijoada brasileira para seis pessoas.” | Aproveita os dados, confirma a variante quando necessário e pergunta apenas pelas condições que faltam. |
| “Tenho arroz, feijão e abóbora. O que dá para fazer?” | Oferece poucas opções com ingredientes básicos; você escolhe antes da pesquisa completa do prato. |
| “Tenho R$ 40 para quatro pessoas.” | Pergunta o que já existe em casa e monta uma proposta compatível, sem inventar preços atuais. |
| “Preciso de um jantar em meia hora.” | Confere o tempo total, incluindo espera; avisa se a opção escolhida não cabe e pede sua decisão. |
| “Quero fazer batata na air fryer.” | Confere o equipamento e o resultado desejado; não pressupõe que o preparo no forno é idêntico. |
| “Quero canjica.” | Mostra opções por região e ingredientes, como milho branco com leite ou creme de milho verde, e espera sua escolha. |
| “Quero uma receita japonesa tradicional, sem peixe.” | Respeita a exclusão, apresenta opções compatíveis e identifica adaptações necessárias. |
| “Não tenho esse ingrediente.” | Examina a função dele e propõe uma substituição compatível, quando houver, explicando o que muda. |
| “Meu caldo ficou aguado e sem gosto.” | Pergunta em que etapa está e o que já entrou; oferece um ajuste por vez, respeitando as restrições confirmadas. |
| “Leia uma etapa de cada vez e espere eu terminar.” | Apresenta a próxima ação e o sinal de ponto; continua quando você responder. |

Se a sua IA aceitar imagens, você também pode mostrar os ingredientes. Ela deve confirmar o que reconheceu e perguntar sobre o que não conseguiu identificar. A foto não comprova frescor, composição nem condições de conservação.

## O que você recebe

A receita começa pelo que ajuda a cozinhar: rendimento explicado, tempo, utensílios, quantidades, medidas caseiras quando úteis e passos com sinais de ponto. Depois vêm o toque de sabor encontrado, eventuais adaptações e os links das sete receitas consultadas no país de origem. A IA deve dizer claramente quando não conseguir completar essa pesquisa.

Durante o preparo da mesma receita, você pode continuar perguntando sem reiniciar o cadastro nem a pesquisa inteira. Uma mudança importante de prato ou variante exige nova conferência. Quando existir algo que só você pode verificar, como um rótulo, a IA mostra a ação necessária e mantém essa informação pendente.

Para descobrir o detalhe que melhora o prato, consulte [sabor e umami](SABOR_E_UMAMI.md). A pesquisa que orientou estes exemplos está em [pedidos culinários e uso de IA](PESQUISA_DE_USO_2026.md).
