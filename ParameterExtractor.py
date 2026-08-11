import re


class ParameterExtractor:
    def _explicit_number(self, command, patterns):
        for pattern in patterns:
            match = re.search(pattern, command)
            if match:
                return float(match.group(1))

        return None

    def _apply_explicit_measurements(self, command, data):
        """Prefer labeled construction measurements over number position."""
        dimension_match = re.search(
            r"(\d+(?:\.\d+)?)\s*(?:ft|feet|')?\s*"
            r"(?:x|by)\s*"
            r"(\d+(?:\.\d+)?)\s*(?:ft|feet|')?"
            r"(?:\s*(?:x|by)\s*"
            r"(\d+(?:\.\d+)?)\s*(?:in|inch|inches|\")?)?",
            command
        )

        if dimension_match:
            data["length"] = float(dimension_match.group(1))
            data["width"] = float(dimension_match.group(2))

            # In wall requests, the second dimension is a height rather
            # than a plan width: "4 walls, 20 x 8" means 20 ft by 8 ft.
            if "wall" in command:
                data["height"] = float(dimension_match.group(2))

            if dimension_match.group(3) is not None:
                data["thickness"] = float(dimension_match.group(3))

        length = self._explicit_number(
            command,
            [
                r"(?:length|long)\s*(?:is\s*)?(\d+(?:\.\d+)?)",
                r"(\d+(?:\.\d+)?)\s*(?:ft|feet|')\s*(?:long|length)"
            ]
        )
        width = self._explicit_number(
            command,
            [
                r"(?:width|wide)\s*(?:is\s*)?(\d+(?:\.\d+)?)",
                r"(\d+(?:\.\d+)?)\s*(?:ft|feet|')\s*(?:wide|width)"
            ]
        )
        height = self._explicit_number(
            command,
            [
                r"(?:height|high|tall)\s*(?:is\s*)?(\d+(?:\.\d+)?)",
                r"(\d+(?:\.\d+)?)\s*(?:ft|feet|')\s*(?:high|tall|height)"
            ]
        )
        thickness = self._explicit_number(
            command,
            [
                r"(?:thickness|thick)\s*(?:is\s*)?(\d+(?:\.\d+)?)",
                r"(\d+(?:\.\d+)?)\s*(?:in|inch|inches|\")\s*"
                r"(?:thick|thickness)"
            ]
        )
        depth = self._explicit_number(
            command,
            [
                r"(?:depth|deep)\s*(?:is\s*)?(\d+(?:\.\d+)?)",
                r"(\d+(?:\.\d+)?)\s*(?:in|inch|inches|\")\s*"
                r"(?:deep|depth)",
                r"(\d+(?:\.\d+)?)\s*(?:in|inch|inches|\")\s*"
                r"(?:aggregate|gravel|base)"
            ]
        )
        spacing = self._explicit_number(
            command,
            [
                r"(\d+(?:\.\d+)?)\s*(?:in|inch|inches)?\s*"
                r"(?:o\.?\s*c\.?|on center)"
            ]
        )
        overhang = self._explicit_number(
            command,
            [
                r"(\d+(?:\.\d+)?)\s*(?:in|inch|inches|\")\s*"
                r"(?:overhang|eave|rake)"
            ]
        )
        pitch_match = re.search(r"(\d+(?:\.\d+)?)\s*/\s*12", command)
        quantity = self._explicit_number(
            command,
            [
                r"(\d+)\s+(?:identical\s+|same\s+)?"
                r"(?:walls?|sections?|runs?|rooms?|ceilings?)"
            ]
        )
        area = self._explicit_number(
            command,
            [r"(\d+(?:\.\d+)?)\s*(?:sq\.?\s*ft|square\s*feet)"]
        )

        if length is not None:
            data["length"] = length
        if width is not None:
            data["width"] = width
        if height is not None:
            data["height"] = height
        if thickness is not None:
            data["thickness"] = thickness
        if depth is not None:
            data["depth"] = depth
        if spacing is not None:
            data["stud_spacing_inches"] = spacing
        if overhang is not None:
            data["overhang_inches"] = overhang
        if pitch_match:
            data["pitch"] = float(pitch_match.group(1))
        if quantity is not None:
            data["quantity"] = int(quantity)
        if area is not None:
            data["area"] = area

        # A leading count must not become a dimension. For example,
        # "4 walls, 20 ft long" has a known quantity and length, but Eden
        # still needs to ask for the wall height.
        if "wall" in command and length is not None and height is None:
            data["height"] = None

        if "shed roof" in command or "shed" in command:
            data["roof_type"] = "shed"
        elif "gable roof" in command or "gable" in command:
            data["roof_type"] = "gable"

    def extract_dimensions(self,command):
        command=command.lower()
        numbers=re.findall(r"\d+\.?\d*",command)
        numbers=[float(num) for num in numbers]
        data= {
            "length": numbers[0] if len(numbers)>0 else None,
            "width": numbers[1] if len (numbers)>1 else None,
            "thickness": numbers[2] if len(numbers)>2 else None,

            "height": numbers[1] if len(numbers) > 1 else None,
            "depth": numbers[2] if len(numbers) > 2 else None,

            "diameter": numbers[0] if len(numbers) > 0 else None,
            "radius": numbers[0] if len(numbers) > 0 else None,

            "quantity": numbers[2] if len(numbers) > 2 else None,

            "tread_depth": numbers[1] if len(numbers) > 1 else None,
            "riser_height": numbers[2] if len(numbers) > 2 else None,
            "steps": numbers[3] if len(numbers) > 3 else None,
            "pitch": None,
            "area": numbers[0] if len(numbers) > 0 else None,
            "stud_spacing_inches": None,
            "overhang_inches": None,
            "roof_type": None,
        }
        if "step" in command or "steps" in command:
            if len(numbers) >= 4:
                data["width"] = numbers[0]
                data["tread_depth"] = numbers[1]
                data["riser_height"] = numbers[2]
                data["steps"] = numbers[3]

        elif "column" in command:
            if len(numbers) >= 3:
                data["diameter"] = numbers[0]
                data["height"] = numbers[1]
                data["quantity"] = numbers[2]

        elif "pier" in command:
            if len(numbers) >= 3:
                data["diameter"] = numbers[0]
                data["depth"] = numbers[1]
                data["quantity"] = numbers[2]

        elif "round footing" in command:
            if len(numbers) >= 3:
                data["diameter"] = numbers[0]
                data["depth"] = numbers[1]
                data["quantity"] = numbers[2]

        elif "grade" in command and "beam" in command:
            if len(numbers) >= 3:
                data["length"] = numbers[0]
                data["width"] = numbers[1]
                data["height"] = numbers[2]

        elif "beam" in command:
            if len(numbers) >= 3:
                data["length"] = numbers[0]
                data["width"] = numbers[1]
                data["height"] = numbers[2]

        elif "trench" in command:
            if len(numbers) >= 3:
                data["length"] = numbers[0]
                data["width"] = numbers[1]
                data["depth"] = numbers[2]

        elif "retaining wall" in command:
            if len(numbers) >= 3:
                data["length"] = numbers[0]
                data["height"] = numbers[1]
                data["thickness"] = numbers[2]

        elif "foundation wall" in command:
            if len(numbers) >= 3:
                data["length"] = numbers[0]
                data["height"] = numbers[1]
                data["thickness"] = numbers[2]

        elif "curb" in command:
            if len(numbers) >= 3:
                data["length"] = numbers[0]
                data["width"] = numbers[1]
                data["height"] = numbers[2]

        elif "lintel" in command:
            if len(numbers) >= 3:
                data["length"] = numbers[0]
                data["width"] = numbers[1]
                data["height"] = numbers[2]

        elif "footing" in command and "round footing" not in command:
            if len(numbers) >= 3:
                data["length"] = numbers[0]
                data["width"] = numbers[1]
                data["depth"] = numbers[2]

        elif "patio" in command:
            if len(numbers) >= 3:
                data["length"] = numbers[0]
                data["width"] = numbers[1]
                data["thickness"] = numbers[2]

        elif "ramp" in command:
            if len(numbers) >= 3:
                data["length"] = numbers[0]
                data["width"] = numbers[1]
                data["height"] = numbers[2]

        self._apply_explicit_measurements(command, data)

        if "outlet" in command or "receptacle" in command:
            if len(numbers) >= 1:
                data["quantity"] = int(numbers[0])

        if "switch" in command:
            if len(numbers) >= 1:
                data["quantity"] = int(numbers[0])

        if "light" in command or "fixture" in command:
            if len(numbers) >= 1:
                data["quantity"] = int(numbers[0])

        if "switch" in command:
            if len(numbers) >= 1:
                data["quantity"] = int(numbers[0])

        if "light" in command or "fixture" in command:
            if len(numbers) >= 1:
                data["quantity"] = int(numbers[0])

        if "box" in command:
            if len(numbers) >= 1:
                data["quantity"] = int(numbers[0])

        if "wire" in command or "romex" in command:
            if len(numbers) >= 1:
                data["length"] = numbers[0]

        if "breaker" in command:
            if len(numbers) >= 1:
                data["quantity"] = int(numbers[0])

        if "joint compound" in command or "drywall mud" in command:
            if len(numbers) >= 2:
                data["length"] = numbers[0]
                data["width"] = numbers[1]



        return data

    def extract_number(self, command):

        numbers = re.findall(r"\d+\.?\d*", command)

        if numbers:
            return float(numbers[0])

        return None

if __name__ == "__main__":
    extractor = ParameterExtractor()
    print(extractor.extract_dimensions(
        "estimate a 40 by 20 slab 6 inches thick"
    ))
