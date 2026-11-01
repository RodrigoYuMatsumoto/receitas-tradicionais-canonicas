"""Apresentação humana determinística, sem arquivos de saída nem execução de conteúdo."""

from __future__ import annotations

import json
import re

from .core import validate_delivery
from .models import Delivery, GateIssue

_MACHINE_SPANS = re.compile(r"```[\s\S]*?```|`[^`\n]*`|https?://[^\s<>\"'`]+|(?m:^(?:\$ |> |python |python3 |receitas |git |npm |pip ).*$)")


def human_text(value: str) -> str:
    """Normaliza prosa; mantém URLs, código marcado e objetos JSON reconhecidos."""
    protected: list[tuple[int, int]] = [(match.start(), match.end()) for match in _MACHINE_SPANS.finditer(value)]
    decoder = json.JSONDecoder()
    for match in re.finditer(r"[\[{]", value):
        start = match.start()
        if any(left <= start < right for left, right in protected):
            continue
        try:
            parsed, length = decoder.raw_decode(value[start:])
        except ValueError:
            continue
        if isinstance(parsed, (dict, list)):
            protected.append((start, start + length))
    protected.sort()
    opening = True

    def prose(text: str) -> str:
        nonlocal opening
        text = text.translate({0x2013: "-", 0x2014: "-"})
        result = []
        for char in text:
            if char == chr(34):
                result.append("“" if opening else "”")
                opening = not opening
            else:
                result.append(char)
                if char == "“":
                    opening = False
                elif char == "”":
                    opening = True
        return "".join(result)

    output = []
    cursor = 0
    for start, end in protected:
        if start < cursor:
            continue
        output.extend((prose(value[cursor:start]), value[start:end]))
        cursor = end
    output.append(prose(value[cursor:]))
    return "".join(output)


def _plain_action(issue: GateIssue) -> str:
    specific = {
        "ingrediente_restrito": "Retire ou substitua o ingrediente que você pediu para evitar antes de usar esta receita.",
        "restricao_na_ficha": "A ficha ainda menciona um ingrediente que você pediu para evitar. Revise ingredientes, compras e adaptações.",
        "restricao_nas_etapas": "Corrija a etapa que ainda usa um ingrediente excluído.",
        "restricao_nas_notas": "Corrija a adaptação que ainda usa um ingrediente excluído.",
        "realcador_adicionado": "Retire o realçador comercial para respeitar a escolha de cozinhar sem ele.",
        "ficha_pratica_ausente": "Complete as quantidades, o rendimento, os tempos, os utensílios e os sinais de ponto da receita.",
        "quantidade_pendente": "Complete a quantidade indicada. Para ajustar a gosto, explique como adicionar aos poucos e observar ou provar o resultado.",
        "tempos_inconsistentes": "Corrija os tempos: o total precisa incluir o trabalho e as esperas.",
        "tempo_indisponivel": "O preparo demora mais que o tempo disponível. Escolha outro horário ou outro preparo antes de começar.",
        "rendimento_divergente": "Ajuste as quantidades ao número de pessoas ou confirme o rendimento diferente.",
        "estimativa_nao_explicita": "Indique claramente que o rendimento é estimado.",
        "escala_sem_calculo": "Explique de quantas para quantas porções as quantidades foram ajustadas.",
        "inventarios_divergentes": "Faça a lista de ingredientes e as quantidades da ficha corresponderem à mesma receita.",
        "etapas_divergentes": "Corrija as instruções para que a ficha mostre o mesmo preparo que foi conferido.",
        "compras_nao_autorizadas": "A receita ainda pede compras. Ajuste-a ao que há em casa ou confirme se pode comprar.",
        "equipamento_nao_confirmado": "Confirme o tipo e a capacidade dos utensílios necessários antes de escolher este preparo.",
        "busca_do_detalhe_nao_registrada": "Informe se a comparação encontrou algum detalhe especial aplicável. Se não encontrou, diga isso sem inventar um truque.",
        "padrao_alimentar_pendente": "A escolha alimentar ainda precisa ser traduzida em ingredientes que esta receita deve evitar; esclareça somente as dúvidas necessárias.",
        "rotulos_pendentes": "Antes de preparar, confira os ingredientes e os avisos dos rótulos dos produtos compostos.",
        "contato_cruzado_pendente": "Antes de preparar, confira utensílios, superfícies e ingredientes que possam ter contato com o alimento evitado por alergia.",
        "duvidas_alimentares_pendentes": "Esclareça a dúvida sobre o alimento a evitar antes de começar o preparo.",
        "onboarding_pendente": "Confirme os ingredientes a evitar e as informações da sua cozinha.",
        "ambiguidade_pendente": "Escolha qual versão do prato deseja, comparando os ingredientes que distinguem cada opção.",
        "inventario_ausente": "Complete a lista de ingredientes antes de apresentar o preparo.",
        "etapas_ausentes": "Complete os passos do preparo antes de apresentar a receita.",
    }
    if issue.code in specific:
        return specific[issue.code]
    if issue.code.startswith("alcool_"):
        return "Ajuste o preparo para cumprir a escolha de cozinhar sem álcool."
    if issue.code.startswith(("fonte", "duplicado_", "pais_", "independencia_", "leitura_", "secoes_", "data_", "cronologia_", "contagem_", "trajetoria", "saber_", "detalhes_", "reformulacoes_", "busca_", "refinamento_", "teto_", "paginas_")):
        return "Complete ou corrija a pesquisa das sete receitas e suas fontes antes de apresentar este preparo."
    return human_text(issue.message)


