---
lang: pt-BR
title: Como contribuir com o projeto
subject: Sugestões, fontes e alterações verificáveis
author: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
keywords: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
manager: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
---

# Como contribuir

Uma boa contribuição pode ser um detalhe de preparo, uma fonte local, uma explicação mais clara ou a correção de um teste.

Ao sugerir uma receita, informe o nome, o país ou região, o endereço da página e o detalhe que ela documenta. Não cole livros, fotografias ou receitas integrais de terceiros. Se o conhecimento for de sua família, peça autorização antes de divulgar nome, história ou imagem de outra pessoa.

Use os modelos de issue para registrar um erro ou sugerir uma fonte. Não inclua alergias pessoais, diagnósticos, endereço, credenciais ou conversas privadas. É suficiente um exemplo inventado para demonstrar falha de perfil.

Para alterar código, faça um fork, crie uma branch e abra um pull request com problema, comportamento esperado e teste executado. Execute:

```powershell
python -m pip install .
python -m unittest discover -s tests -v
python scripts/validate_repository.py
```

Uma alteração nas regras deve atualizar exemplos e testes afetados. Não reduza o número de sete fontes para acomodar uma falha nem reclassifique um snippet como leitura integral. Quando fontes discordarem, mantenha a diferença regional e sua origem.

A revisão técnica entre agentes do mesmo fornecedor não equivale à verificação por outra família de modelos. A publicação experimental aceita pendências declaradas; promoção estável exige resolver os requisitos descritos em [verificação](docs/VERIFICACAO.md).

Confiança: alta nos critérios de contribuição documentados.

Pendências: zero quanto à definição deste procedimento.
