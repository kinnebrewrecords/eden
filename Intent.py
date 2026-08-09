from typing import Dict, Optional

class IntentDetector:

    def detect(self, command):

        command = command.lower()

        intent: Dict[str, Optional[str]] = {
            "action": None,
            "category": None,
            "type": None
        }
        if any(word in command for word in [
            "estimate",
            "calculate",
            "figure",
            "measure",
            "how much",
        ]):
            intent["action"] = "estimate"

        project_assemblies = {
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
        #### LUMBER ####

        lumber_aliases = {
            "framed wall with an opening": "framed wall with openings",
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


        roofing_terms = [
                "shingles",
                "roof shingles",
                "asphalt shingles",
                "underlayment",
                "roof underlayment",
                "synthetic underlayment",
                "drip edge",
                "drip edges",
                "roof edge",
                "ice barrier",
                "ice and water shield",
                "ice water shield",
                "ice shield",
                "ridge vent",
                "roof vent",
                "vent",
                "flashing",
                "roof flashing"
            ]


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

        if any(item in command for item in project_assemblies):
                intent["category"] = "assembly"

                for item in sorted(
                    project_assemblies,
                    key=len,
                    reverse=True
                ):
                    if item in command:
                        intent["type"] = project_assemblies[item]
                        break

        elif any(item in command for item in specialty_aliases):
                intent["category"] = "specialty"

                for item in sorted(
                    specialty_aliases,
                    key=len,
                    reverse=True
                ):
                    if item in command:
                        intent["type"] = specialty_aliases[item]
                        break

        elif any(item in command for item in concrete_types):
                intent["category"] = "concrete"

                for item in concrete_types:
                    if item in command:
                        intent["type"] = item
                        break

        elif any(item in command for item in lumber_aliases):

            intent["category"] = "lumber"

            for item in sorted(
                lumber_aliases,
                key=len,
                reverse=True
            ):
                if item in command:
                    intent["type"] = lumber_aliases[item]
                    break

        elif any(item in command for item in roofing_terms):

                intent["category"] = "roofing"

                for item in roofing_terms:
                    if item in command:
                        intent["type"] = item
                        break

        elif any(item in command for item in insulation_types):

                intent["category"] = "insulation"

                for item in insulation_types:
                    if item in command:
                        intent["type"] = insulation_type_map.get(
                            item,
                            item
                        )
                        break

        elif any(item in command for item in drywall_finish_terms):

                intent["category"] = "drywall finish"

                for item in drywall_finish_terms:
                    if item in command:
                        intent["type"] = item
                        break

        elif any(item in command for item in drywall_terms):

                intent["category"] = "drywall"

                for item in drywall_terms:
                    if item in command:
                        intent["type"] = item
                        break

        elif any(item in command for item in electrical_types):

                intent["category"] = "electrical"

                for item in electrical_types:
                    if item in command:
                        intent["type"] = item
                        break

        elif any(item in command for item in plumbing_types):

                intent["category"] = "plumbing"

                for item in plumbing_types:
                    if item in command:
                        intent["type"] = item
                        break

        elif any(item in command for item in hvac_types):

            intent["category"] = "hvac"

            for item in hvac_types:
                if item in command:
                    intent["type"] = item
                    break



            return intent

        return intent

# detector=IntentDetector()
# print(detector.detect("Can you estimate a concrete driveway for me?"))
# print(detector.detect("How much concrete do I need for a slab edge?"))
#print(detector.detect("I need a grade beam estimate"))
