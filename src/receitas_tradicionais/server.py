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


@mcp.tool(title="Perguntas de levantamento alimentar", annotations=LOCAL_READ_ONLY)
def onboarding_questions() -> dict[str, Any]:
    """Fornece perguntas sem coletar identidade, diagnosticar ou persistir o perfil."""
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
    """Confere lote, perfil, inventário e revisão declarada, sem certificar segurança alimentar."""
    return core.validate_delivery(delivery)


@mcp.resource("receitas://project/instructions", mime_type="text/plain")
def project_instructions() -> str:
    """Instruções embarcadas no pacote, disponíveis sem depender do diretório de documentação."""
    return core.PROJECT_INSTRUCTIONS


@mcp.resource("receitas://schema/{name}", mime_type="application/json")
def contract_schema(name: str) -> dict[str, Any]:
    """Exporta somente um dos contratos embarcados e conhecidos, sem ler arquivos."""
    model = SCHEMA_MODELS.get(name)
    if model is None:
        raise ValueError("Contrato desconhecido. Escolha profile, request, research ou delivery.")
    return model.model_json_schema()


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
