"""Regressões com dados sintéticos explícitos; nenhuma fixture comprova fonte real."""

from __future__ import annotations

import copy
import unittest
from datetime import date, timedelta

from pydantic import ValidationError

from receitas_tradicionais.core import normalize_text, normalize_url, onboarding_questions, plan_research, validate_delivery, validate_research
from receitas_tradicionais.models import Delivery, Profile, Request, ResearchBatch


def request_data() -> dict:
    return {
        "dish": "Prato sintético de teste",
        "country": "BR",
        "variant": "Variante sintética sem alegação histórica",
        "ambiguity_resolved": True,
        "profile": {"onboarding_confirmed": True, "servings": 4},
    }


def batch_data() -> dict:
    request = request_data()
    return {
        "request": request,
        "sources": [
            {
                "id": f"teste_{index}",
                "title": f"Receita sintética de teste {index}",
                "url": f"https://fonte{index}.example.test/receita",
                "author": "Autoria sintética de teste",
                "publisher": f"Publicação sintética {index}",
                "editorial_group": f"Grupo sintético {index}",
                "country": "BR",
                "editorial_country_evidence": {"text": "Declaração sintética para teste do contrato.", "url": f"https://fonte{index}.example.test/sobre"},
                "accessed_at": date.today().isoformat(),
                "publication_date": None,
                "read_status": "complete",
                "kind": "domestic" if index == 0 else "editorial",
                "research_track": "domestic_regional" if index == 0 else "base",
                "sections": {"ingredients": "read", "method": "read", "notes": "read", "comments": "unavailable"},
                "ingredients": ["arroz", "água"],
                "technique_summary": "Técnica sintética registrada somente para testar o contrato.",
                "detail_notes": ["Detalhe sintético documentado apenas no contexto do teste."],
                "provenance_origin": f"https://fonte{index}.example.test/receita",
            }
            for index in range(7)
        ],
        "queries": [{"text": request["dish"], "derived_from": None}],
        "completed_tracks": ["base", "domestic_regional"],
        "pages_read": 7,
        "researchers_count": 2,
        "reformulations_by_track": {"base": 1, "domestic_regional": 0},
    }


def delivery_data() -> dict:
    return {
        "research": batch_data(),
        "ingredients": [{"name": "arroz"}, {"name": "água"}],
        "steps": ["Etapa sintética para teste do contrato."],
        "labels_reviewed": True,
    }


