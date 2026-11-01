"""Planejamento e controles determinísticos, sem busca externa ou geração de receitas."""

from __future__ import annotations

import unicodedata
import re
from datetime import date
from fractions import Fraction
from importlib.resources import files
from urllib.parse import quote, unquote, urlsplit, urlunsplit

from .models import Delivery, GateIssue, Request, ResearchBatch, ValidationReport
from .onboarding import onboarding_questions

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
    "A pendência de ingrediente genérico usa núcleos de restrições compostas, nomes declarados e uma lista explícita de descritores de preparo em pt-BR; não é uma ontologia alimentar nem comprova compatibilidade clínica.",
    "A ação de conferência de rótulos depende de label_required ou components declarados pelo host; omissões desses campos podem ocultar a necessidade de conferência.",
    "A declaração de revisão dos rótulos não comprova ausência de contaminação ou contato cruzado.",
    "O resultado não certifica segurança alimentar nem representa orientação clínica.",
    "Técnicas, identidade editorial, direitos autorais e fidelidade da adaptação exigem revisão humana.",
    "A detecção de termos explícitos nas etapas e notas de adaptação é conservadora, não interpreta negações e pode exigir reformulação do texto.",
    "practical_ready verifica a completude declarada da ficha, não prova viabilidade, preço, rendimento real ou sabor.",
    "preparation_ready registra a ausência de pendências explícitas neste contrato, sem certificar segurança individual.",
    "A revisão de padrões alimentares é uma declaração semântica do host; não prova decomposição completa nem constitui avaliação clínica.",
]

FLAVOR_ENHANCER_TERMS = ("ajinomoto", "glutamato monossodico", "monosodium glutamate", "msg", "e621", "ins 621")

