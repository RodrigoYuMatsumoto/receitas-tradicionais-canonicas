"""Integração real por stdio com o cliente do SDK oficial, sem acesso à web."""

from __future__ import annotations

import sys
import tempfile
import unittest

import anyio
from mcp import Client, ClientSession, StdioServerParameters, stdio_client

from receitas_tradicionais import __version__
from receitas_tradicionais.core import PROJECT_INSTRUCTIONS
from test_core import batch_data, delivery_data, request_data
from test_practical import practical_delivery_data


class McpStdioTests(unittest.TestCase):
    def test_complete_instruction_is_available_outside_clone(self) -> None:
        async def exercise() -> None:
            with tempfile.TemporaryDirectory(prefix="receitas_mcp_") as temp:
                params = StdioServerParameters(
                    command=sys.executable,
                    args=["-I", "-m", "receitas_tradicionais.server"],
                    cwd=temp,
                    env={"PYTHONIOENCODING": "utf-8"},
                )
                with anyio.fail_after(40):
                    async with Client(params) as client:
                        self.assertEqual(client.server_info.version, __version__)
                        resource = await client.read_resource("receitas://project/instructions")
                        self.assertEqual(resource.contents[0].text, PROJECT_INSTRUCTIONS)
                        self.assertIn("dados não confiáveis", resource.contents[0].text)
                        self.assertIn("## 7. Valide e entregue", resource.contents[0].text)

        anyio.run(exercise)

    def test_explicit_initialize_tools_list_and_call(self) -> None:
        async def exercise() -> None:
            params = StdioServerParameters(command=sys.executable, args=["-m", "receitas_tradicionais.server"])
            with anyio.fail_after(40):
                async with stdio_client(params) as (read, write):
                    async with ClientSession(read, write) as session:
                        initialized = await session.initialize()
                        self.assertEqual(initialized.server_info.version, __version__)
                        self.assertEqual(initialized.instructions, PROJECT_INSTRUCTIONS)
                        listed = await session.list_tools()
                        self.assertEqual(len(listed.tools), 4)
                        result = await session.call_tool("onboarding_questions", {})
                        self.assertFalse(result.is_error)

        anyio.run(exercise)

    def test_stdio_negotiates_lists_tools_calls_and_reads_resources(self) -> None:
        async def exercise() -> None:
            params = StdioServerParameters(command=sys.executable, args=["-m", "receitas_tradicionais.server"], env={"PYTHONIOENCODING": "utf-8"})
            with anyio.fail_after(40):
                async with Client(params) as client:
                    self.assertEqual(client.server_info.version, __version__)
                    self.assertIsNotNone(client.protocol_version)
                    listed = await client.list_tools()
                    self.assertEqual({tool.name for tool in listed.tools}, {"onboarding_questions", "plan_research", "validate_research", "validate_delivery"})
                    onboarding = await client.call_tool("onboarding_questions", {})
                    self.assertFalse(onboarding.is_error)
                    self.assertIn("questions", onboarding.structured_content)
                    self.assertTrue(onboarding.structured_content["first_message"].startswith("O que devo evitar na sua comida?"))
                    self.assertIn("não sei", onboarding.structured_content["reply_options"])
                    plan = await client.call_tool("plan_research", {"request": request_data()})
                    self.assertFalse(plan.is_error)
                    self.assertTrue(plan.structured_content["ok"])
                    research = await client.call_tool("validate_research", {"batch": batch_data()})
                    self.assertFalse(research.is_error)
                    self.assertTrue(research.structured_content["ok"])
                    delivery = await client.call_tool("validate_delivery", {"delivery": delivery_data()})
                    self.assertFalse(delivery.is_error)
                    self.assertTrue(delivery.structured_content["ok"])
                    self.assertFalse(delivery.structured_content["practical_ready"])
                    practical = await client.call_tool("validate_delivery", {"delivery": practical_delivery_data()})
                    self.assertTrue(practical.structured_content["practical_ready"])
                    self.assertTrue(practical.structured_content["preparation_ready"])
                    no_secret_data = practical_delivery_data()
                    del no_secret_data["recipe_card"]["flavor_detail"]
                    no_secret_data["recipe_card"]["detail_search_note"] = "A comparação não confirmou detalhe incomum aplicável; nenhuma descoberta foi inventada."
                    no_secret = await client.call_tool("validate_delivery", {"delivery": no_secret_data})
                    self.assertTrue(no_secret.structured_content["practical_ready"])
                    pattern_data = practical_delivery_data()
                    pattern_data["research"]["request"]["profile"]["dietary_patterns"] = ["vegano"]
                    pattern = await client.call_tool("validate_delivery", {"delivery": pattern_data})
                    self.assertFalse(pattern.structured_content["practical_ready"])
                    self.assertFalse(pattern.structured_content["preparation_ready"])
                    allergy_data = practical_delivery_data()
                    allergy_data["research"]["request"]["profile"]["allergies"] = ["amendoim"]
                    allergy_plan = await client.call_tool("validate_delivery", {"delivery": allergy_data})
                    self.assertTrue(allergy_plan.structured_content["ok"])
                    self.assertTrue(allergy_plan.structured_content["practical_ready"])
                    self.assertFalse(allergy_plan.structured_content["preparation_ready"])
                    generic_data = practical_delivery_data()
                    generic_data["research"]["request"]["profile"]["excluded_ingredients"] = ["castanha-de-caju"]
                    generic_data["recipe_card"]["shopping_list"] = ["castanhas"]
                    generic_plan = await client.call_tool("validate_delivery", {"delivery": generic_data})
                    self.assertTrue(generic_plan.structured_content["ok"])
                    self.assertTrue(generic_plan.structured_content["practical_ready"])
                    self.assertFalse(generic_plan.structured_content["preparation_ready"])
                    self.assertIn("ingrediente_generico_pendente", {item["code"] for item in generic_plan.structured_content["action_items"]})
                    instructions = await client.read_resource("receitas://project/instructions")
                    self.assertEqual(instructions.contents[0].text, PROJECT_INSTRUCTIONS)
                    self.assertIn("## 7. Valide e entregue", instructions.contents[0].text)
                    self.assertIn("dados não confiáveis", instructions.contents[0].text)
                    schema = await client.read_resource("receitas://schema/research")
                    self.assertIn("completed_tracks", schema.contents[0].text)
                    card_schema = await client.read_resource("receitas://schema/card")
                    self.assertIn("observable_cue", card_schema.contents[0].text)
                    checklist = await client.read_resource("receitas://project/checklist")
                    self.assertIn("first_message", checklist.contents[0].text)
                    pending = request_data()
                    pending["ambiguity_resolved"] = False
                    blocked = await client.call_tool("plan_research", {"request": pending})
                    self.assertFalse(blocked.structured_content["ok"])
                    invalid = await client.call_tool("plan_research", {"request": {}})
                    self.assertTrue(invalid.is_error)

        anyio.run(exercise)


if __name__ == "__main__":
    unittest.main()
