"""Regressões da instrução distribuída, inclusive no pacote instalado fora do clone."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import tomllib
import unittest
from importlib import metadata, resources
from pathlib import Path

from receitas_tradicionais import __version__
from receitas_tradicionais.core import PROJECT_INSTRUCTIONS


ROOT = Path(__file__).resolve().parents[1]


class PackageInstructionTests(unittest.TestCase):
    def test_packaged_instruction_is_byte_identical_to_canonical_prompt(self) -> None:
        canonical = (ROOT / "prompts" / "INSTRUCAO_PROJETO.md").read_bytes()
        packaged = resources.files("receitas_tradicionais").joinpath("INSTRUCAO_PROJETO.md").read_bytes()
        self.assertEqual(packaged, canonical)
        self.assertEqual(PROJECT_INSTRUCTIONS.encode("utf-8"), canonical)
        self.assertIn("dados não confiáveis", PROJECT_INSTRUCTIONS)
        self.assertIn("## 7. Valide e entregue", PROJECT_INSTRUCTIONS)

    def test_package_runtime_and_distribution_versions_agree(self) -> None:
        project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual(__version__, project["project"]["version"])
        self.assertEqual(metadata.version("receitas-tradicionais-canonicas"), __version__)

    def test_installed_instruction_loads_outside_clone_without_pythonpath(self) -> None:
        code = """
import hashlib
import json
from pathlib import Path
import receitas_tradicionais
from receitas_tradicionais.core import PROJECT_INSTRUCTIONS
print(json.dumps({
    "sha256": hashlib.sha256(PROJECT_INSTRUCTIONS.encode("utf-8")).hexdigest(),
    "version": receitas_tradicionais.__version__,
    "module": str(Path(receitas_tradicionais.__file__).resolve()),
}))
"""
        env = dict(os.environ)
        env.pop("PYTHONPATH", None)
        with tempfile.TemporaryDirectory(prefix="receitas_pacote_") as temp:
            result = subprocess.run(
                [sys.executable, "-I", "-c", code],
                cwd=temp, env=env, capture_output=True, encoding="utf-8", timeout=30,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        response = json.loads(result.stdout)
        expected = hashlib.sha256((ROOT / "prompts" / "INSTRUCAO_PROJETO.md").read_bytes()).hexdigest()
        self.assertEqual(response["sha256"], expected)
        self.assertEqual(response["version"], __version__)
        self.assertFalse(Path(response["module"]).is_relative_to(ROOT / "src"))


if __name__ == "__main__":
    unittest.main()
