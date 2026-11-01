"""A saída humana preserva as declarações e a sintaxe dos trechos de máquina."""

from __future__ import annotations

import unittest

from receitas_tradicionais.models import Delivery
from receitas_tradicionais.presentation import human_text, render_delivery
from test_core import delivery_data
from test_practical import practical_delivery_data


class PresentationTests(unittest.TestCase):
    def test_typography_is_deterministic_and_keeps_machine_fragments_intact(self) -> None:
        straight = chr(34)
        for separator in [chr(0x2013), chr(0x2014)]:
            data = practical_delivery_data()
            data["recipe_card"]["title"] = f"Arroz {straight}de casa{straight} {separator} teste"
            url = "https://fonte0.example.test/receita?dados=%22valor%22"
            data["research"]["sources"][0]["url"] = url
            command = f"`python -c {straight}print(1){straight}`"
            encoded = f"{{{straight}campo{straight}: {straight}valor{straight}}}"
            data["recipe_card"]["adaptations"] = [f"Trechos de máquina preservados: {command} e {encoded}."]
            text, code = render_delivery(Delivery.model_validate(data))
            self.assertEqual(code, 0)
            self.assertIn("Arroz “de casa” - teste", text)
            self.assertNotIn(chr(0x2013), text)
            self.assertNotIn(chr(0x2014), text)
            self.assertIn(url, text)
            self.assertIn(command, text)
            self.assertIn(encoded, text)
            self.assertEqual(text, render_delivery(Delivery.model_validate(data))[0])

    def test_plain_incomplete_record_is_not_presented_as_a_recipe(self) -> None:
        text, code = render_delivery(Delivery.model_validate(delivery_data()))
        self.assertEqual(code, 1)
        self.assertIn("quantidades", text)
        self.assertNotIn("Como fazer", text)
        self.assertNotIn("ficha_pratica_ausente", text)

    def test_quoted_url_does_not_keep_a_human_closing_quote_as_machine_text(self) -> None:
        quote = chr(34)
        url = "https://exemplo.example.test/caminho?x=%22y%22"
        self.assertEqual(human_text(f"Veja {quote}{url}{quote}."), f"Veja “{url}”.")


if __name__ == "__main__":
    unittest.main()
