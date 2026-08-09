import json
from pathlib import Path


class PricingCatalog:
    def __init__(self):
        self.file_path = Path(__file__).with_name(
            "pricing_catalog.json"
        )

        self.data = {
            "material_prices": {},
            "labor_rates": {}
        }

        self.load()

    def load(self):
        if not self.file_path.exists():
            return

        with open(self.file_path, "r") as file:
            saved_data = json.load(file)

        self.data.update(saved_data)

        if "material_prices" not in self.data:
            self.data["material_prices"] = {}

        if "labor_rates" not in self.data:
            self.data["labor_rates"] = {}

    def save(self):
        with open(self.file_path, "w") as file:
            json.dump(
                self.data,
                file,
                indent=4
            )

    def _make_key(self, item, unit):
        return (
            f"{item.strip().lower()}|"
            f"{unit.strip().upper()}"
        )

    def set_material_price(self, item, unit, unit_cost):
        unit_cost = float(unit_cost)

        if unit_cost < 0:
            raise ValueError(
                "Unit cost cannot be negative."
            )

        key = self._make_key(item, unit)

        self.data["material_prices"][key] = {
            "item": item.strip(),
            "unit": unit.strip().upper(),
            "unit_cost": round(unit_cost, 2)
        }

        self.save()

    def get_material_price(self, item, unit):
        key = self._make_key(item, unit)

        material = self.data["material_prices"].get(key)

        if material is None:
            return None

        return material["unit_cost"]

    def get_all_material_prices(self):
        prices = list(
            self.data["material_prices"].values()
        )

        return sorted(
            prices,
            key=lambda price: (
                price["item"].lower(),
                price["unit"]
            )
        )

    def price_material_takeoff(self, material_takeoff):
        priced_items = []
        unpriced_items = []
        total_material_cost = 0.0

        for item in material_takeoff:
            name = item.get("item")
            unit = item.get("unit")
            quantity = item.get("quantity")

            if not name or not unit or quantity is None:
                continue

            unit_cost = self.get_material_price(
                name,
                unit
            )

            priced_item = {
                "item": name,
                "unit": unit,
                "quantity": quantity,
                "unit_cost": unit_cost
            }

            if unit_cost is None:
                priced_item["extended_cost"] = None
                priced_item["status"] = "Price needed"

                unpriced_items.append(priced_item)

            else:
                extended_cost = round(
                    float(quantity) * unit_cost,
                    2
                )

                priced_item["extended_cost"] = extended_cost
                priced_item["status"] = "Priced"

                total_material_cost += extended_cost

            priced_items.append(priced_item)

        return {
            "priced_items": priced_items,
            "unpriced_items": unpriced_items,
            "total_material_cost": round(
                total_material_cost,
                2
            )
        }

    def set_labor_rate(self, trade, hourly_rate):
        hourly_rate = float(hourly_rate)

        if hourly_rate < 0:
            raise ValueError(
                "Labor rate cannot be negative."
            )

        self.data["labor_rates"][trade.strip().lower()] = {
            "trade": trade.strip(),
            "hourly_rate": round(hourly_rate, 2)
        }

        self.save()

    def get_labor_rate(self, trade):
        labor = self.data["labor_rates"].get(
            trade.strip().lower()
        )

        if labor is None:
            return None

        return labor["hourly_rate"]