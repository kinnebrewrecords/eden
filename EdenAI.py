import os
import json

from openai import OpenAI


class EdenAI:
    """Small, safe entry point for Eden's future AI features."""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            try:
                import streamlit as st

                api_key = st.secrets.get("OPENAI_API_KEY")
            except Exception:
                pass

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY was not found. Add it to your environment "
                "variables or Streamlit secrets."
            )

        self.client = OpenAI(api_key=api_key)

    def test_connection(self):
        """Make one minimal request to confirm Eden can reach the API."""
        response = self.client.responses.create(
            model="gpt-5.6-luna",
            input=(
                "Reply with exactly: Eden AI connection successful."
            )
        )

        return response.output_text.strip()

    def normalize_new_request(self, user_message):
        """Translate everyday wording into one safe Eden command.

        The result is still processed by Eden's existing command parser.
        AI does not calculate quantities or answer required field prompts.
        """
        response = self.client.responses.create(
            model="gpt-5.6-luna",
            instructions=(
                "You translate a construction contractor's first message "
                "into one short command for the Eden estimating app. "
                "Return only the command—no explanation, no markdown, "
                "and no quotation marks. Preserve every user-provided "
                "number, measurement, product, and project name exactly. "
                "Never invent a dimension, material specification, "
                "structural decision, supplier, or price. Use commands such "
                "as 'estimate a concrete patio', 'estimate framed wall', "
                "'show project', 'create project <name>', or 'help'. If "
                "the request is unclear, return the user's message unchanged."
            ),
            input=user_message
        )

        command = response.output_text.strip().splitlines()[0].strip()
        return command.strip("`\\\"") or user_message

    def extract_supplier_prices(self, supplier_text):
        """Extract reviewable price candidates from user-provided text."""
        response = self.client.responses.create(
            model="gpt-5.6-luna",
            instructions=(
                "Extract supplier material prices from the user's supplied "
                "quote, receipt, cart, or product-page text. Return only a "
                "JSON array. Each array item must have item (string), unit "
                "(string), and unit_cost (number). Include only a unit price "
                "that is explicitly present or directly calculable from an "
                "explicit quantity and line total. Do not estimate, search "
                "the internet, invent a price, infer a material grade, or "
                "include tax, delivery, discounts, or totals as a unit price. "
                "Use an empty string for unit when the supplied text does not "
                "state a reliable unit. If no reliable prices exist, return []."
            ),
            input=supplier_text
        )

        raw_result = response.output_text.strip()

        if raw_result.startswith("```"):
            raw_result = raw_result.split("\n", 1)[-1]
            raw_result = raw_result.rsplit("```", 1)[0].strip()

        extracted_items = json.loads(raw_result)

        if not isinstance(extracted_items, list):
            raise ValueError("AI did not return a price list.")

        candidates = []

        for item in extracted_items:
            try:
                name = str(item["item"]).strip()
                unit = str(item.get("unit", "")).strip().upper()
                unit_cost = round(float(item["unit_cost"]), 2)
            except (KeyError, TypeError, ValueError):
                continue

            if name and unit_cost >= 0:
                candidates.append(
                    {
                        "item": name,
                        "unit": unit,
                        "unit_cost": unit_cost
                    }
                )

        return candidates


if __name__ == "__main__":
    print(EdenAI().test_connection())
