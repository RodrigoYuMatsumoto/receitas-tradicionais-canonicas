---
lang: pt-BR
title: Instalação e conexão com sua IA
subject: Uso pela conversa, pacote local e configuração de clientes MCP
author: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
keywords: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
manager: Rodrigo Yú Matsumoto OAB/PE nº 1.338-B
---

# Instalação e conexão com sua IA

## Comece pela conversa

Copie [o comando de início](../prompts/COMECE_AQUI.md) para uma conversa nova ou coloque [a instrução completa](../prompts/INSTRUCAO_PROJETO.md) nas instruções do projeto da sua IA. A primeira resposta deve mostrar o checklist alimentar numerado com exemplos, aceitando “nenhum”, “não sei” e respostas livres. Depois a IA pergunta apenas os dados de cozinha ainda ausentes. Não é necessário ouvir um relatório de instalação antes de começar.

A IA precisa conseguir pesquisar e abrir páginas para executar uma pesquisa nova. Um link para o repositório não significa que ela tenha lido a instrução. Quando a interface aceitar voz, você pode responder falando e pedir a leitura de uma etapa por vez; este projeto não instala áudio próprio.

Essa alternativa também serve a clientes web que não conseguem iniciar processos locais. O projeto fornece MCP local por `stdio`; não há endpoint remoto hospedado. Os resultados observados em cada interface estão em [clientes testados](CLIENTES_TESTADOS.md).

## Instale o pacote local

Esta opção exige Git e Python 3.11 ou superior. Execute em uma pasta escolhida por você:

```powershell
git clone https://github.com/RodrigoYuMatsumoto/receitas-tradicionais-canonicas.git
cd receitas-tradicionais-canonicas
python -m venv .venv
.venv\Scripts\python.exe -m pip install .
.venv\Scripts\python.exe -m receitas_tradicionais onboarding
```

Para mostrar somente o checklist em linguagem comum, use `.venv\Scripts\python.exe -m receitas_tradicionais iniciar`. Esse comando não lê respostas nem salva perfil. `onboarding` é a alternativa técnica interativa que devolve JSON.

No Linux ou macOS, troque `.venv\Scripts\python.exe` por `.venv/bin/python`. O onboarding devolve um perfil em JSON e não grava as respostas automaticamente. Para uso cotidiano, a conversa com a IA costuma ser mais simples.

O pacote fixa MCP 2.3.0 e Pydantic 2.14.2. Atualizar essas dependências exige os testes de integração, além da troca dos números.

## Entenda a conexão MCP

No transporte `stdio`, o cliente inicia o Python instalado e conversa com ele pela entrada e saída padrão. Não é necessário abrir porta. O servidor oferece:

| Ferramenta | Para que serve |
|---|---|
| `onboarding_questions` | Fornecer checklist com exemplos e primeira mensagem pronta. |
| `plan_research` | Planejar a pesquisa após perfil e prato confirmados. |
| `validate_research` | Conferir o registro das sete fontes. |
| `validate_delivery` | Conferir a entrega e as exclusões do perfil incorporado. |

A instrução integral agora está embarcada no pacote, na inicialização MCP e no recurso `receitas://project/instructions`. Ela funciona fora da pasta do clone. Caso o cliente não aplique as instruções recebidas do servidor, carregue também o prompt completo no projeto ou na sessão, como no exemplo Claude Code abaixo.

O MCP não pesquisa na web, não chama modelos, não salva perfis e não altera configurações globais. A IA conectada fornece busca e agentes. Aprovação estrutural não comprova, sozinha, leitura real ou tradição culinária.

## Claude Code: configuração ensaiada

O ensaio de 31/10/2026 usou **Claude Code 2.1.304**, MCP local e instrução completa anexada à sessão. Houve chamadas reais às quatro ferramentas, aceitação do lote de sete fontes, rejeição do lote de seis e rejeição de entrega incompatível com uma exclusão fictícia. Outro teste pediu escolha entre sentidos de canjica antes de pesquisar. Isso não foi uma nova pesquisa culinária nem um estudo de usabilidade.

1. Copie [o modelo Claude Code](../configs/claude_code.json) para `.local/claude_code.json` no clone. Crie a pasta `.local` se necessário. Se o arquivo já existir, use outro nome para preservar a configuração anterior.
2. No arquivo copiado, substitua `CAMINHO_ABSOLUTO_DO_PYTHON` pelo executável do ambiente instalado. Use caminho absoluto; no Windows, barras simples `/` evitam escapes no JSON. Mantenha o arquivo preenchido apenas na sua máquina.
3. Abra uma sessão interativa a partir da raiz do clone:

```powershell
claude --mcp-config .local/claude_code.json --strict-mcp-config --append-system-prompt-file prompts/INSTRUCAO_PROJETO.md
```

Diga: “Vamos configurar minha cozinha. Comece pelo checklist com exemplos”. A IA consulta as ferramentas nos bastidores e mostra diretamente a pergunta prática. A configuração vale para essa execução. `--strict-mcp-config` restringe os servidores MCP aos fornecidos no arquivo; as demais políticas e permissões do Claude continuam aplicáveis. O modo interativo segue a política de histórico do aplicativo.

Para um diagnóstico curto sem persistir a sessão local do Claude:

