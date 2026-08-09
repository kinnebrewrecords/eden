import json
import os


class Memory:

    def __init__(self):
        self.data = {}
        self.load()


    def remember(self, key, value):
        self.data[key] = value
        self.save()


    def recall(self, key):
        return self.data.get(key)


    def set(self, key, value):
        self.remember(key, value)


    def save(self):
        with open("memory_backup.json", "w") as f:
            json.dump(self.data, f, indent=4)


    def load(self):
        if os.path.exists("memory_backup.json"):
            with open("memory_backup.json", "r") as f:
                self.data = json.load(f)


    def forget(self, key):
        if key in self.data:
            del self.data[key]
            self.save()
            return True

        return False



class ProjectMemory:

    def __init__(self):

        self.preferences = {}

        self.load()


    def save_preference(
            self,
            category,
            item,
            settings
    ):

        if category not in self.preferences:
            self.preferences[category] = {}


        self.preferences[category][item] = settings

        self.save()



    def get_preference(
            self,
            category,
            item
    ):

        return self.preferences.get(
            category,
            {}
        ).get(item)

    def save_last_package_choice(self, category, choice):
        choice = str(choice)

        if choice not in ["1", "2", "3"]:
            raise ValueError("Package choice must be 1, 2, or 3")

        self.save_preference(
            category,
            "last_package_choice",
            choice
        )

    def get_last_package_choice(self, category):
        return self.get_preference(
            category,
            "last_package_choice"
        )

    def save(self):

        with open("project_memory.json", "w") as f:
            json.dump(
                self.preferences,
                f,
                indent=4
            )



    def load(self):

        if os.path.exists("project_memory.json"):

            with open("project_memory.json", "r") as f:

                self.preferences = json.load(f)