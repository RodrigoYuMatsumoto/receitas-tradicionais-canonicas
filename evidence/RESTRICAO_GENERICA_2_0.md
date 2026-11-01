---
lang: pt-BR
title: "Conferência complementar de ingredientes genéricos"
subject: "Identificação de ingrediente antes do preparo quando há exclusão específica"
author: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
keywords: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
manager: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
version: "2.0.0"
status: versioned
---

# Identifique o ingrediente antes de começar

Uma referência genérica pode abranger um alimento que a pessoa excluiu. O projeto pede esclarecimento antes do preparo, sem transformar essa possibilidade em diagnóstico ou em confirmação de que o ingrediente proibido está presente.

## Caso reproduzido

No commit `d597261fb4c0a2d912a2933f6dd4b529ccd48d9a`, o perfil fictício excluía castanha-de-caju e os dois inventários declarados continham apenas arroz e água. Em casos separados, o preparo dizia “Adicione castanhas picadas.” ou a lista de compras continha “castanhas”. Os três estados de validação eram verdadeiros, sem ação de esclarecimento. O caso foi reproduzido depois do parecer inicial e não integrou os testes que fundamentaram aquele veredito.

## Tratamento operacional

Para uma exclusão composta, a conferência procura o núcleo lexical inicial significativo e suas flexões regulares nos textos operacionais. Uma ocorrência genérica sem identificação suficiente produz `ingrediente_generico_pendente`. O plano pode continuar consultável, mas `preparation_ready` permanece falso enquanto faltar a identificação.

Cada ocorrência é conferida. Uma menção completa a outro tipo de castanha, declarado no inventário, não resolve automaticamente outra menção genérica na mesma frase. Palavras de preparo, como picada ou torrada, não identificam a variedade. Palavras funcionais compartilhadas, como de ou com, não estabelecem correspondência de ingredientes.

Uma variedade alternativa explicitamente identificada e declarada no inventário pode resolver a ocorrência correspondente. Isso não a transforma no item excluído: castanha-do-pará não é identificada automaticamente como castanha-de-caju. A menção explícita ao alimento excluído continua sujeita ao bloqueio já existente.

O tratamento é lexical e depende dos nomes, aliases e componentes declarados. Não é uma ontologia completa de alimentos, não entende toda expressão em linguagem natural e não certifica segurança individual. O host continua responsável pela revisão semântica e por não introduzir ingredientes desconhecidos na entrega.

## Evidência e revisão

Os [resultados e hashes da correção](TESTES_RESTRICAO_GENERICA_2_0.json) distinguem o caso anterior, as regressões executadas e o escopo do teste. Os dados são sintéticos; não houve teste de cozinha.

Este registro descreve implementação e testes da família OpenAI, sem valor de revisão B.9 independente. A aprovação do conjunto funcional anterior não se transfere aos novos bytes. Antes de criar uma tag estável, exija que o [parecer independente](B9_2_0_0.md) cubra explicitamente esta correção e os hashes correspondentes.

Confiança: alta nos casos reproduzidos e testes registrados; limitada fora da cobertura lexical declarada.

Pendências de cobertura: expressões não abrangidas pelo método e condições reais de preparo permanecem sujeitas a revisão semântica.
