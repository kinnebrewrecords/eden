import streamlit as st

from EdenWebAdapter import run_eden
from EdenAI import EdenAI
from EdenTheme import apply_eden_theme
import html
from Sidebar import render_sidebar
from AuthGate import require_eden_login


def format_chat_content(content, is_assistant=False):
    """Render estimate reports with hierarchy while escaping all content."""
    text = str(content)
    lines = text.splitlines()
    is_estimate = is_assistant and any(
        line.strip().endswith("ESTIMATE")
        for line in lines
    )

    if not is_estimate:
        return html.escape(text).replace("\n", "<br>")

    rendered_lines = []

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        safe_line = html.escape(line)

        if line.startswith("Review this estimate"):
            css_class = "eden-report-note"
        elif line.endswith("ESTIMATE"):
            css_class = "eden-report-title"
        elif (
                line.rstrip(":").isupper()
                and len(line) <= 50
        ):
            css_class = "eden-report-section"
        elif line.startswith("- "):
            css_class = "eden-report-item"
            safe_line = html.escape(line[2:])
        else:
            css_class = "eden-report-detail"
            if ": " in line:
                label, value = line.split(": ", 1)
                safe_line = (
                    '<span class="eden-report-label">'
                    f'{html.escape(label)}:</span> {html.escape(value)}'
                )

        rendered_lines.append(
            f'<div class="{css_class}">{safe_line}</div>'
        )

    return '<div class="eden-report">' + "".join(rendered_lines) + "</div>"


st.set_page_config(
    page_title="Chat with Eden",
    layout="wide"
)

apply_eden_theme()
require_eden_login()
render_sidebar(
    show_command_center=False
)

