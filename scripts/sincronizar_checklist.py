"""Confere ou sincroniza o checklist portátil com a fonte Python, com backup local."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from receitas_tradicionais.onboarding import first_message  # noqa: E402

BEGIN = "<!-- BEGIN CHECKLIST_CANONICO -->"
END = "<!-- END CHECKLIST_CANONICO -->"
OWNER = "Rodrigo Yú Matsumoto OAB/PE nº 1.338-B"


def generated_contents() -> dict[Path, str]:
    canonical = ROOT / "prompts" / "INSTRUCAO_PROJETO.md"
    current = canonical.read_text(encoding="utf-8")
    if current.count(BEGIN) != 1 or current.count(END) != 1:
        raise ValueError("A instrução precisa conter um único par de marcadores de checklist.")
    before, remainder = current.split(BEGIN, 1)
    _, after = remainder.split(END, 1)
    text = first_message()
    instruction = before + BEGIN + "\n\n" + text + "\n\n" + END + after
    frontmatter = f'''---
lang: pt-BR
title: "Checklist inicial para cozinhar com sua IA"
subject: "Alimentos a evitar, exemplos e respostas possíveis"
author: "{OWNER}"
keywords: "{OWNER}"
manager: "{OWNER}"
version: "2.0.0-rc.1"
status: candidate
---

'''
    checklist = frontmatter + text + "\n\nEsta lista ajuda a lembrar e aceita outros alimentos. Não é uma lista clínica exaustiva. O perfil vale somente para a conversa, salvo sua escolha explícita de salvar.\n"
    return {
        canonical: instruction,
        ROOT / "src" / "receitas_tradicionais" / "INSTRUCAO_PROJETO.md": instruction,
        ROOT / "docs" / "CHECKLIST_INICIAL.md": checklist,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Confere a fonte única do checklist; só grava com --write.")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        expected = generated_contents()
        changes = {path: text for path, text in expected.items() if not path.exists() or path.read_bytes() != text.encode("utf-8")}
        if args.write and changes:
            backup = ROOT / ".local" / "checklist_backups" / datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
            backup.mkdir(parents=True, exist_ok=False)
            for path, text in changes.items():
                if not path.resolve().is_relative_to(ROOT):
                    raise ValueError("Destino fora do repositório.")
                if path.exists():
                    saved = backup / path.relative_to(ROOT)
                    saved.parent.mkdir(parents=True, exist_ok=True)
                    saved.write_bytes(path.read_bytes())
                temporary = path.with_name(path.name + ".checklist.tmp")
                if temporary.exists():
                    raise ValueError("Há arquivo intermediário pendente; confira antes de continuar.")
                temporary.write_bytes(text.encode("utf-8"))
                os.replace(temporary, path)
                if path.read_bytes() != text.encode("utf-8"):
                    raise ValueError("O arquivo gravado diverge do conteúdo esperado.")
        print(json.dumps({"ok": args.write or not changes, "written": bool(args.write and changes), "changed": [path.relative_to(ROOT).as_posix() for path in changes]}, ensure_ascii=False))
        return 0 if args.write or not changes else 1
    except (OSError, ValueError):
        print(json.dumps({"ok": False, "error": "Não foi possível conferir ou sincronizar o checklist. Confira marcadores, permissões e arquivos intermediários."}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
