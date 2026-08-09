from Intent import IntentDetector


class Brain:
    def __init__(self,memory,commands):
        self.memory=memory
        self.commands=commands
        self.intent_detector=IntentDetector()


    def think(self,command):
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