def _actions(issues: list[GateIssue]) -> list[str]:
    return list(dict.fromkeys(_plain_action(issue) for issue in issues))


def render_delivery(delivery: Delivery) -> tuple[str, int]:
    """Retorna somente texto e código de saída; jamais salva nem executa o conteúdo."""
    report = validate_delivery(delivery)
    if not report.ok or not report.practical_ready:
        actions = _actions([*report.issues, *report.action_items])
        lines = ["Esta receita ainda precisa de ajustes antes de apresentar o preparo.", ""]
        lines.extend(f"- {human_text(item)}" for item in actions)
        lines.extend(["", "Confiança: baixa enquanto estes ajustes estiverem pendentes.", "Pendências: resolver os itens acima."])
        return "\n".join(lines), 1

    card = delivery.recipe_card
    assert card is not None
    lines = [human_text(card.title), ""]
    actions = _actions(report.action_items)
    if actions:
        lines.extend(["Plano da receita. Antes de começar:", *[f"- {human_text(item)}" for item in actions], ""])
    lines.extend([
        f"Rendimento: {card.servings} porções. {human_text(card.yield_note)}",
        f"Tempo total: {card.total_minutes} minutos. Tempo de trabalho: {card.active_minutes} minutos.",
        f"Utensílios: {', '.join(human_text(item) for item in card.equipment)}.",
        "", "Ingredientes", "",
    ])
    for ingredient in card.ingredients:
        if ingredient.quantity.casefold() == "a gosto":
            line = f"- {human_text(ingredient.name)}: a gosto (medida para ajustar: {human_text(ingredient.unit)})"
        else:
            line = f"- {human_text(ingredient.name)}: {human_text(ingredient.quantity)} {human_text(ingredient.unit)}"
        if ingredient.household_measure:
            line += f" ({human_text(ingredient.household_measure)})"
        if ingredient.note:
            line += f". {human_text(ingredient.note)}"
        lines.append(line)
    lines.extend(["", "Como fazer", ""])
    for index, step in enumerate(card.steps, 1):
        lines.append(f"{index}. {human_text(step.instruction)}")
        lines.append(f"   Como reconhecer o ponto: {human_text(step.observable_cue)}")
        if step.time_hint:
            lines.append(f"   Tempo desta etapa: {human_text(step.time_hint)}")
    source_map = {source.id: source for source in delivery.research.sources}
    if card.flavor_detail is not None:
        detail = card.flavor_detail
        lines.extend(["", "Detalhe de sabor", "", human_text(detail.action), human_text(detail.effect)])
        for source_id in detail.source_ids:
            source = source_map[source_id]
            lines.append(f"Fonte do detalhe: {human_text(source.title)} - {source.url}")
    elif card.detail_search_note:
        lines.extend(["", human_text(card.detail_search_note)])
    if card.shopping_list:
        lines.extend(["", "O que falta comprar", "", *[f"- {human_text(item)}" for item in card.shopping_list]])
    adaptations = list(dict.fromkeys([*delivery.adaptation_notes, *card.adaptations]))
    if adaptations:
        lines.extend(["", "Adaptações deste preparo", "", *[f"- {human_text(item)}" for item in adaptations]])
    lines.extend(["", "As sete receitas consultadas", ""])
    for index, source_id in enumerate(card.source_ids, 1):
        source = source_map[source_id]
        lines.append(f"{index}. {human_text(source.title)}. {human_text(source.publisher)} - {source.url}")
    lines.extend(["", "Confiança: média, baseada nas fontes e revisões declaradas."])
    if actions:
        lines.append("Pendências: " + " ".join(human_text(item) for item in actions))
    else:
        lines.append("Pendências: conferir as fontes e as condições reais do preparo.")
    return "\n".join(lines), 0