```powershell
claude --print --no-session-persistence --max-budget-usd 0.50 --mcp-config .local/claude_code.json --strict-mcp-config --append-system-prompt-file prompts/INSTRUCAO_PROJETO.md "Liste as quatro ferramentas do MCP receitas e chame onboarding_questions. Não pesquise nem salve arquivos."
```

Os nomes das ferramentas podem aparecer com o prefixo `mcp__receitas__`. A opção de orçamento aplica-se ao modo `--print`. O arquivo de prompt evita exceder o limite de argumentos do Windows ao transportar instruções longas; foi usado no ensaio final da candidata. O ensaio automatizado também limitou as ferramentas permitidas às quatro deste servidor, usou diretório temporário e não alterou configuração global. Não usou modo de permissões irrestritas nem modo mínimo de autenticação. A ausência de persistência local não altera a política de histórico ou retenção do provedor.

As opções acima foram conferidas em `claude --help` e na [referência oficial da CLI](https://code.claude.com/docs/en/cli-reference). A [documentação oficial MCP](https://code.claude.com/docs/en/mcp) explica conexão, permissões e políticas gerenciadas.

## Gemini CLI: modelo disponível, sem homologação local

O [modelo Gemini CLI](../configs/gemini_cli.json) apresenta o bloco `mcpServers` para o arquivo `.gemini/settings.json` da pasta de trabalho escolhida. Preencha o executável e mescle apenas esse bloco com configurações existentes; não substitua um arquivo inteiro nem altere o perfil global. O modelo mantém confirmações de ferramentas, conforme a [documentação oficial do Gemini CLI](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md).

O ensaio com **Gemini CLI 0.61.0** foi recusado pelo provedor com `UNSUPPORTED_CLIENT`, antes de qualquer chamada de modelo ou ferramenta MCP. Portanto, o exemplo não é comprovação de compatibilidade funcional nesta instalação. Não foi feita nova tentativa nem alteração de credenciais ou da confiança da pasta para contornar a recusa. Use a instrução portátil na interface web enquanto esse cliente estiver indisponível; consulte [clientes testados](CLIENTES_TESTADOS.md) para o estado dos ensaios web.

Em uma instalação elegível, a futura conferência começa na pasta do projeto com `gemini --allowed-mcp-server-names receitas`. Esse comando foi conferido no help local, mas seu funcionamento com o servidor ainda exige novo ensaio. Reveja normalmente as solicitações de confiança e permissão apresentadas pelo aplicativo.

## Como reconhecer uma conexão funcional

A IA deve reconhecer as quatro ferramentas, chamar `onboarding_questions` e mostrar `first_message` diretamente, com grupos e exemplos, sem presumir ausência de restrições. Não deve usar a abertura técnica dos antigos exemplos da 1.0.0. Um nome ambíguo exige opções com ingredientes básicos antes da escolha. Depois, o plano precisa conservar o nome confirmado como primeira consulta.

Na candidata 2.0.0-rc.1, `receitas://project/checklist` permite ler o checklist e os esquemas incluem `kitchen` e `card`. O cartão de receita em `Delivery.recipe_card` alimenta `practical_ready`; o antigo `ok` continua indicando somente a conferência documental. `preparation_ready` também considera as ações humanas aplicáveis antes de começar. Veja a [revisão da jornada](REVISAO_JORNADA_2_0.md) para migração, compatibilidade e testes da candidata; os ensaios históricos abaixo pertencem à versão indicada em cada registro.

Para uma verificação completa, o cliente deve aceitar o lote real de sete fontes e rejeitar uma cópia com seis. Também deve rejeitar entrega que recomende ingrediente explicitamente excluído. O relato precisa distinguir esses dados de teste de uma pesquisa nova. Se só houver texto simulando chamadas, a conexão ainda não foi comprovada.

Os exemplos podem ser conferidos diretamente:

```powershell
.venv\Scripts\python.exe -m receitas_tradicionais validate examples/feijoada_revalidada.json
.venv\Scripts\python.exe -m receitas_tradicionais validate examples/pesquisa_sintetica.json
.venv\Scripts\python.exe -m receitas_tradicionais validate examples/feijoada_pesquisa.json
.venv\Scripts\python.exe -m receitas_tradicionais schema
```

Os dois primeiros retornam código 0 para estrutura aceita. O registro histórico retorna código 1 porque seus retries não foram medidos e não contém os novos estados de qualificação; as lacunas foram preservadas. O comando `schema` exporta contratos e não pesquisa.

## Atualização e retirada

Para atualizar, preserve a configuração particular, leia o changelog e instale a nova versão em outro ambiente antes de trocar o executável em uso. Para voltar, aponte para o ambiente anterior. No Claude Code iniciado pelos comandos acima, basta encerrar e deixar de fornecer o arquivo. No Gemini CLI, remova apenas a entrada `receitas` do arquivo local usado. O projeto não instala tarefas recorrentes.

Confiança: alta nos comportamentos observados do Claude Code e nos testes do pacote; limitada nos demais clientes e interfaces, conforme [clientes testados](CLIENTES_TESTADOS.md).

Pendências: ensaio funcional do Gemini CLI em instalação elegível e estudo de compreensão com usuários finais. Outras limitações e a cobertura de cada versão estão em [verificação](VERIFICACAO.md).