st.markdown(
    """
    <style>
    
            .eden-command-deck {
            background: linear-gradient(135deg, #0E1621, #101F31);
            border: 1px solid #2E435E;
            border-radius: 16px;
            box-shadow: 0 0 28px rgba(56, 189, 248, 0.10);
            margin-bottom: 18px;
            padding: 26px;
        }

        .eden-command-deck h1 {
            color: #F8FAFC;
            margin: 4px 0 8px 0;
        }

        .eden-command-deck p {
            color: #AAB7C8;
            margin: 0;
        }

        .eden-system-label {
            color: #38BDF8 !important;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.12em;
        }
    
        .eden-response {
        background: #0B111A;
        border: 1px solid #2E435E;
        border-radius: 10px;
        color: #EAF2FF;
        font-family: "Segoe UI", sans-serif;
        line-height: 1.55;
        padding: 16px;
        white-space: pre-wrap;
        }
    
                [data-testid="stChatMessage"] {
            background: transparent;
            border: none;
            margin-bottom: 8px;
            padding: 0;
        }

                        .eden-bubble {
            backdrop-filter: blur(18px) saturate(140%);
            -webkit-backdrop-filter: blur(18px) saturate(140%);
            border-radius: 18px;
            line-height: 1.55;
            max-width: 82%;
            overflow: hidden;
            padding: 15px 17px;
            position: relative;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            white-space: pre-wrap;
        }

        .eden-bubble::before {
            background: linear-gradient(
                115deg,
                rgba(255, 255, 255, 0.20) 0%,
                rgba(255, 255, 255, 0.06) 18%,
                transparent 42%,
                transparent 74%,
                rgba(56, 189, 248, 0.10) 100%
            );
            content: "";
            inset: 0;
            pointer-events: none;
            position: absolute;
        }

        .eden-bubble:hover {
            box-shadow:
                0 16px 38px rgba(0, 0, 0, 0.38),
                0 0 22px rgba(56, 189, 248, 0.14);
            transform: translateY(-3px);
        }

        .eden-bubble-assistant {
            background: linear-gradient(
                135deg,
                rgba(35, 56, 82, 0.72),
                rgba(10, 17, 28, 0.78)
            );
            border: 1px solid rgba(125, 211, 252, 0.34);
            border-top-left-radius: 4px;
            box-shadow:
                inset 0 1px 0 rgba(255, 255, 255, 0.16),
                0 10px 28px rgba(0, 0, 0, 0.30);
            color: #EAF2FF;
        }

        .eden-bubble-user {
            background: linear-gradient(
                135deg,
                rgba(56, 189, 248, 0.68),
                rgba(14, 116, 144, 0.72)
            );
            border: 1px solid rgba(186, 230, 253, 0.72);
            border-top-right-radius: 4px;
            box-shadow:
                inset 0 1px 0 rgba(255, 255, 255, 0.26),
                0 10px 28px rgba(56, 189, 248, 0.18);
            color: #061019;
            font-weight: 500;
            margin-left: auto;
        }

        .eden-report {
            display: grid;
            gap: 7px;
            white-space: normal;
        }

        .eden-report-note {
            border-left: 3px solid #38BDF8;
            color: #C8D6E8;
            font-size: 0.88rem;
            margin-bottom: 4px;
            padding: 5px 10px;
        }

        .eden-report-title {
            color: #F8FAFC;
            font-size: 1.1rem;
            font-weight: 800;
            letter-spacing: 0.055em;
            padding: 3px 0 7px 0;
        }

        .eden-report-section {
            border-top: 1px solid rgba(125, 211, 252, 0.24);
            color: #7DD3FC;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.09em;
            margin-top: 7px;
            padding-top: 10px;
        }

        .eden-report-detail,
        .eden-report-item {
            background: rgba(7, 15, 25, 0.34);
            border-radius: 8px;
            color: #DCE8F7;
            padding: 7px 10px;
        }

        .eden-report-item {
            border-left: 2px solid rgba(56, 189, 248, 0.62);
        }

        .eden-report-label {
            color: #F8FAFC;
            font-weight: 700;
        }

        [data-testid="stChatInput"] {
            background: #111C2A;
            border: 1px solid #2E435E;
            border-radius: 12px;
        }

        [data-testid="stChatInput"] textarea {
            color: #F8FAFC !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="eden-command-deck">
        <p class="eden-system-label">EDEN // LIVE COMMAND LINK</p>
        <h1>What are we building today?</h1>
        <p>
            Describe the work, answer Eden’s questions, and save the
            resulting estimate to your active project.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption("QUICK COMMANDS")

quick_left, quick_center, quick_right, quick_project = st.columns(4)

with quick_left:
    patio_command = st.button(
        "◈ Estimate Patio",
        use_container_width=True
    )

with quick_center:
    slab_command = st.button(
        "◈ Estimate Slab",
        use_container_width=True
    )

with quick_right:
    wall_command = st.button(
        "◈ Frame a Wall",
        use_container_width=True
    )

with quick_project:
    project_command = st.button(
        "◈ Show Project",
        use_container_width=True
    )

if "eden_browser_messages" not in st.session_state:
    st.session_state.eden_browser_messages = [
        {
            "role": "assistant",
            "content": (
                "Eden online.\n\n"
                "Tell me what you are building in plain language. "
                "I will gather the details, create a material estimate, "
                "and save it to the active project when it is ready.\n\n"
                "Try:\n"
                "• Estimate a 20 by 20 patio, 4 inches thick\n"
                "• Estimate four 20 foot framed walls, 9 feet high\n"
                "• Show project"
            )
        }
    ]

if "eden_pending_command" not in st.session_state:
    st.session_state.eden_pending_command = None

if "eden_pending_answers" not in st.session_state:
    st.session_state.eden_pending_answers = []

if "eden_pending_review" not in st.session_state:
    st.session_state.eden_pending_review = None

def add_message(role, content):
    st.session_state.eden_browser_messages.append(
        {
            "role": role,
            "content": content
        }
    )


def should_try_ai_fallback(result):
    """Use AI only after Eden's deterministic chat cannot understand."""
    return (
        result.get("kind") == "complete" and
        str(result.get("text", "")).strip().lower()
        == "i don't understand yet."
    )


def normalize_with_ai_as_last_resort(command):
    """Make at most one optional AI call for an otherwise unknown request."""
    eden_ai = st.session_state.get("eden_ai")

    if eden_ai is None:
        eden_ai = EdenAI()
        st.session_state.eden_ai = eden_ai

    return eden_ai.normalize_new_request(command)


def handle_eden_result(command, answers):
    result = run_eden(command, answers)

    if not answers and should_try_ai_fallback(result):
        try:
            normalized_command = normalize_with_ai_as_last_resort(command)

            if normalized_command.lower().strip() != command.lower().strip():
                result = run_eden(normalized_command, [])
        except Exception:
            # A missing key, API outage, or exhausted credit never stops
            # Eden's code-based estimator from responding.
            pass

    if result["kind"] == "question":
        if result.get("is_estimate_review"):
            st.session_state.eden_pending_command = None
            st.session_state.eden_pending_answers = []
            st.session_state.eden_pending_review = {
                "command": command,
                "answers": answers,
                "prompts": result.get("answer_prompts", [])
            }
            st.session_state.pop("eden_review_editor", None)

            add_message(
                "assistant",
                result["text"]
            )
            return

        st.session_state.eden_pending_review = None
        st.session_state.eden_pending_command = result.get(
            "resume_command",
            command
        )
        st.session_state.eden_pending_answers = answers

        add_message(
            "assistant",
            result["text"]
        )

    elif result["kind"] == "complete":
        st.session_state.eden_pending_command = None
        st.session_state.eden_pending_answers = []
        st.session_state.eden_pending_review = None

        add_message(
            "assistant",
            result["text"]
        )

    elif result["kind"] == "change":
        st.session_state.eden_pending_command = None
        st.session_state.eden_pending_answers = []
        st.session_state.eden_pending_review = None

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
        st.session_state.eden_pending_review = None

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
    st.session_state.eden_pending_review = None

    st.rerun()


for message in st.session_state.eden_browser_messages:
    avatar = "⚡" if message["role"] == "assistant" else "👤"

    with st.chat_message(
            message["role"],
            avatar=avatar
    ):
        safe_content = format_chat_content(
            message["content"],
            is_assistant=message["role"] == "assistant"
        )

        bubble_class = (
            "eden-bubble-assistant"
            if message["role"] == "assistant"
            else "eden-bubble-user"
        )

        st.markdown(
            f'<div class="eden-bubble {bubble_class}">'
            f'{safe_content}'
            f'</div>',
            unsafe_allow_html=True
        )


review = st.session_state.eden_pending_review

if review:
    st.markdown("### Review estimate details")
    st.caption(
        "Change any entered value below, then recalculate the preview. "
        "Eden will use the revised values for the final saved estimate."
    )

    review_rows = [
        {
            "Detail": prompt.rstrip(": "),
            "Value": answer
        }
        for prompt, answer in zip(
            review["prompts"],
            review["answers"]
        )
    ]

    edited_rows = st.data_editor(
        review_rows,
        disabled=["Detail"],
        hide_index=True,
        key="eden_review_editor",
        use_container_width=True
    )

    if hasattr(edited_rows, "to_dict"):
        edited_rows = edited_rows.to_dict("records")

    edited_answers = [
        str(row.get("Value", "")).strip()
        for row in edited_rows
    ]

    recalculate_col, save_col = st.columns(2)

    with recalculate_col:
        recalculate_preview = st.button(
            "Recalculate Preview",
            use_container_width=True,
            key="eden_recalculate_preview"
        )

    with save_col:
        save_reviewed_estimate = st.button(
            "Save to Project",
            type="primary",
            use_container_width=True,
            key="eden_save_reviewed_estimate"
        )

    if recalculate_preview:
        add_message("user", "Recalculate estimate with revised details")
        handle_eden_result(review["command"], edited_answers)
        st.rerun()

    if save_reviewed_estimate:
        add_message("user", "Save reviewed estimate")
        handle_eden_result(
            review["command"],
            edited_answers + ["yes"]
        )
        st.rerun()


prompt = st.chat_input(
    "Describe work or ask Eden a question..."
)

if patio_command:
    prompt = "estimate a patio"

elif slab_command:
    prompt = "estimate a slab"

elif wall_command:
    prompt = "estimate a framed wall"

elif project_command:
    prompt = "show project"

if prompt:
    add_message(
        "user",
        prompt
    )

    normalized_prompt = prompt.lower().strip()
    project_command_prefixes = (
        "create project",
        "select project",
        "open project",
        "move estimate",
        "move last estimate",
        "move latest estimate",
        "save last estimate",
        "save latest estimate",
        "wrong project",
        "show project",
        "show projects",
        "list projects"
    )

    # Project commands must always start immediately. They should never be
    # mistaken for an answer to a previous estimate question.
    if normalized_prompt.startswith(project_command_prefixes):
        st.session_state.eden_pending_command = None
        st.session_state.eden_pending_answers = []
        command = prompt
        answers = []

    elif st.session_state.eden_pending_command:
        command = st.session_state.eden_pending_command

        answers = (
            st.session_state.eden_pending_answers +
            [prompt]
        )

    else:
        # Normal chat stays calculation-first: Eden's intent detector,
        # parameter extractor, and command handlers receive the exact user
        # request without an AI rewrite or API call. AI is considered only
        # after that code reports it cannot understand the request.
        command = prompt
        answers = []

    handle_eden_result(
        command,
        answers
    )

    st.rerun()
