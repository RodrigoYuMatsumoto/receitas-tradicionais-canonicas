"""Confere metadados, referências locais, exemplos e integridade da distribuição."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWNER = "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"
IGNORED = {".git", ".venv", ".local", "__pycache__", "dist", "build", ".pytest_cache", "profiles"}
MANIFEST = ROOT / "MANIFEST.sha256"
METADATA = ROOT / "ARTIFACT_METADATA.json"


def public_files() -> list[Path]:
    result = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if d not in IGNORED and not d.endswith(".egg-info"))
        for name in sorted(files):
            if name.endswith((".pyc", ".log", ".sqlite", ".sqlite3")) or name.startswith(".env"):
                continue
            result.append(Path(base) / name)
    return sorted(result)


def preserve(path: Path) -> None:
    if path.exists():
        backup = ROOT / ".local" / "previous_metadata" / datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        backup.mkdir(parents=True, exist_ok=False)
        shutil.copy2(path, backup / path.name)


def refresh() -> None:
    paths = sorted({*public_files(), MANIFEST, METADATA})
    metadata = {
        "lang": "pt-BR",
        "title": "Metadados dos artefatos distribuídos",
        "subject": "Idioma, autoria e propriedades dos arquivos do repositório",
        "author": OWNER,
        "keywords": OWNER,
        "manager": OWNER,
        "limitations": [
            "Markdown registra campos no frontmatter; não há propriedade Office nativa.",
            "Código, JSON, YAML, TOML e manifest não têm campos documentais nativos universais; este arquivo os registra por caminho.",
            "O pacote Python suporta autor e palavras-chave; gerente e idioma ficam na tabela personalizada do pyproject e neste registro.",
        ],
        "artifacts": [{
            "path": p.relative_to(ROOT).as_posix(), "lang": "pt-BR", "author": OWNER,
            "keywords": OWNER, "manager": OWNER,
            "title": "Artefato de receitas tradicionais: " + p.stem,
            "subject": "Instruções, contratos, código ou evidências de pesquisa culinária documentada",
        } for p in paths],
    }
    preserve(METADATA)
    METADATA.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    lines = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT).as_posix()}" for p in public_files() if p != MANIFEST]
    preserve(MANIFEST)
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def check() -> list[str]:
    errors = []
    paths = public_files()
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"Codificação não UTF-8: {relative}")
            continue
        if any(chr(c) in content for c in (0x2013, 0x2014)):
            errors.append(f"Pontuação incompatível: {relative}")
        if re.search(r"[CD]:[\\/]Users[\\/]|[CD]:[\\/]Meu Drive", content, re.I):
            errors.append(f"Caminho pessoal na distribuição: {relative}")
        if path.suffix == ".json":
            try:
                json.loads(content)
            except json.JSONDecodeError:
                errors.append(f"JSON inválido: {relative}")
        if path.suffix == ".md":
            front = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
            if not front:
                errors.append(f"Frontmatter ausente: {relative}")
            else:
                fields = dict(line.split(":", 1) for line in front.group(1).splitlines() if ":" in line)
                fields = {key: value.strip().strip(chr(34)) for key, value in fields.items()}
                expected = {"lang": "pt-BR", "author": OWNER, "keywords": OWNER, "manager": OWNER}
                if not all(fields.get(key) == value for key, value in expected.items()) or not all(fields.get(key) for key in ("title", "subject")):
                    errors.append(f"Metadados incompletos: {relative}")
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
                target = target.strip("<>").split("#", 1)[0]
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                if not (path.parent / target).resolve().exists():
                    errors.append(f"Referência local ausente em {relative}: {target}")
    if not MANIFEST.exists() or not METADATA.exists():
        errors.append("Manifest ou registro de metadados ausente.")
        return errors
    registered = set()
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        target = ROOT / relative
        registered.add(target)
        if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            errors.append(f"Integridade divergente: {relative}")
    actual = set(paths) - {MANIFEST}
    if actual != registered:
        errors.append("O manifest não corresponde ao conjunto atual de arquivos distribuídos.")
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    if {p.relative_to(ROOT).as_posix() for p in paths} != {a["path"] for a in metadata["artifacts"]}:
        errors.append("O registro de metadados não cobre todos os arquivos distribuídos.")
    case = json.loads((ROOT / "examples" / "feijoada_pesquisa.json").read_text(encoding="utf-8"))
    target = "hortel" + chr(0xE3)
    if any(target in q["text"].casefold() for q in case["queries"]):
        errors.append("Ingrediente-alvo presente nas consultas do ensaio.")
    from receitas_tradicionais.core import PROJECT_INSTRUCTIONS, onboarding_questions, validate_delivery, validate_research
    from receitas_tradicionais.models import SCHEMA_MODELS, Delivery, ResearchBatch
    canonical = (ROOT / "prompts" / "INSTRUCAO_PROJETO.md").read_bytes()
    packaged = (ROOT / "src" / "receitas_tradicionais" / "INSTRUCAO_PROJETO.md").read_bytes()
    if canonical != packaged or canonical != PROJECT_INSTRUCTIONS.encode("utf-8"):
        errors.append("A instrução canônica, a cópia empacotada e a instrução instalada divergem.")
    contracts = json.loads((ROOT / "schemas" / "contratos.json").read_text(encoding="utf-8"))
    if contracts != {name: model.model_json_schema() for name, model in SCHEMA_MODELS.items()}:
        errors.append("Os esquemas distribuídos divergem dos contratos atuais do pacote.")
    checklist = onboarding_questions()
    rendered = (ROOT / "docs" / "CHECKLIST_INICIAL.md").read_text(encoding="utf-8")
    if checklist["first_message"] not in rendered:
        errors.append("O checklist humano distribuído diverge da primeira mensagem do servidor.")
    if checklist["first_message"] not in PROJECT_INSTRUCTIONS:
        errors.append("O checklist da instrução portátil diverge da primeira mensagem do servidor.")
    report = validate_research(ResearchBatch.model_validate(case))
    # Compatibilidade do registro 0.1: os novos campos ausentes permanecem pendentes.
    historical_issues = {"reformulacoes_nao_medidas", "pais_editorial_pendente", "independencia_pendente"}
    if report.ok or {issue.code for issue in report.issues} != historical_issues:
        errors.append("O lote histórico 0.1 deve preservar os retries não medidos e as qualificações estruturadas ainda não registradas, sem retropreenchimento.")
    revalidated = json.loads((ROOT / "examples" / "feijoada_revalidada.json").read_text(encoding="utf-8"))
    if not validate_research(ResearchBatch.model_validate(revalidated)).ok:
        errors.append("O lote real revalidado precisa passar no contrato documental.")
    practical_case = json.loads((ROOT / "examples" / "entrega_pratica_sintetica.json").read_text(encoding="utf-8"))
    practical_report = validate_delivery(Delivery.model_validate(practical_case))
    if not practical_report.ok or not practical_report.practical_ready or not practical_report.preparation_ready:
        errors.append("O exemplo sintético de cartão operacional não passa na jornada prática.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Confere os artefatos públicos do projeto.")
    parser.add_argument("--refresh", action="store_true", help="Atualiza metadados e manifest, preservando versões anteriores localmente.")
    args = parser.parse_args()
    if args.refresh:
        refresh()
    errors = check()
    print(json.dumps({"ok": not errors, "files": len(public_files()), "errors": errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
