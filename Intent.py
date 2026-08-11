import re
from typing import Dict, Optional

class IntentDetector:

    def _normalize_command(self, command):
        command = command.lower().strip()
        command = command.replace("&", " and ")
        command = re.sub(r"[^a-z0-9#./\-\s]", " ", command)
        return " ".join(command.split())

    def _contains_phrase(self, command, phrase):
        pattern = rf"(?<!\w){re.escape(phrase)}(?!\w)"
        return re.search(pattern, command) is not None

    def _contains_any(self, command, phrases):
        return any(
            self._contains_phrase(command, phrase)
            for phrase in phrases
        )

    def detect(self, command):

        command = self._normalize_command(command)

        intent: Dict[str, Optional[str]] = {
            "action": None,
            "category": None,
            "type": None
        }
        if self._contains_any(command, [
            "estimate",
            "calculate",
            "figure",
            "measure",
            "how much",
        ]):
            intent["action"] = "estimate"

        project_assemblies = {
            "whole house takeoff": "residential whole-house takeoff",
            "whole house estimate": "residential whole-house takeoff",
            "two story house takeoff": "residential whole-house takeoff",
            "two story house estimate": "residential whole-house takeoff",
            "residential house takeoff": "residential whole-house takeoff",
            "residential whole house": "residential whole-house takeoff",
            "interior finish assembly": "interior finish assembly",
            "interior finish package": "interior finish assembly",
            "interior package": "interior finish assembly",
            "floor system assembly": "floor system assembly",
            "residential floor system": "floor system assembly",
            "floor framing assembly": "floor system assembly",
            "roof covering assembly": "roof covering assembly",
            "residential roof system": "roof covering assembly",
            "roof system assembly": "roof covering assembly",
            "foundation system assembly": "foundation system assembly",
            "residential foundation system": "foundation system assembly",
            "foundation assembly": "foundation system assembly",
            "exterior wall assembly": "exterior wall assembly",
            "exterior wall package": "exterior wall assembly",
            "exterior wall system": "exterior wall assembly",
            "backyard studio shell": "backyard studio shell",
            "backyard studio": "backyard studio shell",
            "small studio shell": "backyard studio shell",
            "studio shell": "backyard studio shell"
        }

        #### CONCRETE ####

        concrete_types = [
            "footing system",
            "foundation footing system",
            "continuous footing system",
            "custom flatwork",
            "flatwork",
            "foundation wall", "retaining wall", "grade beam",
            "round footing", "spread footing", "pile cap",
            "slab edge", "footing", "lintel", "trench", "sidewalk",
            "driveway", "steps", "column", "ramp", "beam",
            "pad", "pier", "curb", "patio", "slab"
        ]

        concrete_aliases = {
            "aggregate base": "aggregate base",
            "gravel base": "aggregate base",
            "crusher run": "aggregate base",
            "crushed stone": "aggregate base",
            "#57 stone": "aggregate base",
            "concrete flatwork": "custom flatwork",
            "irregular flatwork": "custom flatwork",
            "radius slab": "custom flatwork",
            "rounded slab": "custom flatwork",
            "continuous footings": "footing system",
            "foundation footings": "footing system",
            "footings": "footing system"
        }
        #### LUMBER ####

        lumber_aliases = {
            "framing hardware": "framing hardware",
            "hardware package": "framing hardware",
            "joist hangers": "framing hardware",
            "hurricane ties": "framing hardware",
            "roof trusses": "roof trusses",
            "roof truss": "roof trusses",
            "trusses": "roof trusses",
            "truss": "roof trusses",
            "wall framing package": "wall framing package",
            "framing package": "wall framing package",
            "stair framing": "stair framing",
            "stairs": "stair framing",
            "deck framing": "deck framing",
            "garage door framing": "garage door framing",
            "garage door header": "garage door framing",
            "framed wall with an opening": "framed wall with openings",
            "framed wall with a door": "framed wall with openings",
            "framed wall with a window": "framed wall with openings",
            "framed wall with doors": "framed wall with openings",
            "framed wall with windows": "framed wall with openings",
            "wall with a door": "framed wall with openings",
            "wall with a window": "framed wall with openings",
            "wall opening": "framed wall with openings",
            "framed wall with opening": "framed wall with openings",
            "wall with opening": "framed wall with openings",
            "framed wall with openings": "framed wall with openings",
            "frame wall with openings": "framed wall with openings",
            "wall with openings": "framed wall with openings",

            "framed wall": "framed wall",
            "frame wall": "framed wall",
            "stud wall": "framed wall",

            "ceiling joists": "ceiling joists",
            "floor joists": "floor joists",
            "floor joist": "floor joists",

            "roof sheathing": "roof sheathing",
            "wall sheathing": "wall sheathing",
            "subfloor sheathing": "subfloor sheathing",
            "subfloor": "subfloor sheathing",

            "roof rafters": "rafters",
            "roof rafter": "rafters",
            "rafters": "rafters",
            "rafter": "rafters",

            "ridge board": "ridge board",
            "collar ties": "collar ties",

            "fire blocking": "blocking",
            "wall blocking": "blocking",
            "blocking": "blocking",

            "king studs": "king studs",
            "king stud": "king studs",
            "jack studs": "jack studs",
            "jack stud": "jack studs",
            "cripple studs": "cripple studs",
            "cripple stud": "cripple studs",
            "corner posts": "corner posts",
            "corner post": "corner posts",
            "wood posts": "posts",
            "posts": "posts",
            "studs": "studs",
            "stud": "studs",

            "built-up beam": "beam",
            "built up beam": "beam",
            "support beams": "beam",
            "support beam": "beam",
            "wood beam": "beam",
            "beam": "beam",

            "bottom plate": "bottom plate",
            "top plate": "top plate",
            "sill plates": "sill plate",
            "sill plate": "sill plate",
            "wall plates": "plates",
            "plates": "plates",
            "plate": "plates",

            "rim joists": "rim joists",
            "rim joist": "rim joists",
            "band boards": "rim joists",
            "band joist": "rim joists",
        }


    #### ROOFING ####


        roofing_aliases = {
            "asphalt shingles": "shingles",
            "roof shingles": "shingles",
            "shingles": "shingles",
            "synthetic underlayment": "underlayment",
            "roof underlayment": "underlayment",
            "underlayment": "underlayment",
            "drip edges": "drip edge",
            "drip edge": "drip edge",
            "roof edge": "drip edge",
            "ice and water shield": "ice water shield",
            "ice water shield": "ice water shield",
            "ice barrier": "ice water shield",
            "ice shield": "ice water shield",
            "ridge vent": "ridge vent",
            "roof vent": "ridge vent",
            "roof flashing": "flashing",
            "flashing": "flashing"
        }


    #### INSULATION ####

        insulation_types = [
            "spray foam",
            "spray foam insulation",
            "batt insulation",
            "blown insulation",
            "blown-in insulation",
            "blown fiberglass",
            "insulation batts",
            "fiberglass insulation",
            "batt",
            "insulation"
        ]

        insulation_type_map = {
            "spray foam insulation": "spray foam",
            "batt": "batt insulation",
            "insulation batts": "batt insulation",
            "fiberglass insulation": "batt insulation",
            "blown-in insulation": "blown insulation",
            "blown fiberglass": "blown insulation"
        }


        #### DRYWALL FINISH ####

        drywall_finish_terms = [
                "joint compound",
                "drywall mud",
                "drywall tape",
                "tape",
                "corner bead",
                "drywall screws",
                "corner bead",
                "corner beads",
                "drywall screws",
                "screws",
                "drywall sanding",
                "sanding",
                "primer",
                "drywall primer",
                "drywall texture",
                "texture",
                "ceiling paint",
                "interior paint",
                "exterior paint",
                "trim paint",
                "door paint",
                "paint"
            ]

        #### DRYWALL ####

        drywall_terms = [
                "ceiling drywall",
                "wall drywall",
                "drywall",
                "sheetrock"
            ]

       #### ELECTRICAL ####

        electrical_types = [
                "outlets",
                "receptacles",
                "switches",
                "lights",
                "fixtures",
                "wire",
                "romex",
                "nm-b",
                "breaker",
                "breakers",
                "panel",
                "electrical boxes",
                "junction boxes",
                "boxes"
            ]


        #### PLUMBING ####

        plumbing_types = [
            "pex pipe",
            "pex",
            "copper pipe",
            "copper tubing",
            "copper",
            "pvc pipe",
            "pvc drain pipe",
            "pvc drain",
            "drain pipe",
            "water heater",
            "water heaters",
            "toilet",
            "toilets",
            "sink",
            "sinks",
            "lavatory",
            "vanity",
            "faucet",
            "faucets",
            "shower",
            "showers",
            "tub",
            "tubs",
            "bathtub",
            "shutoff valve",
            "shutoff valves",
            "ball valve",
            "ball valves",
            "plumbing valves",
            "plumbing valve",
            "angle stop",
            "angle stops",
            "fittings",
            "elbows",
            "tees",
            "couplings",
            "adapters",
        ]


            #### HVAC ####
        hvac_types = [
            "ductwork",
            "flex duct",
            "flexible duct",
            "supply registers",
            "supply register",
            "registers",
            "return grille",
            "return grilles",
            "grille",
            "thermostat",
            "thermostats",
            "hvac unit",
            "air conditioner",
            "air conditioning",
            "ac unit",
            "condenser",
            "furnace",
            "furnaces",
            "air filter",
            "air filters",
            "filter",
            "refrigerant line",
            "refrigerant line set",
            "line set",
            "condensate drain",
            "condensate",
            "drain line",
        ]

        specialty_aliases = {
            "exterior siding": "siding",
            "siding": "siding",
            "house wrap": "housewrap",
            "housewrap": "housewrap",
            "weather resistive barrier": "housewrap",
            "exterior trim": "exterior trim",
            "deck boards": "decking",
            "decking": "decking",
            "fence": "fence",
            "fencing": "fence",
            "flooring": "flooring",
            "lvp flooring": "flooring",
            "vinyl plank flooring": "flooring",
            "baseboard trim": "baseboard",
            "baseboard": "baseboard",
            "interior doors": "interior doors",
            "interior door": "interior doors",
            "exterior doors": "exterior doors",
            "exterior door": "exterior doors",
            "windows": "windows",
            "window": "windows"
        }

        if self._contains_any(command, project_assemblies):
                intent["category"] = "assembly"

                for item in sorted(
                    project_assemblies,
                    key=len,
                    reverse=True
                ):
                    if self._contains_phrase(command, item):
                        intent["type"] = project_assemblies[item]
                        break

        elif self._contains_any(command, specialty_aliases):
                intent["category"] = "specialty"

                for item in sorted(
                    specialty_aliases,
                    key=len,
                    reverse=True
                ):
                    if self._contains_phrase(command, item):
                        intent["type"] = specialty_aliases[item]
                        break

        elif self._contains_any(command, concrete_aliases):
                intent["category"] = "concrete"

                for item in sorted(
                    concrete_aliases,
                    key=len,
                    reverse=True
                ):
                    if self._contains_phrase(command, item):
                        intent["type"] = concrete_aliases[item]
                        break

        elif self._contains_any(command, concrete_types):
                intent["category"] = "concrete"

                for item in sorted(concrete_types, key=len, reverse=True):
                    if self._contains_phrase(command, item):
                        intent["type"] = item
                        break

        elif self._contains_any(command, lumber_aliases):

            intent["category"] = "lumber"

            for item in sorted(
                lumber_aliases,
                key=len,
                reverse=True
            ):
                if self._contains_phrase(command, item):
                    intent["type"] = lumber_aliases[item]
                    break

        elif self._contains_any(command, roofing_aliases):

                intent["category"] = "roofing"

                for item in sorted(
                    roofing_aliases,
                    key=len,
                    reverse=True
                ):
                    if self._contains_phrase(command, item):
                        intent["type"] = roofing_aliases[item]
                        break

        elif self._contains_any(command, insulation_types):

                intent["category"] = "insulation"

                for item in sorted(insulation_types, key=len, reverse=True):
                    if self._contains_phrase(command, item):
                        intent["type"] = insulation_type_map.get(
                            item,
                            item
                        )
                        break

        elif self._contains_any(command, drywall_finish_terms):

                intent["category"] = "drywall finish"

                for item in sorted(drywall_finish_terms, key=len, reverse=True):
                    if self._contains_phrase(command, item):
                        intent["type"] = item
                        break

        elif self._contains_any(command, drywall_terms):

                intent["category"] = "drywall"

                for item in sorted(drywall_terms, key=len, reverse=True):
                    if self._contains_phrase(command, item):
                        intent["type"] = item
                        break

        elif self._contains_any(command, electrical_types):

                intent["category"] = "electrical"

                for item in sorted(electrical_types, key=len, reverse=True):
                    if self._contains_phrase(command, item):
                        intent["type"] = item
                        break

        elif self._contains_any(command, plumbing_types):

                intent["category"] = "plumbing"

                for item in sorted(plumbing_types, key=len, reverse=True):
                    if self._contains_phrase(command, item):
                        intent["type"] = item
                        break

        elif self._contains_any(command, hvac_types):

            intent["category"] = "hvac"

            for item in sorted(hvac_types, key=len, reverse=True):
                if self._contains_phrase(command, item):
                    intent["type"] = item
                    break

        if intent["category"] and intent["action"] is None:
            intent["action"] = "estimate"

        return intent

# detector=IntentDetector()
# print(detector.detect("Can you estimate a concrete driveway for me?"))
# print(detector.detect("How much concrete do I need for a slab edge?"))
#print(detector.detect("I need a grade beam estimate"))
