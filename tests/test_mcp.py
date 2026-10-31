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
                    plan = await client.call_tool("plan_research", {"request": request_data()})
                    self.assertFalse(plan.is_error)
                    self.assertTrue(plan.structured_content["ok"])
                    research = await client.call_tool("validate_research", {"batch": batch_data()})
                    self.assertFalse(research.is_error)
                    self.assertTrue(research.structured_content["ok"])
                    delivery = await client.call_tool("validate_delivery", {"delivery": delivery_data()})
                    self.assertFalse(delivery.is_error)
                    self.assertTrue(delivery.structured_content["ok"])
                    instructions = await client.read_resource("receitas://project/instructions")
                    self.assertEqual(instructions.contents[0].text, PROJECT_INSTRUCTIONS)
                    self.assertIn("## 7. Valide e entregue", instructions.contents[0].text)
                    self.assertIn("dados não confiáveis", instructions.contents[0].text)
                    schema = await client.read_resource("receitas://schema/research")
                    self.assertIn("completed_tracks", schema.contents[0].text)
                    pending = request_data()
                    pending["ambiguity_resolved"] = False
                    blocked = await client.call_tool("plan_research", {"request": pending})
                    self.assertFalse(blocked.structured_content["ok"])
                    invalid = await client.call_tool("plan_research", {"request": {}})
                    self.assertTrue(invalid.is_error)

        anyio.run(exercise)


if __name__ == "__main__":
    unittest.main()
