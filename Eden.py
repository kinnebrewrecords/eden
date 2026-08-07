from Memory import Memory
from Estimating import Estimator
from Reports import ReportGenerator
from Commands import CommandHandler
from Brain import Brain
from ProjectManager import ProjectManager
from Commands import EstimateChange

class Eden:
    def __init__(self):
        self.name = "Eden"
        self.memory=Memory()
        self.estimator=Estimator()
        self.reports=ReportGenerator()
        self.projects=ProjectManager()
        self.commands = CommandHandler(
            self.memory,
            self.estimator,
            self.reports,
            self.projects,
        )
        self.brain=Brain(self.memory,self.commands)
        self.status = "Online"
        self.personality="Professional assistant"
        self.version="0.1"


        print("Eden Online")

    def show_first_run_guide(self):
            if self.memory.recall("eden_welcome_guide_shown"):
                print(
                    "Welcome back to Eden. "
                    "What would you like to estimate today?"
                )
                return

            print("""
    Welcome to Eden E.

    I help you create material estimates and save them to projects.

    Start with:
    1. create project <project name>
    2. select project <project name>
    3. estimate a 20 x 20 slab, 6 inches thick
    4. show project

    Helpful commands:
    - help
    - cancel
    - delete project <project name>
    - exit

    While entering a measurement, you can type:
    - cancel
    - change to <estimate type>

    Let’s build your first estimate.
            """)

            self.memory.remember("eden_welcome_guide_shown", True)

    def introduce(self):
        print(f"Hello, my name is {self.name} What can I assist you with today?")

    def check_status(self):
        print(f"EDEN STATUS: {self.status}")

    def start(self):
        self.show_first_run_guide()

        while self.status == "Online":
            command = input("You: ").strip()

            if command.lower() == "exit":
                print("Thank you for using Eden.")
                self.status = "Offline"
                continue

            if not command:
                continue

            while command:
                try:
                    response = self.brain.think(command)

                except EstimateChange as change:
                    if change.new_command:
                        print(
                            f"Okay, switching to: {change.new_command}"
                        )
                        command = change.new_command
                        continue

                    print(
                        "No problem. I cancelled that estimate. "
                        "What would you like to estimate instead?"
                    )
                    break

                print(response)
                break



    def system_info(self):
        print(f"EDEN VERSION: {self.version}")
        print(f"EDEN STATUS: {self.status}")