ALCOHOL_TERMS = frozenset({
    "alcool", "alcohol", "etanol", "ethanol", "cerveja", "beer", "biere", "cerveza",
    "vinho", "wine", "vino", "vin", "champagne", "espumante", "prosecco", "cava",
    "rum", "rhum", "cachaca", "vodca", "vodka", "whisky", "whiskey", "bourbon",
    "conhaque", "cognac", "brandy", "tequila", "gin", "gim", "licor", "liqueur",
    "sake", "saque", "mirin", "marsala", "sherry", "xerez", "vermouth", "vermute",
    "aguardente", "aguardiente", "pisco", "mezcal", "cider", "cognac",
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
    if ":" in host:
        host = f"[{host}]"
    port = parsed.port
    if port and not (parsed.scheme.lower() == "http" and port == 80) and not (parsed.scheme.lower() == "https" and port == 443):
        host += f":{port}"
    path = quote(unquote(parsed.path), safe="/:-._~").rstrip("/") or "/"
    return urlunsplit(("https", host, path, "", ""))


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
        "kitchen": request.kitchen.model_dump(mode="json"),
        "practical_checks": [
            "Compare o tempo total da fonte, incluindo molho, descanso e espera, com o tempo disponível. Se não couber, explique e peça a escolha; não prometa acelerar a técnica.",
            "Confira equipamento, capacidade da panela, porções, ingredientes disponíveis e compras permitidas antes de montar a ficha.",
            "Orçamento não informado é desconhecido; preço estimado não é cotação local confirmada.",
            "Dúvidas alimentares permanecem registradas; nenhuma resposta em branco ou não sei se transforma em ausência de restrições.",
        ],
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


def _plural_forms(token: str) -> set[str]:
    """Gera flexões regulares explícitas sem reduzir radicais de palavras distintas."""
    forms = set()
    if token.endswith("ao"):
        forms.update({token[:-2] + ending for ending in ("oes", "aes", "aos")})
    if token.endswith("al"):
        forms.add(token[:-2] + "ais")
    if token.endswith("el"):
        forms.add(token[:-2] + "eis")
    if token.endswith("ol"):
        forms.add(token[:-2] + "ois")
    if token.endswith("ul"):
        forms.add(token[:-2] + "uis")
    if token.endswith("m"):
        forms.add(token[:-1] + "ns")
    elif token.endswith(("r", "s", "z")):
        forms.add(token + "es")
    elif token.endswith(("a", "e", "i", "o", "u")):
        forms.add(token + "s")
    return forms


def _ingredient_match(restriction: str, label: str, *, allow_generic_label: bool = True) -> bool:
    left, right = normalize_text(restriction).split(), normalize_text(label).split()
    if not left or not right:
        return False

    def contained(short: list[str], long: list[str]) -> bool:
        return any(
            all(a == b or b in _plural_forms(a) or a in _plural_forms(b)
                for a, b in zip(short, long[index:index + len(short)]))
            for index in range(len(long) - len(short) + 1)
        )

    return contained(left, right) or (allow_generic_label and contained(right, left))


_GENERIC_FUNCTION_WORDS = frozenset({"a", "as", "o", "os", "de", "do", "da", "dos", "das", "e", "ou", "com", "em", "sem", "para", "por", "no", "na", "nos", "nas"})
# Lista limitada de descritores de preparo em pt-BR, sem inferir espécie ou variedade.
_PREPARATION_WORDS = frozenset(
    form
    for word in (
        "picado", "picada", "torrado", "torrada", "moido", "moida", "inteiro", "inteira",
        "triturado", "triturada", "cru", "crua", "fresco", "fresca", "seco", "seca",
        "ralado", "ralada", "laminado", "laminada", "cortado", "cortada", "cozido", "cozida",
        "assado", "assada", "descascado", "descascada", "congelado", "congelada", "desidratado",
        "desidratada", "salgado", "salgada", "fino", "fina", "grosso", "grossa", "natural",
        "organico", "organica", "pedaco", "cubo", "casca", "sal", "po", "fritar", "assar", "cozinhar", "fritura",
    )
    for form in (word, *_plural_forms(word))
)


def _same_ingredient_word(left: str, right: str) -> bool:
    return left == right or right in _plural_forms(left) or left in _plural_forms(right)


def _ingredient_content(words: list[str]) -> list[str]:
    # A normalização também converte o nome geográfico Pará em para.
    return [word for index, word in enumerate(words) if word not in _GENERIC_FUNCTION_WORDS or (word == "para" and index > 0 and words[index - 1] in {"do", "da"})]


def _generic_ingredient_context(restriction: str, labels: list[str]) -> tuple[str, list[list[str]]] | None:
    """Qualificação lexical declarada, sem deduzir variedade de um adjetivo de preparo."""
    content = _ingredient_content(normalize_text(restriction).split())
    if len(content) < 2:
        return None
    # Palavras como sal e casca também podem ser o próprio ingrediente excluído.
    head = next((word for word in content if len(word) >= 3), None)
    if head is None:
        return None
    # A menção exata já recebe o bloqueio de restrição; não é uma identidade pendente.
    identified = [normalize_text(restriction).split()]
    for label in labels:
        words = normalize_text(label).split()
        if _ingredient_match(restriction, label):
            continue
        for index, word in enumerate(words):
            if not _same_ingredient_word(head, word):
                continue
            # Coordenação ou acompanhamento não identifica a variedade do núcleo.
            end = next((i for i in range(index + 1, len(words)) if words[i] in {"com", "e", "ou"}), len(words))
            identity = [term for term in _ingredient_content(words[index:end]) if term not in _PREPARATION_WORDS]
            if len(identity) >= 2:
                identified.append(words)
                break
    return head, identified


def _unresolved_generic_ingredient(words: list[str], context: tuple[str, list[list[str]]]) -> bool:
    """Uma menção qualificada não libera outras menções genéricas no mesmo texto."""
    head, identified = context
    positions = {index for index, word in enumerate(words) if _same_ingredient_word(head, word)}
    if not positions:
        return False
    covered = set()
    for label in identified:
        for start in range(len(words) - len(label) + 1):
            if all(_same_ingredient_word(left, right) for left, right in zip(label, words[start:start + len(label)])):
                covered.update(range(start, start + len(label)))
    return bool(positions - covered)


def _contains_alcohol(value: str) -> bool:
    """Desconsidera apenas nomes explícitos de vinagre, preservando outras bebidas no texto."""
    normalized = normalize_text(value)
    drinks = "|".join(re.escape(term) for term in sorted(ALCOHOL_TERMS, key=len, reverse=True))
    normalized = re.sub(rf"\bvinagre de (?:(?:arroz|apple|rice) )?(?:{drinks})(?: (?:tinto|branco|rose))?\b", " ", normalized)
    normalized = re.sub(rf"\b(?:(?:apple|rice) )?(?:{drinks}) vinegar\b", " ", normalized)
    return bool(ALCOHOL_TERMS.intersection(normalized.split()))


def _equipment_key(value: str) -> str:
    """Equivalências explícitas; nome genérico não comprova tipo nem capacidade."""
    normalized = normalize_text(value)
    aliases = {
        "panela comum": "panela",
        "airfryer": "air fryer",
        "fritadeira sem oleo": "air fryer",
        "microondas": "micro ondas",
    }
    return aliases.get(normalized, normalized)


def _positive_quantity(value: str, note: str | None) -> bool:
    """Aceita medidas numéricas legíveis; a unidade fica em campo separado."""
    if normalize_text(value) == "a gosto":
        adjustment = normalize_text(note or "")
        return bool(
            any(phrase in adjustment for phrase in ("por vez", "aos poucos"))
            and any(word in adjustment.split() for word in ("prove", "observe", "pare", "ajuste"))
        )
    # NFKC torna frações tipográficas legíveis; separa a parte inteira antes.
    separated = re.sub(r"(?<=\d)([\u00bc-\u00be\u2150-\u215e])", r" \1", value)
    normalized = unicodedata.normalize("NFKC", separated).replace(chr(0x2044), "/").strip()

    def scalar(part: str) -> Fraction | None:
        if re.fullmatch(r"\d+[.,]\d+|\d+", part):
            result = Fraction(part.replace(",", "."))
        elif re.fullmatch(r"\d+/\d+", part):
            numerator, denominator = part.split("/")
            if int(denominator) == 0:
                return None
            result = Fraction(int(numerator), int(denominator))
        elif re.fullmatch(r"\d+\s+\d+/\d+", part):
            whole, fraction = part.split()
            fractional = scalar(fraction)
            if fractional is None:
                return None
            result = Fraction(int(whole)) + fractional
        else:
            return None
        return result if result > 0 else None

    parts = re.split(r"\s*(?:-|\ba\b|\baté\b)\s*", normalized, flags=re.I)
    if len(parts) == 1:
        return scalar(parts[0]) is not None
    if len(parts) == 2:
        lower, upper = (scalar(part) for part in parts)
        return lower is not None and upper is not None and lower <= upper
    return False


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
    restrictions = profile.excluded_ingredients + profile.allergies + profile.intolerances
    for index, ingredient in enumerate(delivery.ingredients):
        labels = [ingredient.name, *ingredient.aliases, *ingredient.components]
        if ingredient.alcohol or any(_contains_alcohol(label) for label in labels):
            add("alcool_na_entrega", "A política deste projeto exige entrega sem álcool.", f"ingredients.{index}.alcohol")
        if any(_ingredient_match(restriction, label) for restriction in restrictions for label in labels):
            add("ingrediente_restrito", "O inventário contém correspondência com uma exclusão, alergia ou intolerância declarada.", f"ingredients.{index}")
        if profile.avoid_added_flavor_enhancers and (
            ingredient.added_flavor_enhancer or any(_ingredient_match(term, label) for term in FLAVOR_ENHANCER_TERMS for label in labels)
        ):
            add("realcador_adicionado", "O inventário contém realçador comercial incompatível com a preferência declarada.", f"ingredients.{index}")
    for index, step in enumerate(delivery.steps):
        if _contains_alcohol(step):
            add("alcool_nas_etapas", "As etapas contêm termo explícito incompatível com a política sem álcool.", f"steps.{index}")
        if any(_ingredient_match(restriction, step, allow_generic_label=False) for restriction in restrictions):
            add("restricao_nas_etapas", "As etapas contêm correspondência textual com uma restrição declarada.", f"steps.{index}")
    for index, note in enumerate(delivery.adaptation_notes):
        if _contains_alcohol(note):
            add("alcool_nas_notas", "As notas de adaptação contêm termo explícito incompatível com a política sem álcool.", f"adaptation_notes.{index}")
        if any(_ingredient_match(restriction, note, allow_generic_label=False) for restriction in restrictions):
            add("restricao_nas_notas", "As notas de adaptação contêm correspondência textual com uma restrição declarada.", f"adaptation_notes.{index}")
    for field in ("steps", "adaptation_notes"):
        if profile.avoid_added_flavor_enhancers:
            for index, text in enumerate(getattr(delivery, field)):
                if any(_ingredient_match(term, text) for term in FLAVOR_ENHANCER_TERMS):
                    add("realcador_adicionado", "O preparo contém realçador comercial incompatível com a preferência declarada.", f"{field}.{index}")

    actions: list[GateIssue] = []

    def action(code: str, message: str, path: str) -> None:
        actions.append(GateIssue(code=code, message=message, path=path))

    # O host decompõe o padrão em exclusões e revê a compatibilidade culinária.
    # O booleano registra sua declaração auditável, não um atestado humano ou clínico.
    declared_exclusions = {normalize_text(item) for item in profile.excluded_ingredients}
    for pattern in profile.dietary_patterns:
        matching = [item for item in delivery.dietary_pattern_review if normalize_text(item.pattern) == normalize_text(pattern)]
        if (
            len(matching) != 1
            or not matching[0].compatibility_reviewed
            or not {normalize_text(item) for item in matching[0].excluded_ingredients}.issubset(declared_exclusions)
        ):
            action("padrao_alimentar_pendente", "O host precisa traduzir o padrão em exclusões concretas e registrar a revisão da compatibilidade da receita; perguntar ao usuário somente ambiguidades reais.", "dietary_pattern_review")

    card = delivery.recipe_card
    if card is None:
        action("ficha_pratica_ausente", "Monte a ficha com quantidades, rendimento, tempos, utensílios e sinais de ponto antes de apresentar uma receita completa.", "recipe_card")
    else:
        source_ids = {source.id for source in delivery.research.sources}
        if len(set(card.source_ids)) != 7 or set(card.source_ids) != source_ids:
            action("fontes_da_ficha_divergentes", "Vincule a ficha às mesmas sete fontes selecionadas na pesquisa.", "recipe_card.source_ids")
        if card.active_minutes > card.total_minutes:
            action("tempos_inconsistentes", "O tempo ativo não pode exceder o tempo total, que inclui esperas.", "recipe_card.active_minutes")
        if profile.servings is None:
            action("porcoes_nao_confirmadas", "Confirme para quantas pessoas é a receita antes de aceitar o rendimento da ficha.", "research.request.profile.servings")
        elif card.servings != profile.servings:
            action("rendimento_divergente", "Ajuste a ficha às porções pedidas ou peça confirmação da diferença.", "recipe_card.servings")
        if card.yield_basis == "estimate" and "estim" not in normalize_text(card.yield_note):
            action("estimativa_nao_explicita", "Identifique expressamente o rendimento como estimativa.", "recipe_card.yield_note")
        if card.yield_basis == "scaled" and not any(c.isdigit() for c in card.yield_note):
            action("escala_sem_calculo", "Explique com números o rendimento original e o cálculo da adaptação.", "recipe_card.yield_note")
        inventory_names = [normalize_text(item.name) for item in delivery.ingredients]
        card_names = [normalize_text(item.name) for item in card.ingredients]
        if len(set(card_names)) != len(card_names) or set(card_names) != set(inventory_names):
            action("inventarios_divergentes", "A ficha e o inventário precisam conter os mesmos ingredientes, sem nomes duplicados.", "recipe_card.ingredients")
        if [normalize_text(step.instruction) for step in card.steps] != [normalize_text(step) for step in delivery.steps]:
            action("etapas_divergentes", "As instruções da ficha precisam corresponder às etapas efetivamente validadas.", "recipe_card.steps")
        for index, ingredient in enumerate(card.ingredients):
            if not set(ingredient.source_ids).issubset(source_ids):
                action("fonte_de_ingrediente_desconhecida", "Use somente IDs das receitas-fontes selecionadas.", f"recipe_card.ingredients.{index}.source_ids")
            if not _positive_quantity(ingredient.quantity, ingredient.note):
                action("quantidade_pendente", "Informe número positivo, fração, medida mista ou faixa. Para a gosto, registre uma nota com adição gradual e prova ou observação do ponto.", f"recipe_card.ingredients.{index}.quantity")
        if card.flavor_detail is not None and not set(card.flavor_detail.source_ids).issubset(source_ids):
            action("fonte_do_detalhe_desconhecida", "Ligue o detalhe de sabor a uma receita-fonte selecionada.", "recipe_card.flavor_detail.source_ids")
        if card.flavor_detail is None and not card.detail_search_note:
            action("busca_do_detalhe_nao_registrada", "Se não encontrou um detalhe de sabor aplicável, registre essa conclusão sem inventar um segredo.", "recipe_card.detail_search_note")
        kitchen = delivery.research.request.kitchen
        if kitchen.time_available_minutes is not None and card.total_minutes > kitchen.time_available_minutes:
            action("tempo_indisponivel", "O tempo total excede o disponível. Peça ao usuário que escolha outro horário ou outro preparo.", "recipe_card.total_minutes")
        if kitchen.shopping_allowed is False and card.shopping_list:
            action("compras_nao_autorizadas", "A pessoa escolheu cozinhar sem compras; revise o plano com ela.", "recipe_card.shopping_list")
        if not profile.equipment:
            action("equipamento_nao_confirmado", "Confirme quais utensílios da ficha estão disponíveis antes de usar o plano.", "recipe_card.equipment")
        else:
            missing = [item for item in card.equipment if _equipment_key(item) not in {_equipment_key(known) for known in profile.equipment}]
            if missing:
                action("equipamento_nao_confirmado", "Confirme os utensílios da ficha que ainda não constam entre os disponíveis; não troque a técnica automaticamente.", "recipe_card.equipment")
        # Todos os textos que a pessoa recebe passam pelas mesmas exclusões.
        # Notas, lista de compras e detalhe de sabor não são canais para reintroduzir ingredientes.
        texts: list[tuple[str, str]] = [("title", card.title), ("yield_note", card.yield_note)]
        for index, item in enumerate(card.ingredients):
            for field, text in [("name", item.name), ("quantity", item.quantity), ("unit", item.unit), ("note", item.note), ("household_measure", item.household_measure)]:
                if text is not None:
                    texts.append((f"ingredients.{index}.{field}", text))
            texts.extend((f"ingredients.{index}.aliases.{i}", text) for i, text in enumerate(item.aliases))
            texts.extend((f"ingredients.{index}.components.{i}", text) for i, text in enumerate(item.components))
            if item.alcohol:
                add("alcool_na_ficha", "A política deste projeto exige entrega sem álcool.", f"recipe_card.ingredients.{index}.alcohol")
            if profile.avoid_added_flavor_enhancers and item.added_flavor_enhancer:
                add("realcador_adicionado", "A ficha contém realçador comercial incompatível com a preferência declarada.", f"recipe_card.ingredients.{index}.added_flavor_enhancer")
        for index, step in enumerate(card.steps):
            texts.extend([(f"steps.{index}.instruction", step.instruction), (f"steps.{index}.observable_cue", step.observable_cue)])
            if step.time_hint is not None:
                texts.append((f"steps.{index}.time_hint", step.time_hint))
        for field in ("shopping_list", "adaptations", "equipment"):
            texts.extend((f"{field}.{index}", text) for index, text in enumerate(getattr(card, field)))
        if card.flavor_detail is not None:
            texts.extend([(f"flavor_detail.{field}", getattr(card.flavor_detail, field)) for field in ("action", "effect")])
        if card.detail_search_note is not None:
            texts.append(("detail_search_note", card.detail_search_note))
        for path, text in texts:
            if _contains_alcohol(text):
                add("alcool_na_ficha", "A ficha contém termo explícito incompatível com a política sem álcool.", f"recipe_card.{path}")
            ingredient_label = re.fullmatch(r"ingredients\.\d+\.(?:name|aliases\.\d+|components\.\d+)", path) is not None
            if any(_ingredient_match(restriction, text, allow_generic_label=ingredient_label) for restriction in restrictions):
                add("restricao_na_ficha", "A ficha contém correspondência textual com uma restrição declarada.", f"recipe_card.{path}")
            if profile.avoid_added_flavor_enhancers and any(_ingredient_match(term, text) for term in FLAVOR_ENHANCER_TERMS):
                add("realcador_adicionado", "A ficha contém realçador comercial incompatível com a preferência declarada.", f"recipe_card.{path}")

    practical_ready = not issues and not actions
    # Revisões humanas pendentes não impedem consultar o plano. Nunca são atestadas pela IA.
    label_items = [*delivery.ingredients, *(card.ingredients if card else [])]
    declared_labels = [label for item in label_items for label in (item.name, *item.aliases, *item.components)]
    contexts = [context for restriction in set(restrictions) if (context := _generic_ingredient_context(restriction, declared_labels)) is not None]
    operational_texts = [(f"steps.{index}", text) for index, text in enumerate(delivery.steps)]
    operational_texts.extend((f"adaptation_notes.{index}", text) for index, text in enumerate(delivery.adaptation_notes))
    if card is not None:
        operational_texts.extend((f"recipe_card.{path}", text) for path, text in texts)
    for path, text in operational_texts:
        words = normalize_text(text).split()
        if any(_unresolved_generic_ingredient(words, context) for context in contexts):
            action("ingrediente_generico_pendente", "Identifique o ingrediente citado pelo nome genérico e confira sua correspondência com o inventário e os alimentos evitados antes de preparar.", path)
    if (profile.allergies or profile.intolerances) and any(item.label_required or item.components for item in label_items) and not delivery.labels_reviewed:
        action("rotulos_pendentes", "Antes de preparar, a pessoa responsável precisa conferir os componentes e rótulos aplicáveis aos ingredientes compostos.", "labels_reviewed")
    if profile.allergies and not delivery.cross_contact_reviewed:
        action("contato_cruzado_pendente", "Antes de preparar, a pessoa responsável precisa revisar as condições reais de contato cruzado.", "cross_contact_reviewed")
    if profile.onboarding_unknowns:
        action("duvidas_alimentares_pendentes", "Esclareça as dúvidas alimentares registradas antes de tratar o preparo como pronto para começar.", "research.request.profile.onboarding_unknowns")
    return ValidationReport(
        ok=not issues, issues=issues,
        limitations=[*RESEARCH_LIMITATIONS, *DELIVERY_LIMITATIONS], checked_at=report.checked_at,
        practical_ready=practical_ready, preparation_ready=practical_ready and not actions, action_items=actions,
    )
