"""Planejamento e controles determinísticos, sem busca externa ou geração de receitas."""

from __future__ import annotations

import unicodedata
from datetime import date
from importlib.resources import files
from urllib.parse import quote, unquote, urlsplit, urlunsplit

from .models import Delivery, GateIssue, Request, ResearchBatch, ValidationReport

PROJECT_INSTRUCTIONS = files("receitas_tradicionais").joinpath("INSTRUCAO_PROJETO.md").read_text(encoding="utf-8")

RESEARCH_LIMITATIONS = [
    "Controle documental local: URLs, país, grupo e autoria são declarações que exigem revisão semântica humana.",
    "A ferramenta não acessa páginas nem comprova leitura, proveniência, tradição ou independência editorial.",
    "Aprovação da pesquisa não aprova ingredientes para o perfil nem substitui validate_delivery.",
    "Notas e comentários podem estar declarados como inacessíveis; isso não comprova sua ausência nem sua leitura.",
    "As qualificações confirmadas são declarações do pesquisador e do revisor; não são comprovação automática de país ou independência.",
]
DELIVERY_LIMITATIONS = [
    "A correspondência usa somente nomes, aliases e componentes declarados; não detecta todos os alérgenos.",
    "A declaração de revisão dos rótulos não comprova ausência de contaminação ou contato cruzado.",
    "O resultado não certifica segurança alimentar nem representa orientação clínica.",
    "Técnicas, identidade editorial, direitos autorais e fidelidade da adaptação exigem revisão humana.",
    "A detecção de termos explícitos nas etapas e notas de adaptação é conservadora, não interpreta negações e pode exigir reformulação do texto.",
]

ALCOHOL_TERMS = frozenset({
    "alcool", "alcohol", "etanol", "ethanol", "cerveja", "beer", "biere", "cerveza",
    "vinho", "wine", "vino", "vin", "champagne", "espumante", "prosecco", "cava",
    "rum", "rhum", "cachaca", "vodca", "vodka", "whisky", "whiskey", "bourbon",
    "conhaque", "cognac", "brandy", "tequila", "gin", "gim", "licor", "liqueur",
    "sake", "saque", "mirin", "marsala", "sherry", "xerez", "vermouth", "vermute",
    "aguardente", "aguardiente", "pisco", "mezcal", "cider", "cidra", "cognac",
    "chopp", "sidra", "soju", "shaoxing",
})


def normalize_text(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value).casefold()
    letters = "".join(c for c in decomposed if not unicodedata.combining(c))
    return " ".join("".join(c if c.isalnum() else " " for c in letters).split())


def normalize_url(value: str) -> str:
    """Agrupa variações de rastreamento; pode exigir revisão de falsos duplicados."""
    parsed = urlsplit(value)
    host = (parsed.hostname or "").lower().rstrip(".").removeprefix("www.").encode("idna").decode("ascii")
    port = parsed.port
    if port and not (parsed.scheme.lower() == "http" and port == 80) and not (parsed.scheme.lower() == "https" and port == 443):
        host += f":{port}"
    path = quote(unquote(parsed.path), safe="/:-._~").rstrip("/") or "/"
    return urlunsplit(("https", host, path, "", ""))


def onboarding_questions() -> dict:
    return {
        "questions": [
            {"field": "excluded_ingredients", "question": "Quais ingredientes devem ser excluídos? Informe também os nomes alternativos que conhece."},
            {"field": "allergies", "question": "Há alergias alimentares já conhecidas que deseja declarar? Não é necessário informar diagnóstico ou identidade."},
            {"field": "intolerances", "question": "Há intolerâncias alimentares já conhecidas que deseja declarar?"},
            {"field": "preferences", "question": "Quais são suas preferências alimentares?"},
            {"field": "equipment", "question": "Quais utensílios e equipamentos tem disponíveis?"},
            {"field": "region", "question": "Deseja informar uma região culinária ampla para contextualizar os ingredientes? Não informe endereço."},
            {"field": "servings", "question": "Para quantas porções deseja preparar?"},
            {"field": "language_style", "question": "Prefere linguagem simples ou técnica?"},
            {"field": "onboarding_confirmed", "question": "Confirma que revisou essas informações e deseja usá-las neste pedido?"},
        ],
        "alcohol_free_default": True,
        "privacy": "O servidor não persiste perfis. O host pode ter sua própria política de histórico.",
        "next_step": "Antes da pesquisa, confirme nome, país, variante e ingredientes característicos para resolver possíveis homônimos.",
    }


