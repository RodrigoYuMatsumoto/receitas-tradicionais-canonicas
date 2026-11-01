---
lang: pt-BR
title: "Entrada do projeto no GEMINI"
subject: "Carregamento da instrução culinária e início pelo checklist"
author: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
keywords: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
manager: "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
version: "2.0.0-rc.1"
status: candidate
---

# Receitas Tradicionais Canônicas

Leia [a instrução completa](prompts/INSTRUCAO_PROJETO.md) e [os papéis](agents/PAPEIS.md) deste mesmo clone antes de atender um pedido culinário. [AGENTS.md](AGENTS.md) contém as regras de manutenção do repositório.

Para uso na cozinha, comece diretamente pelo checklist numerado e com exemplos. Se o MCP estiver conectado, apresente `onboarding_questions.first_message`. Sem ele, use o roteiro portátil da instrução. Aproveite informações já dadas e deixe relatórios de versão, ferramentas e agentes para quando forem solicitados.

Depois obtenha somente os dados de cozinha ausentes. Não pesquise antes de resolver ambiguidade material por opções com ingredientes. O host faz as buscas; o MCP valida declarações. Guarde o perfil só na conversa, salvo escolha explícita. Não altere configuração global nem presuma instalação pelo simples acesso ao clone.

Esta candidata não herda revisão ou homologação da versão estável anterior. Consulte [a revisão da jornada](docs/REVISAO_JORNADA_2_0.md) para testes e limites.
