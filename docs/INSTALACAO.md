---
lang: pt-BR
title: Instalação e conexão com sua IA
subject: Uso por instrução copiada, repositório local e MCP
author: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
keywords: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
manager: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
---

# Instalação e conexão com sua IA

## Pela conversa, sem instalar programas

Copie [a instrução completa](../prompts/INSTRUCAO_PROJETO.md) para sua IA. Se houver um campo de instruções de projeto, prefira esse campo. Caso contrário, cole no início de uma conversa e peça que a IA confirme as perguntas iniciais.

A IA precisa conseguir pesquisar e abrir páginas. Se só conhece informações memorizadas, não pode declarar que pesquisou sete receitas nesta utilização. Um link para este repositório não significa que uma IA tenha lido seu conteúdo.

Quando a interface aceitar voz, você pode responder falando e pedir que ela leia uma etapa por vez. O projeto não instala um serviço próprio de áudio.

## Pelo repositório local

Requisitos: Git e Python 3.11 ou superior. Execute em uma pasta de sua escolha:

```powershell
git clone https://github.com/RodrigoYuMatsumoto/receitas-tradicionais-canonicas.git
cd receitas-tradicionais-canonicas
python -m venv .venv
.venv\Scripts\python.exe -m pip install .
.venv\Scripts\python.exe -m receitas_tradicionais onboarding
```

No Linux ou macOS, use `.venv/bin/python` no lugar de `.venv\Scripts\python.exe`.

O onboarding faz perguntas e devolve um perfil em JSON. Não grava as respostas automaticamente. A conversa com a IA é a opção mais simples; o comando é útil para integrações.

Para conferir a revalidação real, o exemplo sintético e o registro histórico da pesquisa:

```powershell
.venv\Scripts\python.exe -m receitas_tradicionais validate examples/feijoada_revalidada.json
.venv\Scripts\python.exe -m receitas_tradicionais validate examples/pesquisa_sintetica.json
.venv\Scripts\python.exe -m receitas_tradicionais validate examples/feijoada_pesquisa.json
.venv\Scripts\python.exe -m receitas_tradicionais schema
```

A revalidação real e o exemplo sintético devem retornar código 0, que indica estrutura aceita. A revalidação reutiliza fontes conhecidas e mede seus próprios contadores; o exemplo sintético não apresenta fontes reais. O registro histórico de feijoada deve retornar código 1: há sete fontes, mas as reformulações após buscas sem fonte elegível não foram medidas. O protocolo novo bloqueia essa lacuna; os contadores desconhecidos não foram preenchidos com zero. O comando `schema` retorna código 0 e não faz pesquisa.

O pacote fixa o SDK oficial MCP em 2.3.0. Uma atualização da dependência exige os testes de integração, não apenas a troca do número.

## MCP local

Use um cliente que aceite servidores MCP por `stdio`. Nesse transporte, o cliente inicia um processo local e se comunica com ele pela entrada e saída padrão. Não é necessário abrir uma porta nem publicar um serviço.

O [modelo de configuração](../configs/mcp_local.json) usa a estrutura `mcpServers`, comum em clientes desktop. Substitua o caminho do executável pelo Python do ambiente que acabou de criar. Esse caminho deve ser absoluto. A sintaxe e o local de configuração variam entre clientes; importe a configuração pelo mecanismo documentado pelo seu cliente.

O processo executado é:

```powershell
CAMINHO_DO_PYTHON_DO_AMBIENTE -m receitas_tradicionais mcp
```

Depois da conexão, peça à IA para listar as ferramentas deste projeto e chamar `onboarding_questions`. Confirme que as ferramentas `plan_research`, `validate_research` e `validate_delivery` também aparecem. Em seguida, carregue a instrução completa no projeto da IA.

O MCP não faz instalação automática em aplicativos, não altera instruções globais e não guarda perfis. As configurações de um usuário não são distribuídas com o repositório.

Clientes web que aceitam somente MCP remoto não conseguem iniciar diretamente este servidor local. Nesses clientes, use a instrução pela conversa. Esta versão não fornece um endpoint remoto hospedado.

## Papéis e acesso à internet

Uma IA com subagentes pode distribuir as duas frentes de pesquisa e a auditoria conforme [os papéis](../agents/PAPEIS.md). Se não tiver subagentes, executa os papéis em etapas e informa que a revisão ocorreu no mesmo contexto. O MCP não cria agentes nem contrata provedores.

As ferramentas de busca e leitura pertencem à IA utilizada. Verifique seus custos e permissões nesse aplicativo. O servidor deste repositório não solicita chave de API e não envia perfis à rede por conta própria.

## Atualização e retirada

Para atualizar, mantenha suas configurações particulares fora do clone, leia o changelog e faça novo ambiente antes de trocar uma versão em uso. Para voltar, use a versão anterior em seu próprio ambiente. Para retirar a conexão, remova a entrada deste MCP no cliente; o projeto não instala tarefas recorrentes.

Confiança: alta nos comandos testados no ambiente descrito em [verificação](VERIFICACAO.md); média no encaixe com interfaces ainda não ensaiadas.

Pendências: confirmação de configuração nas interfaces específicas de cada cliente e teste de compreensão com usuários finais.
