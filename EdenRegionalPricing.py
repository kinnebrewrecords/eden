"""Eden-managed regional average pricing.

This price book is intentionally separate from a contractor's private
pricing.json file.  Supplier quotes always take priority over these values.
Each material record must be reviewed at least every 90 days before Eden
uses it as an estimated regional average.
"""

from datetime import date, timedelta


PRICEBOOK_VERSION = "beta-1"
REVIEW_INTERVAL_DAYS = 90


# These are the regions available in Eden 1.0. Material averages are added
# here only after they have been researched and reviewed; Eden must never
# invent a market price when a region/material has no vetted entry.
REGIONAL_PRICEBOOK = {
    "Atlanta Metro": {"reviewed_on": None, "prices": {}},
    "Dallas-Fort Worth": {"reviewed_on": None, "prices": {}},
    "Houston": {"reviewed_on": None, "prices": {}},
    "Phoenix": {"reviewed_on": None, "prices": {}},
    "Bay Area": {"reviewed_on": None, "prices": {}},
    "Central Valley": {"reviewed_on": None, "prices": {}},
    "Los Angeles / Orange County": {"reviewed_on": None, "prices": {}},
    "Seattle": {"reviewed_on": None, "prices": {}}
}


def _material_key(item, unit):
    return f"{item.strip().lower()}|{unit.strip().upper()}"


def get_eden_average(item, unit, region_name):
    """Return a vetted Eden price-book entry, or None when unavailable."""
    region = REGIONAL_PRICEBOOK.get(region_name)

    if region is None:
        return None

    entry = region["prices"].get(_material_key(item, unit))

    if entry is None:
        return None

    reviewed_on = date.fromisoformat(entry["reviewed_on"])
    review_due = reviewed_on + timedelta(days=REVIEW_INTERVAL_DAYS)

    if date.today() > review_due:
        return None

    return {
        "item": item.strip(),
        "unit": unit.strip().upper(),
        "unit_cost": float(entry["unit_cost"]),
        "supplier": "Eden regional average",
        "price_date": entry["reviewed_on"],
        "review_due": review_due.isoformat(),
        "pricebook_version": PRICEBOOK_VERSION
    }


def get_region_pricebook_status(region_name):
    """Return coverage data for Settings and future price-book management."""
    region = REGIONAL_PRICEBOOK.get(region_name)

    if region is None:
        return None

    return {
        "region": region_name,
        "price_count": len(region["prices"]),
        "review_interval_days": REVIEW_INTERVAL_DAYS,
        "reviewed_on": region["reviewed_on"]
    }
