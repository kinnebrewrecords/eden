from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from Commands import EstimateChange
from Eden import Eden


class EdenQuestion(Exception):
    pass


eden = Eden()


def create_browser_input(answers):
    position = 0

    def browser_input(prompt=""):
        nonlocal position

        if position >= len(answers):
            raise EdenQuestion(prompt)

        answer = str(answers[position]).strip()
        position += 1

        lower_answer = answer.lower()

        if lower_answer in [
            "cancel",
            "start over",
            "never mind",
            "nevermind"
        ]:
            raise EstimateChange()

        if lower_answer.startswith("change to "):
            new_item = answer[10:].strip()

            if new_item:
                raise EstimateChange(f"estimate {new_item}")

        return answer

    return browser_input


def useful_messages(output):
    messages = []

    for line in output.splitlines():
        line = line.strip()

        if not line or line.startswith("{"):
            continue

        messages.append(line)

    return "\n".join(messages)


def run_eden(command, answers=None):
    if answers is None:
        answers = []

    browser_input = create_browser_input(answers)
    terminal_output = StringIO()

    try:
        with redirect_stdout(terminal_output):
            with patch("builtins.input", browser_input):
                response = eden.brain.think(command)

        return {
            "kind": "complete",
            "text": response
        }

    except EdenQuestion as question:
        messages = useful_messages(terminal_output.getvalue())
        prompt = str(question).strip()

        if messages and prompt:
            text = f"{messages}\n\n{prompt}"
        else:
            text = messages or prompt

        return {
            "kind": "question",
            "text": text
        }

    except EstimateChange as change:
        if change.new_command:
            return {
                "kind": "change",
                "command": change.new_command
            }

        return {
            "kind": "cancelled",
            "text": (
                "No problem. I cancelled that estimate. "
                "What would you like to estimate instead?"
            )
        }

    except Exception as error:
        return {
            "kind": "error",
            "text": f"Eden could not complete that request: {error}"
        }