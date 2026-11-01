"""Jornadas sintéticas de entrada, ficha útil e preparo com revisão proporcional."""

from __future__ import annotations

import unittest

from pydantic import ValidationError

from receitas_tradicionais.core import normalize_url, onboarding_questions, plan_research, validate_delivery
from receitas_tradicionais.models import Delivery, Request, validate_http_url
from test_core import delivery_data, request_data


def practical_delivery_data() -> dict:
    data = delivery_data()
    data["research"]["request"]["profile"]["equipment"] = ["panela"]
    data["steps"] = ["Cozinhe o arroz com a água em fogo baixo."]
    data["labels_reviewed"] = False
    data["recipe_card"] = {
        "title": "Arroz sintético para testar a ficha",
        "servings": 4,
        "yield_basis": "estimate",
        "yield_note": "Rendimento estimado, usado somente como fixture de teste.",
        "active_minutes": 5,
        "total_minutes": 25,
        "equipment": ["panela"],
        "ingredients": [
            {"name": "arroz", "quantity": "1", "unit": "xícara", "household_measure": "1 xícara de chá", "source_ids": ["teste_0"]},
            {"name": "água", "quantity": "2", "unit": "xícaras", "source_ids": ["teste_0"]},
        ],
        "steps": [{"instruction": data["steps"][0], "observable_cue": "Os grãos ficam macios e a água é absorvida.", "time_hint": "Observe o ponto; o tempo é aproximado."}],
        "shopping_list": [],
        "flavor_detail": {"action": "Use fogo baixo durante a etapa descrita.", "effect": "Detalhe sintético de textura para testar a atribuição.", "category": "texture", "source_ids": ["teste_0"]},
        "source_ids": [f"teste_{i}" for i in range(7)],
    }
    return data


