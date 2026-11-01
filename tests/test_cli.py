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
from test_practical import practical_delivery_data


class CliTests(unittest.TestCase):
    def run_cli(self, *args: str, input: str | None = None) -> subprocess.CompletedProcess:
        env = dict(os.environ)
        env.pop("PYTHONIOENCODING", None)
        return subprocess.run([sys.executable, "-m", "receitas_tradicionais", *args], input=input, capture_output=True, encoding="utf-8", env=env, timeout=30)

    def test_schema_export(self) -> None:
        result = self.run_cli("schema", "all")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(set(json.loads(result.stdout)), {"profile", "request", "research", "delivery", "kitchen", "card"})
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
        answers = "nenhum\namendoim\nnenhum\nnenhum\npanela\n\n4\nsimples\nsim\n"
        result = self.run_cli("onboarding", input=answers)
        self.assertEqual(result.returncode, 0, result.stderr)
        profile = json.loads(result.stdout)
        self.assertEqual(profile["allergies"], ["amendoim"])
        self.assertTrue(profile["onboarding_confirmed"])
        self.assertTrue(profile["alcohol_free"])

    def test_blank_answer_does_not_confirm_absence_of_restrictions(self) -> None:
        result = self.run_cli("onboarding", input="\n")
        self.assertEqual(result.returncode, 2)
        response = json.loads(result.stdout)
        self.assertFalse(response["ok"])
        self.assertIn("não confirma ausência", response["message"])
        self.assertNotIn("onboarding_confirmed", response)

    def test_start_shows_checklist_directly_without_diagnostics_or_writes(self) -> None:
        result = self.run_cli("iniciar")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.startswith("O que devo evitar na sua comida?"))
        for example in ["lactose", "amendoim", "pistache", "camarão", "aipo", "tempero pronto", "não sei"]:
            self.assertIn(example, result.stdout)
        for technical_word in ["MCP", "version", "validação", "hash", "B.9"]:
            self.assertNotIn(technical_word, result.stdout)
        self.assertEqual(result.stderr, "")

    def test_unknown_is_distinct_from_explicit_none_in_onboarding(self) -> None:
        answers = "não sei\nnenhum\nnenhum\nnenhum\npanela\n\n4\nsimples\nsim\n"
        result = self.run_cli("onboarding", input=answers)
        self.assertEqual(result.returncode, 0, result.stderr)
        profile = json.loads(result.stdout)
        self.assertEqual(profile["excluded_ingredients"], [])
        self.assertEqual(profile["allergies"], [])
        self.assertEqual(profile["onboarding_unknowns"], ["excluded_ingredients"])

    def test_onboarding_normalizes_unknown_and_none_answers(self) -> None:
        for answer, unknown in [("Não sei.", True), ("  NAO   SEI!  ", True), ("Prefiro não informar.", True), ("Nenhum.", False), ("NENHUMA!", False)]:
            responses = f"{answer}\n{answer}\nnenhum\nnenhum\npanela\n\n4\nsimples\nsim\n"
            with self.subTest(answer=answer):
                result = self.run_cli("onboarding", input=responses)
                self.assertEqual(result.returncode, 0, result.stderr)
                profile = json.loads(result.stdout)
                self.assertEqual(profile["excluded_ingredients"], [])
                self.assertEqual(profile["allergies"], [])
                self.assertEqual(profile["onboarding_unknowns"], ["excluded_ingredients", "allergies"] if unknown else [])

    def test_cli_disliked_ingredients_become_exclusions_without_duplicates(self) -> None:
        answers = "coentro\nnenhum\nnenhum\nCOENTRO; pimenta\npanela\n\n4\nsimples\nsim\n"
        result = self.run_cli("onboarding", input=answers)
        self.assertEqual(result.returncode, 0, result.stderr)
        profile = json.loads(result.stdout)
        self.assertEqual(profile["excluded_ingredients"], ["coentro", "pimenta"])
        self.assertEqual(profile["preferences"], ["COENTRO", "pimenta"])

    def show_delivery(self, data: dict) -> subprocess.CompletedProcess:
        with tempfile.TemporaryDirectory(prefix="receitas_saida_") as temp:
            path = Path(temp) / "ficha de teste.json"
            original = json.dumps(data, ensure_ascii=False)
            path.write_text(original, encoding="utf-8")
            result = self.run_cli("mostrar", str(path))
            self.assertEqual(path.read_text(encoding="utf-8"), original)
            self.assertEqual(list(Path(temp).iterdir()), [path])
            return result

    def test_show_is_human_readable_and_puts_ingredients_before_sources(self) -> None:
        result = self.show_delivery(practical_delivery_data())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertLess(result.stdout.index("Ingredientes"), result.stdout.index("As sete receitas consultadas"))
        self.assertIn("arroz: 1 xícara", result.stdout)
        self.assertIn("Como reconhecer o ponto:", result.stdout)
        self.assertIn("Rendimento: 4 porções", result.stdout)
        for field in ["practical_ready", "preparation_ready", "recipe_card", "source_ids", "MCP"]:
            self.assertNotIn(field, result.stdout)
        self.assertEqual(result.stderr, "")

    def test_show_blocks_a_restricted_ingredient_before_rendering_steps(self) -> None:
        data = practical_delivery_data()
        data["research"]["request"]["profile"]["excluded_ingredients"] = ["arroz"]
        result = self.show_delivery(data)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("pediu para evitar", result.stdout)
        self.assertNotIn("Como fazer", result.stdout)
        self.assertNotIn("arroz: 1 xícara", result.stdout)

    def test_show_pending_allergy_checks_as_actions_with_the_plan(self) -> None:
        data = practical_delivery_data()
        data["research"]["request"]["profile"]["allergies"] = ["amendoim"]
        data["ingredients"][0]["label_required"] = True
        result = self.show_delivery(data)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Plano da receita. Antes de começar:", result.stdout)
        self.assertIn("rótulos", result.stdout)
        self.assertIn("contato", result.stdout)
        self.assertIn("Ingredientes", result.stdout)
        self.assertIn("Como fazer", result.stdout)

    def test_missing_path_and_unknown_argument_are_json(self) -> None:
        for args in [("plan",), ("comando_inexistente",)]:
            result = self.run_cli(*args)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(json.loads(result.stdout)["ok"])


if __name__ == "__main__":
    unittest.main()
