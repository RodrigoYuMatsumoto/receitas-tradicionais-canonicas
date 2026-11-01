"""Interface local com saída JSON, leitura explícita e erros sem conteúdo de entrada."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pydantic import ValidationError

from .core import onboarding_questions, plan_research, validate_delivery, validate_research
from .models import MAX_INPUT_BYTES, SCHEMA_MODELS, Delivery, Profile, Request, ResearchBatch
from .core import normalize_text


class InputError(Exception):
    pass


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise InputError("Argumentos inválidos. Consulte --help.")


def _reject_constant(value: str) -> None:
    raise InputError("JSON inválido: números não finitos não são aceitos.")


def _unique_pairs(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputError("JSON inválido: campos repetidos não são aceitos.")
        result[key] = value
    return result


def read_json(path: str) -> dict:
    try:
        with Path(path).open("rb") as stream:
            raw = stream.read(MAX_INPUT_BYTES + 1)
    except OSError as exc:
        raise InputError("Não foi possível ler o arquivo explicitamente informado.") from exc
    if len(raw) > MAX_INPUT_BYTES:
        raise InputError("A entrada excede o limite de 1 MiB.")
    try:
        result = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_pairs, parse_constant=_reject_constant)
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise InputError("O arquivo precisa conter JSON UTF-8 válido.") from exc
    if not isinstance(result, dict):
        raise InputError("A entrada JSON precisa ser um objeto.")
    return result


def _ask(question: str) -> str:
    print(question, file=sys.stderr, flush=True)
    answer = sys.stdin.buffer.readline(MAX_INPUT_BYTES + 1)
    if not answer:
        raise InputError("Levantamento alimentar interrompido antes da confirmação.")
    if len(answer) > MAX_INPUT_BYTES:
        raise InputError("A resposta excede o limite de 1 MiB.")
    try:
        return answer.decode("utf-8").strip()
    except UnicodeError as exc:
        raise InputError("A resposta precisa estar em UTF-8.") from exc


def interactive_onboarding() -> Profile:
    values: dict = {}
    unknowns: list[str] = []
    list_fields = {"excluded_ingredients", "allergies", "intolerances", "preferences", "equipment"}
    print(onboarding_questions()["first_message"], file=sys.stderr, flush=True)
    for item in onboarding_questions()["questions"]:
        field = item["field"]
        suffix = " Separe itens por ponto e vírgula; digite nenhum para confirmar ausência. Não deixe em branco." if field in list_fields else ""
        answer = _ask(item["question"] + suffix)
        if field in list_fields:
            if not answer:
                raise InputError("Resposta em branco não confirma ausência. Informe os itens ou digite nenhum; se preferir não informar, use o modo de conversa e declare a lacuna.")
            if answer.casefold() in {"não sei", "nao sei", "prefiro não informar", "prefiro nao informar"}:
                unknowns.append(field)
                values[field] = []
            else:
                values[field] = [] if answer.casefold() in {"nenhum", "nenhuma"} else [value.strip() for value in answer.split(";") if value.strip()]
        elif field == "region":
            values[field] = answer or None
        elif field == "servings":
            try:
                values[field] = int(answer)
            except ValueError as exc:
                raise InputError("Informe um número inteiro positivo de porções.") from exc
        elif field == "language_style":
            style = {"simples": "simples", "técnica": "tecnico", "tecnica": "tecnico", "técnico": "tecnico", "tecnico": "tecnico"}
            if answer.casefold() not in style:
                raise InputError("Escolha linguagem simples ou técnica.")
            values[field] = style[answer.casefold()]
        elif field == "onboarding_confirmed":
            values[field] = answer.casefold() in {"sim", "s"}
    values["onboarding_unknowns"] = unknowns
    # Nesta pergunta da CLI, preferência significa ingrediente a evitar.
    # A API continua aceitando preferências gerais sem convertê-las silenciosamente.
    excluded = values["excluded_ingredients"]
    for ingredient in values["preferences"]:
        if normalize_text(ingredient) not in {normalize_text(item) for item in excluded}:
            excluded.append(ingredient)
    return Profile.model_validate(values)


def _print_json(value: object) -> None:
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    print(json.dumps(value, ensure_ascii=False, indent=2))


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = JsonArgumentParser(description="Pesquisa culinária documentada e local.")
    sub = parser.add_subparsers(dest="command", required=True, parser_class=JsonArgumentParser)
    sub.add_parser("iniciar", help="Mostra o checklist inicial em texto simples, sem coletar nem salvar respostas.")
    sub.add_parser("onboarding", help="Levantamento alimentar interativo, sem salvar perfil.")
    plan = sub.add_parser("plan", help="Planeja a busca a partir de pedido JSON explícito.")
    plan.add_argument("path")
    validate = sub.add_parser("validate", help="Valida lote de pesquisa JSON explícito.")
    validate.add_argument("path")
    delivery = sub.add_parser("validate-delivery", help="Valida entrega e lote incorporado.")
    delivery.add_argument("path")
    show = sub.add_parser("mostrar", help="Mostra uma ficha em texto para cozinhar, sem salvar resultado.")
    show.add_argument("path")
    schema = sub.add_parser("schema", help="Exporta contratos JSON Schema para stdout.")
    schema.add_argument("model", choices=[*SCHEMA_MODELS, "all"], default="all", nargs="?")
    sub.add_parser("mcp", help="Inicia o servidor MCP oficial por stdio.")
    human_output = False
    try:
        args = parser.parse_args(argv)
        human_output = args.command == "mostrar"
        if args.command == "iniciar":
            print(onboarding_questions()["first_message"])
            return 0
        if args.command == "mostrar":
            from .presentation import render_delivery

            rendered, exit_code = render_delivery(Delivery.model_validate(read_json(args.path)))
            print(rendered)
            return exit_code
        if args.command == "mcp":
            from .server import main as run_server

            run_server()
            return 0
        if args.command == "onboarding":
            result = interactive_onboarding()
        elif args.command == "plan":
            result = plan_research(Request.model_validate(read_json(args.path)))
        elif args.command == "validate":
            result = validate_research(ResearchBatch.model_validate(read_json(args.path)))
        elif args.command == "validate-delivery":
            result = validate_delivery(Delivery.model_validate(read_json(args.path)))
        else:
            result = {key: model.model_json_schema() for key, model in SCHEMA_MODELS.items()} if args.model == "all" else SCHEMA_MODELS[args.model].model_json_schema()
        _print_json(result)
        if hasattr(result, "ok"):
            return 0 if result.ok else 1
        if isinstance(result, dict) and result.get("ok") is False:
            return 1
        return 0
    except ValidationError:
        if human_output:
            print("A ficha está incompleta ou contém dados inválidos. Complete as informações da receita antes de mostrar o preparo.")
            return 2
        _print_json({"ok": False, "error": "dados_invalidos", "message": "Dados inválidos: confira o contrato, os tipos, as datas e os campos obrigatórios com o comando schema."})
        return 2
    except InputError as exc:
        if human_output:
            print(str(exc))
            return 2
        _print_json({"ok": False, "error": "entrada_invalida", "message": str(exc)})
        return 2
    except (KeyboardInterrupt, EOFError):
        if human_output:
            print("Operação interrompida, sem salvar a ficha.")
            return 130
        _print_json({"ok": False, "error": "interrompido", "message": "Operação interrompida, sem salvar perfil."})
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
