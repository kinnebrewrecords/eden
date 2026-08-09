
from Estimating import Estimator
from ParameterExtractor import ParameterExtractor
from AssemblyReports import create_backyard_studio_shell_report
from SpecialtyReports import create_specialty_report


class EstimateChange(Exception):
    def __init__(self, new_command=None):
        self.new_command = new_command

class CommandHandler:
    def __init__(self, memory, estimator, reports, projects):
        self.memory = memory
        self.estimator = estimator
        self.reports = reports
        self.projects = projects
        self.extractor=ParameterExtractor()
        self.pending_estimate=None
        self.pending_project_deletion = False
        self.commands = {
            "remember": self.remember_command,
            "recall": self.recall_command,
            "list": self.list_command,
            "forget": self.forget_command,
            "help": self.help_command,
            "create": self.create_project_command,
            "select": self.select_project_command,
            "show": self.show_project_command,
            "delete": self.delete_project_command,
            "open": self.open_project_command,
        }

    def ask_positive_float(self, prompt):
        while True:
            try:
                value = float(self.ask_input(prompt))

                if value <= 0:
                    print("Please enter a number greater than zero.")
                    continue

                return value

            except ValueError:
                print("Please enter a valid number.")

    def ask_positive_int(self, prompt):
        while True:
            try:
                value = int(self.ask_input(prompt))

                if value <= 0:
                    print("Please enter a whole number greater than zero.")
                    continue

                return value

            except ValueError:
                print("Please enter a whole number.")

    def ask_required_text(self, prompt):
        while True:
            value = self.ask_input(prompt).strip()

            if value:
                return value

            print("Please enter a value.")

    def choose_concrete_package(self, package_menu):

        self.reusing_last_concrete_package = False

        last_choice = self.memory.recall(
            "concrete_last_package_choice"
        )

        labels = {
            "1": "Standard package",
            "2": "Concrete only",
            "3": "Custom package"
        }

        if last_choice in labels:
            use_last = input(
                f"""
        Last concrete package: {labels[last_choice]}

        1. Use last package
        2. Choose a new package

        Choice:
        """
            ).lower()

            if use_last in ["1", "use", "last", ""]:
                self.reusing_last_concrete_package = True
                return last_choice

        choice = input(package_menu).lower()

        choice_map = {
            "1": "1",
            "standard": "1",
            "standard package": "1",
            "2": "2",
            "concrete": "2",
            "concrete only": "2",
            "3": "3",
            "custom": "3",
            "customize": "3"
        }

        choice = choice_map.get(choice)

        if choice is None:
            print("Invalid choice. Defaulting to concrete only.")
            choice = "2"

        self.memory.remember(
            "concrete_last_package_choice",
            choice
        )

        return choice

    def remember_command(self, command):
        words = command.split()

        if len(words) < 3:
            return "Usage: remember <key> <value>"
        key = words[1]
        value = " ".join(words[2:])
        self.memory.remember(key, value)
        return "I will remember that!"

    def recall_command(self, command):
        words = command.split()

        if len(words) < 2:
            return "Usage: recall <key>"

        value = self.memory.recall(words[1])
        if value is not None:
            return str(value)

        return "I don't have anything saved under that key."

    def list_command(self, command):
        memories = ""

        for key, value in self.memory.data.items():
            memories += f"{key}: {value}\n"
        return memories

    def forget_command(self, command):
        words = command.split()
        if len(words) < 2:
            return "Usage: forget <key>"
        key = words[1]
        result = self.memory.forget(key)
        if result:
            return "No problem."
        else:
            return "Is this something we talked about?"

    def help_command(self, command):
        return """

    Hi, I’m Eden. I can help you build material estimates and save them
    to your active project.

    Try commands like:

    Concrete:
    - estimate a 20 x 20 slab, 6 inches thick
    - estimate a concrete footing
    - estimate a concrete beam

    Lumber and Roofing:
    - estimate a framed wall
    - estimate roof sheathing
    - estimate shingles

    Exterior and Finish Work:
    - estimate exterior siding
    - estimate housewrap
    - estimate decking
    - estimate a fence
    - estimate flooring
    - estimate baseboard
    - estimate interior doors

    Project Assemblies:
    - estimate a backyard studio shell

    Interior:
    - estimate wall drywall
    - estimate batt insulation
    - estimate interior paint

    MEP:
    - estimate outlets
    - estimate pex pipe
    - estimate ductwork

    Project and Memory:
    - create project <project name>
    - select project <project name>
    - show project
    - remember <key> <value>
    - recall <key>
    - list
    - forget <key>

    Type "exit" when you are finished.

        """

    def ask_rebar_size(self, prompt):
        supported_sizes = ["#3", "#4", "#5", "#6", "#7", "#8"]

        while True:
            bar_size = self.ask_required_text(prompt).upper()

            if not bar_size.startswith("#"):
                bar_size = f"#{bar_size}"

            if bar_size in supported_sizes:
                return bar_size

            print(
                "Please enter a supported rebar size: "
                "#3, #4, #5, #6, #7, or #8."
            )

    def ask_input(self, prompt):
        answer = input(prompt).strip()
        lower_answer = answer.lower()

        if lower_answer in ["cancel", "start over", "never mind"]:
            raise EstimateChange()

        if lower_answer.startswith("change to "):
            new_item = answer[10:].strip()

            if new_item:
                raise EstimateChange(f"estimate {new_item}")

        return answer

    def estimate_command(self, command, intent):

        if intent["category"] == "assembly":
            return self.assembly_estimate(command, intent)

        elif intent["category"] == "specialty":
            return self.specialty_estimate(command, intent)

        elif intent["category"] == "lumber":
            return self.lumber_estimate(command, intent)

        elif intent["category"] == "roofing":
            return self.roofing_estimate(command, intent)

        elif intent["category"] == "concrete":
            return self.concrete_estimate(command, intent)

        elif intent["category"] == "drywall":
            return self.drywall_estimate(command, intent)

        elif intent["category"] == "insulation":
            return self.insulation_estimate(command, intent)

        elif intent["category"] == "drywall finish":
            return self.drywall_finish_estimate(command, intent)

        elif intent["category"] == "electrical":
            return self.electrical_estimate(command, intent)

        elif intent["category"] == "plumbing":

            return self.plumbing_estimate( command,intent)

        elif intent["category"] == "hvac":

            return self.hvac_estimate( command,intent)






        return (
            "I’m not set up to estimate that item yet. "
            "Try typing \"help\" to see the estimate types I currently support."
        )
    def finish_estimate(self, estimate, report):
        project = self.projects.get_active_project()

        if project is None:
            return f"{report}\nNo project is selected, so this estimate was not saved."

        self.projects.add_estimate(estimate)
        return f'Saved to project: {project["name"]}\n{report}'

    def assembly_estimate(self, command, intent):
        if intent["type"] != "backyard studio shell":
            return (
                "I’m not set up for that project assembly yet. "
                "Try estimating a backyard studio shell."
            )

        print(
            "\nBackyard Studio Shell combines a slab, wall framing, "
            "wall and roof sheathing, and shingles into one starter "
            "material takeoff."
        )

        length = self.ask_positive_float("Studio length (ft): ")
        width = self.ask_positive_float("Studio width (ft): ")
        wall_height = self.ask_positive_float("Wall height (ft): ")
        slab_thickness = self.ask_positive_float(
            "Slab thickness (in): "
        )

        include_interior_finish = self.ask_input(
            "Include insulation, drywall, and interior wall paint? "
            "(yes/no): "
        ).lower() in ["yes", "y"]

        insulation_r_value = "R-13"

        if include_interior_finish:
            insulation_r_value = self.ask_required_text(
                "Required wall insulation R-value from plans "
                "(example: R-13): "
            ).upper()

        estimate = self.estimator.backyard_studio_shell(
            length=length,
            width=width,
            wall_height=wall_height,
            slab_thickness_inches=slab_thickness,
            include_interior_finish=include_interior_finish,
            insulation_r_value=insulation_r_value
        )

        report = create_backyard_studio_shell_report(estimate)

        return self.finish_estimate(estimate, report)

    def specialty_estimate(self, command, intent):
        estimate_type = intent["type"]

        if estimate_type == "siding":
            area = self.ask_positive_float("Exterior wall area (sq ft): ")
            siding_type = self.ask_input(
                "Siding product/type (press Enter for generic siding): "
            ) or "Siding"
            estimate = self.estimator.siding(area, siding_type)

        elif estimate_type == "housewrap":
            area = self.ask_positive_float("Exterior wall area (sq ft): ")
            estimate = self.estimator.housewrap(area)

        elif estimate_type == "exterior trim":
            length = self.ask_positive_float("Exterior trim length (LF): ")
            trim_spec = self.ask_input(
                "Trim product/spec (press Enter for 1x4 Exterior Trim): "
            ) or "1x4 Exterior Trim"
            estimate = self.estimator.exterior_trim(length, trim_spec)

        elif estimate_type == "windows":
            quantity = self.ask_positive_int("Number of windows: ")
            window_spec = self.ask_input(
                "Window specification (press Enter for Window Unit): "
            ) or "Window Unit"
            estimate = self.estimator.windows(quantity, window_spec)

        elif estimate_type == "exterior doors":
            quantity = self.ask_positive_int("Number of exterior doors: ")
            door_spec = self.ask_input(
                "Door specification (press Enter for Exterior Door Unit): "
            ) or "Exterior Door Unit"
            estimate = self.estimator.exterior_doors(quantity, door_spec)

        elif estimate_type == "decking":
            length = self.ask_positive_float("Deck length (ft): ")
            width = self.ask_positive_float("Deck width (ft): ")
            estimate = self.estimator.decking(length, width)

        elif estimate_type == "fence":
            length = self.ask_positive_float("Fence length (LF): ")
            height = self.ask_positive_float("Fence height (ft): ")
            estimate = self.estimator.fence(length, height)

        elif estimate_type == "flooring":
            area = self.ask_positive_float("Floor area (sq ft): ")
            flooring_type = self.ask_input(
                "Flooring product/type (press Enter for Flooring): "
            ) or "Flooring"
            estimate = self.estimator.flooring(area, flooring_type)

        elif estimate_type == "baseboard":
            length = self.ask_positive_float("Baseboard length (LF): ")
            baseboard_spec = self.ask_input(
                "Baseboard specification (press Enter for Baseboard Trim): "
            ) or "Baseboard Trim"
            estimate = self.estimator.baseboard(
                length,
                baseboard_spec=baseboard_spec
            )

        elif estimate_type == "interior doors":
            quantity = self.ask_positive_int("Number of interior doors: ")
            door_spec = self.ask_input(
                "Door specification (press Enter for Interior Door Unit): "
            ) or "Interior Door Unit"
            estimate = self.estimator.interior_doors(quantity, door_spec)

        else:
            return (
                "I’m not set up to estimate that item yet. "
                "Try typing \"help\" to see what I can estimate."
            )

        return self.finish_estimate(
            estimate,
            create_specialty_report(estimate)
        )

    def concrete_estimate(self, command,intent):
        if intent["type"] == "slab edge":
            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length = self.ask_positive_float("Slab length (ft): ")

            width = dimensions["width"]
            if width is None:
                width = self.ask_positive_float("Slab width (ft): ")

            edge_width = self.ask_positive_float(
                "Thickened edge width (in): "
            )

            edge_depth = self.ask_positive_float(
                "Thickened edge depth (in): "
            )

            estimate = self.estimator.concrete_slab_edge(
                length,
                width,
                edge_width,
                edge_depth
            )

            report = self.reports.create_concrete_slab_edge_report(
                estimate
            )

            return self.finish_estimate(estimate, report)

        elif intent["type"] == "slab":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length = self.ask_positive_float("Length (ft): ")

            width = dimensions["width"]
            if width is None:
                width = self.ask_positive_float("Width (ft): ")

            thickness = dimensions["thickness"]
            if thickness is None:
                thickness = self.ask_positive_float("Thickness (in): ")

            # Slab Assembly Selection

            choice = self.choose_concrete_package(
                """
        How would you like to build this slab?

        1. Standard slab package
        2. Concrete only
        3. Customize materials

        Choice:
        """
            )

            # Standard slab package

            if choice in [
                "1",
                "standard",
                "standard package"
            ]:

                reinforced = True

                rebar = {
                    "status": "plan_required",
                    "source": "approved_structural_plan",
                    "schedule": None
                }

                wire_mesh = True

                vapor_barrier = True

                gravel_base = True

                control_joints = True

                forms = False

                build_type = "Standard Slab Package"



            # Concrete only

            elif choice in [
                "2",
                "concrete",
                "concrete only",
                "none"
            ]:

                reinforced = False

                rebar = None

                wire_mesh = False

                vapor_barrier = False

                gravel_base = False

                control_joints = False

                forms = False

                build_type = "Concrete Only"



            # Custom materials

            elif choice in [
                "3",
                "custom",
                "customize"
            ]:

                build_type = "Custom Slab Package"

                reinforced = input(
                    "Is this a reinforced slab? (yes/no): "
                ).lower() in [
                                 "yes",
                                 "y"
                             ]

                # Rebar
                rebar = None

                if reinforced:
                    has_schedule = input(
                        "Do you have an approved structural rebar schedule? (yes/no): "
                    ).lower() in ["yes", "y"]

                    if has_schedule:
                        direction_1_size = self.ask_rebar_size(
                            "Direction 1 bar size from approved plan: "
                        )

                        direction_1_linear_feet = self.ask_positive_float(
                            "Total Direction 1 rebar linear feet from approved plan: "
                        )

                        direction_2_size = self.ask_rebar_size(
                            "Direction 2 bar size from approved plan: "
                        )

                        direction_2_linear_feet = self.ask_positive_float(
                            "Total Direction 2 rebar linear feet from approved plan: "
                        )

                        rebar = {
                            "status": "specified",
                            "source": "approved_structural_plan",
                            "schedule": {
                                "direction_1": {
                                    "bar_size": direction_1_size,
                                    "linear_feet": direction_1_linear_feet
                                },
                                "direction_2": {
                                    "bar_size": direction_2_size,
                                    "linear_feet": direction_2_linear_feet
                                }
                            },
                            "takeoff": [
                                self.estimator.calculate_rebar(
                                    direction_1_size,
                                    direction_1_linear_feet
                                ),
                                self.estimator.calculate_rebar(
                                    direction_2_size,
                                    direction_2_linear_feet
                                )
                            ]
                        }

                    else:
                        rebar = {
                            "status": "plan_required",
                            "source": "approved_structural_plan",
                            "schedule": None
                        }


                else:

                    rebar = None

                # Wire Mesh

                wire_mesh = input(
                    "Include wire mesh? "
                ).lower() in [
                                "yes",
                                "y"
                            ]

                # Vapor Barrier

                vapor_barrier = input(
                    "Include vapor barrier? "
                ).lower() in [
                                    "yes",
                                    "y"
                                ]

                # Gravel Base

                gravel_base = input(
                    "Include gravel base? "
                ).lower() in [
                                  "yes",
                                  "y"
                              ]

                # Control Joints

                control_joints = input(
                    "Include control joints? "
                ).lower() in [
                                     "yes",
                                     "y"
                                 ]

                forms = input(
                    "Include forms? "
                ).lower() in [
                            "yes",
                            "y"
                        ]

            else:

                print(
                    "Invalid choice. Defaulting to concrete only."
                )

                reinforced = False

                rebar = None

                wire_mesh = False

                vapor_barrier = False

                gravel_base = False

                control_joints = False

                forms = False

                build_type = "Concrete Only"

            estimate = self.estimator.concrete_slab(
                length,
                width,
                thickness,
                reinforced=reinforced,
                rebar=rebar,
                wire_mesh=wire_mesh,
                vapor_barrier=vapor_barrier,
                gravel_base=gravel_base,
                control_joints=control_joints,
                forms=forms,
                build_type=build_type
            )

            report = self.reports.create_concrete_slab_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )

        elif intent["type"] == "grade beam":
            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length = self.ask_positive_float("Length (ft): ")

            width = dimensions["width"]
            if width is None:
                width = self.ask_positive_float("Width (in): ")

            height = dimensions["height"]
            if height is None:
                height = self.ask_positive_float("Height (in): ")

            choice = self.choose_concrete_package(
                """
        How would you like to build this concrete grade beam?

        1. Standard grade beam package
        2. Concrete only
        3. Customize materials

        Choice:
        """
            )

            if choice in ["1", "standard", "standard package"]:
                reinforced = True
                rebar = {
                    "status": "plan_required",
                    "source": "approved_structural_plan",
                    "schedule": None
                }
                forms = True
                build_type = "Standard Concrete Grade Beam Package"

            elif choice in ["3", "custom", "customize"]:
                build_type = "Custom Concrete Grade Beam Package"
                reinforced = input(
                    "Is this grade beam reinforced? (yes/no): "
                ).lower() in ["yes", "y"]

                rebar = None

                if reinforced:
                    has_schedule = input(
                        "Do you have an approved structural rebar schedule? (yes/no): "
                    ).lower() in ["yes", "y"]

                    if has_schedule:
                        main_size = input(
                            "Main bar size from approved plan: "
                        ).upper()

                        main_linear_feet = self.ask_positive_float(
                            "Total main bar linear feet from approved plan: "
                        )

                        stirrup_size = input(
                            "Stirrup bar size from approved plan: "
                        ).upper()

                        stirrup_linear_feet = self.ask_positive_float(
                            "Total stirrup rebar linear feet from approved plan: "
                        )

                        rebar = {
                            "status": "specified",
                            "source": "approved_structural_plan",
                            "schedule": {
                                "main": {
                                    "bar_size": main_size,
                                    "linear_feet": main_linear_feet
                                },
                                "stirrups": {
                                    "bar_size": stirrup_size,
                                    "linear_feet": stirrup_linear_feet
                                }
                            },
                            "takeoff": [
                                self.estimator.calculate_rebar(
                                    main_size, main_linear_feet
                                ),
                                self.estimator.calculate_rebar(
                                    stirrup_size, stirrup_linear_feet
                                )
                            ]
                        }

                    else:
                        rebar = {
                            "status": "plan_required",
                            "source": "approved_structural_plan",
                            "schedule": None
                        }

                forms = input(
                    "Include forms? (yes/no): "
                ).lower() in ["yes", "y"]

            else:
                reinforced = False
                rebar = None
                forms = False
                build_type = "Concrete Only"

            estimate = self.estimator.concrete_grade_beam(
                length,
                width,
                height,
                reinforced=reinforced,
                rebar=rebar,
                forms=forms,
                build_type=build_type
            )

            report = self.reports.create_concrete_grade_beam_report(estimate)
            return self.finish_estimate(estimate, report)




        elif intent["type"] == "beam":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length = self.ask_positive_float("Length (ft): ")

            width_inches = dimensions["width"]
            if width_inches is None:
                width_inches = self.ask_positive_float("Width (in): ")

            height_inches = dimensions["height"]
            if height_inches is None:
                height_inches = self.ask_positive_float("Height (in): ")

            choice = self.choose_concrete_package(
                """
        How would you like to build this concrete beam?

        1. Standard beam package
        2. Concrete only
        3. Customize materials

        Choice:
        """
            ).lower()

            # Standard Beam Package

            if choice in [
                "1",
                "standard",
                "standard package"
            ]:

                reinforced = True

                rebar = {
                    "status": "plan_required",
                    "source": "approved_structural_plan",
                    "schedule": None
                }

                forms = True

                build_type = "Standard Concrete Beam Package"



            # Concrete Only

            elif choice in [
                "2",
                "concrete",
                "concrete only",
                "none"
            ]:

                reinforced = False

                rebar = None

                forms = False

                build_type = "Concrete Only"



            # Custom

            elif choice in [
                "3",
                "custom",
                "customize"
            ]:

                build_type = "Custom Concrete Beam Package"

                reinforced = input(
                    "Is this reinforced? (yes/no): "
                ).lower() in [
                                 "yes",
                                 "y"
                             ]

                rebar = None

                if reinforced:
                    has_schedule = input(
                        "Do you have an approved structural rebar schedule? (yes/no): "
                    ).lower() in ["yes", "y"]

                    if has_schedule:
                        main_size = self.ask_rebar_size(
                            "Main bar size from approved plan: "
                        )

                        main_linear_feet = self.ask_positive_float(
                            "Total main bar linear feet from approved plan: "
                        )

                        stirrup_size = self.ask_rebar_size(
                            "Stirrup bar size from approved plan: "
                        )

                        stirrup_linear_feet = self.ask_positive_float(
                            "Total stirrup rebar linear feet from approved plan: "
                        )

                        main_takeoff = self.estimator.calculate_rebar(
                            main_size,
                            main_linear_feet
                        )

                        stirrup_takeoff = self.estimator.calculate_rebar(
                            stirrup_size,
                            stirrup_linear_feet
                        )

                        rebar = {
                            "status": "specified",
                            "source": "approved_structural_plan",
                            "schedule": {
                                "main": {
                                    "bar_size": main_size,
                                    "linear_feet": main_linear_feet
                                },
                                "stirrups": {
                                    "bar_size": stirrup_size,
                                    "linear_feet": stirrup_linear_feet
                                }
                            },
                            "takeoff": [
                                main_takeoff,
                                stirrup_takeoff
                            ]
                        }

                    else:
                        rebar = {
                            "status": "plan_required",
                            "source": "approved_structural_plan",
                            "schedule": None
                        }

                else:

                    rebar = None

                forms = input(
                    "Include forms? "
                ).lower() in [
                            "yes",
                            "y"
                        ]



            else:

                reinforced = False

                rebar = None

                forms = False

                build_type = "Concrete Only"

            estimate = self.estimator.concrete_beam(
                length,
                width_inches,
                height_inches,
                reinforced=reinforced,
                rebar=rebar,
                forms=forms
            )

            estimate["build_type"] = build_type

            report = self.reports.create_concrete_beam_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )


        elif intent["type"] == "ramp":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length = self.ask_positive_float("Length (ft): ")

            width = dimensions["width"]
            if width is None:
                width = self.ask_positive_float("Width (ft): ")

            height = dimensions["height"]
            if height is None:
                height = self.ask_positive_float("Height (in): ")

            choice = self.choose_concrete_package(
                """
        How would you like to build this concrete ramp?

        1. Standard ramp package
        2. Concrete only
        3. Customize materials

        Choice:
        """
            )

            # Standard Ramp Package

            if choice in [
                "1",
                "standard",
                "standard package"
            ]:

                reinforced = True

                rebar = {
                    "status": "plan_required",
                    "source": "approved_structural_plan",
                    "schedule": None
                }

                gravel_base = True

                forms = True

                build_type = "Standard Concrete Ramp Package"



            # Concrete Only

            elif choice in [
                "2",
                "concrete",
                "concrete only",
                "none"
            ]:

                reinforced = False

                rebar = None

                gravel_base = False

                forms = False

                build_type = "Concrete Only"



            # Custom

            elif choice in [
                "3",
                "custom",
                "customize"
            ]:

                build_type = "Custom Concrete Ramp Package"

                reinforced = input(
                    "Is this reinforced? (yes/no): "
                ).lower() in [
                                 "yes",
                                 "y"
                             ]

                rebar = None

                if reinforced:
                    has_schedule = input(
                        "Do you have an approved structural rebar schedule? (yes/no): "
                    ).lower() in ["yes", "y"]

                    if has_schedule:
                        direction_1_size = input(
                            "Direction 1 bar size from approved plan: "
                        ).upper()

                        direction_1_linear_feet =self.ask_positive_float (
                            "Total Direction 1 rebar linear feet from approved plan: "
                        )

                        direction_2_size = input(
                            "Direction 2 bar size from approved plan: "
                        ).upper()

                        direction_2_linear_feet = self.ask_positive_float(
                            "Total Direction 2 rebar linear feet from approved plan: "
                        )

                        rebar = {
                            "status": "specified",
                            "source": "approved_structural_plan",
                            "schedule": {
                                "direction_1": {
                                    "bar_size": direction_1_size,
                                    "linear_feet": direction_1_linear_feet
                                },
                                "direction_2": {
                                    "bar_size": direction_2_size,
                                    "linear_feet": direction_2_linear_feet
                                }
                            },
                            "takeoff": [
                                self.estimator.calculate_rebar(
                                    direction_1_size,
                                    direction_1_linear_feet
                                ),
                                self.estimator.calculate_rebar(
                                    direction_2_size,
                                    direction_2_linear_feet
                                )
                            ]
                        }

                    else:
                        rebar = {
                            "status": "plan_required",
                            "source": "approved_structural_plan",
                            "schedule": None
                        }

                else:

                    rebar = None

                gravel_base = input(
                    "Include gravel base? "
                ).lower() in [
                                  "yes",
                                  "y"
                              ]

                forms = input(
                    "Include forms? "
                ).lower() in [
                            "yes",
                            "y"
                        ]



            else:

                reinforced = False

                rebar = None

                gravel_base = False

                forms = False

                build_type = "Concrete Only"

            estimate = self.estimator.concrete_ramp(
                length,
                width,
                height,
                reinforced=reinforced,
                rebar=rebar,
                gravel_base=gravel_base,
                forms=forms
            )

            estimate["build_type"] = build_type

            report = self.reports.create_concrete_ramp_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )

        elif intent["type"] == "column":
            dimensions = self.extractor.extract_dimensions(command)

            diameter = dimensions["diameter"]
            if diameter is None:
                diameter = self.ask_positive_float("Diameter (in): ")

            height = dimensions["height"]
            if height is None:
                height = self.ask_positive_float("Height (ft): ")

            quantity = dimensions["quantity"]
            if quantity is None:
                quantity = int(input("Quantity: "))

            choice = self.choose_concrete_package(
                """
        How would you like to build this concrete column?

        1. Standard reinforced column package
        2. Concrete only
        3. Customize materials

        Choice:
        """
            )

            if choice in ["1", "standard", "standard package"]:
                reinforced = True
                rebar = {
                            "status": "plan_required",
                            "source": "approved_structural_plan",
                            "schedule": None
                        }
                forms = True
                build_type = "Standard Reinforced Column Package"

            elif choice in ["3", "custom", "customize"]:
                build_type = "Custom Concrete Column Package"
                reinforced = input(
                    "Is this column reinforced? (yes/no): "
                ).lower() in ["yes", "y"]

                rebar = None

                if reinforced:
                    has_schedule = input(
                        "Do you have an approved structural rebar schedule? (yes/no): "
                    ).lower() in ["yes", "y"]

                    if has_schedule:
                        vertical_size = input(
                            "Vertical bar size from approved plan (example: #5): "
                        ).upper()

                        vertical_linear_feet = self.ask_positive_float(
                            "Total vertical rebar linear feet from approved plan: "
                        )

                        ties_size = input(
                            "Tie bar size from approved plan (example: #3): "
                        ).upper()

                        ties_linear_feet = self.ask_positive_float(
                            "Total tie rebar linear feet from approved plan: "
                        )

                        vertical_takeoff = self.estimator.calculate_rebar(
                            vertical_size,
                            vertical_linear_feet
                        )

                        ties_takeoff = self.estimator.calculate_rebar(
                            ties_size,
                            ties_linear_feet
                        )

                        rebar = {
                            "status": "specified",
                            "source": "approved_structural_plan",
                            "schedule": {
                                "vertical": {
                                    "bar_size": vertical_size,
                                    "linear_feet": vertical_linear_feet
                                },
                                "ties": {
                                    "bar_size": ties_size,
                                    "linear_feet": ties_linear_feet
                                }
                            },
                            "takeoff": [
                                vertical_takeoff,
                                ties_takeoff
                            ]
                        }

                    else:
                        rebar = {
                            "status": "plan_required",
                            "source": "approved_structural_plan",
                            "schedule": None
                        }

                forms = input(
                    "Include forms? (yes/no): "
                ).lower() in ["yes", "y"]

            else:
                reinforced = False
                rebar = None
                forms = False
                build_type = "Concrete Only"

            estimate = self.estimator.concrete_column(
                diameter,
                height,
                quantity,
                reinforced=reinforced,
                rebar=rebar,
                forms=forms
            )

            estimate["build_type"] = build_type

            report = self.reports.create_concrete_column_report(estimate)
            return self.finish_estimate(estimate, report)


        elif intent["type"] == "trench":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length = self.ask_positive_float("Length (ft): ")

            width_inches = dimensions["width"]
            if width_inches is None:
                width_inches = self.ask_positive_float("Width (in): ")

            depth_inches = dimensions["depth"]
            if depth_inches is None:
                depth_inches = self.ask_positive_float("Depth (in): ")

            estimate = self.estimator.concrete_trench(
                length,
                width_inches,
                depth_inches
            )

            report = self.reports.create_concrete_trench_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )



        elif intent["type"] == "spread footing":
            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length = self.ask_positive_float("Length (ft): ")

            width = dimensions["width"]
            if width is None:
                width = self.ask_positive_float("Width (ft): ")

            depth = dimensions["depth"]
            if depth is None:
                depth = self.ask_positive_float("Depth (in): ")
            estimate = self.estimator.concrete_spread_footing(
                length,
                width,
                depth
            )
            report = self.reports.create_concrete_spread_footing_report(estimate)
            return self.finish_estimate(estimate, report)


        elif intent["type"] == "round footing":
            dimensions = self.extractor.extract_dimensions(command)

            diameter = dimensions["diameter"]
            if diameter is None:
                diameter =self.ask_positive_float("Diameter (in): ")

            depth = dimensions["depth"]
            if depth is None:
                depth = self.ask_positive_float("Depth (ft): ")

            quantity = dimensions["quantity"]
            if quantity is None:
                quantity = int(input("Quantity: "))
            estimate = self.estimator.concrete_round_footing(
                diameter,
                depth,
                quantity

            )
            report = self.reports.create_concrete_round_footing_report(estimate)
            return self.finish_estimate(estimate, report)



        elif intent["type"] == "pile cap":
            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length = self.ask_positive_float("Length (ft): ")

            width = dimensions["width"]
            if width is None:
                width = self.ask_positive_float("Width (ft): ")

            depth = dimensions["depth"]
            if depth is None:
                depth = self.ask_positive_float("Depth (in): ")
            estimate = self.estimator.concrete_pile_cap(
                length,
                width,
                depth
            )
            report = self.reports.create_concrete_pile_cap_report(estimate)
            return self.finish_estimate(estimate, report)



        elif intent["type"] == "retaining wall":
            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Length (ft): ")

            height = dimensions["height"]
            if height is None:
                height= self.ask_positive_float("Height (ft): ")

            thickness = dimensions["thickness"]
            if thickness is None:
                thickness= self.ask_positive_float("Thickness (in): ")
            estimate = self.estimator.concrete_retaining_wall(
                length,
                height,
                thickness
            )
            report = self.reports.create_concrete_retaining_wall_report(estimate)
            return self.finish_estimate(estimate, report)


        elif intent["type"] == "steps":
            dimensions = self.extractor.extract_dimensions(command)

            width = dimensions.get("width")
            if width is None:
                width= self.ask_positive_float("Width (ft): ")

            tread_depth = dimensions.get("tread_depth")
            if tread_depth is None:
                tread_depth= self.ask_positive_float("Tread Depth (in): ")

            riser_height = dimensions.get("riser_height")
            if riser_height is None:
                riser_height= self.ask_positive_float("Riser Height (in): ")

            steps = dimensions.get("steps")
            if steps is None:
                steps = int(input("Number of Steps: "))

            choice = self.choose_concrete_package(
                """
        How would you like to build these concrete steps?

        1. Standard steps package
        2. Concrete only
        3. Customize materials

        Choice:
        """
            )

            if choice in ["1", "standard", "standard package"]:
                reinforced = True
                rebar = {
                    "status": "plan_required",
                    "source": "approved_structural_plan",
                    "schedule": None
                }
                gravel_base = True
                vapor_barrier = False
                forms = True
                build_type = "Standard Concrete Steps Package"

            elif choice in ["3", "custom", "customize"]:
                build_type = "Custom Concrete Steps Package"

                reinforced = input(
                    "Are these steps reinforced? (yes/no): "
                ).lower() in ["yes", "y"]

                rebar = None

                if reinforced:
                    has_schedule = input(
                        "Do you have an approved structural rebar schedule? (yes/no): "
                    ).lower() in ["yes", "y"]

                    if has_schedule:
                        bar_size = input(
                            "Rebar size from approved plan: "
                        ).upper()

                        linear_feet = float(input(
                            "Total rebar linear feet from approved plan: "
                        ))

                        rebar = {
                            "status": "specified",
                            "source": "approved_structural_plan",
                            "schedule": {
                                "main": {
                                    "bar_size": bar_size,
                                    "linear_feet": linear_feet
                                }
                            },
                            "takeoff": [
                                self.estimator.calculate_rebar(
                                    bar_size,
                                    linear_feet
                                )
                            ]
                        }

                    else:
                        rebar = {
                            "status": "plan_required",
                            "source": "approved_structural_plan",
                            "schedule": None
                        }

                gravel_base = input(
                    "Include gravel base? (yes/no): "
                ).lower() in ["yes", "y"]

                vapor_barrier = input(
                    "Include vapor barrier? (yes/no): "
                ).lower() in ["yes", "y"]

                forms = input(
                    "Include forms? (yes/no): "
                ).lower() in ["yes", "y"]

            else:
                reinforced = False
                rebar = None
                gravel_base = False
                vapor_barrier = False
                forms = False
                build_type = "Concrete Only"

            estimate = self.estimator.concrete_steps(
                width,
                tread_depth,
                riser_height,
                steps,
                reinforced=reinforced,
                rebar=rebar,
                gravel_base=gravel_base,
                vapor_barrier=vapor_barrier,
                forms=forms
            )

            estimate["build_type"] = build_type

            report = self.reports.create_concrete_steps_report(estimate)
            return self.finish_estimate(estimate, report)


        elif intent["type"] == "lintel":
            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Length (ft): ")

            width = dimensions["width"]
            if width is None:
                width= self.ask_positive_float("Width (in): ")

            height = dimensions["height"]
            if height is None:
                height= self.ask_positive_float("Height (in): ")
            estimate = self.estimator.concrete_lintel(
                length,
                width,
                height
            )
            report = self.reports.create_concrete_lintel_report(estimate)
            return self.finish_estimate(estimate, report)



        elif intent["type"] in [
                "footing system",
                "foundation footing system",
                "continuous footing system"
        ]:
            print(
                "\nA footing system combines several continuous footing "
                "runs into one concrete order."
            )
            run_type_count = self.ask_positive_int(
                "Number of different footing run types: "
            )
            footing_runs = []

            for number in range(1, run_type_count + 1):
                print(f"\nFooting run type {number}")
                footing_runs.append(
                    {
                        "length": self.ask_positive_float(
                            "Continuous run length (ft): "
                        ),
                        "width_inches": self.ask_positive_float(
                            "Footing width (in): "
                        ),
                        "depth_inches": self.ask_positive_float(
                            "Footing depth (in): "
                        ),
                        "quantity": self.ask_positive_int(
                            "Number of identical runs: "
                        )
                    }
                )

            reinforced = input(
                "Is this footing system reinforced? (yes/no): "
            ).strip().lower() in ["yes", "y"]
            rebar = (
                {
                    "status": "plan_required",
                    "source": "approved_structural_plan",
                    "schedule": None
                }
                if reinforced
                else None
            )
            forms = input("Include forms? (yes/no): ").strip().lower() in [
                "yes", "y"
            ]
            gravel_base = input(
                "Include gravel base? (yes/no): "
            ).strip().lower() in ["yes", "y"]

            estimate = self.estimator.concrete_footing_system(
                footing_runs,
                reinforced=reinforced,
                rebar=rebar,
                forms=forms,
                gravel_base=gravel_base
            )
            run_lines = "\n".join(
                (
                    f"- {run['quantity']} run(s): {run['length']} ft × "
                    f"{run['width_inches']} in wide × "
                    f"{run['depth_inches']} in deep"
                )
                for run in estimate["footing_runs"]
            )
            takeoff_lines = "\n".join(
                f"- {item['item']}: {item['quantity']} {item['unit']}"
                for item in estimate["material_takeoff"]
            )
            report = (
                "\nCONCRETE FOOTING SYSTEM ESTIMATE\n\n"
                f"Footing runs: {estimate['run_count']}\n\n"
                f"{run_lines}\n\n"
                f"Concrete volume: {estimate['cubic_yards']} CY\n"
                f"Order quantity: {estimate['order_quantity']} CY\n"
                f"Waste: {estimate['waste_percent']}%\n\n"
                "MATERIAL TAKEOFF:\n\n"
                f"{takeoff_lines}\n\n"
                f"Note: {estimate['structural_note']}\n"
            )
            return self.finish_estimate(estimate, report)

        elif intent["type"] == "footing":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Length (ft): ")

            width = dimensions["width"]
            if width is None:
                width= self.ask_positive_float("Width (ft): ")

            depth = dimensions["depth"]
            if depth is None:
                depth= self.ask_positive_float("Depth (in): ")

            # Footing Assembly Selection

            choice = self.choose_concrete_package(
                """
        How would you like to build this footing?

        1. Standard footing package
        2. Concrete only
        3. Customize materials

        Choice:
        """
            )

            # Standard Package

            if choice in [
                "1",
                "standard",
                "standard package"
            ]:

                reinforced = True

                rebar = {
                    "status": "plan_required",
                    "source": "approved_structural_plan",
                    "schedule": None
                }

                forms = True

                gravel_base = False

                build_type = "Standard Footing Package"



            # Concrete Only

            elif choice in [
                "2",
                "concrete",
                "concrete only",
                "none"
            ]:

                reinforced = False

                rebar = None

                forms = False

                gravel_base = False

                build_type = "Concrete Only"



            # Custom

            elif choice in [
                "3",
                "custom",
                "customize"
            ]:

                build_type = "Custom Footing Package"

                reinforced = input(
                    "Is this footing reinforced? (yes/no): "
                ).lower() in [
                                 "yes",
                                 "y"
                             ]

                rebar = None

                if reinforced:
                    has_schedule = input(
                        "Do you have an approved structural rebar schedule? (yes/no): "
                    ).lower() in ["yes", "y"]

                    if has_schedule:
                        bar_size = self.ask_rebar_size(
                            "Bar size from approved plan: "
                        )

                        linear_feet = self.ask_positive_float(
                            "Total rebar linear feet from approved plan: "
                        )

                        rebar_takeoff = self.estimator.calculate_rebar(
                            bar_size,
                            linear_feet
                        )

                        rebar = {
                            "status": "specified",
                            "source": "approved_structural_plan",
                            "schedule": {
                                "main": {
                                    "bar_size": bar_size,
                                    "linear_feet": linear_feet
                                }
                            },
                            "takeoff": [rebar_takeoff]
                        }

                    else:
                        rebar = {
                            "status": "plan_required",
                            "source": "approved_structural_plan",
                            "schedule": None
                        }

                else:

                    rebar = None

                forms = input(
                    "Include forms? "
                ).lower() in [
                            "yes",
                            "y"
                        ]

                gravel_base = input(
                    "Include gravel base? "
                ).lower() in [
                                  "yes",
                                  "y"
                              ]



            else:

                print(
                    "Invalid choice. Defaulting to concrete only."
                )

                reinforced = False

                rebar = None

                forms = False

                gravel_base = False

                build_type = "Concrete Only"

            estimate = self.estimator.concrete_footing(
                length,
                width,
                depth,
                reinforced=reinforced,
                rebar=rebar,
                forms=forms,
                gravel_base=gravel_base
            )

            estimate["build_type"] = build_type

            report = self.reports.create_concrete_footing_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )


        elif intent["type"] == "foundation wall":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Length (ft): ")

            height = dimensions["height"]
            if height is None:
                height= self.ask_positive_float("Height (ft): ")

            thickness = dimensions["thickness"]
            if thickness is None:
                thickness= self.ask_positive_float("Thickness (in): ")

            # Foundation Wall Assembly Selection

            choice = self.choose_concrete_package(
                """
        How would you like to build this foundation wall?

        1. Standard foundation wall package
        2. Concrete only
        3. Customize materials

        Choice:
        """
            )

            # Standard Package

            if choice in [
                "1",
                "standard",
                "standard package"
            ]:

                reinforced = True

                rebar = {
                    "vertical": "#5 @ 24 OC",
                    "horizontal": "#4 continuous"
                }

                forms = True

                waterproofing = True

                build_type = "Standard Foundation Wall Package"



            # Concrete Only

            elif choice in [
                "2",
                "concrete",
                "concrete only",
                "none"
            ]:

                reinforced = False

                rebar = None

                forms = False

                waterproofing = False

                build_type = "Concrete Only"



            # Custom

            elif choice in [
                "3",
                "custom",
                "customize"
            ]:

                build_type = "Custom Foundation Wall Package"

                reinforced = input(
                    "Is this wall reinforced? (yes/no): "
                ).lower() in [
                                 "yes",
                                 "y"
                             ]

                rebar = None

                if reinforced:
                    has_schedule = input(
                        "Do you have an approved structural rebar schedule? (yes/no): "
                    ).lower() in ["yes", "y"]

                    if has_schedule:
                        vertical_size = input(
                            "Vertical bar size from approved plan: "
                        ).upper()

                        vertical_linear_feet = float(input(
                            "Total vertical rebar linear feet from approved plan: "
                        ))

                        horizontal_size = input(
                            "Horizontal bar size from approved plan: "
                        ).upper()

                        horizontal_linear_feet = float(input(
                            "Total horizontal rebar linear feet from approved plan: "
                        ))

                        vertical_takeoff = self.estimator.calculate_rebar(
                            vertical_size,
                            vertical_linear_feet
                        )

                        horizontal_takeoff = self.estimator.calculate_rebar(
                            horizontal_size,
                            horizontal_linear_feet
                        )

                        rebar = {
                            "status": "specified",
                            "source": "approved_structural_plan",
                            "schedule": {
                                "vertical": {
                                    "bar_size": vertical_size,
                                    "linear_feet": vertical_linear_feet
                                },
                                "horizontal": {
                                    "bar_size": horizontal_size,
                                    "linear_feet": horizontal_linear_feet
                                }
                            },
                            "takeoff": [
                                vertical_takeoff,
                                horizontal_takeoff
                            ]
                        }

                    else:
                        rebar = {
                            "status": "plan_required",
                            "source": "approved_structural_plan",
                            "schedule": None
                        }


                else:

                    rebar = None

                forms = input(
                    "Include forms? "
                ).lower() in [
                            "yes",
                            "y"
                        ]

                waterproofing = input(
                    "Include waterproofing? "
                ).lower() in [
                                    "yes",
                                    "y"
                                ]



            else:

                print(
                    "Invalid choice. Defaulting to concrete only."
                )

                reinforced = False

                rebar = None

                forms = False

                waterproofing = False

                build_type = "Concrete Only"

            estimate = self.estimator.concrete_foundation_wall(
                length,
                height,
                thickness,
                reinforced=reinforced,
                rebar=rebar,
                forms=forms,
                build_type=build_type,
                waterproofing=waterproofing
            )

            estimate["build_type"] = build_type

            report = self.reports.create_concrete_foundation_wall_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )



        elif intent["type"] == "pad":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Length (ft): ")

            width = dimensions["width"]
            if width is None:
                width= self.ask_positive_float("Width (ft): ")

            thickness = dimensions["thickness"]
            if thickness is None:
                thickness= self.ask_positive_float("Thickness (in): ")

            choice = self.choose_concrete_package(
                """
        How would you like to build this concrete pad?

        1. Standard pad package
        2. Concrete only
        3. Customize materials

        Choice:
        """
            )

            # Standard Pad Package

            if choice in [
                "1",
                "standard",
                "standard package"
            ]:

                reinforced = True

                rebar = {
                    "size": "#4",
                    "spacing": "16 OC"
                }

                wire_mesh = True

                vapor_barrier = False

                gravel_base = True

                control_joints = True

                forms = True

                build_type = "Standard Concrete Pad Package"



            # Concrete Only

            elif choice in [
                "2",
                "concrete",
                "concrete only",
                "none"
            ]:

                reinforced = False

                rebar = None

                wire_mesh = False

                vapor_barrier = False

                gravel_base = False

                control_joints = False

                forms = False

                build_type = "Concrete Only"



            # Custom

            elif choice in [
                "3",
                "custom",
                "customize"
            ]:

                build_type = "Custom Concrete Pad Package"

                reinforced = input(
                    "Is this pad reinforced? (yes/no): "
                ).lower() in [
                                 "yes",
                                 "y"
                             ]

                rebar = None

                if reinforced:
                    has_schedule = input(
                        "Do you have an approved structural rebar schedule? (yes/no): "
                    ).lower() in ["yes", "y"]

                    if has_schedule:
                        direction_1_size = input(
                            "Direction 1 bar size from approved plan: "
                        ).upper()

                        direction_1_linear_feet = float(input(
                            "Total Direction 1 rebar linear feet from approved plan: "
                        ))

                        direction_2_size = input(
                            "Direction 2 bar size from approved plan: "
                        ).upper()

                        direction_2_linear_feet = float(input(
                            "Total Direction 2 rebar linear feet from approved plan: "
                        ))

                        rebar = {
                            "status": "specified",
                            "source": "approved_structural_plan",
                            "schedule": {
                                "direction_1": {
                                    "bar_size": direction_1_size,
                                    "linear_feet": direction_1_linear_feet
                                },
                                "direction_2": {
                                    "bar_size": direction_2_size,
                                    "linear_feet": direction_2_linear_feet
                                }
                            },
                            "takeoff": [
                                self.estimator.calculate_rebar(
                                    direction_1_size,
                                    direction_1_linear_feet
                                ),
                                self.estimator.calculate_rebar(
                                    direction_2_size,
                                    direction_2_linear_feet
                                )
                            ]
                        }

                    else:
                        rebar = {
                            "status": "plan_required",
                            "source": "approved_structural_plan",
                            "schedule": None
                        }

                else:

                    rebar = None

                wire_mesh = input(
                    "Include wire mesh? "
                ).lower() in [
                                "yes",
                                "y"
                            ]

                vapor_barrier = input(
                    "Include vapor barrier? "
                ).lower() in [
                                    "yes",
                                    "y"
                                ]

                gravel_base = input(
                    "Include gravel base? "
                ).lower() in [
                                  "yes",
                                  "y"
                              ]

                control_joints = input(
                    "Include control joints? "
                ).lower() in [
                                     "yes",
                                     "y"
                                 ]

                forms = input(
                    "Include forms? "
                ).lower() in [
                            "yes",
                            "y"
                        ]



            else:

                print(
                    "Invalid choice. Defaulting to concrete only."
                )

                reinforced = False

                rebar = None

                wire_mesh = False

                vapor_barrier = False

                gravel_base = False

                control_joints = False

                forms = False

                build_type = "Concrete Only"

            estimate = self.estimator.concrete_pad(
                length,
                width,
                thickness,
                reinforced=reinforced,
                rebar=rebar,
                wire_mesh=wire_mesh,
                vapor_barrier=vapor_barrier,
                gravel_base=gravel_base,
                control_joints=control_joints,
                forms=forms
            )

            estimate["build_type"] = build_type

            report = self.reports.create_concrete_pad_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )



        elif intent["type"] == "pier":

            dimensions = self.extractor.extract_dimensions(command)

            diameter = dimensions["diameter"]
            if diameter is None:
                diameter= self.ask_positive_float("Diameter (in): ")

            depth = dimensions["depth"]
            if depth is None:
                depth= self.ask_positive_float("Depth (ft): ")

            quantity = dimensions["quantity"]
            if quantity is None:
                quantity = int(input("Quantity: "))

            choice = self.choose_concrete_package(
                """
        How would you like to build this concrete pier?

        1. Standard pier package
        2. Concrete only
        3. Customize materials

        Choice:
        """
            )

            # Standard Package

            if choice in [
                "1",
                "standard",
                "standard package"
            ]:

                reinforced = True

                rebar = {
                    "status": "plan_required",
                    "source": "approved_structural_plan",
                    "schedule": None
                }

                forms = True

                gravel_base = True

                build_type = "Standard Concrete Pier Package"



            # Concrete Only

            elif choice in [
                "2",
                "concrete",
                "concrete only",
                "none"
            ]:

                reinforced = False

                rebar = None

                forms = False

                gravel_base = False

                build_type = "Concrete Only"



            # Custom

            elif choice in [
                "3",
                "custom",
                "customize"
            ]:

                build_type = "Custom Concrete Pier Package"

                reinforced = input(
                    "Is this pier reinforced? (yes/no): "
                ).lower() in [
                                 "yes",
                                 "y"
                             ]

                rebar = None

                if reinforced:
                    has_schedule = input(
                        "Do you have an approved structural rebar schedule? (yes/no): "
                    ).lower() in ["yes", "y"]

                    if has_schedule:
                        vertical_size = input(
                            "Vertical bar size from approved plan (example: #5): "
                        ).upper()

                        vertical_linear_feet = float(input(
                            "Total vertical rebar linear feet from approved plan: "
                        ))

                        ties_size = input(
                            "Tie bar size from approved plan (example: #3): "
                        ).upper()

                        ties_linear_feet = float(input(
                            "Total tie rebar linear feet from approved plan: "
                        ))

                        vertical_takeoff = self.estimator.calculate_rebar(
                            vertical_size,
                            vertical_linear_feet
                        )

                        ties_takeoff = self.estimator.calculate_rebar(
                            ties_size,
                            ties_linear_feet
                        )

                        rebar = {
                            "status": "specified",
                            "source": "approved_structural_plan",
                            "schedule": {
                                "vertical": {
                                    "bar_size": vertical_size,
                                    "linear_feet": vertical_linear_feet
                                },
                                "ties": {
                                    "bar_size": ties_size,
                                    "linear_feet": ties_linear_feet
                                }
                            },
                            "takeoff": [
                                vertical_takeoff,
                                ties_takeoff
                            ]
                        }

                    else:
                        rebar = {
                            "status": "plan_required",
                            "source": "approved_structural_plan",
                            "schedule": None
                        }

                else:

                    rebar = None

                forms = input(
                    "Include forms? "
                ).lower() in [
                            "yes",
                            "y"
                        ]

                gravel_base = input(
                    "Include gravel base? "
                ).lower() in [
                                  "yes",
                                  "y"
                              ]



            else:

                print(
                    "Invalid choice. Defaulting to concrete only."
                )

                reinforced = False

                rebar = None

                forms = False

                gravel_base = False

                build_type = "Concrete Only"

            estimate = self.estimator.concrete_pier(
                diameter,
                depth,
                quantity,
                reinforced=reinforced,
                rebar=rebar,
                forms=forms,
                gravel_base=gravel_base
            )

            estimate["build_type"] = build_type

            report = self.reports.create_concrete_pier_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )



        elif intent["type"] == "curb":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Length (ft): ")

            width = dimensions["width"]
            if width is None:
                width= self.ask_positive_float("Width (in): ")

            height = dimensions["height"]
            if height is None:
                height= self.ask_positive_float("Height (in): ")

            choice = self.choose_concrete_package(
                """
        How would you like to build this concrete curb?

        1. Standard curb package
        2. Concrete only
        3. Customize materials

        Choice:
        """
            )

            if choice in [
                "1",
                "standard",
                "standard package"
            ]:

                reinforced = True

                rebar = {
                    "status": "plan_required",
                    "source": "approved_structural_plan",
                    "schedule": None
                }

                forms = True

                gravel_base = True

                build_type = "Standard Concrete Curb Package"



            elif choice in [
                "2",
                "concrete",
                "concrete only",
                "none"
            ]:

                reinforced = False

                rebar = None

                forms = False

                gravel_base = False

                build_type = "Concrete Only"



            elif choice in [
                "3",
                "custom",
                "customize"
            ]:

                build_type = "Custom Concrete Curb Package"

                reinforced = input(
                    "Is this curb reinforced? (yes/no): "
                ).lower() in [
                                 "yes",
                                 "y"
                             ]

                rebar = None

                if reinforced:
                    has_schedule = input(
                        "Do you have an approved structural rebar schedule? (yes/no): "
                    ).lower() in ["yes", "y"]

                    if has_schedule:
                        bar_size = self.ask_rebar_size(
                            "Bar size from approved plan: "
                        )

                        linear_feet = self.ask_positive_float(
                            "Total rebar linear feet from approved plan: "
                        )

                        rebar = {
                            "status": "specified",
                            "source": "approved_structural_plan",
                            "schedule": {
                                "main": {
                                    "bar_size": bar_size,
                                    "linear_feet": linear_feet
                                }
                            },
                            "takeoff": [
                                self.estimator.calculate_rebar(
                                    bar_size,
                                    linear_feet
                                )
                            ]
                        }

                    else:
                        rebar = {
                            "status": "plan_required",
                            "source": "approved_structural_plan",
                            "schedule": None
                        }

                else:

                    rebar = None

                forms = input(
                    "Include forms? "
                ).lower() in [
                            "yes",
                            "y"
                        ]

                gravel_base = input(
                    "Include gravel base? "
                ).lower() in [
                                  "yes",
                                  "y"
                              ]



            else:

                reinforced = False
                rebar = None
                forms = False
                gravel_base = False

                build_type = "Concrete Only"

            estimate = self.estimator.concrete_curb(
                length,
                width,
                height,
                reinforced=reinforced,
                rebar=rebar,
                forms=forms,
                gravel_base=gravel_base
            )

            estimate["build_type"] = build_type

            report = self.reports.create_concrete_curb_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )


        elif intent["type"] in [
            "custom flatwork",
            "flatwork"
        ]:

            print(
                "\nCustom flatwork uses measured area and form perimeter "
                "from plans or field layout."
            )

            area_sqft = self.ask_positive_float(
                "Measured area (sq ft): "
            )

            perimeter_lf = self.ask_positive_float(
                "Form perimeter (linear ft): "
            )

            thickness = self.ask_positive_float(
                "Thickness (in): "
            )

            choice = self.choose_concrete_package(
                """
        How would you like to build this custom flatwork?

        1. Standard flatwork package
        2. Concrete only
        3. Customize materials

        Choice:
        """
            )

            if choice in [
                "1",
                "standard",
                "standard package"
            ]:
                reinforced = False
                rebar = None
                wire_mesh = True
                vapor_barrier = False
                gravel_base = True
                control_joints = True
                forms = True
                build_type = "Standard Custom Flatwork Package"

            elif choice in [
                "2",
                "concrete",
                "concrete only",
                "none"
            ]:
                reinforced = False
                rebar = None
                wire_mesh = False
                vapor_barrier = False
                gravel_base = False
                control_joints = False
                forms = False
                build_type = "Concrete Only"

            elif choice in [
                "3",
                "custom",
                "customize"
            ]:
                build_type = "Custom Flatwork Package"

                reinforced = input(
                    "Is this flatwork reinforced? (yes/no): "
                ).lower() in ["yes", "y"]

                rebar = None

                if reinforced:
                    has_schedule = input(
                        "Do you have an approved structural rebar schedule? "
                        "(yes/no): "
                    ).lower() in ["yes", "y"]

                    if has_schedule:
                        direction_1_size = self.ask_rebar_size(
                            "Direction 1 bar size from approved plan: "
                        )

                        direction_1_linear_feet = (
                            self.ask_positive_float(
                                "Total Direction 1 rebar linear feet "
                                "from approved plan: "
                            )
                        )

                        direction_2_size = self.ask_rebar_size(
                            "Direction 2 bar size from approved plan: "
                        )

                        direction_2_linear_feet = (
                            self.ask_positive_float(
                                "Total Direction 2 rebar linear feet "
                                "from approved plan: "
                            )
                        )

                        rebar = {
                            "status": "specified",
                            "source": "approved_structural_plan",
                            "takeoff": [
                                self.estimator.calculate_rebar(
                                    direction_1_size,
                                    direction_1_linear_feet
                                ),
                                self.estimator.calculate_rebar(
                                    direction_2_size,
                                    direction_2_linear_feet
                                )
                            ]
                        }

                    else:
                        rebar = {
                            "status": "plan_required",
                            "source": "approved_structural_plan",
                            "schedule": None
                        }

                wire_mesh = input(
                    "Include wire mesh? "
                ).lower() in ["yes", "y"]

                vapor_barrier = input(
                    "Include vapor barrier? "
                ).lower() in ["yes", "y"]

                gravel_base = input(
                    "Include gravel base? "
                ).lower() in ["yes", "y"]

                control_joints = input(
                    "Include control joints? "
                ).lower() in ["yes", "y"]

                forms = input(
                    "Include forms? "
                ).lower() in ["yes", "y"]

            else:
                print(
                    "Invalid choice. Defaulting to concrete only."
                )

                reinforced = False
                rebar = None
                wire_mesh = False
                vapor_barrier = False
                gravel_base = False
                control_joints = False
                forms = False
                build_type = "Concrete Only"

            estimate = self.estimator.concrete_custom_flatwork(
                area_sqft=area_sqft,
                perimeter_lf=perimeter_lf,
                thickness_inches=thickness,
                reinforced=reinforced,
                rebar=rebar,
                wire_mesh=wire_mesh,
                vapor_barrier=vapor_barrier,
                gravel_base=gravel_base,
                control_joints=control_joints,
                forms=forms,
                build_type=build_type
            )

            report = (
                self.reports.create_custom_concrete_flatwork_report(
                    estimate
                )
            )

            return self.finish_estimate(
                estimate,
                report
            )


        elif intent["type"] == "patio":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Length (ft): ")

            width = dimensions["width"]
            if width is None:
                width= self.ask_positive_float("Width (ft): ")

            thickness = dimensions["thickness"]
            if thickness is None:
                thickness= self.ask_positive_float("Thickness (in): ")

            choice = self.choose_concrete_package(
                """
        How would you like to build this concrete patio?

        1. Standard patio package
        2. Concrete only
        3. Customize materials

        Choice:
        """
            )

            # Standard Patio Package

            if choice in [
                "1",
                "standard",
                "standard package"
            ]:

                reinforced = False

                rebar = None

                wire_mesh = True

                vapor_barrier = False

                gravel_base = True

                control_joints = True

                forms = True

                build_type = "Standard Concrete Patio Package"



            # Concrete Only

            elif choice in [
                "2",
                "concrete",
                "concrete only",
                "none"
            ]:

                reinforced = False

                rebar = None

                wire_mesh = False

                vapor_barrier = False

                gravel_base = False

                control_joints = False

                forms = False

                build_type = "Concrete Only"



            # Custom

            elif choice in [
                "3",
                "custom",
                "customize"
            ]:

                build_type = "Custom Concrete Patio Package"

                last_custom_options = self.memory.recall(
                    "concrete_patio_last_custom_options"
                )

                reuse_last_options = bool(
                    self.reusing_last_concrete_package
                    and last_custom_options
                )

                if reuse_last_options:
                    print("Using the last custom patio assembly.")
                    reinforced = last_custom_options["reinforced"]

                else:
                    reinforced = input(
                        "Is this patio reinforced? (yes/no): "
                    ).lower() in ["yes", "y"]

                rebar = None

                if reinforced:
                    has_schedule = input(
                        "Do you have an approved structural rebar schedule? (yes/no): "
                    ).lower() in ["yes", "y"]

                    if has_schedule:
                        direction_1_size = self.ask_rebar_size(
                            "Direction 1 bar size from approved plan: "
                        )

                        direction_1_linear_feet = self.ask_positive_float(
                            "Total Direction 1 rebar linear feet from approved plan: "
                        )

                        direction_2_size = self.ask_rebar_size(
                            "Direction 2 bar size from approved plan: "
                        )

                        direction_2_linear_feet = self.ask_positive_float(
                            "Total Direction 2 rebar linear feet from approved plan: "
                        )

                        rebar = {
                            "status": "specified",
                            "source": "approved_structural_plan",
                            "schedule": {
                                "direction_1": {
                                    "bar_size": direction_1_size,
                                    "linear_feet": direction_1_linear_feet
                                },
                                "direction_2": {
                                    "bar_size": direction_2_size,
                                    "linear_feet": direction_2_linear_feet
                                }
                            },
                            "takeoff": [
                                self.estimator.calculate_rebar(
                                    direction_1_size,
                                direction_1_linear_feet
                                ),
                                self.estimator.calculate_rebar(
                                    direction_2_size,
                                    direction_2_linear_feet
                                )
                            ]
                        }

                    else:
                        rebar = {
                            "status": "plan_required",
                            "source": "approved_structural_plan",
                            "schedule": None
                        }

                else:

                    rebar = None

                if reuse_last_options:
                    wire_mesh = last_custom_options["wire_mesh"]
                    vapor_barrier = last_custom_options["vapor_barrier"]
                    gravel_base = last_custom_options["gravel_base"]
                    control_joints = last_custom_options["control_joints"]
                    forms = last_custom_options["forms"]

                else:
                    wire_mesh = input(
                        "Include wire mesh? "
                    ).lower() in ["yes", "y"]

                    vapor_barrier = input(
                        "Include vapor barrier? "
                    ).lower() in ["yes", "y"]

                    gravel_base = input(
                        "Include gravel base? "
                    ).lower() in ["yes", "y"]

                    control_joints = input(
                        "Include control joints? "
                    ).lower() in ["yes", "y"]

                    forms = input(
                        "Include forms? "
                    ).lower() in ["yes", "y"]

                    self.memory.remember(
                        "concrete_patio_last_custom_options",
                        {
                            "reinforced": reinforced,
                            "wire_mesh": wire_mesh,
                            "vapor_barrier": vapor_barrier,
                            "gravel_base": gravel_base,
                            "control_joints": control_joints,
                            "forms": forms
                        }
                    )



            else:

                print(
                    "Invalid choice. Defaulting to concrete only."
                )

                reinforced = False

                rebar = None

                wire_mesh = False

                vapor_barrier = False

                gravel_base = False

                control_joints = False

                forms = False

                build_type = "Concrete Only"

            estimate = self.estimator.concrete_patio(
                length,
                width,
                thickness,
                reinforced=reinforced,
                rebar=rebar,
                wire_mesh=wire_mesh,
                vapor_barrier=vapor_barrier,
                gravel_base=gravel_base,
                control_joints=control_joints,
                forms=forms
            )

            estimate["build_type"] = build_type

            report = self.reports.create_concrete_patio_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )

        elif intent["type"] == "sidewalk":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Length (ft): ")

            width = dimensions["width"]
            if width is None:
                width= self.ask_positive_float("Width (ft): ")

            thickness = dimensions["thickness"]
            if thickness is None:
                thickness= self.ask_positive_float("Thickness (in): ")

            choice = self.choose_concrete_package(
                """
        How would you like to build this concrete sidewalk?

        1. Standard sidewalk package
        2. Concrete only
        3. Customize materials

        Choice:
        """
            )

            # Standard Package

            if choice in [
                "1",
                "standard",
                "standard package"
            ]:

                reinforced = False

                rebar = None

                wire_mesh = True

                vapor_barrier = False

                gravel_base = True

                control_joints = True

                forms = True

                build_type = "Standard Concrete Sidewalk Package"



            # Concrete Only

            elif choice in [
                "2",
                "concrete",
                "concrete only",
                "none"
            ]:

                reinforced = False

                rebar = None

                wire_mesh = False

                vapor_barrier = False

                gravel_base = False

                control_joints = False

                forms = False

                build_type = "Concrete Only"



            # Custom

            elif choice in [
                "3",
                "custom",
                "customize"
            ]:

                build_type = "Custom Concrete Sidewalk Package"

                reinforced = input(
                    "Is this sidewalk reinforced? (yes/no): "
                ).lower() in [
                                 "yes",
                                 "y"
                             ]

                rebar = None

                if reinforced:
                    has_schedule = input(
                        "Do you have an approved structural rebar schedule? (yes/no): "
                    ).lower() in ["yes", "y"]

                    if has_schedule:
                        bar_size = self.ask_rebar_size(
                            "Bar size from approved plan: "
                        )

                        linear_feet = self.ask_positive_float(
                            "Total rebar linear feet from approved plan: "
                        )

                        rebar = {
                            "status": "specified",
                            "source": "approved_structural_plan",
                            "schedule": {
                                "main": {
                                    "bar_size": bar_size,
                                    "linear_feet": linear_feet
                                }
                            },
                            "takeoff": [
                                self.estimator.calculate_rebar(
                                    bar_size,
                                    linear_feet
                                )
                            ]
                        }

                    else:
                        rebar = {
                            "status": "plan_required",
                            "source": "approved_structural_plan",
                            "schedule": None
                        }

                else:

                    rebar = None

                wire_mesh = input(
                    "Include wire mesh? "
                ).lower() in [
                                "yes",
                                "y"
                            ]

                vapor_barrier = input(
                    "Include vapor barrier? "
                ).lower() in [
                                    "yes",
                                    "y"
                                ]

                gravel_base = input(
                    "Include gravel base? "
                ).lower() in [
                                  "yes",
                                  "y"
                              ]

                control_joints = input(
                    "Include control joints? "
                ).lower() in [
                                     "yes",
                                     "y"
                                 ]

                forms = input(
                    "Include forms? "
                ).lower() in [
                            "yes",
                            "y"
                        ]



            else:

                print(
                    "Invalid choice. Defaulting to concrete only."
                )

                reinforced = False
                rebar = None
                wire_mesh = False
                vapor_barrier = False
                gravel_base = False
                control_joints = False
                forms = False

                build_type = "Concrete Only"

            estimate = self.estimator.concrete_sidewalk(
                length,
                width,
                thickness,
                reinforced=reinforced,
                rebar=rebar,
                wire_mesh=wire_mesh,
                vapor_barrier=vapor_barrier,
                gravel_base=gravel_base,
                control_joints=control_joints,
                forms=forms
            )

            estimate["build_type"] = build_type

            report = self.reports.create_concrete_sidewalk_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )

        elif intent["type"] == "driveway":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Length (ft): ")

            width = dimensions["width"]
            if width is None:
                width= self.ask_positive_float("Width (ft): ")

            thickness = dimensions["thickness"]
            if thickness is None:
                thickness= self.ask_positive_float("Thickness (in): ")

            choice = self.choose_concrete_package(
                """
        How would you like to build this concrete driveway?

        1. Standard driveway package
        2. Concrete only
        3. Customize materials

        Choice:
        """
            )

            # Standard Driveway Package

            if choice in [
                "1",
                "standard",
                "standard package"
            ]:

                reinforced = True

                rebar = {
                    "status": "plan_required",
                    "source": "approved_structural_plan",
                    "schedule": None
                }

                wire_mesh = False

                vapor_barrier = False

                gravel_base = True

                control_joints = True

                forms = True

                build_type = "Standard Concrete Driveway Package"



            # Concrete Only

            elif choice in [
                "2",
                "concrete",
                "concrete only",
                "none"
            ]:

                reinforced = False

                rebar = None

                wire_mesh = False

                vapor_barrier = False

                gravel_base = False

                control_joints = False

                forms = False

                build_type = "Concrete Only"



            # Custom Package

            elif choice in [
                "3",
                "custom",
                "customize"
            ]:

                build_type = "Custom Concrete Driveway Package"

                reinforced = input(
                    "Is this driveway reinforced? (yes/no): "
                ).lower() in [
                                 "yes",
                                 "y"
                             ]

                rebar = None

                if reinforced:
                    has_schedule = input(
                        "Do you have an approved structural rebar schedule? (yes/no): "
                    ).lower() in ["yes", "y"]

                    if has_schedule:
                        direction_1_size = self.ask_rebar_size(
                            "Direction 1 bar size from approved plan: "
                        )

                        direction_1_linear_feet = self.ask_positive_float(
                            "Total Direction 1 rebar linear feet from approved plan: "
                        )

                        direction_2_size = self.ask_rebar_size(
                            "Direction 2 bar size from approved plan: "
                        )

                        direction_2_linear_feet = self.ask_positive_float(
                            "Total Direction 2 rebar linear feet from approved plan: "
                        )

                        rebar = {
                            "status": "specified",
                            "source": "approved_structural_plan",
                            "schedule": {
                                "direction_1": {
                                    "bar_size": direction_1_size,
                                    "linear_feet": direction_1_linear_feet
                                },
                                "direction_2": {
                                    "bar_size": direction_2_size,
                                    "linear_feet": direction_2_linear_feet
                                }
                            },
                            "takeoff": [
                                self.estimator.calculate_rebar(
                                    direction_1_size,
                                    direction_1_linear_feet
                                ),
                                self.estimator.calculate_rebar(
                                    direction_2_size,
                                    direction_2_linear_feet
                                )
                            ]
                        }

                    else:
                        rebar = {
                            "status": "plan_required",
                            "source": "approved_structural_plan",
                            "schedule": None
                        }

                else:

                    rebar = None

                wire_mesh = input(
                    "Include wire mesh? "
                ).lower() in [
                                "yes",
                                "y"
                            ]

                vapor_barrier = input(
                    "Include vapor barrier? "
                ).lower() in [
                                    "yes",
                                    "y"
                                ]

                gravel_base = input(
                    "Include gravel base? "
                ).lower() in [
                                  "yes",
                                  "y"
                              ]

                control_joints = input(
                    "Include control joints? "
                ).lower() in [
                                     "yes",
                                     "y"
                                 ]

                forms = input(
                    "Include forms? "
                ).lower() in [
                            "yes",
                            "y"
                        ]



            else:

                print(
                    "Invalid choice. Defaulting to concrete only."
                )

                reinforced = False

                rebar = None

                wire_mesh = False

                vapor_barrier = False

                gravel_base = False

                control_joints = False

                forms = False

                build_type = "Concrete Only"

            estimate = self.estimator.concrete_driveway(
                length,
                width,
                thickness,
                reinforced=reinforced,
                rebar=rebar,
                wire_mesh=wire_mesh,
                vapor_barrier=vapor_barrier,
                gravel_base=gravel_base,
                control_joints=control_joints,
                forms=forms
            )

            estimate["build_type"] = build_type

            report = self.reports.create_concrete_driveway_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )


        else:
            return (
                "I’m not set up to estimate that concrete item yet. "
                "Try typing \"help\" to see what I can estimate."
            )

    def handle(self, command, intent):

        command = command.lower().strip()

        if self.pending_project_deletion:
            if command in ["cancel", "never mind", "nevermind"]:
                self.pending_project_deletion = False
                return "Project deletion cancelled."

            self.pending_project_deletion = False
            return self.delete_project_by_name(command)

        if not command:
            return "I didn’t catch that. What would you like me to estimate?"

        words = command.split()
        action = words[0]

        if self.pending_estimate:

            answer = command

            if "wall" in answer:
                old_command = self.pending_estimate["command"]
                self.pending_estimate = None

                return self.drywall_estimate(
                    old_command,
                    {"type": "wall drywall"}
                )

            elif "ceiling" in answer:
                old_command = self.pending_estimate["command"]
                self.pending_estimate = None

                return self.drywall_estimate(
                    old_command,
                    {"type": "ceiling drywall"}
                )

        if action in self.commands:
            return self.commands[action](command)

        if intent["action"] == "estimate":
            return self.estimate_command(command, intent)

        return (
            "I’m not sure how to help with that yet. "
            "Try typing \"help\" to see what I can estimate."
        )

    def lumber_estimate(self, command, intent):

        if intent["type"] == "framed wall with openings":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length = self.ask_positive_float(
                    "Wall length (ft): "
                )

            height = dimensions["height"]
            if height is None:
                height = self.ask_positive_float(
                    "Wall height (ft): "
                )

            quantity = self.ask_positive_int(
                "Number of identical walls: "
            )

            opening_count = self.ask_positive_int(
                "Number of openings in each wall: "
            )

            openings = []

            for number in range(1, opening_count + 1):
                opening_type = input(
                    f"Opening {number} type (door/window): "
                ).strip().lower()

                while opening_type not in [
                    "door",
                    "window"
                ]:
                    print(
                        "Please enter either door or window."
                    )

                    opening_type = input(
                        f"Opening {number} type (door/window): "
                    ).strip().lower()

                opening_width = self.ask_positive_float(
                    f"Opening {number} width (ft): "
                )

                opening_height = self.ask_positive_float(
                    f"Opening {number} height (ft): "
                )

                openings.append(
                    {
                        "type": opening_type,
                        "width_feet": opening_width,
                        "height_feet": opening_height
                    }
                )

            has_header_schedule = input(
                "Do you have an approved header specification "
                "for these openings? (yes/no): "
            ).lower() in ["yes", "y"]

            header_spec = None
            header_plies = None

            if has_header_schedule:
                header_spec = input(
                    "Header size/specification from plan "
                    "(example: 2x10, 2x12, or LVL): "
                ).strip()

                while not header_spec:
                    print(
                        "Please enter the header material from the plan."
                    )

                    header_spec = input(
                        "Header size/specification from plan: "
                    ).strip()

                header_plies = self.ask_positive_int(
                    "Number of header plies from plan: "
                )

            else:
                print(
                    "No problem. I’ll estimate framing, plates, and "
                    "window sills. Header material will remain "
                    "plan-required and will not be added to the "
                    "material takeoff."
                )

            estimate = self.estimator.frame_wall_with_openings(
                length_feet=length,
                height_feet=height,
                openings=openings,
                quantity=quantity,
                header_spec=header_spec,
                header_plies=header_plies
            )

            report = (
                self.reports.create_frame_wall_with_openings_report(
                    estimate
                )
            )

            return self.finish_estimate(
                estimate,
                report
            )


        elif intent["type"] == "framed wall":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Length (ft): ")

            height = dimensions["height"]
            if height is None:
                height= self.ask_positive_float("Height (ft): ")

            quantity = self.ask_positive_int(
                "Number of identical walls: "
            )

            estimate = self.estimator.lumber.frame_wall(
                length,
                height,
                quantity=quantity
            )

            report = self.reports.create_frame_wall_report(estimate)
            return self.finish_estimate(estimate, report)

        elif intent["type"] == "floor joists":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Floor span (ft): ")

            width = dimensions["width"]
            if width is None:
                width= self.ask_positive_float("Floor width (ft): ")

            joist_spec = None

            has_plan = input(
                "Do you have an approved floor-framing plan? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_plan:
                joist_spec = {
                    "size": input(
                        "Joist size from approved plan (example: 2x10): "
                    ),
                    "member_length_feet": float(input(
                        "Joist member length from approved plan (ft): "
                    )),
                    "spacing_inches": float(input(
                        "Joist spacing from approved plan (inches OC): "
                    ))
                }

            estimate = self.estimator.floor_joists(
                length,
                width,
                joist_spec=joist_spec
            )

            report = self.reports.create_floor_joists_report(estimate)
            return self.finish_estimate(estimate, report)

        elif intent["type"] == "ceiling joists":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Ceiling span (ft): ")

            width = dimensions["width"]
            if width is None:
                width= self.ask_positive_float("Ceiling width (ft): ")

            joist_spec = None

            has_plan = input(
                "Do you have an approved ceiling-framing plan? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_plan:
                joist_spec = {
                    "size": input(
                        "Joist size from approved plan (example: 2x8): "
                    ),
                    "member_length_feet": float(input(
                        "Joist member length from approved plan (ft): "
                    )),
                    "spacing_inches": float(input(
                        "Joist spacing from approved plan (inches OC): "
                    ))
                }

            estimate = self.estimator.ceiling_joists(
                length,
                width,
                joist_spec=joist_spec
            )

            report = self.reports.create_ceiling_joists_report(estimate)
            return self.finish_estimate(estimate, report)

        elif intent["type"] == "rafters":

            dimensions = self.extractor.extract_dimensions(command)

            span = dimensions["length"]
            if span is None:
                span= self.ask_positive_float("Roof span (ft): ")

            roof_length= self.ask_positive_float("Roof length (ft): ")

            pitch = dimensions["pitch"]
            if pitch is None:
                pitch= self.ask_positive_float("Roof pitch (example 6): ")

            rafter_spec = None

            has_plan = input(
                "Do you have an approved rafter schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_plan:
                rafter_spec = {
                    "size": input(
                        "Rafter size from approved plan (example: 2x10): "
                    ),
                    "member_length_feet": float(input(
                        "Rafter member length from approved plan (ft): "
                    )),
                    "quantity": int(input(
                        "Total rafter quantity from approved plan: "
                    )),
                    "spacing_inches": float(input(
                        "Rafter spacing from approved plan (inches OC): "
                    ))
                }

            estimate = self.estimator.rafters(
                span,
                roof_length,
                pitch,
                rafter_spec=rafter_spec
            )

            report = self.reports.create_rafter_report(estimate)
            return self.finish_estimate(estimate, report)

        elif intent["type"] == "ridge board":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Ridge length (ft): ")

            ridge_spec = None

            has_plan = input(
                "Do you have an approved ridge-board specification? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_plan:
                ridge_spec = {
                    "size": input(
                        "Ridge-board size from approved plan (example: 2x10): "
                    ),
                    "stock_length_feet": float(input(
                        "Stock length to order (ft): "
                    ))
                }

            estimate = self.estimator.ridge_board(
                length,
                ridge_spec=ridge_spec
            )

            report = self.reports.create_ridge_board_report(estimate)
            return self.finish_estimate(estimate, report)

        elif intent["type"] == "collar ties":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Roof length (ft): ")

            tie_spec = None

            has_plan = input(
                "Do you have an approved collar-tie specification? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_plan:
                tie_spec = {
                    "size": input(
                        "Collar-tie size from approved plan (example: 2x6): "
                    ),
                    "member_length_feet": float(input(
                        "Tie member length from approved plan (ft): "
                    )),
                    "spacing_inches": float(input(
                        "Tie spacing from approved plan (inches OC): "
                    ))
                }

            estimate = self.estimator.collar_ties(
                length,
                tie_spec=tie_spec
            )

            report = self.reports.create_collar_ties_report(estimate)
            return self.finish_estimate(estimate, report)

        elif intent["type"] == "roof sheathing":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            width = dimensions["width"]

            if length is None:
                length = self.ask_positive_float("Building length (ft): ")

            if width is None:
                width = self.ask_positive_float("Building span / width (ft): ")

            roof_type = input(
                "Roof type (gable/shed, press Enter for gable): "
            ).strip().lower() or "gable"

            while roof_type not in ["gable", "shed"]:
                print("Please enter gable or shed.")
                roof_type = input(
                    "Roof type (gable/shed, press Enter for gable): "
                ).strip().lower() or "gable"

            pitch_text = input(
                "Roof pitch rise (example: 6 for 6/12, press Enter for 6): "
            ).strip()
            pitch_rise = float(pitch_text) if pitch_text else 6.0

            while pitch_rise <= 0:
                print("Roof pitch must be greater than zero.")
                pitch_rise = self.ask_positive_float(
                    "Roof pitch rise (example: 6 for 6/12): "
                )

            overhang_text = input(
                "Eave/rake overhang (inches, press Enter for 12): "
            ).strip()
            overhang_inches = float(overhang_text) if overhang_text else 12.0

            while overhang_inches < 0:
                print("Overhang cannot be negative.")
                overhang_inches = float(input(
                    "Eave/rake overhang (inches): "
                ).strip())

            estimate = self.estimator.roof_sheathing(
                length,
                width,
                roof_type=roof_type,
                pitch_rise=pitch_rise,
                overhang_inches=overhang_inches
            )

            report = self.reports.create_roof_sheathing_report(estimate)
            return self.finish_estimate(estimate, report)

        elif intent["type"] == "wall sheathing":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]

            if length is None:
                length= self.ask_positive_float("Wall length (ft): ")

            height = dimensions["height"]

            if height is None:
                height= self.ask_positive_float("Wall height (ft): ")

            estimate = self.estimator.wall_sheathing(
                length,
                height
            )

            report = self.reports.create_wall_sheathing_report(estimate)
            return self.finish_estimate(estimate, report)

        elif intent["type"] == "headers":

            dimensions = self.extractor.extract_dimensions(command)

            width = dimensions["length"]
            if width is None:
                width= self.ask_positive_float("Opening width (ft): ")

            header_spec = None

            has_plan = input(
                "Do you have an approved header schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_plan:
                header_spec = {
                    "size": input(
                        "Header size from approved plan (example: 2x10): "
                    ),
                    "length_feet": float(input(
                        "Header member length from approved plan (ft): "
                    )),
                    "pieces": int(input(
                        "Number of header members from approved plan: "
                    ))
                }

            estimate = self.estimator.headers(
                width,
                header_spec=header_spec
            )

            report = self.reports.create_header_report(estimate)
            return self.finish_estimate(estimate, report)

        elif intent["type"] == "blocking":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]

            if length is None:
                length= self.ask_positive_float("Wall length (ft): ")

            estimate = self.estimator.blocking(
                length
            )

            report = self.reports.create_blocking_report(estimate)
            return self.finish_estimate(estimate, report)

        elif intent["type"] == "plates":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]

            if length is None:
                length= self.ask_positive_float("Wall length (ft): ")

            estimate = self.estimator.plates(
                length
            )

            report = self.reports.create_plates_report(estimate)
            return self.finish_estimate(estimate, report)

        elif intent["type"] == "subfloor sheathing":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Length (ft): ")

            width = dimensions["width"]
            if width is None:
                width= self.ask_positive_float("Width (ft): ")

            estimate = self.estimator.subfloor_sheathing(
                length,
                width
            )

            report = self.reports.create_subfloor_sheathing_report(estimate)
            return self.finish_estimate(estimate, report)

        elif intent["type"] == "rim joists":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Floor length (ft): ")

            width = dimensions["width"]
            if width is None:
                width= self.ask_positive_float("Floor width (ft): ")

            rim_spec = None

            has_plan = input(
                "Do you have an approved rim-joist specification? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_plan:
                rim_spec = {
                    "size": input(
                        "Rim-joist size from approved plan (example: 2x10): "
                    ),
                    "stock_length_feet": float(input(
                        "Stock length to order (ft): "
                    ))
                }

            estimate = self.estimator.rim_joists(
                length,
                width,
                rim_spec=rim_spec
            )

            report = self.reports.create_rim_joists_report(estimate)
            return self.finish_estimate(estimate, report)



        elif intent["type"] in ["stud", "studs"]:

            dimensions = self.extractor.extract_dimensions(command)

            wall_length = dimensions["length"]
            wall_height = dimensions["height"]

            if wall_length is None:
                wall_length= self.ask_positive_float("Wall length (ft): ")

            if wall_height is None:
                wall_height= self.ask_positive_float("Wall height (ft): ")

            estimate = self.estimator.studs(
                wall_length,
                wall_height
            )

            report = self.reports.create_studs_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )

        elif intent["type"] in ["king stud", "king studs"]:

            dimensions = self.extractor.extract_dimensions(command)

            openings = self.extractor.extract_number(command)

            if openings is None:
                openings= self.ask_positive_float("Number of openings: ")

            wall_height = dimensions["height"]

            if wall_height is None:
                wall_height= self.ask_positive_float("Wall height (ft): ")

            estimate = self.estimator.king_studs(
                openings,
                wall_height
            )

            report = self.reports.create_king_studs_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )

        elif intent["type"] in ["jack stud", "jack studs"]:

            openings = self.extractor.extract_number(command)

            if openings is None:
                openings= self.ask_positive_float("Number of openings: ")

            dimensions = self.extractor.extract_dimensions(command)

            opening_height = dimensions["height"]

            if opening_height is None:
                opening_height= self.ask_positive_float("Opening height (ft): ")

            estimate = self.estimator.jack_studs(
                openings,
                opening_height
            )

            report = self.reports.create_jack_studs_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )

        elif intent["type"] in ["cripple stud", "cripple studs"]:

            openings = self.extractor.extract_number(command)

            if openings is None:
                openings= self.ask_positive_float("Number of openings: ")

            dimensions = self.extractor.extract_dimensions(command)

            opening_width = dimensions["width"]

            if opening_width is None:
                opening_width= self.ask_positive_float("Opening width (ft): ")

            estimate = self.estimator.cripple_studs(
                openings,
                opening_width
            )

            report = self.reports.create_cripple_studs_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )

        elif intent["type"] in ["corner post", "corner posts"]:

            corners = self.extractor.extract_number(command)

            if corners is None:
                corners= self.ask_positive_float("Number of corners: ")

            dimensions = self.extractor.extract_dimensions(command)

            wall_height = dimensions["height"]

            if wall_height is None:
                wall_height= self.ask_positive_float("Wall height (ft): ")

            estimate = self.estimator.corner_posts(
                corners,
                wall_height
            )

            report = self.reports.create_corner_posts_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )

        elif intent["type"] in ["top plate", "top plates"]:

            length = self.extractor.extract_number(command)

            if length is None:
                length= self.ask_positive_float("Wall length (ft): ")

            estimate = self.estimator.plates(
                length,
                "top"
            )

            report = self.reports.create_plate_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )


        elif intent["type"] in ["bottom plate", "bottom plates"]:

            length = self.extractor.extract_number(command)

            if length is None:
                length= self.ask_positive_float("Wall length (ft): ")

            estimate = self.estimator.plates(
                length,
                "bottom"
            )

            report = self.reports.create_plate_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )

        elif intent["type"] in ["sill plate", "sill plates"]:

            length = self.extractor.extract_number(command)

            if length is None:
                length= self.ask_positive_float("Foundation length (ft): ")

            estimate = self.estimator.sill_plate(
                length
            )

            report = self.reports.create_sill_plate_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )

        elif intent["type"] == "posts":

            quantity = self.extractor.extract_number(command)

            if quantity is None:
                quantity = int(input("Number of posts: "))
            else:
                quantity = int(quantity)

            dimensions = self.extractor.extract_dimensions(command)

            height = dimensions["height"]
            if height is None:
                height= self.ask_positive_float("Post height (ft): ")

            post_spec = None

            has_plan = input(
                "Do you have an approved post specification? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_plan:
                post_spec = {
                    "size": input(
                        "Post size from approved plan (example: 6x6): "
                    ),
                    "member_length_feet": float(input(
                        "Post member length from approved plan (ft): "
                    ))
                }

            estimate = self.estimator.posts(
                quantity,
                height,
                post_spec=post_spec
            )

            report = self.reports.create_post_report(estimate)

            return self.finish_estimate(
                estimate,
                report
            )

        elif intent["type"] == "beam":

            length = self.extractor.extract_number(command)

            if length is None:
                length= self.ask_positive_float("Beam length (ft): ")

            beam_spec = None

            has_plan = input(
                "Do you have an approved beam schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_plan:
                beam_spec = {
                    "size": input(
                        "Beam size from approved plan (example: 3-2x12): "
                    ),
                    "member_length_feet": float(input(
                        "Beam member length from approved plan (ft): "
                    )),
                    "members": int(input(
                        "Number of beam members from approved plan: "
                    ))
                }

            estimate = self.estimator.beams(
                length,
                beam_spec=beam_spec
            )

            report = self.reports.create_beam_report(estimate)

            return self.finish_estimate(
                estimate,
                report
            )

        else:
            return (
                "I’m not set up to estimate that concrete item yet. "
                "Try typing \"help\" to see what I can estimate."
            )

    def roofing_estimate(self, command, intent):

        if intent["type"] == "shingles":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length = self.ask_positive_float("Building length (ft): ")

            width = dimensions["width"]
            if width is None:
                width = self.ask_positive_float("Building span / width (ft): ")

            roof_type = input(
                "Roof type (gable/shed, press Enter for gable): "
            ).strip().lower() or "gable"

            while roof_type not in ["gable", "shed"]:
                print("Please enter gable or shed.")
                roof_type = input(
                    "Roof type (gable/shed, press Enter for gable): "
                ).strip().lower() or "gable"

            while True:
                pitch_text = input(
                    "Roof pitch rise (example: 6 for 6/12, press Enter for 6): "
                ).strip()
                try:
                    pitch_rise = float(pitch_text) if pitch_text else 6.0
                    if pitch_rise > 0:
                        break
                except ValueError:
                    pass
                print("Enter a positive number, such as 6.")

            while True:
                overhang_text = input(
                    "Eave/rake overhang (inches, press Enter for 12): "
                ).strip()
                try:
                    overhang_inches = (
                        float(overhang_text) if overhang_text else 12.0
                    )
                    if overhang_inches >= 0:
                        break
                except ValueError:
                    pass
                print("Enter zero or a positive number of inches.")

            estimate = self.estimator.roofing.shingles(
                length,
                width,
                roof_type=roof_type,
                pitch_rise=pitch_rise,
                overhang_inches=overhang_inches
            )

            report = self.reports.create_shingle_report(estimate)
            return self.finish_estimate(estimate, report)

        elif intent["type"] == "underlayment":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length = self.ask_positive_float("Building length (ft): ")

            width = dimensions["width"]
            if width is None:
                width = self.ask_positive_float("Building span / width (ft): ")

            roof_type = input(
                "Roof type (gable/shed, press Enter for gable): "
            ).strip().lower() or "gable"

            while roof_type not in ["gable", "shed"]:
                print("Please enter gable or shed.")
                roof_type = input(
                    "Roof type (gable/shed, press Enter for gable): "
                ).strip().lower() or "gable"

            while True:
                pitch_text = input(
                    "Roof pitch rise (example: 6 for 6/12, press Enter for 6): "
                ).strip()
                try:
                    pitch_rise = float(pitch_text) if pitch_text else 6.0
                    if pitch_rise > 0:
                        break
                except ValueError:
                    pass
                print("Enter a positive number, such as 6.")

            while True:
                overhang_text = input(
                    "Eave/rake overhang (inches, press Enter for 12): "
                ).strip()
                try:
                    overhang_inches = (
                        float(overhang_text) if overhang_text else 12.0
                    )
                    if overhang_inches >= 0:
                        break
                except ValueError:
                    pass
                print("Enter zero or a positive number of inches.")

            estimate = self.estimator.roofing.underlayment(
                length,
                width,
                roof_type=roof_type,
                pitch_rise=pitch_rise,
                overhang_inches=overhang_inches
            )

            report = self.reports.create_underlayment_report(estimate)
            return self.finish_estimate(estimate, report)

        elif intent["type"] == "drip edge":

            dimensions = self.extractor.extract_dimensions(command)

            required_length = dimensions["length"]
            if required_length is None:
                required_length = float(input(
                    "Required drip-edge length from roof plan (ft): "
                ))

            estimate = self.estimator.drip_edge(
                required_length
            )

            report = self.reports.create_drip_edge_report(estimate)
            return self.finish_estimate(estimate, report)

        elif intent["type"] == "ice water shield":

            required_coverage = self.extractor.extract_number(command)

            if required_coverage is None:
                required_coverage = float(input(
                    "Required ice & water shield coverage from roof plan (sq ft): "
                ))

            estimate = self.estimator.ice_water_shield(
                required_coverage
            )

            report = self.reports.create_ice_water_report(estimate)
            return self.finish_estimate(estimate, report)

        elif intent["type"] == "ridge vent":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]

            if length is None:
                length= self.ask_positive_float("Length (ft): ")

            estimate = self.estimator.roofing.ridge_vent(
                length
            )

            report = self.reports.create_rideg_vent_report(estimate)
            return self.finish_estimate(estimate, report)

        elif intent["type"] == "flashing":

            quantity = self.extractor.extract_number(command)

            if quantity is None:
                quantity = int(input("Number of flashing locations: "))

            estimate = self.estimator.roofing.flashing(
                quantity
            )

            report = self.reports.create_flashing_report(estimate)
            return self.finish_estimate(estimate, report)

        else:
            return (
                "I’m not set up to estimate that concrete item yet. "
                "Try typing \"help\" to see what I can estimate."
            )

    def create_project_command(self,command):
        parts = command.split(maxsplit=2)

        if len(parts)<3 or parts[1].lower() != "project":
            return "Usage: create project <project name>"

        name = parts[2]

        if self.projects.create_project(name):
            self.projects.select_project(name)
            return f"Project {name} created and selected successfully."
        return f"A project named {name} already exists."

    def drywall_estimate(self, command, intent):

        if intent["type"] == "wall drywall":
            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Wall length (ft): ")

            height = dimensions["height"]
            if height is None:
                height= self.ask_positive_float("Wall height (ft): ")

            quantity = self.ask_positive_int(
                "Number of identical wall sections: "
            )

            estimate = self.estimator.wall_drywall(
                length,
                height,
                quantity=quantity
            )
            report = self.reports.create_wall_drywall_report(estimate)
            return self.finish_estimate(estimate, report)

        elif intent["type"] == "ceiling drywall":
            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Ceiling length (ft): ")

            width = dimensions["width"]
            if width is None:
                width= self.ask_positive_float("Ceiling width (ft): ")

            estimate = self.estimator.ceiling_drywall(length, width)

            report = self.reports.create_ceiling_drywall_report(estimate)
            return self.finish_estimate(estimate, report)

        elif intent["type"] == "drywall":
            self.pending_estimate = {
                "type": "drywall",
                "command": command
            }

            return (
                "Absolutely — are you estimating drywall for a wall "
                "or a ceiling?"
            )

        else:
            return (
                "I’m not set up to estimate that concrete item yet. "
                "Try typing \"help\" to see what I can estimate."
            )
    def insulation_estimate(self, command, intent):

        if intent["type"] in [None, "insulation"]:
            choice = self.ask_required_text(
                "What type of insulation? "
                "(batt, blown, or spray foam): "
            ).lower()

            choice_map = {
                "batt": "batt insulation",
                "batt insulation": "batt insulation",
                "blown": "blown insulation",
                "blown insulation": "blown insulation",
                "spray foam": "spray foam"
            }

            selected_type = choice_map.get(choice)

            if selected_type is None:
                return (
                    "Please choose batt insulation, blown insulation, "
                    "or spray foam."
                )

            intent = {"type": selected_type}

        if intent["type"] == "batt insulation":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Wall length (ft): ")

            height = dimensions["height"]
            if height is None:
                height= self.ask_positive_float("Wall height (ft): ")

            r_value = input(
                "Required insulation R-value from plans (example: R-13): "
            ).strip().upper()

            stud_spacing = float(input(
                "Stud spacing (inches OC, example: 16): "
            ))

            quantity = self.ask_positive_int(
                "Number of identical wall sections: "
            )

            estimate = self.estimator.batt_insulation(
                length,
                height,
                r_value=r_value,
                stud_spacing=stud_spacing,
                quantity = quantity,
            )

            report = self.reports.create_batt_insulation_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] == "blown insulation":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Attic length (ft): ")

            width = dimensions["width"]
            if width is None:
                width= self.ask_positive_float("Attic width (ft): ")

            r_value = input(
                "Required insulation R-value from plans (example: R-38): "
            ).strip().upper()

            estimate = self.estimator.blown_insulation(
                length,
                width,
                r_value=r_value
            )

            report = self.reports.create_blown_insulation_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] == "spray foam":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Wall length (ft): ")

            height = dimensions["height"]
            if height is None:
                height= self.ask_positive_float("Wall height (ft): ")

            thickness_inches = float(input(
                "Required spray-foam thickness (inches): "
            ))

            coverage_per_kit_sqft = float(input(
                "Manufacturer coverage per kit at that thickness (sq ft): "
            ))

            estimate = self.estimator.spray_foam(
                length,
                height,
                thickness_inches,
                coverage_per_kit_sqft
            )

            report = self.reports.create_spray_foam_report(estimate)

            return self.finish_estimate(estimate, report)

        else:
            return (
                "I’m not set up to estimate that concrete item yet. "
                "Try typing \"help\" to see what I can estimate."
            )

    def drywall_finish_estimate(self, command, intent):

        if intent["type"] == "joint compound":
            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Surface length (ft): ")

            width = dimensions["width"]
            if width is None:
                width= self.ask_positive_float("Surface width (ft): ")

            area = length * width

            estimate = self.estimator.joint_compound(area)

            report = self.reports.create_joint_compound_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] == "drywall tape":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Surface length (ft): ")

            width = dimensions["width"]
            if width is None:
                width= self.ask_positive_float("Surface width (ft): ")

            area = length * width

            estimate = self.estimator.drywall_tape(area)

            report = self.reports.create_drywall_tape_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] == "corner bead":

            dimensions = self.extractor.extract_dimensions(command)

            length= self.ask_positive_float("Total outside-corner length (ft): ")

            if length is None:
                length= self.ask_positive_float("Corner Length (ft): ")

            estimate = self.estimator.corner_bead(
                length
            )

            report = self.reports.create_corner_bead_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )

        elif intent["type"] == "drywall screws":

            area = self.extractor.extract_number(command)

            if area is None:
                area= self.ask_positive_float("Drywall area (sq ft): ")

            estimate = self.estimator.drywall_screws(
                area
            )

            report = self.reports.create_drywall_screws_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )

        elif intent["type"] == "drywall sanding":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Surface length (ft): ")

            width = dimensions["width"]
            if width is None:
                width= self.ask_positive_float("Surface width (ft): ")

            area = length * width

            estimate = self.estimator.drywall_sanding(area)

            report = self.reports.create_drywall_sanding_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] in ["drywall primer", "primer"]:

            area = self.extractor.extract_number(command)

            if area is None:
                area= self.ask_positive_float("Surface area to prime (sq ft): ")

            estimate = self.estimator.drywall_primer(area)

            report = self.reports.create_primer_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] in ["drywall texture", "texture"]:

            area = self.extractor.extract_number(command)

            if area is None:
                area= self.ask_positive_float("Surface area to texture (sq ft): ")

            estimate = self.estimator.drywall_texture(area)

            report = self.reports.create_texture_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] == "interior paint":

            area = self.extractor.extract_number(command)

            if area is None:
                area= self.ask_positive_float("Interior wall paint area (sq ft): ")

            estimate = self.estimator.interior_paint(area)

            report = self.reports.create_interior_paint_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] == "ceiling paint":

            area = self.extractor.extract_number(command)

            if area is None:
                area= self.ask_positive_float("Ceiling paint area (sq ft): ")

            estimate = self.estimator.ceiling_paint(area)

            report = self.reports.create_ceiling_paint_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] == "trim paint":

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Total trim length (LF): ")

            face_width_inches = float(input(
                "Trim face width (inches): "
            ))

            estimate = self.estimator.trim_paint(
                length,
                face_width_inches
            )

            report = self.reports.create_trim_paint_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] == "door paint":

            quantity = self.extractor.extract_number(command)

            if quantity is None:
                quantity = int(input("Number of doors: "))

            estimate = self.estimator.door_paint(quantity)

            report = self.reports.create_door_paint_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] == "exterior paint":

            area = self.extractor.extract_number(command)

            if area is None:
                area= self.ask_positive_float("Exterior paint area (sq ft): ")

            estimate = self.estimator.exterior_paint(area)

            report = self.reports.create_exterior_paint_report(estimate)

            return self.finish_estimate(estimate, report)


        else:

            return (

                "I’m not set up to estimate that concrete item yet. "

                "Try typing \"help\" to see what I can estimate."

            )

    def electrical_estimate(self, command, intent):

        if intent["type"] == "outlets":

            dimensions = self.extractor.extract_dimensions(command)

            quantity = dimensions["quantity"]
            if quantity is None:
                quantity = self.ask_positive_int("Number of outlets: ")

            outlet_spec = None

            has_schedule = input(
                "Do you have an approved outlet/device schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                outlet_spec = input(
                    "Outlet specification from approved schedule: "
                ).strip()

            estimate = self.estimator.electrical_outlets(
                quantity,
                outlet_spec=outlet_spec
            )

            report = self.reports.create_outlet_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] == "switches":

            dimensions = self.extractor.extract_dimensions(command)

            quantity = dimensions["quantity"]
            if quantity is None:
                quantity = self.ask_positive_int("Number of switches: ")

            switch_spec = None

            has_schedule = input(
                "Do you have an approved switch/device schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                switch_spec = input(
                    "Switch specification from approved schedule: "
                ).strip()

            estimate = self.estimator.electrical_switches(
                quantity,
                switch_spec=switch_spec
            )

            report = self.reports.create_switch_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] in ["lights", "fixtures", "lighting fixtures"]:

            dimensions = self.extractor.extract_dimensions(command)

            quantity = dimensions["quantity"]
            if quantity is None:
                quantity = self.ask_positive_int("Number of fixtures: ")

            fixture_spec = None

            has_schedule = input(
                "Do you have an approved lighting fixture schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                fixture_spec = input(
                    "Fixture specification from approved schedule: "
                ).strip()

            estimate = self.estimator.electrical_lighting_fixtures(
                quantity,
                fixture_spec=fixture_spec
            )

            report = self.reports.create_lighting_fixture_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] in ["electrical boxes", "boxes"]:

            dimensions = self.extractor.extract_dimensions(command)

            quantity = dimensions["quantity"]
            if quantity is None:
                quantity = self.ask_positive_int("Number of electrical boxes: ")
            box_spec = None

            has_schedule = input(
                "Do you have an approved electrical-box schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                box_spec = input(
                    "Electrical-box specification from approved schedule: "
                ).strip()

            estimate = self.estimator.electrical_boxes(
                quantity,
                box_spec=box_spec
            )

            report = self.reports.create_electrical_box_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] in ["wire", "romex", "electrical cable"]:

            dimensions = self.extractor.extract_dimensions(command)

            length = dimensions["length"]
            if length is None:
                length= self.ask_positive_float("Cable length from approved plan (ft): ")

            wire_type = None

            has_schedule = input(
                "Do you have an approved wire schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                wire_type = input(
                    "Wire/cable specification from approved schedule: "
                ).strip()

            estimate = self.estimator.electrical_romex(
                length,
                wire_type=wire_type
            )

            report = self.reports.create_romex_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] in ["breaker", "breakers"]:

            dimensions = self.extractor.extract_dimensions(command)

            quantity = dimensions["quantity"]
            if quantity is None:
                quantity = self.ask_positive_int("Number of breakers: ")

            breaker_spec = None

            has_schedule = input(
                "Do you have an approved breaker schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                breaker_spec = input(
                    "Breaker specification from approved schedule: "
                ).strip()

            estimate = self.estimator.electrical_breakers(
                quantity,
                breaker_spec=breaker_spec
            )

            report = self.reports.create_breaker_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] == "panel":

            panel_spec = None

            has_schedule = input(
                "Do you have an approved electrical panel schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                panel_spec = input(
                    "Panel specification from approved schedule: "
                ).strip()

            estimate = self.estimator.electrical_panel(
                panel_spec=panel_spec
            )

            report = self.reports.create_panel_report(estimate)

            return self.finish_estimate(estimate, report)


        else:

            return (

                "I’m not set up to estimate that concrete item yet. "

                "Try typing \"help\" to see what I can estimate."

            )

    def plumbing_estimate(self, command, intent):

        if intent["type"] in ["pex", "pex pipe"]:

            length = self.extractor.extract_number(command)

            if length is None:
                length = float(input("PEX pipe length from plan (ft): "))

            pipe_spec = None

            has_schedule = input(
                "Do you have an approved plumbing pipe schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                pipe_spec = input(
                    "PEX pipe specification from approved schedule: "
                ).strip()

            estimate = self.estimator.pex_pipe(
                length,
                pipe_spec=pipe_spec
            )

            report = self.reports.create_pex_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] in ["pvc drain pipe", "drain pipe"]:

            length = self.extractor.extract_number(command)

            if length is None:
                length = float(input("Drain pipe length from plan (ft): "))

            pipe_spec = None

            has_schedule = input(
                "Do you have an approved plumbing pipe schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                pipe_spec = input(
                    "Drain pipe specification from approved schedule: "
                ).strip()

            estimate = self.estimator.pvc_drain_pipe(
                length,
                pipe_spec=pipe_spec
            )

            report = self.reports.create_pvc_drain_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] == "copper pipe":

            length = self.extractor.extract_number(command)

            if length is None:
                length = float(input("Copper pipe length from plan (ft): "))

            pipe_spec = None

            has_schedule = input(
                "Do you have an approved plumbing pipe schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                pipe_spec = input(
                    "Copper pipe specification from approved schedule: "
                ).strip()

            estimate = self.estimator.copper_pipe(
                length,
                pipe_spec=pipe_spec
            )

            report = self.reports.create_copper_pipe_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] == "fittings":

            quantity = self.extractor.extract_number(command)

            if quantity is None:
                quantity = self.ask_positive_int("Number of fittings: ")
            fitting_spec = None

            has_schedule = input(
                "Do you have an approved plumbing fitting schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                fitting_spec = input(
                    "Fitting specification from approved schedule: "
                ).strip()

            estimate = self.estimator.plumbing_fittings(
                quantity,
                fitting_spec=fitting_spec
            )

            report = self.reports.create_fittings_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] in ["valves", "valve", "plumbing valve", "plumbing valves"]:

            quantity = self.extractor.extract_number(command)

            if quantity is None:
                quantity = self.ask_positive_int("Number of valves: ")
            valve_spec = None

            has_schedule = input(
                "Do you have an approved plumbing valve schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                valve_spec = input(
                    "Valve specification from approved schedule: "
                ).strip()

            estimate = self.estimator.plumbing_valve(
                quantity,
                valve_spec=valve_spec
            )

            report = self.reports.create_plumbing_valve_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] in ["toilet", "toilets"]:

            quantity = self.extractor.extract_number(command)

            if quantity is None:
                quantity = self.ask_positive_int("Number of toilets: ")
            fixture_spec = None

            has_schedule = input(
                "Do you have an approved plumbing fixture schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                fixture_spec = input(
                    "Toilet specification from approved schedule: "
                ).strip()

            estimate = self.estimator.toilets(
                quantity,
                fixture_spec=fixture_spec
            )

            report = self.reports.create_toilet_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] in ["sink", "sinks"]:

            quantity = self.extractor.extract_number(command)

            if quantity is None:
                quantity = self.ask_positive_int("Number of sinks: ")
            fixture_spec = None

            has_schedule = input(
                "Do you have an approved plumbing fixture schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                fixture_spec = input(
                    "Sink specification from approved schedule: "
                ).strip()

            estimate = self.estimator.sink(
                quantity,
                fixture_spec=fixture_spec
            )

            report = self.reports.create_sink_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] in ["faucets", "faucet"]:

            quantity = self.extractor.extract_number(command)

            if quantity is None:
                quantity = self.ask_positive_int("Number of faucets: ")
            fixture_spec = None

            has_schedule = input(
                "Do you have an approved plumbing fixture schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                fixture_spec = input(
                    "Faucet specification from approved schedule: "
                ).strip()

            estimate = self.estimator.faucet(
                quantity,
                fixture_spec=fixture_spec
            )

            report = self.reports.create_faucet_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] in [
            "shower/tub", "shower", "showers",
            "tub", "tubs", "bathtub"
        ]:

            quantity = self.extractor.extract_number(command)

            if quantity is None:
                quantity = self.ask_positive_int("Number of showers/tubs: ")
            fixture_spec = None

            has_schedule = input(
                "Do you have an approved plumbing fixture schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                fixture_spec = input(
                    "Shower/tub specification from approved schedule: "
                ).strip()

            estimate = self.estimator.showers_tubs(
                quantity,
                fixture_spec=fixture_spec
            )

            report = self.reports.create_shower_report(estimate)

            return self.finish_estimate(estimate, report)

        elif intent["type"] == "water heater":

            quantity = self.extractor.extract_number(command)

            if quantity is None:
                quantity = self.ask_positive_int("Number of water heaters: ")
            heater_spec = None

            has_schedule = input(
                "Do you have an approved water-heater/MEP schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                heater_spec = input(
                    "Water-heater specification from approved schedule: "
                ).strip()

            estimate = self.estimator.water_heater(
                quantity,
                heater_spec=heater_spec
            )

            report = self.reports.create_water_heater_report(estimate)

            return self.finish_estimate(estimate, report)
        else:
            return (
                "I’m not set up to estimate that concrete item yet. "
                "Try typing \"help\" to see what I can estimate."
            )

    def hvac_estimate(self, command, intent):

        # ---------------- DUCTWORK ----------------

        if intent["type"] == "ductwork":

            length = self.extractor.extract_number(command)

            if length is None:
                length = float(input("Ductwork length from plan (ft): "))

            duct_spec = None

            has_schedule = input(
                "Do you have an approved HVAC duct schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                duct_spec = input(
                    "Duct specification from approved schedule: "
                ).strip()

            estimate = self.estimator.ductwork(
                length,
                duct_spec=duct_spec
            )

            report = self.reports.create_duct_report(estimate)

            return self.finish_estimate(estimate, report)


        # ---------------- REGISTERS ----------------

        elif intent["type"] in ["supply register", "supply registers"]:

            quantity = self.extractor.extract_number(command)

            if quantity is None:
                quantity = self.ask_positive_int("Number of supply registers: ")
            register_spec = None

            has_schedule = input(
                "Do you have an approved HVAC register schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                register_spec = input(
                    "Supply-register specification from approved schedule: "
                ).strip()

            estimate = self.estimator.supply_register(
                quantity,
                register_spec=register_spec
            )

            report = self.reports.create_supply_register_report(estimate)

            return self.finish_estimate(estimate, report)


        # ---------------- RETURN GRILLES ----------------

        elif intent["type"] in ["return grille", "return grilles"]:

            quantity = self.extractor.extract_number(command)

            if quantity is None:
                quantity = self.ask_positive_int("Number of return grilles: ")
            grille_spec = None

            has_schedule = input(
                "Do you have an approved HVAC grille schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                grille_spec = input(
                    "Return-grille specification from approved schedule: "
                ).strip()

            estimate = self.estimator.return_grilles(
                quantity,
                grille_spec=grille_spec
            )

            report = self.reports.create_return_grille_report(estimate)

            return self.finish_estimate(estimate, report)


        # ---------------- FLEX DUCT ----------------

        elif intent["type"] == "flex duct":

            length = self.extractor.extract_number(command)

            if length is None:
                length = float(input("Flex-duct length from plan (ft): "))

            duct_spec = None

            has_schedule = input(
                "Do you have an approved HVAC duct schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                duct_spec = input(
                    "Flex-duct specification from approved schedule: "
                ).strip()

            estimate = self.estimator.flex_duct(
                length,
                duct_spec=duct_spec
            )

            report = self.reports.create_flex_duct_report(estimate)

            return self.finish_estimate(estimate, report)


        # ---------------- THERMOSTAT ----------------

        elif intent["type"] in ["thermostat", "thermostats"]:

            quantity = self.extractor.extract_number(command)

            if quantity is None:
                quantity = self.ask_positive_int("Number of thermostats: ")
            thermostat_spec = None

            has_schedule = input(
                "Do you have an approved HVAC controls schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                thermostat_spec = input(
                    "Thermostat specification from approved schedule: "
                ).strip()

            estimate = self.estimator.thermostat(
                quantity,
                thermostat_spec=thermostat_spec
            )

            report = self.reports.create_thermostat_report(estimate)

            return self.finish_estimate(estimate, report)


        # ---------------- AIR FILTER ----------------

        elif intent["type"] in ["air filter", "air filters"]:

            quantity = self.extractor.extract_number(command)

            if quantity is None:
                quantity = self.ask_positive_int("Number of air filters: ")

            filter_spec = None

            has_schedule = input(
                "Do you have an approved HVAC equipment schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                filter_spec = input(
                    "Air-filter specification from approved schedule: "
                ).strip()

            estimate = self.estimator.air_filters(
                quantity,
                filter_spec=filter_spec
            )

            report = self.reports.create_air_filter_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )


        # ---------------- REFRIGERANT LINE ----------------

        elif intent["type"] in [
            "refrigerant line",
            "refrigerant line set",
            "line set"
        ]:

            length = self.extractor.extract_number(command)

            if length is None:
                length = float(input(
                    "Refrigerant line-set length from plan (ft): "
                ))

            line_set_spec = None

            has_schedule = input(
                "Do you have an approved HVAC line-set schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                line_set_spec = input(
                    "Refrigerant line-set specification from approved schedule: "
                ).strip()

            estimate = self.estimator.refrigerant_line_set(
                length,
                line_set_spec=line_set_spec
            )

            report = self.reports.create_refrigerant_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )


        # ---------------- CONDENSATE DRAIN ----------------

        elif intent["type"] in [
            "condensate drain",
            "condensate"
        ]:

            length = self.extractor.extract_number(command)

            if length is None:
                length = float(input(
                    "Condensate drain length from plan (ft): "
                ))

            drain_spec = None

            has_schedule = input(
                "Do you have an approved condensate-drain specification? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                drain_spec = input(
                    "Condensate drain specification from approved plan: "
                ).strip()

            estimate = self.estimator.condensate_drain(
                length,
                drain_spec=drain_spec
            )

            report = self.reports.create_condensate_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )


        # ---------------- FURNACE ----------------

        elif intent["type"] in [
            "furnace",
            "furnaces"
        ]:

            quantity = self.extractor.extract_number(command)

            if quantity is None:
                quantity = self.ask_positive_int("Number of furnaces: ")

            furnace_spec = None

            has_schedule = input(
                "Do you have an approved HVAC equipment schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                furnace_spec = input(
                    "Furnace specification from approved schedule: "
                ).strip()

            estimate = self.estimator.furnace(
                quantity,
                furnace_spec=furnace_spec
            )

            report = self.reports.create_furnace_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )


        # ---------------- AIR CONDITIONER ----------------

        elif intent["type"] in [
            "air conditioner",
            "air conditioning",
            "ac unit",
            "condenser"
        ]:

            quantity = self.extractor.extract_number(command)

            if quantity is None:
                quantity = self.ask_positive_int("Number of AC Units: ")

            ac_spec = None

            has_schedule = input(
                "Do you have an approved HVAC equipment schedule? (yes/no): "
            ).lower() in ["yes", "y"]

            if has_schedule:
                ac_spec = input(
                    "Air-conditioner specification from approved schedule: "
                ).strip()

            estimate = self.estimator.air_conditioner(
                quantity,
                ac_spec=ac_spec
            )

            report = self.reports.create_ac_report(
                estimate
            )

            return self.finish_estimate(
                estimate,
                report
            )



        else:

            return (

                "I’m not set up to estimate that concrete item yet. "

                "Try typing \"help\" to see what I can estimate."

            )

    def select_project_command(self, command):
        parts = command.split(maxsplit=2)

        if len(parts) < 3 or parts[1].lower() != "project":
            return "Usage: select project <project name>"

        name = parts[2]

        if self.projects.select_project(name):
            project = self.projects.get_active_project()

            return f"Now working on '{project['name']}'."

        return f"I couldn't find a project with the name '{name}'."

    def show_project_command(self, command):
        parts = command.split()

        if len(parts) < 2 or parts[1].lower() not in ["project", "projects"]:
            return "Usage: show project"

        if parts[1].lower() == "projects":
            return self.list_projects_command()

        project = self.projects.get_active_project()

        if project is None:
            return (
                "No project is selected. "
                "Use: select project <project name>"
            )

        estimate_count = len(project["estimates"])
        takeoff = self.projects.get_active_material_takeoff()

        report = (
            f"\nCURRENT PROJECT: {project['name']}\n"
            f"Saved Estimates: {estimate_count}\n"
        )

        if not takeoff:
            return report + "\nNo material takeoffs have been saved yet."

        report += "\nMATERIAL TAKEOFF:\n"

        for item in takeoff:
            quantity = item["quantity"]

            if isinstance(quantity, float) and quantity.is_integer():
                quantity = int(quantity)

            report += (
                f"\n- {item['item']}: "
                f"{quantity} {item['unit']}"
            )

        return report

    def delete_project_command(self, command):
        parts = command.split(maxsplit=2)

        if len(parts) == 2 and parts[1].lower() == "project":
            self.pending_project_deletion = True

            return (
                f"{self.list_projects_command()}\n\n"
                "Which project would you like to delete? "
                "Type its name, or type cancel."
            )

        if len(parts) < 3 or parts[1].lower() != "project":
            return "Usage: delete project <project name>"

        return self.delete_project_by_name(parts[2])

    def open_project_command(self, command):
        parts = command.split(maxsplit=2)

        if len(parts) < 3 or parts[1].lower() not in ["project", "projects"]:
            return "Usage: open project <project name>"

        project_name = parts[2].strip()

        if self.projects.select_project(project_name):
            project = self.projects.get_active_project()

            return (
                f'Opened project: {project["name"]}\n'
                "New estimates will be saved to this project."
            )

        return f'I could not find a project named "{project_name}".'

    def list_projects_command(self):
        projects = self.projects.list_projects()

        if not projects:
            return "No projects found. Use: create project <project name>"

        report = "\nPROJECTS:\n"

        for project in projects:
            active_label = " (ACTIVE)" if project["is_active"] else ""

            report += (
                f"\n- {project['name']}{active_label}"
                f" — {project['estimate_count']} saved estimates"
            )

        return report

    def delete_project_by_name(self, project_name):
        project_name = project_name.strip()

        confirmation = input(
            f'Permanently delete project "{project_name}" and all saved '
            "estimates? Type DELETE to confirm: "
        ).strip()

        if confirmation.upper() != "DELETE":
            return "Project was not deleted."

        if self.projects.delete_project(project_name):
            return f'Project "{project_name}" was deleted.'

        return f'I could not find a project named "{project_name}".'
