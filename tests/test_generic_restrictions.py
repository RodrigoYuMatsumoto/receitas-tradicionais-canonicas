"""Menção genérica não identifica uma variedade compatível com exclusão composta."""

from __future__ import annotations

import unittest

from receitas_tradicionais.core import validate_delivery
from receitas_tradicionais.models import Delivery
from receitas_tradicionais.presentation import render_delivery
from test_practical import practical_delivery_data


class GenericRestrictionTests(unittest.TestCase):
    def data(self, field: str = "excluded_ingredients") -> dict:
        data = practical_delivery_data()
        data["research"]["request"]["profile"][field] = ["castanha-de-caju"]
        data["labels_reviewed"] = True
        data["cross_contact_reviewed"] = True
        return data

    def step(self, data: dict, text: str) -> None:
        data["steps"] = [text]
        data["recipe_card"]["steps"][0]["instruction"] = text

    def declare_alternative(self, data: dict, name: str = "castanha-do-pará") -> None:
        data["ingredients"].append({"name": name})
        data["recipe_card"]["ingredients"].append({"name": name, "quantity": "1", "unit": "unidade", "source_ids": ["teste_0"]})

    def report(self, data: dict):
        return validate_delivery(Delivery.model_validate(data))

    def assert_identification_pending(self, data: dict) -> None:
        report = self.report(data)
        self.assertTrue(report.ok)
        self.assertTrue(report.practical_ready)
        self.assertFalse(report.preparation_ready)
        self.assertIn("ingrediente_generico_pendente", {item.code for item in report.action_items})

    def test_generic_step_or_shopping_item_does_not_become_ready(self) -> None:
        for surface in ("steps", "shopping_list"):
            data = self.data()
            if surface == "steps":
                self.step(data, "Adicione castanhas picadas.")
            else:
                data["recipe_card"]["shopping_list"] = ["castanhas"]
            with self.subTest(surface=surface):
                self.assert_identification_pending(data)

    def test_exclusion_allergy_and_intolerance_preserve_the_same_question(self) -> None:
        for field in ("excluded_ingredients", "allergies", "intolerances"):
            data = self.data(field)
            self.step(data, "Adicione castanhas picadas.")
            with self.subTest(field=field):
                self.assert_identification_pending(data)

    def test_other_operational_texts_cannot_introduce_the_generic_item(self) -> None:
        for surface in ("adaptation_notes", "adaptations", "note", "observable_cue", "time_hint", "title", "yield_note", "flavor_action", "flavor_effect", "detail_search_note"):
            data = self.data()
            card = data["recipe_card"]
            text = "Use castanhas picadas."
            if surface == "adaptation_notes":
                data[surface] = [text]
            elif surface == "adaptations":
                card[surface] = [text]
            elif surface == "note":
                card["ingredients"][0][surface] = text
            elif surface in {"observable_cue", "time_hint"}:
                card["steps"][0][surface] = text
            elif surface == "yield_note":
                card[surface] = "Rendimento estimado, com castanhas picadas."
            elif surface.startswith("flavor_"):
                card["flavor_detail"][surface.removeprefix("flavor_")] = text
            else:
                card[surface] = text
            with self.subTest(surface=surface):
                self.assert_identification_pending(data)

    def test_declared_alternative_named_explicitly_is_not_the_excluded_variety(self) -> None:
        data = self.data()
        self.declare_alternative(data)
        self.step(data, "Adicione castanhas-do-pará.")
        report = self.report(data)
        self.assertTrue(report.ok)
        self.assertTrue(report.practical_ready)
        self.assertTrue(report.preparation_ready)
        self.assertEqual(report.action_items, [])

    def test_qualified_mention_does_not_release_a_later_generic_mention(self) -> None:
        data = self.data()
        self.declare_alternative(data)
        self.step(data, "Adicione castanhas-do-pará e depois castanhas picadas.")
        self.assert_identification_pending(data)

    def test_specific_alternative_not_in_inventory_needs_identification(self) -> None:
        data = self.data()
        self.step(data, "Adicione castanhas-do-pará.")
        self.assert_identification_pending(data)

    def test_preparation_description_in_inventory_does_not_establish_variety(self) -> None:
        for name in ("castanhas picadas", "castanhas torradas", "castanhas sem sal", "castanhas com arroz"):
            data = self.data()
            self.declare_alternative(data, name)
            self.step(data, f"Adicione {name}.")
            with self.subTest(name=name):
                self.assert_identification_pending(data)

    def test_declared_alias_or_component_can_identify_the_explicit_alternative(self) -> None:
        for field in ("aliases", "components"):
            data = self.data()
            self.declare_alternative(data, "mistura identificada")
            data["ingredients"][-1][field] = ["castanha-do-pará"]
            data["recipe_card"]["ingredients"][-1][field] = ["castanha-do-pará"]
            self.step(data, "Adicione castanhas-do-pará.")
            report = self.report(data)
            with self.subTest(field=field):
                self.assertTrue(report.ok)
                self.assertTrue(report.preparation_ready)

    def test_function_words_and_word_fragments_do_not_create_a_food_family(self) -> None:
        for restriction, instruction in (("leite em pó", "Acrescente cacau em pó."), ("sal grosso", "Acrescente salsa."), ("mel puro", "Acrescente melado.")):
            data = practical_delivery_data()
            data["research"]["request"]["profile"]["excluded_ingredients"] = [restriction]
            self.step(data, instruction)
            report = self.report(data)
            with self.subTest(restriction=restriction):
                self.assertTrue(report.ok)
                self.assertTrue(report.preparation_ready)
                self.assertNotIn("ingrediente_generico_pendente", {item.code for item in report.action_items})

    def test_a_food_word_can_be_the_head_even_when_it_is_also_a_preparation_descriptor(self) -> None:
        for restriction, instruction in (("sal grosso", "Adicione sal."), ("casca de limão", "Acrescente a casca ralada.")):
            data = practical_delivery_data()
            data["research"]["request"]["profile"]["excluded_ingredients"] = [restriction]
            self.step(data, instruction)
            with self.subTest(restriction=restriction):
                self.assert_identification_pending(data)

    def test_simple_or_explicit_restriction_keeps_the_existing_block(self) -> None:
        for restriction, instruction in (("amendoim", "Adicione amendoim."), ("castanha-de-caju", "Adicione castanhas-de-caju.")):
            data = practical_delivery_data()
            data["research"]["request"]["profile"]["excluded_ingredients"] = [restriction]
            self.step(data, instruction)
            report = self.report(data)
            with self.subTest(restriction=restriction):
                self.assertFalse(report.ok)
                self.assertFalse(report.preparation_ready)
                self.assertIn("restricao_nas_etapas", {item.code for item in report.issues})
                self.assertNotIn("ingrediente_generico_pendente", {item.code for item in report.action_items})

    def test_human_output_shows_the_plan_and_the_identification_action(self) -> None:
        data = self.data()
        self.step(data, "Adicione castanhas picadas.")
        text, code = render_delivery(Delivery.model_validate(data))
        self.assertEqual(code, 0)
        self.assertIn("Plano da receita. Antes de começar:", text)
        self.assertIn("Identifique qual ingrediente será usado", text)
        self.assertIn("Como fazer", text)
        self.assertNotIn("ingrediente_generico_pendente", text)

    def test_identifying_the_ingredient_resolves_the_pending_action(self) -> None:
        data = self.data()
        self.step(data, "Adicione castanhas picadas.")
        self.assert_identification_pending(data)
        self.declare_alternative(data)
        self.step(data, "Adicione castanhas-do-pará.")
        self.assertTrue(self.report(data).preparation_ready)


if __name__ == "__main__":
    unittest.main()