class PracticalJourneyTests(unittest.TestCase):
    def report(self, data: dict):
        return validate_delivery(Delivery.model_validate(data))

    def test_number_flexions_block_every_delivery_surface_in_both_directions(self) -> None:
        pairs = [
            ("ovo", "ovos"), ("camarão", "camarões"), ("pimentão", "pimentões"),
            ("noz", "nozes"), ("noz-pecã", "nozes-pecãs"), ("arroz", "arrozes"),
            ("anis", "anises"), ("pão", "pães"), ("pastel", "pastéis"),
            ("vagem", "vagens"), ("atum", "atuns"), ("sal", "sais"),
            ("farol", "faróis"), ("azul", "azuis"), ("mão", "mãos"),
        ]
        for restriction, ingredient in [*pairs, *((b, a) for a, b in pairs)]:
            for field in ("excluded_ingredients", "allergies", "intolerances"):
                data = practical_delivery_data()
                data["research"]["request"]["profile"][field] = [restriction]
                data["ingredients"].append({"name": ingredient})
                data["recipe_card"]["ingredients"].append({"name": ingredient, "quantity": "1", "unit": "unidade", "source_ids": ["teste_0"]})
                data["steps"] = [f"Adicione {ingredient}."]
                data["recipe_card"]["steps"] = [{"instruction": data["steps"][0], "observable_cue": "Mistura homogênea."}]
                data["adaptation_notes"] = [f"Use {ingredient} na adaptação."]
                with self.subTest(restriction=restriction, ingredient=ingredient, field=field):
                    report = self.report(data)
                    self.assertFalse(report.ok)
                    self.assertFalse(report.practical_ready)
                    self.assertTrue({"ingrediente_restrito", "restricao_na_ficha", "restricao_nas_etapas", "restricao_nas_notas"}.issubset({issue.code for issue in report.issues}))

    def test_specific_restriction_matches_generic_ingredient_label_only(self) -> None:
        for restriction, ingredient in (("castanhas-de-caju", "castanha"), ("cogumelo shiitake", "cogumelos")):
            data = practical_delivery_data()
            data["research"]["request"]["profile"]["excluded_ingredients"] = [restriction]
            data["ingredients"].append({"name": ingredient})
            data["recipe_card"]["ingredients"].append({"name": ingredient, "quantity": "1", "unit": "unidade", "source_ids": ["teste_0"]})
            data["steps"] = [f"Adicione {ingredient}."]
            data["recipe_card"]["steps"] = [{"instruction": data["steps"][0], "observable_cue": "Mistura homogênea."}]
            data["adaptation_notes"] = [f"Use {ingredient} na adaptação."]
            with self.subTest(restriction=restriction, ingredient=ingredient):
                codes = {issue.code for issue in self.report(data).issues}
                self.assertIn("ingrediente_restrito", codes)
                self.assertIn("restricao_na_ficha", codes)
                self.assertNotIn("restricao_nas_etapas", codes)
                self.assertNotIn("restricao_nas_notas", codes)

    def test_number_flexions_in_aliases_and_components(self) -> None:
        for field in ("aliases", "components"):
            for restriction, label in (("noz", "nozes"), ("pães", "pão"), ("vagem", "vagens")):
                data = practical_delivery_data()
                data["research"]["request"]["profile"]["excluded_ingredients"] = [restriction]
                data["ingredients"][0][field] = [label]
                data["recipe_card"]["ingredients"][0][field] = [label]
                with self.subTest(field=field, restriction=restriction, label=label):
                    codes = {issue.code for issue in self.report(data).issues}
                    self.assertIn("ingrediente_restrito", codes)
                    self.assertIn("restricao_na_ficha", codes)

    def test_specific_restriction_in_steps_and_notes_requires_full_phrase(self) -> None:
        for restriction, phrase in (("castanha de caju", "castanhas-de-caju"), ("cogumelo shiitake", "cogumelos shiitake")):
            data = practical_delivery_data()
            data["research"]["request"]["profile"]["excluded_ingredients"] = [restriction]
            data["steps"] = [f"Acrescente {phrase}."]
            data["recipe_card"]["steps"] = [{"instruction": data["steps"][0], "observable_cue": "Mistura homogênea."}]
            data["adaptation_notes"] = [f"Use {phrase} na adaptação."]
            with self.subTest(restriction=restriction, phrase=phrase):
                codes = {issue.code for issue in self.report(data).issues}
                self.assertIn("restricao_nas_etapas", codes)
                self.assertIn("restricao_nas_notas", codes)
                self.assertIn("restricao_na_ficha", codes)

    def test_generic_word_in_card_note_does_not_complete_specific_restriction(self) -> None:
        data = practical_delivery_data()
        data["research"]["request"]["profile"]["excluded_ingredients"] = ["castanhas de caju"]
        data["recipe_card"]["ingredients"][0]["note"] = "Confira a castanha no rótulo de outro produto."
        codes = {issue.code for issue in self.report(data).issues}
        self.assertNotIn("restricao_na_ficha", codes)

    def test_missing_equipment_requires_confirmation(self) -> None:
        data = practical_delivery_data()
        data["research"]["request"]["profile"].pop("equipment")
        data["recipe_card"]["equipment"] = ["panela de pressão de 6 litros", "liquidificador"]
        report = self.report(data)
        self.assertTrue(report.ok)
        self.assertFalse(report.practical_ready)
        self.assertIn("equipamento_nao_confirmado", {item.code for item in report.action_items})

    def test_missing_servings_requires_confirmation(self) -> None:
        data = practical_delivery_data()
        data["research"]["request"]["profile"].pop("servings")
        request = Request.model_validate(data["research"]["request"])
        self.assertIsNone(request.profile.servings)
        self.assertTrue(plan_research(request)["ok"])
        report = self.report(data)
        self.assertTrue(report.ok)
        self.assertFalse(report.practical_ready)
        self.assertIn("porcoes_nao_confirmadas", {item.code for item in report.action_items})

    def test_complete_card_is_usable_without_universal_label_attestation(self) -> None:
        report = self.report(practical_delivery_data())
        self.assertTrue(report.ok)
        self.assertTrue(report.practical_ready)
        self.assertTrue(report.preparation_ready)
        self.assertEqual(report.action_items, [])
        self.assertTrue(report.semantic_review_required)

    def test_legacy_delivery_remains_readable_but_is_not_a_complete_recipe(self) -> None:
        report = self.report(delivery_data())
        self.assertTrue(report.ok)
        self.assertFalse(report.practical_ready)
        self.assertFalse(report.preparation_ready)
        self.assertIn("ficha_pratica_ausente", {issue.code for issue in report.action_items})

    def test_uncertainty_does_not_become_an_allergy_or_a_clean_bill(self) -> None:
        data = practical_delivery_data()
        data["research"]["request"]["profile"]["onboarding_unknowns"] = ["leite: motivo ainda desconhecido"]
        parsed = Delivery.model_validate(data)
        self.assertEqual(parsed.research.request.profile.allergies, [])
        report = validate_delivery(parsed)
        self.assertTrue(report.ok)
        self.assertTrue(report.practical_ready)
        self.assertFalse(report.preparation_ready)
        self.assertIn("duvidas_alimentares_pendentes", {issue.code for issue in report.action_items})

    def test_allergy_allows_plan_and_requires_applicable_human_checks(self) -> None:
        data = practical_delivery_data()
        data["research"]["request"]["profile"]["allergies"] = ["amendoim"]
        data["ingredients"][0]["label_required"] = True
        report = self.report(data)
        self.assertTrue(report.ok)
        self.assertTrue(report.practical_ready)
        self.assertFalse(report.preparation_ready)
        self.assertEqual({issue.code for issue in report.action_items}, {"rotulos_pendentes", "contato_cruzado_pendente"})
        data["labels_reviewed"] = True
        data["cross_contact_reviewed"] = True
        self.assertTrue(self.report(data).preparation_ready)

    def test_intolerance_with_compound_ingredient_checks_labels_not_cross_contact(self) -> None:
        data = practical_delivery_data()
        data["research"]["request"]["profile"]["intolerances"] = ["lactose"]
        data["recipe_card"]["ingredients"][0]["components"] = ["arroz", "sal"]
        report = self.report(data)
        self.assertTrue(report.practical_ready)
        self.assertEqual({issue.code for issue in report.action_items}, {"rotulos_pendentes"})

    def test_restriction_cannot_enter_via_shopping_flavor_measure_or_adaptation(self) -> None:
        for field in ["shopping_list", "flavor_detail", "adaptations", "household_measure", "observable_cue"]:
            data = practical_delivery_data()
            data["research"]["request"]["profile"]["excluded_ingredients"] = ["amendoim"]
            card = data["recipe_card"]
            if field in {"shopping_list", "adaptations"}:
                card[field] = ["Acrescente amendoim torrado."]
            elif field == "flavor_detail":
                card[field]["action"] = "Acrescente amendoim torrado."
            elif field == "household_measure":
                card["ingredients"][0][field] = "1 xícara de amendoim"
            else:
                card["steps"][0][field] = "Observe o amendoim dourar."
            with self.subTest(field=field):
                report = self.report(data)
                self.assertFalse(report.ok)
                self.assertFalse(report.practical_ready)
                self.assertIn("restricao_na_ficha", {issue.code for issue in report.issues})

    def test_card_cannot_hide_alcohol_or_added_commercial_enhancer(self) -> None:
        for term, expected in [("ajinomoto", "realcador_adicionado"), ("wine", "alcool_na_ficha")]:
            data = practical_delivery_data()
            data["recipe_card"]["shopping_list"] = [term]
            with self.subTest(term=term):
                report = self.report(data)
                self.assertFalse(report.ok)
                self.assertIn(expected, {issue.code for issue in report.issues})

    def test_commercial_enhancer_preference_is_not_an_implicit_health_claim(self) -> None:
        data = practical_delivery_data()
        data["research"]["request"]["profile"]["avoid_added_flavor_enhancers"] = False
        data["ingredients"][0]["added_flavor_enhancer"] = True
        self.assertNotIn("realcador_adicionado", {issue.code for issue in self.report(data).issues})

    def test_card_missing_measure_or_observable_point_is_rejected(self) -> None:
        for field in ["quantity", "unit"]:
            data = practical_delivery_data()
            del data["recipe_card"]["ingredients"][0][field]
            with self.subTest(field=field), self.assertRaises(ValidationError):
                Delivery.model_validate(data)
        data = practical_delivery_data()
        del data["recipe_card"]["steps"][0]["observable_cue"]
        with self.assertRaises(ValidationError):
            Delivery.model_validate(data)

    def test_zero_negative_or_unresolved_quantity_does_not_make_a_complete_card(self) -> None:
        for quantity in ["0", "0,0", "0/2", "1/0", "-1", "a definir", "não sei", "banana", "zero", "0e0", "1/0 kg", "2 a 1"]:
            data = practical_delivery_data()
            data["recipe_card"]["ingredients"][0]["quantity"] = quantity
            with self.subTest(quantity=quantity):
                report = self.report(data)
                self.assertFalse(report.practical_ready)
                self.assertIn("quantidade_pendente", {issue.code for issue in report.action_items})

    def test_fraction_and_household_measure_remain_usable(self) -> None:
        for quantity in ["1/2", "0,5", "1.5", "1 1/2", "1 a 2", "1/2 até 3/4", "1-2", "½", "1½"]:
            data = practical_delivery_data()
            data["recipe_card"]["ingredients"][0]["quantity"] = quantity
            with self.subTest(quantity=quantity):
                self.assertTrue(self.report(data).practical_ready)

    def test_to_taste_requires_an_observable_gradual_adjustment(self) -> None:
        data = practical_delivery_data()
        data["recipe_card"]["ingredients"][0]["quantity"] = "a gosto"
        for note in [None, "a gosto", "como preferir", "adicione por vez"]:
            data["recipe_card"]["ingredients"][0]["note"] = note
            with self.subTest(note=note):
                self.assertFalse(self.report(data).practical_ready)
        data["recipe_card"]["ingredients"][0]["note"] = "Acrescente uma pequena pitada por vez, misture e prove antes de repetir."
        self.assertTrue(self.report(data).practical_ready)

    def test_common_pan_does_not_prove_pressure_type_or_capacity(self) -> None:
        data = practical_delivery_data()
        data["research"]["request"]["profile"]["equipment"] = ["panela"]
        for required in ["panela de pressão", "panela de pressão de 4 litros", "panela de 4 litros"]:
            data["recipe_card"]["equipment"] = [required]
            with self.subTest(required=required):
                report = self.report(data)
                self.assertFalse(report.practical_ready)
                self.assertIn("equipamento_nao_confirmado", {issue.code for issue in report.action_items})
        data["recipe_card"]["equipment"] = ["panela comum"]
        self.assertTrue(self.report(data).practical_ready)
        data["research"]["request"]["profile"]["equipment"] = ["airfryer"]
        data["recipe_card"]["equipment"] = ["air fryer"]
        self.assertTrue(self.report(data).practical_ready)

    def test_dietary_pattern_is_not_silently_ignored_or_a_user_ontology_task(self) -> None:
        data = practical_delivery_data()
        profile = data["research"]["request"]["profile"]
        profile["dietary_patterns"] = ["vegano"]
        data["ingredients"][0]["name"] = "carne bovina"
        data["recipe_card"]["ingredients"][0]["name"] = "carne bovina"
        report = self.report(data)
        self.assertFalse(report.practical_ready)
        self.assertFalse(report.preparation_ready)
        self.assertIn("padrao_alimentar_pendente", {issue.code for issue in report.action_items})
        data["dietary_pattern_review"] = [{"pattern": "vegano", "excluded_ingredients": ["carne bovina"], "compatibility_reviewed": True, "review_note": "O host registrou as exclusões e reviu a composição da receita."}]
        self.assertFalse(self.report(data).practical_ready)
        profile["excluded_ingredients"] = ["carne bovina"]
        report = self.report(data)
        self.assertFalse(report.ok)
        self.assertIn("ingrediente_restrito", {issue.code for issue in report.issues})

    def test_host_pattern_review_allows_compatible_recipe_without_clinical_attestation(self) -> None:
        data = practical_delivery_data()
        profile = data["research"]["request"]["profile"]
        profile["dietary_patterns"] = ["vegano"]
        profile["excluded_ingredients"] = ["carne", "peixe", "ovo", "leite", "mel", "gelatina"]
        data["dietary_pattern_review"] = [{"pattern": "vegano", "excluded_ingredients": profile["excluded_ingredients"], "compatibility_reviewed": True, "review_note": "Revisão culinária declarada pelo host para a ficha de arroz e água; não é orientação clínica."}]
        self.assertTrue(self.report(data).practical_ready)
        data["dietary_pattern_review"][0]["compatibility_reviewed"] = False
        self.assertFalse(self.report(data).practical_ready)

    def test_api_general_preferences_remain_informative(self) -> None:
        data = practical_delivery_data()
        data["research"]["request"]["profile"]["preferences"] = ["crocante"]
        self.assertTrue(self.report(data).practical_ready)

    def test_a_complete_recipe_does_not_require_an_invented_secret(self) -> None:
        data = practical_delivery_data()
        del data["recipe_card"]["flavor_detail"]
        self.assertFalse(self.report(data).practical_ready)
        data["recipe_card"]["detail_search_note"] = "As sete receitas foram comparadas; não foi confirmado detalhe incomum aplicável a esta versão."
        report = self.report(data)
        self.assertTrue(report.practical_ready)
        self.assertTrue(report.preparation_ready)
        self.assertIsNone(Delivery.model_validate(data).recipe_card.flavor_detail)

    def test_mismatched_inventory_or_steps_cannot_be_called_ready(self) -> None:
        for field in ["ingredients", "steps"]:
            data = practical_delivery_data()
            if field == "ingredients":
                data["recipe_card"][field][0]["name"] = "feijão"
            else:
                data["recipe_card"][field][0]["instruction"] = "Uma instrução diferente daquela validada."
            with self.subTest(field=field):
                report = self.report(data)
                self.assertFalse(report.practical_ready)
                self.assertTrue(any("divergent" in issue.code for issue in report.action_items))

    def test_yield_basis_does_not_silently_turn_requested_portions_into_source_fact(self) -> None:
        data = practical_delivery_data()
        data["recipe_card"]["yield_note"] = "Quatro porções."
        self.assertFalse(self.report(data).practical_ready)
        data["recipe_card"]["yield_basis"] = "scaled"
        self.assertIn("escala_sem_calculo", {issue.code for issue in self.report(data).action_items})
        data["recipe_card"]["yield_note"] = "A fonte rende 2 porções; quantidades multiplicadas por 2 para 4 porções."
        self.assertTrue(self.report(data).practical_ready)

    def test_card_and_detail_source_references_must_belong_to_selected_seven(self) -> None:
        for field in ["source_ids", "flavor_detail", "ingredients"]:
            data = practical_delivery_data()
            card = data["recipe_card"]
            if field == "source_ids":
                card[field][0] = "outra_fonte"
            elif field == "flavor_detail":
                card[field]["source_ids"] = ["outra_fonte"]
            else:
                card[field][0]["source_ids"] = ["outra_fonte"]
            with self.subTest(field=field):
                self.assertFalse(self.report(data).practical_ready)

    def test_time_equipment_and_no_shopping_constraints_are_actionable(self) -> None:
        data = practical_delivery_data()
        data["research"]["request"]["kitchen"] = {"time_available_minutes": 15, "shopping_allowed": False}
        data["research"]["request"]["profile"]["equipment"] = ["micro-ondas"]
        data["recipe_card"]["shopping_list"] = ["arroz"]
        report = self.report(data)
        self.assertTrue(report.ok)
        self.assertFalse(report.practical_ready)
        self.assertEqual({issue.code for issue in report.action_items}, {"tempo_indisponivel", "compras_nao_autorizadas", "equipamento_nao_confirmado"})

    def test_active_time_cannot_exceed_total_time(self) -> None:
        data = practical_delivery_data()
        data["recipe_card"]["active_minutes"] = 30
        self.assertIn("tempos_inconsistentes", {issue.code for issue in self.report(data).action_items})

    def test_plan_keeps_neutral_keyword_and_actual_kitchen_conditions(self) -> None:
        data = request_data()
        data["dish"] = "Feijoada tradicional brasileira"
        data["kitchen"] = {"available_ingredients": ["feijão preto"], "time_available_minutes": 30, "budget": "até R$ 40", "shopping_allowed": False, "output_mode": "passo_a_passo", "taste_goal": "mais aroma"}
        plan = plan_research(Request.model_validate(data))
        self.assertEqual(plan["queries"], [{"text": data["dish"], "derived_from": None}])
        self.assertEqual(plan["kitchen"], Request.model_validate(data).kitchen.model_dump(mode="json"))
        self.assertIn("tempo total", plan["practical_checks"][0])

    def test_checklist_supports_recognition_and_progressive_assistance(self) -> None:
        result = onboarding_questions()
        self.assertEqual(len(result["checklist"]), 10)
        self.assertIn("nenhum", result["reply_options"])
        self.assertIn("não sei", result["reply_options"])
        self.assertIn("um grupo por vez", result["reply_options"])
        self.assertIn("não exclui automaticamente", result["questions"][0]["question"])
        fields = {item["field"] for item in result["kitchen_checklist"]}
        self.assertTrue({"time_available_minutes", "budget", "available_ingredients", "shopping_allowed", "output_mode"}.issubset(fields))

    def test_url_blocks_literal_private_reserved_and_local_hosts_without_dns(self) -> None:
        for url in ["http://127.0.0.1/r", "https://10.1.2.3/r", "http://169.254.169.254/r", "http://192.168.1.1/r", "http://0.0.0.0/r", "http://[::1]/r", "http://[fc00::1]/r", "http://localhost/r", "http://cozinha.local/r", "http://127.1/r", "https://a_b.example.com/r", "https://a\x00.example.com/r"]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                validate_http_url(url)
        for url in ["https://receitas.example.test/r", "https://8.8.8.8/r", "https://[2606:4700:4700::1111]/r"]:
            self.assertEqual(validate_http_url(url), url)
        self.assertEqual(normalize_url("https://[2606:4700:4700::1111]:443/r?ref=1"), "https://[2606:4700:4700::1111]/r")


if __name__ == "__main__":
    unittest.main()
