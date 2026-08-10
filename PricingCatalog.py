import json
from datetime import date
from pathlib import Path

from WorkspaceFiles import workspace_file


class PricingCatalog:
    STARTER_REGIONS = [
        "Dallas-Fort Worth",
        "Houston",
        "Atlanta Metro",
        "Phoenix",
        "Bay Area",
        "Central Valley",
        "Los Angeles / Orange County",
        "Seattle"
    ]

    def __init__(self):
        self.file_path = workspace_file(__file__, "pricing.json")
        self.data = {
            "labor_rate_per_hour": 0.0,
            "labor_rates": {},
            "suppliers": {},
            "material_prices": {},
            "regions": {},
            "default_region": None
        }
        self.load()
        self._migrate_legacy_prices()
        self._migrate_supplier_price_keys()
        self._migrate_suppliers()

    def load(self):
        if not self.file_path.exists():
            return

        with open(self.file_path, "r") as file:
            self.data.update(json.load(file))

        self.data.setdefault("material_prices", {})
        self.data.setdefault("labor_rates", {})
        self.data.setdefault("suppliers", {})
        self.data.setdefault("regions", {})
        self.data.setdefault("default_region", None)

    def save(self):
        with open(self.file_path, "w") as file:
            json.dump(self.data, file, indent=4)

    def _make_key(self, value):
        return " ".join(value.strip().lower().split())

    def _make_material_key(self, item, unit, supplier=None):
        key = f"{item.strip().lower()}|{unit.strip().upper()}"

        if supplier is None:
            return key

        return f"{key}|{self._make_key(supplier)}"

    def _migrate_legacy_prices(self):
        if self.data["regions"] or not self.data["material_prices"]:
            return

        key = "company default"
        self.data["regions"][key] = {
            "name": "Company Default",
            "material_prices": self.data["material_prices"]
        }
        self.data["default_region"] = key
        self.save()

    def _migrate_supplier_price_keys(self):
        changed = False

        for region in self.data["regions"].values():
            prices = region.get("material_prices", {})
            migrated_prices = {}

            for price in prices.values():
                supplier = price.get("supplier", "Not recorded")
                price.setdefault("supplier", supplier)
                price.setdefault("price_date", "Not recorded")
                price.setdefault("history", [])

                key = self._make_material_key(
                    price["item"],
                    price["unit"],
                    supplier
                )
                migrated_prices[key] = price

            if migrated_prices != prices:
                region["material_prices"] = migrated_prices
                changed = True

        if changed:
            self.save()

    def _migrate_suppliers(self):
        changed = False

        for region in self.data["regions"].values():
            for price in region.get("material_prices", {}).values():
                supplier = price.get("supplier", "Not recorded")
                key = self._make_key(supplier)

                if key not in self.data["suppliers"]:
                    self.data["suppliers"][key] = {"name": supplier}
                    changed = True

        if changed:
            self.save()

    def create_region(self, name):
        name = " ".join(name.strip().split())
        key = self._make_key(name)

        if not name or key in self.data["regions"]:
            return False

        self.data["regions"][key] = {
            "name": name,
            "material_prices": {}
        }

        if self.data["default_region"] is None:
            self.data["default_region"] = key

        self.save()
        return True

    def add_starter_regions(self):
        added = []

        for name in self.STARTER_REGIONS:
            if self.create_region(name):
                added.append(name)

        return added

    def list_regions(self):
        return sorted(
            (
                region["name"]
                for region in self.data["regions"].values()
            ),
            key=str.lower
        )

    def set_default_region(self, name):
        key = self._make_key(name)

        if key not in self.data["regions"]:
            return False

        self.data["default_region"] = key
        self.save()
        return True

    def get_default_region(self):
        key = self.data["default_region"]
        region = self.data["regions"].get(key)

        if region is None:
            return None

        return region["name"]

    def _get_region(self, region_name=None):
        key = (
            self._make_key(region_name)
            if region_name
            else self.data["default_region"]
        )

        return self.data["regions"].get(key)

    def get_labor_rate(self):
        return self.data["labor_rate_per_hour"]

    def set_labor_rate(self, rate):
        self.data["labor_rate_per_hour"] = float(rate)
        self.save()

    def set_trade_labor_rate(self, trade, hourly_rate):
        trade = " ".join(trade.strip().split())
        hourly_rate = float(hourly_rate)

        if not trade:
            raise ValueError("Trade name is required.")

        if hourly_rate < 0:
            raise ValueError("Hourly rate cannot be negative.")

        self.data["labor_rates"][self._make_key(trade)] = {
            "trade": trade,
            "hourly_rate": round(hourly_rate, 2)
        }
        self.save()

    def get_all_trade_labor_rates(self):
        return sorted(
            self.data["labor_rates"].values(),
            key=lambda rate: rate["trade"].lower()
        )

    def add_supplier(self, name):
        name = " ".join(name.strip().split())
        key = self._make_key(name)

        if not name or key in self.data["suppliers"]:
            return False

        self.data["suppliers"][key] = {"name": name}
        self.save()
        return True

    def list_supplier_directory(self):
        return sorted(
            (
                supplier["name"]
                for supplier in self.data["suppliers"].values()
            ),
            key=str.lower
        )

    def set_material_price(
            self,
            item,
            unit,
            unit_cost,
            region_name=None,
            supplier="",
            price_date=None
    ):
        unit_cost = float(unit_cost)

        if unit_cost < 0:
            raise ValueError("Unit cost cannot be negative.")

        if region_name and self._get_region(region_name) is None:
            self.create_region(region_name)

        if self._get_region() is None:
            self.create_region("Company Default")

        region = self._get_region(region_name)
        supplier = supplier.strip() or "Not recorded"
        self.add_supplier(supplier)
        key = self._make_material_key(item, unit, supplier)
        existing_price = region["material_prices"].get(key)
        price_date = str(price_date or date.today())
        history = list(
            existing_price.get("history", [])
            if existing_price is not None
            else []
        )

        if existing_price is not None:
            previous_snapshot = {
                "unit_cost": existing_price.get("unit_cost"),
                "supplier": existing_price.get("supplier", supplier),
                "price_date": existing_price.get(
                    "price_date",
                    "Not recorded"
                )
            }
            incoming_cost = round(unit_cost, 2)

            if (
                    previous_snapshot["unit_cost"] != incoming_cost
                    or previous_snapshot["price_date"] != price_date
            ):
                history.append(previous_snapshot)

        region["material_prices"][key] = {
            "item": item.strip(),
            "unit": unit.strip().upper(),
            "unit_cost": round(unit_cost, 2),
            "supplier": supplier,
            "price_date": price_date,
            "history": history
        }
        self.save()

    def get_material_price_history(
            self,
            item,
            unit,
            region_name=None,
            supplier_name=None
    ):
        price = self.get_material_price_details(
            item,
            unit,
            region_name,
            supplier_name
        )

        if price is None:
            return []

        history = list(price.get("history", []))
        history.append(
            {
                "unit_cost": price["unit_cost"],
                "supplier": price.get("supplier", "Not recorded"),
                "price_date": price.get("price_date", "Not recorded"),
                "current": True
            }
        )
        return history

    def list_suppliers(self, region_name=None):
        region = self._get_region(region_name)

        if region is None:
            return []

        suppliers = set(self.list_supplier_directory())
        suppliers.update({
            price.get("supplier", "Not recorded")
            for price in region["material_prices"].values()
        })

        return sorted(suppliers, key=str.lower)

    def get_material_price_details(
            self,
            item,
            unit,
            region_name=None,
            supplier_name=None
    ):
        region = self._get_region(region_name)

        if region is None:
            return None

        if supplier_name is None:
            material_key = self._make_material_key(item, unit)
            matches = [
                price
                for key, price in region["material_prices"].items()
                if key.startswith(f"{material_key}|")
            ]

            if len(matches) == 1:
                return matches[0]

            return None

        key = self._make_material_key(item, unit, supplier_name)
        return region["material_prices"].get(key)

    def get_material_price(
            self,
            item,
            unit,
            region_name=None,
            supplier_name=None
    ):
        material = self.get_material_price_details(
            item,
            unit,
            region_name,
            supplier_name
        )

        if material is None:
            return None

        return material["unit_cost"]

    def get_regional_average_price_details(
            self,
            item,
            unit,
            region_name=None
    ):
        """Return an estimated average from saved supplier prices in a region."""
        region = self._get_region(region_name)

        if region is None:
            return None

        material_key = self._make_material_key(item, unit)
        matches = [
            price
            for key, price in region["material_prices"].items()
            if key.startswith(f"{material_key}|")
        ]

        if not matches:
            return None

        unit_cost = round(
            sum(float(price["unit_cost"]) for price in matches) /
            len(matches),
            2
        )

        return {
            "item": item.strip(),
            "unit": unit.strip().upper(),
            "unit_cost": unit_cost,
            "supplier": "Eden regional average",
            "price_date": "Based on saved supplier prices",
            "sample_count": len(matches)
        }

    def get_all_material_prices(self, region_name=None):
        region = self._get_region(region_name)

        if region is None:
            return []

        return sorted(
            region["material_prices"].values(),
            key=lambda price: (
                price["item"].lower(),
                price["unit"]
            )
        )

    def list_material_suppliers(self, item, unit, region_name=None):
        """Return suppliers that have an exact saved price for one item."""
        region = self._get_region(region_name)

        if region is None:
            return []

        material_key = self._make_material_key(item, unit)

        suppliers = {
            price.get("supplier", "Not recorded")
            for key, price in region["material_prices"].items()
            if key.startswith(f"{material_key}|")
        }

        return sorted(suppliers, key=str.lower)

    def price_material_takeoff(
            self,
            material_takeoff,
            region_name=None,
            supplier_name=None,
            supplier_by_material=None
    ):
        region = self._get_region(region_name)
        pricing_region = region["name"] if region else None
        priced_items = []
        unpriced_items = []
        total_material_cost = 0.0

        supplier_by_material = supplier_by_material or {}

        for item in material_takeoff:
            name = item.get("item")
            unit = item.get("unit")
            quantity = item.get("quantity")

            if not name or not unit or quantity is None:
                continue

            manual_unit_cost = item.get("manual_unit_cost")
            price_details = None
            price_source = ""

            if manual_unit_cost is not None:
                unit_cost = float(manual_unit_cost)
                price_source = "Project custom price"
            else:
                material_key = self._make_material_key(name, unit)
                item_supplier = supplier_by_material.get(
                    material_key,
                    supplier_name
                )

                price_details = self.get_material_price_details(
                    name,
                    unit,
                    region_name,
                    item_supplier
                )

                unit_cost = (
                    price_details["unit_cost"]
                    if price_details is not None
                    else None
                )

                if price_details is not None:
                    price_source = "Supplier price"
                else:
                    price_details = self.get_regional_average_price_details(
                        name,
                        unit,
                        region_name
                    )
                    unit_cost = (
                        price_details["unit_cost"]
                        if price_details is not None
                        else None
                    )

                    if price_details is not None:
                        price_source = "Estimated regional average"

            priced_item = {
                "item": name,
                "unit": unit,
                "quantity": quantity,
                "unit_cost": unit_cost,
                "supplier": (
                    price_details.get("supplier", "Not recorded")
                    if price_details is not None
                    else (
                        "Project custom cost"
                        if manual_unit_cost is not None
                        else "Not recorded"
                    )
                ),
                "price_date": (
                    price_details.get("price_date", "Not recorded")
                    if price_details is not None
                    else (
                        "Project entry"
                        if manual_unit_cost is not None
                        else "Not recorded"
                    )
                ),
                "price_source": price_source
            }

            if unit_cost is None:
                priced_item["extended_cost"] = None
                priced_item["status"] = "Price needed"
                unpriced_items.append(priced_item)
            else:
                extended_cost = round(float(quantity) * unit_cost, 2)
                priced_item["extended_cost"] = extended_cost
                priced_item["status"] = price_source or "Priced"
                total_material_cost += extended_cost

            priced_items.append(priced_item)

        return {
            "pricing_region": pricing_region,
            "pricing_supplier": supplier_name,
            "priced_items": priced_items,
            "unpriced_items": unpriced_items,
            "total_material_cost": round(total_material_cost, 2)
        }