class ResearchTests(unittest.TestCase):
    def codes(self, data: dict) -> set[str]:
        return {item.code for item in validate_research(ResearchBatch.model_validate(data)).issues}

    def test_complete_batch_passes_only_documentary_checks(self) -> None:
        report = validate_research(ResearchBatch.model_validate(batch_data()))
        self.assertTrue(report.ok)
        self.assertTrue(report.semantic_review_required)
        self.assertIn("declarações", report.limitations[0])

    def test_exact_seven_sources(self) -> None:
        for count in [0, 6, 8]:
            with self.subTest(count=count):
                data = batch_data()
                if count == 8:
                    eighth = copy.deepcopy(data["sources"][0])
                    eighth.update(id="oitava", editorial_group="Oitavo grupo", url="https://oitava.example.test/r", provenance_origin="https://oitava.example.test/r")
                    data["sources"].append(eighth)
                    data["pages_read"] = 8
                else:
                    data["sources"] = data["sources"][:count]
                self.assertIn("contagem_fontes", self.codes(data))

    def test_url_tracking_fragment_and_www_are_duplicates(self) -> None:
        data = batch_data()
        data["sources"][1]["url"] = "http://www.fonte0.example.test/receita/?utm_source=teste#parte"
        self.assertIn("duplicado_url", self.codes(data))

    def test_same_editorial_group_is_duplicate_after_normalization(self) -> None:
        data = batch_data()
        data["sources"][1]["editorial_group"] = "GRUPO SINTETICO-0"
        self.assertIn("duplicado_editorial_group", self.codes(data))

    def test_republication_does_not_count_twice(self) -> None:
        data = batch_data()
        data["sources"][1]["provenance_origin"] = "https://www.fonte0.example.test/receita?ref=outro"
        self.assertIn("duplicado_provenance_origin", self.codes(data))

    def test_country_mismatch_is_blocked(self) -> None:
        data = batch_data()
        data["sources"][0]["country"] = "PT"
        self.assertIn("pais_divergente", self.codes(data))

    def test_editorial_evidence_required(self) -> None:
        for change in [{}, {"text": "", "url": "https://example.test/sobre"}, {"text": "Declaração", "url": ""}]:
            data = batch_data()
            data["sources"][0]["editorial_country_evidence"] = change
            with self.subTest(change=change), self.assertRaises(ValidationError):
                ResearchBatch.model_validate(data)

    def test_snippet_and_unavailable_are_blocked(self) -> None:
        for status in ["snippet", "unavailable"]:
            data = batch_data()
            data["sources"][0]["read_status"] = status
            self.assertIn("leitura_incompleta", self.codes(data))

    def test_future_dates_and_invalid_order_are_blocked(self) -> None:
        for key in ["accessed_at", "publication_date"]:
            data = batch_data()
            data["sources"][0][key] = (date.today() + timedelta(days=1)).isoformat()
            self.assertIn("data_futura", self.codes(data))
        data = batch_data()
        data["sources"][0]["accessed_at"] = (date.today() - timedelta(days=2)).isoformat()
        data["sources"][0]["publication_date"] = date.today().isoformat()
        self.assertIn("cronologia_invalida", self.codes(data))

    def test_missing_ingredients_domestic_details(self) -> None:
        data = batch_data()
        data["sources"][0]["ingredients"] = []
        self.assertIn("ingredientes_ausentes", self.codes(data))
        for source in data["sources"]:
            source["kind"] = "editorial"
            source["detail_notes"] = []
        self.assertTrue({"saber_domestico_ausente", "detalhes_ausentes"}.issubset(self.codes(data)))

    def test_onboarding_allergy_is_accepted_without_diagnosis(self) -> None:
        data = request_data()
        data["profile"]["allergies"] = ["AMENDOIM"]
        self.assertTrue(plan_research(Request.model_validate(data))["ok"])
        self.assertEqual(plan_research(Request.model_validate(data))["queries"], [{"text": data["dish"], "derived_from": None}])

    def test_pending_homonym_and_onboarding_block_all_queries(self) -> None:
        data = request_data()
        data["ambiguity_resolved"] = False
        data["profile"]["onboarding_confirmed"] = False
        result = plan_research(Request.model_validate(data))
        self.assertFalse(result["ok"])
        self.assertEqual(result["queries"], [])
        self.assertEqual({item["code"] for item in result["issues"]}, {"onboarding_pendente", "ambiguidade_pendente"})

    def test_strict_types_extra_fields_iso_country_and_dates(self) -> None:
        for path, value in [("servings", "4"), ("servings", True), ("onboarding_confirmed", "sim"), ("name", "Identificação proibida")]:
            data = request_data()
            data["profile"][path] = value
            with self.subTest(path=path), self.assertRaises(ValidationError):
                Request.model_validate(data)
        data = request_data()
        data["country"] = "ZZ"
        with self.assertRaises(ValidationError):
            Request.model_validate(data)
        data = batch_data()
        data["sources"][0]["accessed_at"] = "2026-02-30"
        with self.assertRaises(ValidationError):
            ResearchBatch.model_validate(data)

    def test_queries_evidence_and_budgets(self) -> None:
        data = batch_data()
        data["queries"][0]["text"] += " dica prévia"
        self.assertIn("busca_inicial", self.codes(data))
        data = batch_data()
        data["queries"].append({"text": "Refinamento"})
        self.assertIn("refinamento_sem_origem", self.codes(data))
        data["queries"] = [batch_data()["queries"][0]] + [{"text": "Refinamento", "derived_from": "Fonte sintética já lida"}] * 32
        self.assertIn("teto_consultas", self.codes(data))
        data["pages_read"] = 41
        self.assertIn("teto_paginas", self.codes(data))
        data["pages_read"] = 0
        self.assertIn("paginas_insuficientes", self.codes(data))

    def test_both_tracks_and_linked_sources_required(self) -> None:
        data = batch_data()
        data["completed_tracks"] = ["base", "base"]
        self.assertIn("trajetorias_pendentes", self.codes(data))
        for source in data["sources"]:
            source["research_track"] = "base"
        self.assertIn("fontes_por_trajetoria", self.codes(data))

    def test_researcher_and_reformulation_limits_are_enforced(self) -> None:
        for field, value in [("researchers_count", 4), ("researchers_count", 0), ("reformulations_by_track", {"base": 3, "domestic_regional": 0})]:
            data = batch_data()
            data[field] = value
            with self.subTest(field=field), self.assertRaises(ValidationError):
                ResearchBatch.model_validate(data)

    def test_unmeasured_reformulations_are_accepted_as_data_but_block_gate(self) -> None:
        for field in ["base", "domestic_regional"]:
            data = batch_data()
            data["reformulations_by_track"][field] = None
            self.assertIn("reformulacoes_nao_medidas", self.codes(data))

    def test_source_sections_need_read_ingredients_and_method(self) -> None:
        for field in ["ingredients", "method"]:
            data = batch_data()
            data["sources"][0]["sections"][field] = "unavailable"
            self.assertIn("secoes_essenciais_pendentes", self.codes(data))
        data = batch_data()
        del data["sources"][0]["sections"]
        with self.assertRaises(ValidationError):
            ResearchBatch.model_validate(data)
        report = validate_research(ResearchBatch.model_validate(batch_data()))
        self.assertTrue(report.ok)
        self.assertTrue(any("inacessíveis" in item for item in report.limitations))

    def test_equipment_question_and_no_profile_persistence_api(self) -> None:
        questions = onboarding_questions()
        self.assertIn("equipment", {q["field"] for q in questions["questions"]})
        self.assertNotIn("name", Profile.model_fields)

    def test_url_port_and_percent_normalization(self) -> None:
        self.assertEqual(normalize_url("https://www.example.test:443/a%62/?x=1#z"), normalize_url("http://example.test/ab"))

    def test_international_ingredient_and_group_names_are_preserved(self) -> None:
        self.assertEqual(normalize_text("小麦"), "小麦")
        data = delivery_data()
        data["research"]["request"]["profile"]["excluded_ingredients"] = ["小麦"]
        data["ingredients"] = [{"name": "Farinha", "aliases": ["小麦"]}]
        self.assertTrue(any(item.code == "ingrediente_restrito" for item in validate_delivery(Delivery.model_validate(data)).issues))


