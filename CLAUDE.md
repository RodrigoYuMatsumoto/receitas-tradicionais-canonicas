---
lang: pt-BR
title: "Entrada do projeto no CLAUDE"
subject: "Carregamento da instrução culinária e início pelo checklist"
author: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
keywords: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
manager: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
version: "2.0.0"
status: versioned
---

# Receitas Tradicionais Canônicas

Leia [a instrução completa](prompts/INSTRUCAO_PROJETO.md) e [os papéis](agents/PAPEIS.md) deste mesmo clone antes de atender um pedido culinário. [AGENTS.md](AGENTS.md) contém as regras de manutenção do repositório.

Para uso na cozinha, comece diretamente pelo checklist numerado e com exemplos. Se o MCP estiver conectado, apresente `onboarding_questions.first_message`. Sem ele, use o roteiro portátil da instrução. Aproveite informações já dadas e deixe relatórios de versão, ferramentas e agentes para quando forem solicitados.

Depois obtenha somente os dados de cozinha ausentes. Não pesquise antes de resolver ambiguidade material por opções com ingredientes. O host faz as buscas; o MCP valida declarações. Guarde o perfil só na conversa, salvo escolha explícita. Não altere configuração global nem presuma instalação pelo simples acesso ao clone.

Esta versão não herda revisão ou homologação da 1.0.0. Consulte [a verificação](docs/VERIFICACAO.md) para o método e o [parecer B.9](evidence/B9_2_0_0.md) para resultados, hashes e veredito dos bytes distribuídos. A tag estável só é criada com parecer aprovado.
