import streamlit as st

from EdenWebAdapter import run_eden


st.set_page_config(
    page_title="Chat with Eden",
    layout="wide"
)

st.title("Chat with Eden")
st.caption(
    "This chat uses Eden's existing commands, reports, and projects."
)

if "eden_browser_messages" not in st.session_state:
    st.session_state.eden_browser_messages = [
        {
            "role": "assistant",
            "content": (
                "Hello. What would you like to estimate today?"
            )
        }
    ]

if "eden_pending_command" not in st.session_state:
    st.session_state.eden_pending_command = None

if "eden_pending_answers" not in st.session_state:
    st.session_state.eden_pending_answers = []


def add_message(role, content):
    st.session_state.eden_browser_messages.append(
        {
            "role": role,
            "content": content
        }
    )


def handle_eden_result(command, answers):
    result = run_eden(command, answers)

    if result["kind"] == "question":
        st.session_state.eden_pending_command = command
        st.session_state.eden_pending_answers = answers

        add_message(
            "assistant",
            result["text"]
        )

    elif result["kind"] == "complete":
        st.session_state.eden_pending_command = None
        st.session_state.eden_pending_answers = []

        add_message(
            "assistant",
            result["text"]
        )

    elif result["kind"] == "change":
        st.session_state.eden_pending_command = None
        st.session_state.eden_pending_answers = []

        add_message(
            "assistant",
            f"Okay, switching to: {result['command']}"
        )

        handle_eden_result(
            result["command"],
            []
        )

    else:
        st.session_state.eden_pending_command = None
        st.session_state.eden_pending_answers = []

        add_message(
            "assistant",
            result["text"]
        )


if st.button("Clear Chat"):
    st.session_state.eden_browser_messages = [
        {
            "role": "assistant",
            "content": (
                "Chat cleared. What would you like to estimate?"
            )
        }
    ]

    st.session_state.eden_pending_command = None
    st.session_state.eden_pending_answers = []

    st.rerun()


for message in st.session_state.eden_browser_messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.code(
                message["content"],
                language=None
            )
        else:
            st.write(message["content"])


prompt = st.chat_input(
    "Example: estimate a slab"
)

if prompt:
    add_message(
        "user",
        prompt
    )

    if st.session_state.eden_pending_command:
        command = st.session_state.eden_pending_command

        answers = (
            st.session_state.eden_pending_answers +
            [prompt]
        )

    else:
        command = prompt
        answers = []

    handle_eden_result(
        command,
        answers
    )

    st.rerun()