class DeliveryTests(unittest.TestCase):
    def codes(self, data: dict) -> set[str]:
        return {item.code for item in validate_delivery(Delivery.model_validate(data)).issues}

    def test_delivery_with_valid_batch_and_inventory(self) -> None:
        report = validate_delivery(Delivery.model_validate(delivery_data()))
        self.assertTrue(report.ok)
        self.assertTrue(report.semantic_review_required)
        self.assertTrue(any("não detecta todos" in text for text in report.limitations))

    def test_bad_research_blocks_delivery(self) -> None:
        data = delivery_data()
        data["research"]["sources"].pop()
        self.assertIn("contagem_fontes", self.codes(data))
        data = delivery_data()
        data["research"]["sources"][0]["country"] = "PT"
        self.assertIn("pais_divergente", self.codes(data))

    def test_profile_cannot_be_swapped_outside_embedded_batch(self) -> None:
        data = delivery_data()
        data["request"] = request_data()
        with self.assertRaises(ValidationError):
            Delivery.model_validate(data)

    def test_historical_exclusion_allowed_but_operational_conflict_blocks(self) -> None:
        data = delivery_data()
        data["research"]["request"]["profile"]["excluded_ingredients"] = ["arroz"]
        research = ResearchBatch.model_validate(data["research"])
        self.assertTrue(validate_research(research).ok)
        self.assertIn("ingrediente_restrito", self.codes(data))

    def test_normalization_aliases_components_and_word_boundaries(self) -> None:
        for field, label in [("name", "ÓLEO DE AMENDOIM"), ("aliases", ["Pasta de amendoim"]), ("components", ["AMENDOIM torrado"])]:
            data = delivery_data()
            data["research"]["request"]["profile"]["allergies"] = ["amendoim"]
            data["cross_contact_reviewed"] = True
            data["ingredients"] = [{"name": "Ingrediente de teste", field: label}]
            self.assertIn("ingrediente_restrito", self.codes(data))
        data = delivery_data()
        data["research"]["request"]["profile"]["excluded_ingredients"] = ["sal"]
        data["ingredients"] = [{"name": "salsa"}]
        self.assertNotIn("ingrediente_restrito", self.codes(data))

    def test_labels_and_allergy_cross_contact_must_be_reviewed(self) -> None:
        data = delivery_data()
        data["labels_reviewed"] = False
        self.assertIn("rotulos_pendentes", self.codes(data))
        data["research"]["request"]["profile"]["allergies"] = ["amendoim"]
        self.assertIn("contato_cruzado_pendente", self.codes(data))

    def test_empty_inventory_and_steps_block(self) -> None:
        data = delivery_data()
        data["ingredients"] = []
        data["steps"] = []
        self.assertTrue({"inventario_ausente", "etapas_ausentes"}.issubset(self.codes(data)))

    def test_alcohol_flag_is_blocked(self) -> None:
        data = delivery_data()
        data["ingredients"][0]["alcohol"] = True
        self.assertIn("alcool_na_entrega", self.codes(data))

    def test_culinary_alcohol_names_are_blocked_without_flag(self) -> None:
        for label in ["vinho branco", "beer", "vino tinto", "vin blanc", "cachaça", "mirin"]:
            data = delivery_data()
            data["ingredients"] = [{"name": label}]
            with self.subTest(label=label):
                self.assertIn("alcool_na_entrega", self.codes(data))

    def test_explicit_restricted_or_alcohol_ingredient_in_steps_blocks(self) -> None:
        data = delivery_data()
        data["research"]["request"]["profile"]["allergies"] = ["amendoim"]
        data["cross_contact_reviewed"] = True
        data["steps"] = ["Adicione amendoim ao recipiente."]
        self.assertIn("restricao_nas_etapas", self.codes(data))
        data["steps"] = ["Adicione wine ao recipiente."]
        self.assertIn("alcool_nas_etapas", self.codes(data))
        data["ingredients"] = [{"name": "Ingrediente sintético", "components": ["Álcool etílico"]}]
        self.assertIn("alcool_na_entrega", self.codes(data))


if __name__ == "__main__":
    unittest.main()
