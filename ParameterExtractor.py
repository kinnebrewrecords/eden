import re


class ParameterExtractor:
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

        elif "pitch" in command:
            if len(numbers) >= 2:
                data["length"] = numbers[0]
                data["pitch"] = numbers[1]

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