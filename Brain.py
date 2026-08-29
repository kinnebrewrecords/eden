import re

from Intent import IntentDetector


class Brain:
    def __init__(self,memory,commands):
        self.memory=memory
        self.commands=commands
        self.intent_detector=IntentDetector()


    def think(self,command):
        normalized_command = command.lower().strip()

        move_estimate_match = re.fullmatch(
            r"(?:move|save)(?:\s+the)?(?:\s+(?:last|latest|most recent))?"
            r"\s+estimate\s+(?:to|in)\s*(?:project\s*)?"
            r"(?:[:=.\-]+\s*)?[\"']?"
            r"(.+?)[\"']?(?:\s+instead)?[.!?]*",
            normalized_command
        )
        wrong_project_match = re.fullmatch(
            r"wrong\s+project[,;:]?\s*(?:move|save)"
            r"(?:\s+(?:it|the\s+last\s+estimate))?"
            r"\s+(?:to|in)\s*(?:project\s*)?"
            r"(?:[:=.\-]+\s*)?[\"']?"
            r"(.+?)[\"']?(?:\s+instead)?[.!?]*",
            normalized_command
        )

        estimate_move = move_estimate_match or wrong_project_match
        if estimate_move:
            destination_name = estimate_move.group(1).strip(" \t\"'.!?")
            return self.commands.move_last_estimate_command(
                destination_name
            )

        waste_match = re.search(
            r"(?:set|change|update)\s+"
            r"(?:(concrete|lumber|framing|roofing|drywall|insulation)\s+)?"
            r"(?:the\s+)?waste(?:\s+(?:allowance|default))?\s+"
            r"(?:to|at)\s+(\d+(?:\.\d+)?)\s*%?",
            normalized_command
        )

        if waste_match:
            trade = waste_match.group(1) or self.memory.recall(
                "last category"
            )
            return self.commands.update_waste_default(
                trade,
                waste_match.group(2)
            )

        if normalized_command in [
                "what can you do",
                "what can eden do",
                "what can you estimate",
                "what do you estimate",
                "show estimate types"
        ]:
            return self.commands.help_command(command)

        if command=="what is my job":
            return self.memory.recall("job")
        if command in ["hello",
                       "hey",
                       "hi",
                       "wassup",
                       "good morning",
                       "good evening",
                       "whats up",
                       "morning",
                       "mornin",
                       "evening",
                       "evenin"
        ]:
            return "How can I help?"
        intent=self.intent_detector.detect(command)

        print(intent)

        if intent.get("action") is None:
            intent["action"]=self.memory.recall("last action")

        if intent.get("category") is None:
            intent["category"]=self.memory.recall("last category")

        response=self.commands.handle(command,intent)

        if intent.get("type"):
            self.memory.remember(
                "last type",
                intent["type"]
            )

        if intent.get("action"):
            self.memory.remember(
                "last action",
                intent["action"],
            )

        if intent.get("category"):
            self.memory.remember(
                "last category",
                intent["category"],
            )

        if response:
            return response

        return "I don't understand yet."