def request_issues(request: Request) -> list[GateIssue]:
    issues = []
    if not request.profile.onboarding_confirmed:
        issues.append(GateIssue(code="onboarding_pendente", message="Conclua e confirme o levantamento alimentar antes da pesquisa.", path="request.profile.onboarding_confirmed"))
    if not request.ambiguity_resolved:
        issues.append(GateIssue(code="ambiguidade_pendente", message="Resolva o nome, o país, a variante e os ingredientes característicos do prato antes da pesquisa.", path="request.ambiguity_resolved"))
    return issues


def plan_research(request: Request) -> dict:
    issues = request_issues(request)
    if issues:
        return {"ok": False, "issues": [item.model_dump() for item in issues], "queries": []}
    return {
        "ok": True,
        "queries": [{"text": request.dish, "derived_from": None}],
        "target_sources": 7,
        "limits": {"queries": 32, "pages_read": 40, "researchers": 3, "reformulations_per_track": 2},
        "next_steps": [
            "O host pesquisa o nome do prato e lê os resultados antes de formular refinamentos regionais.",
            "Registre refinamentos posteriores em queries, usando derived_from para indicar a evidência de origem.",
            "Separe os papéis de pesquisador-base, pesquisador doméstico e regional, e auditor; declare quando forem sequenciais.",
            "Selecione sete receitas-fontes de grupos distintos, com país editorial comprovado e pelo menos uma prática doméstica documentada.",
            "Documente detalhes minoritários, técnicas e divergências; submeta o lote a validate_research antes de sintetizar.",
        ],
        "host_required": "Busca web, leitura, delegação e revisão semântica pertencem ao host; este servidor não as executa.",
    }


def validate_research(batch: ResearchBatch, *, today: date | None = None) -> ValidationReport:
    checked_at = today or date.today()
    issues = request_issues(batch.request)

    def add(code: str, message: str, path: str) -> None:
        issues.append(GateIssue(code=code, message=message, path=path))

    if len(batch.sources) != 7:
        add("contagem_fontes", "O lote precisa conter exatamente sete receitas-fontes.", "sources")
    if batch.reformulations_by_track.base is None or batch.reformulations_by_track.domestic_regional is None:
        add("reformulacoes_nao_medidas", "As reformulações por trajetória não foram medidas; não substitua a lacuna por zero.", "reformulations_by_track")
    if len(batch.queries) > 32:
        add("teto_consultas", "A trajetória excede o teto de 32 consultas.", "queries")
    if batch.pages_read > 40:
        add("teto_paginas", "A trajetória excede o teto de 40 páginas lidas.", "pages_read")
    if batch.pages_read < len(batch.sources):
        add("paginas_insuficientes", "A contagem declarada de páginas lidas precisa abranger as receitas-fontes.", "pages_read")
    if sorted(batch.completed_tracks) != ["base", "domestic_regional"]:
        add("trajetorias_pendentes", "Declare a conclusão das duas trajetórias distintas: base e doméstica/regional.", "completed_tracks")
    if {source.research_track for source in batch.sources} != {"base", "domestic_regional"}:
        add("fontes_por_trajetoria", "Vincule pelo menos uma receita-fonte a cada trajetória de pesquisa.", "sources")
    if not batch.queries or batch.queries[0].text != batch.request.dish or batch.queries[0].derived_from is not None:
        add("busca_inicial", "A primeira consulta precisa conter somente o nome canônico do prato, sem refinamento prévio.", "queries")
    for index, query in enumerate(batch.queries[1:], start=1):
        if not query.derived_from:
            add("refinamento_sem_origem", "Documente a evidência que motivou o refinamento da consulta.", f"queries.{index}.derived_from")
    seen: dict[str, set[str]] = {name: set() for name in ("id", "url", "editorial_group", "provenance_origin")}
    for index, source in enumerate(batch.sources):
        path = f"sources.{index}"
        for field in seen:
            raw = getattr(source, field)
            canonical = normalize_url(raw) if field in {"url", "provenance_origin"} else normalize_text(raw)
            if not canonical or canonical in seen[field]:
                add(f"duplicado_{field}", "Identificador, URL, grupo editorial e origem precisam ser distintos e identificáveis.", f"{path}.{field}")
            seen[field].add(canonical)
        if source.country != batch.request.country:
            add("pais_divergente", "A fonte precisa estar editorialmente estabelecida no país de origem informado para o prato.", f"{path}.country")
        if source.editorial_country_evidence.verification != "confirmed":
            add("pais_editorial_pendente", "Conclua e registre a qualificação da relação editorial com o país antes de admitir a fonte.", f"{path}.editorial_country_evidence.verification")
        if source.provenance_verification != "confirmed":
            add("independencia_pendente", "Conclua e registre a qualificação da origem e da independência editorial antes de admitir a fonte.", f"{path}.provenance_verification")
        if source.read_status != "complete":
            add("leitura_incompleta", "Trecho de busca ou página indisponível não constitui receita-fonte integralmente lida.", f"{path}.read_status")
        if source.sections.ingredients != "read" or source.sections.method != "read":
            add("secoes_essenciais_pendentes", "Leia ingredientes e preparo para admitir a receita-fonte no lote.", f"{path}.sections")
        if source.accessed_at > checked_at or (source.publication_date and source.publication_date > checked_at):
            add("data_futura", "Datas de acesso e publicação não podem estar no futuro.", path)
        if source.publication_date and source.publication_date > source.accessed_at:
            add("cronologia_invalida", "A publicação informada é posterior à data de acesso.", path)
        if not source.ingredients:
            add("ingredientes_ausentes", "Cada receita-fonte precisa ter ingredientes documentados.", f"{path}.ingredients")
    if not any(source.kind == "domestic" for source in batch.sources):
        add("saber_domestico_ausente", "Inclua pelo menos uma receita-fonte que documente prática doméstica.", "sources")
    if not any(source.detail_notes for source in batch.sources):
        add("detalhes_ausentes", "Registre detalhes específicos e divergências documentadas, sem inventar segredos.", "sources")
    return ValidationReport(ok=not issues, issues=issues, limitations=RESEARCH_LIMITATIONS, checked_at=checked_at)


