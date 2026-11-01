"""Contratos estritos de entrada e saída; nenhuma entrada executa instruções."""

from __future__ import annotations

import json
import ipaddress
import re
from datetime import date
from typing import Annotated, Any, Literal
from urllib.parse import urlsplit

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, field_validator, model_validator

MAX_INPUT_BYTES = 1_048_576
Text = Annotated[str, Field(min_length=1, max_length=10_000)]
ShortText = Annotated[str, Field(min_length=1, max_length=500)]
TextList = Annotated[list[Text], Field(max_length=200)]
ISO_COUNTRIES = frozenset(
    "AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ BL BM BN BO BQ BR BS BT BV BW BY BZ "
    "CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CW CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM "
    "FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU ID IE IL IM IN IO IQ IR IS "
    "IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML "
    "MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM "
    "PN PR PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR SS ST SV SX SY SZ TC TD TF "
    "TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW".split()
)


def _parse_date(value: Any) -> date:
    if isinstance(value, date) and type(value) is date:
        return value
    if isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        try:
            return date.fromisoformat(value)
        except ValueError:
            pass
    raise ValueError("Informe uma data válida no formato AAAA-MM-DD.")


ISODate = Annotated[date, BeforeValidator(_parse_date)]


def check_input_size(value: Any) -> None:
    """Limita o conteúdo recebido sem gravar nem devolver seu conteúdo."""
    if isinstance(value, BaseModel):
        value = value.model_dump(mode="json")
    size = len(json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str).encode("utf-8"))
    if size > MAX_INPUT_BYTES:
        raise ValueError("A entrada excede o limite de 1 MiB.")


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, str_strip_whitespace=True, validate_assignment=True)

    @model_validator(mode="before")
    @classmethod
    def bounded_input(cls, value: Any) -> Any:
        check_input_size(value)
        return value


class Profile(StrictModel):
    """Preferências declaradas, sem identificação pessoal nem inferência clínica."""

    onboarding_confirmed: bool
    excluded_ingredients: TextList = Field(default_factory=list)
    allergies: TextList = Field(default_factory=list)
    intolerances: TextList = Field(default_factory=list)
    preferences: TextList = Field(default_factory=list)
    equipment: TextList = Field(default_factory=list)
    region: ShortText | None = None
    language_style: Literal["simples", "tecnico"] = "simples"
    servings: Annotated[int, Field(gt=0, le=1000)] | None = None
    alcohol_free: bool = True
    dietary_patterns: TextList = Field(default_factory=list)
    avoid_added_flavor_enhancers: bool = True
    onboarding_unknowns: TextList = Field(default_factory=list)


class KitchenContext(StrictModel):
    """Condições deste preparo; não se tornam preferências permanentes."""

    available_ingredients: TextList = Field(default_factory=list)
    time_available_minutes: Annotated[int, Field(gt=0, le=43_200)] | None = None
    budget: ShortText | None = None
    shopping_allowed: bool | None = None
    output_mode: Literal["completa", "passo_a_passo"] = "completa"
    taste_goal: ShortText | None = None


class Request(StrictModel):
    """Identidade do prato resolvida pelo usuário e pelo host antes da busca."""

    dish: ShortText
    country: Annotated[str, Field(pattern=r"^[A-Z]{2}$")]
    variant: ShortText
    ambiguity_resolved: bool
    profile: Profile
    kitchen: KitchenContext = Field(default_factory=KitchenContext)

    @field_validator("country")
    @classmethod
    def valid_country(cls, value: str) -> str:
        if value not in ISO_COUNTRIES:
            raise ValueError("Informe um país ISO 3166-1 alfa-2 válido.")
        return value


class EditorialCountryEvidence(StrictModel):
    text: Text
    url: Text
    verification: Literal["confirmed", "pending"] = Field(
        default="pending",
        description="Qualificação declarada da relação editorial com o país; exige revisão semântica das evidências.",
    )

    @field_validator("url")
    @classmethod
    def valid_url(cls, value: str) -> str:
        return validate_http_url(value)


