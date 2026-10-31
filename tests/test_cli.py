"""CLI sem rede, com falhas sanitizadas e entradas explicitamente informadas."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from receitas_tradicionais.models import MAX_INPUT_BYTES
from test_core import batch_data, delivery_data, request_data


class CliTests(unittest.TestCase):
    def run_cli(self, *args: str, input: str | None = None) -> subprocess.CompletedProcess:
        env = dict(os.environ)
        env.pop("PYTHONIOENCODING", None)
        return subprocess.run([sys.executable, "-m", "receitas_tradicionais", *args], input=input, capture_output=True, encoding="utf-8", env=env, timeout=30)

    def test_schema_export(self) -> None:
        result = self.run_cli("schema", "all")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(set(json.loads(result.stdout)), {"profile", "request", "research", "delivery"})
        self.assertIn("Preferências", result.stdout)

    def test_plan_and_validate_with_explicit_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "entrada.json"
            for command, data in [("plan", request_data()), ("validate", batch_data())]:
                path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
                result = self.run_cli(command, str(path))
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(json.loads(result.stdout)["ok"])

    def test_invalid_json_oversize_duplicate_and_nonfinite(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "entrada.json"
            for content in ["{", " " * (MAX_INPUT_BYTES + 1), '{"secret":"marcador_privado","secret":1}', '{"servings":NaN}']:
                path.write_text(content, encoding="utf-8")
                result = self.run_cli("validate", str(path))
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(json.loads(result.stdout)["ok"])
                self.assertNotIn("Traceback", result.stderr + result.stdout)
                self.assertNotIn("marcador_privado", result.stderr + result.stdout)

    def test_pydantic_failure_does_not_echo_input(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "entrada.json"
            path.write_text('{"secret":"marcador_privado"}', encoding="utf-8")
            result = self.run_cli("plan", str(path))
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("marcador_privado", result.stdout + result.stderr)

    def test_invalid_idna_hosts_return_sanitized_json_in_both_validators(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "entrada.json"
            for command in ["validate", "validate-delivery"]:
                for field in ["url", "provenance_origin", "editorial_country_evidence"]:
                    for hostname in ["a..example.test", "a" * 64 + ".example.test"]:
                        data = batch_data() if command == "validate" else delivery_data()
                        batch = data if command == "validate" else data["research"]
                        url = f"https://{hostname}/marcador_privado"
                        if field == "editorial_country_evidence":
                            batch["sources"][0][field]["url"] = url
                        else:
                            batch["sources"][0][field] = url
                        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
                        with self.subTest(command=command, field=field, hostname=hostname):
                            result = self.run_cli(command, str(path))
                            self.assertEqual(result.returncode, 2)
                            response = json.loads(result.stdout)
                            self.assertFalse(response["ok"])
                            self.assertEqual(response["error"], "dados_invalidos")
                            self.assertNotIn("Traceback", result.stdout + result.stderr)
                            self.assertNotIn("marcador_privado", result.stdout + result.stderr)

    def test_interactive_onboarding_accepts_allergy_without_writing(self) -> None:
        answers = "\namendoim\n\n\npanela\n\n4\nsimples\nsim\n"
        result = self.run_cli("onboarding", input=answers)
        self.assertEqual(result.returncode, 0, result.stderr)
        profile = json.loads(result.stdout)
        self.assertEqual(profile["allergies"], ["amendoim"])
        self.assertTrue(profile["onboarding_confirmed"])
        self.assertTrue(profile["alcohol_free"])

    def test_missing_path_and_unknown_argument_are_json(self) -> None:
        for args in [("plan",), ("comando_inexistente",)]:
            result = self.run_cli(*args)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(json.loads(result.stdout)["ok"])


if __name__ == "__main__":
    unittest.main()