def _ingredient_match(restriction: str, label: str) -> bool:
    left, right = normalize_text(restriction), normalize_text(label)
    if not left or not right:
        return False
    return f" {left} " in f" {right} " or f" {right} " in f" {left} "


def validate_delivery(delivery: Delivery, *, today: date | None = None) -> ValidationReport:
    report = validate_research(delivery.research, today=today)
    issues = [issue.model_copy(update={"path": f"research.{issue.path}"}) for issue in report.issues]
    profile = delivery.research.request.profile

    def add(code: str, message: str, path: str) -> None:
        issues.append(GateIssue(code=code, message=message, path=path))

    if not delivery.ingredients:
        add("inventario_ausente", "Declare o inventário completo de ingredientes da entrega operacional.", "ingredients")
    if not delivery.steps:
        add("etapas_ausentes", "Declare as etapas da entrega operacional.", "steps")
    if not delivery.labels_reviewed:
        add("rotulos_pendentes", "A pessoa responsável precisa conferir o inventário, os componentes e os rótulos aplicáveis.", "labels_reviewed")
    if profile.allergies and not delivery.cross_contact_reviewed:
        add("contato_cruzado_pendente", "Com alergias declaradas, a pessoa responsável precisa revisar também o contato cruzado.", "cross_contact_reviewed")
    restrictions = profile.excluded_ingredients + profile.allergies + profile.intolerances
    for index, ingredient in enumerate(delivery.ingredients):
        labels = [ingredient.name, *ingredient.aliases, *ingredient.components]
        if ingredient.alcohol or any(ALCOHOL_TERMS.intersection(normalize_text(label).split()) for label in labels):
            add("alcool_na_entrega", "A política deste projeto exige entrega sem álcool.", f"ingredients.{index}.alcohol")
        if any(_ingredient_match(restriction, label) for restriction in restrictions for label in labels):
            add("ingrediente_restrito", "O inventário contém correspondência com uma exclusão, alergia ou intolerância declarada.", f"ingredients.{index}")
    for index, step in enumerate(delivery.steps):
        if ALCOHOL_TERMS.intersection(normalize_text(step).split()):
            add("alcool_nas_etapas", "As etapas contêm termo explícito incompatível com a política sem álcool.", f"steps.{index}")
        if any(_ingredient_match(restriction, step) for restriction in restrictions):
            add("restricao_nas_etapas", "As etapas contêm correspondência textual com uma restrição declarada.", f"steps.{index}")
    for index, note in enumerate(delivery.adaptation_notes):
        if ALCOHOL_TERMS.intersection(normalize_text(note).split()):
            add("alcool_nas_notas", "As notas de adaptação contêm termo explícito incompatível com a política sem álcool.", f"adaptation_notes.{index}")
        if any(_ingredient_match(restriction, note) for restriction in restrictions):
            add("restricao_nas_notas", "As notas de adaptação contêm correspondência textual com uma restrição declarada.", f"adaptation_notes.{index}")
    return ValidationReport(ok=not issues, issues=issues, limitations=[*RESEARCH_LIMITATIONS, *DELIVERY_LIMITATIONS], checked_at=report.checked_at)
