import math


class Rebar:

    def __init__(self):

        # Weight per linear foot
        # ASTM standard approximate weights

        self.bar_weights = {

            "#3": 0.376,
            "#4": 0.668,
            "#5": 1.043,
            "#6": 1.502,
            "#7": 2.044,
            "#8": 2.670

        }

    def calculate_rebar(
            self,
            bar_size,
            linear_feet,
            waste_percent=10,
            stock_length_feet=20,
            source="approved_structural_plan"
        ):
        bar_size = bar_size.strip().upper()

        if not bar_size.startswith("#"):
            bar_size = f"#{bar_size}"

        if bar_size not in self.bar_weights:
            raise ValueError("Unsupported rebar size")


        if linear_feet <= 0:
            raise ValueError("Linear feet must be greater than zero")

        if waste_percent < 0:
            raise ValueError("Waste percent cannot be negative")

        if stock_length_feet <= 0:
            raise ValueError("Stock length must be greater than zero")

        total_feet = math.ceil(
            linear_feet *
            (1 + waste_percent / 100) -
            1e-9
        )

        sticks = math.ceil(total_feet / stock_length_feet)
        total_weight = total_feet * self.bar_weights[bar_size]

        return {
            "status": "specified",
            "source": source,
            "material": "Rebar",
            "size": bar_size,
            "linear_feet": linear_feet,
            "total_linear_feet": total_feet,
            "stock_length_feet": stock_length_feet,
            "sticks": sticks,
            "weight_lbs": round(total_weight, 2),
            "waste_percent": waste_percent
        }
