"""Servidor MCP oficial por stdio, sem acesso à rede, arquivos ou shell nas ferramentas."""

from __future__ import annotations

from typing import Any

from mcp.server import MCPServer
from mcp.types import ToolAnnotations

from . import __version__
from . import core
from .models import SCHEMA_MODELS, Delivery, Request, ResearchBatch, ValidationReport

mcp = MCPServer(
    "Receitas tradicionais canônicas",
    version=__version__,
    instructions=core.PROJECT_INSTRUCTIONS,
    log_level="WARNING",
)
LOCAL_READ_ONLY = ToolAnnotations(read_only_hint=True, open_world_hint=False)


@mcp.tool(title="Checklist inicial da cozinha", annotations=LOCAL_READ_ONLY)
def onboarding_questions() -> dict[str, Any]:
    """Mostre first_message diretamente; a conversa começa pelo checklist, sem relatório técnico. Não coleta identidade nem persiste respostas."""
    return core.onboarding_questions()


@mcp.tool(title="Planejar pesquisa culinária", annotations=LOCAL_READ_ONLY)
def plan_research(request: Request) -> dict[str, Any]:
    """Após confirmação alimentar e desambiguação, planeja a primeira busca do host."""
    return core.plan_research(request)


@mcp.tool(title="Validar lote de sete receitas-fontes", annotations=LOCAL_READ_ONLY)
def validate_research(batch: ResearchBatch) -> ValidationReport:
    """Verifica declarações documentais, sem acessar páginas ou provar sua veracidade."""
    return core.validate_research(batch)


@mcp.tool(title="Validar entrega operacional", annotations=LOCAL_READ_ONLY)
def validate_delivery(delivery: Delivery) -> ValidationReport:
    """Confere lote e exclusões; practical_ready exige ficha completa e preparation_ready inclui revisões humanas aplicáveis. ok sozinho não significa receita pronta."""
    return core.validate_delivery(delivery)


@mcp.resource("receitas://project/instructions", mime_type="text/plain")
def project_instructions() -> str:
    """Instruções embarcadas no pacote, disponíveis sem depender do diretório de documentação."""
    return core.PROJECT_INSTRUCTIONS


@mcp.resource("receitas://project/checklist", mime_type="application/json")
def project_checklist() -> dict[str, Any]:
    """Checklist e mensagem humana inicial; não grava perfil."""
    return core.onboarding_questions()


@mcp.resource("receitas://schema/{name}", mime_type="application/json")
def contract_schema(name: str) -> dict[str, Any]:
    """Exporta somente um dos contratos embarcados e conhecidos, sem ler arquivos."""
    model = SCHEMA_MODELS.get(name)
    if model is None:
        raise ValueError("Contrato desconhecido. Escolha profile, request, research, delivery, kitchen ou card.")
    return model.model_json_schema()


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