def validate_http_url(value: str) -> str:
    """Validação sintática, sem consulta DNS nem garantia de destino público real."""
    try:
        parsed = urlsplit(value)
        port = parsed.port
        if parsed.hostname:
            parsed.hostname.encode("idna")
    except UnicodeError as exc:
        raise ValueError("Informe uma URL com hostname IDNA válido.") from exc
    except ValueError as exc:
        raise ValueError("Informe uma URL HTTP ou HTTPS válida.") from exc
    if (
        parsed.scheme.lower() not in {"http", "https"}
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or any(char.isspace() for char in value)
        or any(ord(char) < 32 or ord(char) == 127 for char in value)
        or "\\" in value
        or (port is not None and not 0 < port < 65536)
    ):
        raise ValueError("Informe uma URL HTTP ou HTTPS válida e sem credenciais.")
    hostname = parsed.hostname.rstrip(".").casefold()
    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        if (
            "." not in hostname
            or hostname.endswith((".localhost", ".local", ".internal", ".home", ".lan"))
            or hostname == "localhost"
            or re.fullmatch(r"[0-9.]+", hostname)
            or any(not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", label, re.I) for label in hostname.encode("idna").decode("ascii").split("."))
        ):
            raise ValueError("Endereço local ou hostname inválido não é aceito.")
    else:
        if not address.is_global:
            raise ValueError("Endereço IP privado, local ou reservado não é aceito.")
    return value


class SourceSections(StrictModel):
    ingredients: Literal["read", "absent", "unavailable"]
    method: Literal["read", "absent", "unavailable"]
    notes: Literal["read", "absent", "unavailable"]
    comments: Literal["read", "absent", "unavailable"]


class SourceEvidence(StrictModel):
    id: ShortText
    title: Text
    url: Text
    author: ShortText
    publisher: ShortText
    editorial_group: ShortText
    country: Annotated[str, Field(pattern=r"^[A-Z]{2}$")]
    editorial_country_evidence: EditorialCountryEvidence
    accessed_at: ISODate
    publication_date: ISODate | None = None
    read_status: Literal["complete", "snippet", "unavailable"]
    kind: Literal["domestic", "editorial", "institutional"]
    research_track: Literal["base", "domestic_regional"]
    sections: SourceSections
    ingredients: TextList
    technique_summary: Text
    detail_notes: TextList = Field(default_factory=list)
    provenance_origin: Text = Field(
        description="URL HTTP(S) da publicação original da receita, usada para identificar republicações; não informe descrição em prosa.",
        json_schema_extra={"format": "uri"},
    )
    provenance_verification: Literal["confirmed", "pending"] = Field(
        default="pending",
        description="Qualificação declarada da origem e da independência editorial; exige revisão semântica das evidências.",
    )

    @field_validator("country")
    @classmethod
    def valid_country(cls, value: str) -> str:
        if value not in ISO_COUNTRIES:
            raise ValueError("Informe um país ISO 3166-1 alfa-2 válido.")
        return value

    @field_validator("url", "provenance_origin")
    @classmethod
    def valid_urls(cls, value: str) -> str:
        return validate_http_url(value)


class Query(StrictModel):
    text: Text
    derived_from: ShortText | None = None


class ReformulationsByTrack(StrictModel):
    base: Annotated[int, Field(ge=0, le=2)] | None
    domestic_regional: Annotated[int, Field(ge=0, le=2)] | None


class ResearchBatch(StrictModel):
    request: Request
    sources: Annotated[list[SourceEvidence], Field(max_length=100)]
    queries: Annotated[list[Query], Field(max_length=100)]
    completed_tracks: Annotated[list[Literal["base", "domestic_regional"]], Field(max_length=10)]
    pages_read: Annotated[int, Field(ge=0, le=1000)]
    researchers_count: Annotated[int, Field(ge=1, le=3)]
    reformulations_by_track: ReformulationsByTrack
    reviewer_notes: TextList = Field(default_factory=list)


class IngredientItem(StrictModel):
    name: ShortText
    aliases: TextList = Field(default_factory=list)
    components: TextList = Field(default_factory=list)
    alcohol: bool = False
    label_required: bool = False
    added_flavor_enhancer: bool = False


class RecipeIngredient(IngredientItem):
    quantity: ShortText
    unit: ShortText
    household_measure: ShortText | None = None
    note: ShortText | None = None
    source_ids: Annotated[list[ShortText], Field(min_length=1, max_length=7)]


class RecipeStep(StrictModel):
    instruction: Text
    observable_cue: ShortText
    time_hint: ShortText | None = None


class FlavorDetail(StrictModel):
    action: Text
    effect: Text
    category: Literal["umami", "aroma", "texture", "balance"]
    source_ids: Annotated[list[ShortText], Field(min_length=1, max_length=7)]


class RecipeCard(StrictModel):
    """Ficha operacional: medidas, rendimento, tempo e sinais de ponto explícitos."""

    title: ShortText
    servings: Annotated[int, Field(gt=0, le=1000)]
    yield_basis: Literal["source", "scaled", "estimate"]
    yield_note: Text
    active_minutes: Annotated[int, Field(ge=0, le=43_200)]
    total_minutes: Annotated[int, Field(gt=0, le=43_200)]
    equipment: Annotated[list[ShortText], Field(min_length=1, max_length=30)]
    ingredients: Annotated[list[RecipeIngredient], Field(min_length=1, max_length=200)]
    steps: Annotated[list[RecipeStep], Field(min_length=1, max_length=200)]
    shopping_list: TextList = Field(default_factory=list)
    flavor_detail: FlavorDetail | None = None
    detail_search_note: Text | None = None
    adaptations: TextList = Field(default_factory=list)
    source_ids: Annotated[list[ShortText], Field(min_length=7, max_length=7)]


class DietaryPatternReview(StrictModel):
    """Revisão semântica declarada, sem converter um padrão em diagnóstico."""

    pattern: ShortText
    excluded_ingredients: Annotated[list[ShortText], Field(min_length=1, max_length=200)]
    compatibility_reviewed: bool = False
    review_note: Text


class Delivery(StrictModel):
    """Lote e perfil únicos; o pedido operacional deriva exclusivamente do lote."""

    research: ResearchBatch
    ingredients: Annotated[list[IngredientItem], Field(max_length=200)]
    steps: TextList
    labels_reviewed: bool
    cross_contact_reviewed: bool = False
    adaptation_notes: TextList = Field(default_factory=list)
    recipe_card: RecipeCard | None = None
    dietary_pattern_review: Annotated[list[DietaryPatternReview], Field(max_length=50)] = Field(default_factory=list)


class GateIssue(StrictModel):
    code: str
    message: str
    path: str


class ValidationReport(StrictModel):
    ok: bool
    issues: list[GateIssue]
    semantic_review_required: bool = True
    limitations: list[str]
    checked_at: ISODate
    practical_ready: bool = False
    preparation_ready: bool = False
    action_items: list[GateIssue] = Field(default_factory=list)


SCHEMA_MODELS = {
    "profile": Profile,
    "request": Request,
    "research": ResearchBatch,
    "delivery": Delivery,
    "kitchen": KitchenContext,
    "card": RecipeCard,
}
