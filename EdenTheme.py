import streamlit as st


def apply_eden_theme():
    st.markdown(
        """
        <style>
            :root {
                --eden-bg: #101114;
                --eden-panel: #0D1520;
                --eden-panel-strong: #111C2A;
                --eden-border: #243852;
                --eden-text: #F4F8FC;
                --eden-muted: #8EA0B7;
                --eden-blue: #38BDF8;
                --eden-blue-soft: #7DD3FC;
            }

            .stApp {
                background:
                    radial-gradient(ellipse 52% 38% at 92% -8%, rgba(180, 190, 202, 0.20), transparent 62%),
                    radial-gradient(circle at 10% 22%, rgba(56, 61, 70, 0.13), transparent 31%),
                    var(--eden-bg);
            }

            [data-testid="stMainBlockContainer"],
            .block-container {
                max-width: 1480px;
                padding-top: 3.1rem;
                padding-bottom: 4rem;
            }

            [data-testid="stHeader"],
            [data-testid="stAppHeader"] {
                background: rgba(16, 17, 20, 0.96);
                border-bottom: 1px solid rgba(36, 56, 82, 0.55);
            }

            [data-testid="stDecoration"] {
                background: #38BDF8;
            }

            [data-testid="stSidebar"] {
                background: #000000;
                border-right: 1px solid var(--eden-border);
            }

            /* Eden supplies its own organized Workspace navigation. */
            [data-testid="stSidebarNav"] {
                display: none;
            }

            [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
                padding-top: 1.15rem;
            }

            div[data-baseweb="input"],
            div[data-baseweb="input"] > div,
            div[data-baseweb="select"] > div,
            [data-testid="stTextInput"] input,
            [data-testid="stNumberInput"] input,
            [data-testid="stTextArea"] textarea {
                background: #111C2A !important;
                color: #F8FAFC !important;
                border-color: #2E435E !important;
            }

            [data-testid="stTextInput"] input,
            [data-testid="stNumberInput"] input,
            [data-testid="stTextArea"] textarea,
            [data-baseweb="select"] input {
                color: #F8FAFC !important;
                caret-color: #38BDF8;
            }

            [data-testid="stExpander"] {
                background: rgba(14, 22, 33, 0.82);
                border: 1px solid var(--eden-border);
                border-radius: 14px;
                overflow: hidden;
            }

            .eden-tour {
                margin: 1.8rem 0 1rem;
                padding: 1.45rem 1.6rem;
                background: linear-gradient(135deg, rgba(21, 34, 50, 0.88), rgba(13, 21, 32, 0.68));
                border: 1px solid rgba(125, 211, 252, 0.34);
                border-radius: 18px;
                box-shadow: 0 12px 30px rgba(0, 0, 0, 0.22);
            }

            .eden-tour h2 {
                margin: 0.2rem 0 0.35rem;
                color: var(--eden-text);
            }

            .eden-tour p {
                color: var(--eden-muted);
                max-width: 760px;
                margin: 0;
            }

            .eden-tour-kicker {
                color: var(--eden-blue-soft) !important;
                font-size: 0.72rem;
                font-weight: 800;
                letter-spacing: 0.14em;
            }

            .eden-tour-card {
                min-height: 178px;
                margin-top: 0.75rem;
                padding: 1.15rem;
                background: rgba(13, 21, 32, 0.78);
                border: 1px solid rgba(36, 56, 82, 0.95);
                border-radius: 14px;
            }

            .eden-tour-card-start {
                border-color: rgba(56, 189, 248, 0.7);
                box-shadow: 0 0 22px rgba(56, 189, 248, 0.12);
            }

            .eden-tour-card h3 {
                margin: 0.8rem 0 0.45rem;
                font-size: 1rem;
            }

            .eden-tour-card p {
                color: var(--eden-muted);
                font-size: 0.86rem;
                line-height: 1.5;
            }

            .eden-tour-number {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 27px;
                height: 27px;
                border-radius: 50%;
                background: rgba(56, 189, 248, 0.15);
                border: 1px solid rgba(56, 189, 248, 0.62);
                color: var(--eden-blue-soft);
                font-weight: 800;
            }

            .eden-tour-arrow {
                color: var(--eden-blue-soft);
                font-size: 1.2rem;
                font-weight: 800;
            }

            [data-testid="stAppViewContainer"] h1,
            [data-testid="stAppViewContainer"] h2,
            [data-testid="stAppViewContainer"] h3 {
                color: #F8FAFC !important;
            }

            [data-testid="stAppViewContainer"] p,
            [data-testid="stAppViewContainer"] label,
            [data-testid="stAppViewContainer"] .stCaption {
                color: #AAB7C8 !important;
            }

            [data-testid="stSidebar"] * {
                color: #D6E1ED;
            }

            [data-testid="stMetric"] {
                background: linear-gradient(145deg, rgba(18, 30, 45, 0.96), rgba(10, 17, 27, 0.96));
                border: 1px solid var(--eden-border);
                border-radius: 16px;
                padding: 18px;
                box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.035);
            }

            [data-testid="stMetricLabel"] {
                color: var(--eden-muted) !important;
                font-size: 0.78rem;
                font-weight: 700;
                letter-spacing: 0.06em;
                text-transform: uppercase;
            }

            [data-testid="stMetricValue"] {
                color: var(--eden-text) !important;
            }

            div.stButton > button,
            div.stFormSubmitButton > button {
                background: linear-gradient(135deg, #38BDF8, #22A5E3);
                color: #061019;
                border: none;
                border-radius: 10px;
                font-weight: 700;
                min-height: 2.55rem;
                box-shadow: 0 8px 18px rgba(56, 189, 248, 0.16);
            }

            div.stButton > button:hover,
            div.stFormSubmitButton > button:hover {
                background: #7DD3FC;
                color: #061019;
            }

            div.stButton > button *,
            div.stFormSubmitButton > button * {
                color: #061019 !important;
            }

            [data-testid="stDataFrame"],
            [data-testid="stPlotlyChart"],
            [data-testid="stVegaLiteChart"],
            [data-testid="stAltairChart"] {
                background: rgba(14, 22, 33, 0.84);
                border: 1px solid var(--eden-border);
                border-radius: 14px;
                padding: 6px;
                box-shadow: 0 14px 35px rgba(0, 0, 0, 0.16);
                overflow: hidden;
            }

            div[data-baseweb="tab-list"] {
                gap: 0.45rem;
                border-bottom: 1px solid var(--eden-border) !important;
            }

            button[data-baseweb="tab"] {
                border-radius: 9px 9px 0 0;
                color: var(--eden-muted) !important;
                font-weight: 700;
            }

            button[data-baseweb="tab"][aria-selected="true"] {
                color: var(--eden-blue-soft) !important;
                background: rgba(56, 189, 248, 0.09);
            }

            [data-testid="stSidebar"] a {
                border-radius: 9px;
                margin: 0.08rem 0;
                transition: background 120ms ease;
            }

            [data-testid="stSidebar"] a:hover {
                background: rgba(56, 189, 248, 0.10);
            }

            .eden-sidebar-kicker {
                color: var(--eden-blue) !important;
                font-size: 0.68rem;
                font-weight: 800;
                letter-spacing: 0.16em;
                margin-bottom: 0.15rem;
            }

            .eden-sidebar-title {
                color: var(--eden-text) !important;
                font-size: 1.25rem;
                font-weight: 800;
                letter-spacing: 0.08em;
                margin: 0 0 1.1rem 0;
            }

            .eden-welcome-bubble {
                position: relative;
                overflow: hidden;
                text-align: center;
                background:
                    linear-gradient(125deg, rgba(93, 128, 155, 0.26), rgba(25, 36, 48, 0.62) 46%, rgba(13, 18, 25, 0.70));
                border: 1px solid rgba(164, 215, 246, 0.44);
                border-radius: 24px;
                min-height: 220px;
                padding: 2.45rem 2.7rem;
                backdrop-filter: blur(18px) saturate(128%);
                -webkit-backdrop-filter: blur(18px) saturate(128%);
                box-shadow: 0 22px 52px rgba(0, 0, 0, 0.34),
                    0 0 28px rgba(96, 191, 245, 0.12),
                    inset 0 1px 0 rgba(255, 255, 255, 0.18),
                    inset 0 -1px 0 rgba(255, 255, 255, 0.04);
            }

            .eden-welcome-bubble::before {
                content: "";
                position: absolute;
                inset: 0;
                pointer-events: none;
                background: linear-gradient(112deg, rgba(255, 255, 255, 0.15), transparent 29%, transparent 70%, rgba(94, 207, 255, 0.07));
            }

            .eden-welcome-bubble > * {
                position: relative;
                z-index: 1;
            }

            .eden-welcome-kicker {
                color: var(--eden-blue) !important;
                font-size: 0.88rem;
                font-weight: 800;
                letter-spacing: 0.11em;
                text-transform: uppercase;
                margin: 0 0 0.3rem 0;
            }

            .eden-welcome-title {
                color: var(--eden-text) !important;
                font-size: clamp(3.3rem, 5.5vw, 5.6rem) !important;
                font-weight: 850;
                line-height: 0.98;
                margin: 0;
                letter-spacing: -0.045em;
                text-shadow: 0 3px 18px rgba(0, 0, 0, 0.30);
            }

            .eden-welcome-company {
                color: var(--eden-muted) !important;
                font-size: 1.12rem;
                margin: 0.45rem 0 0 0;
            }


            .eden-welcome-stage {
                position: relative;
                min-height: 310px;
                display: flex;
                align-items: center;
                padding: 1rem 0;
            }

            .eden-hero {
                position: relative;
                overflow: hidden;
                z-index: 2;
                background:
                    linear-gradient(120deg, rgba(18, 37, 57, 0.96), rgba(11, 19, 31, 0.96));
                border: 1px solid rgba(70, 124, 171, 0.52);
                border-radius: 20px;
                padding: 1.65rem 1.85rem;
                margin: 0.25rem 0 1.15rem 0;
                width: 100%;
                box-shadow: 0 20px 45px rgba(0, 0, 0, 0.20);
            }

            .eden-hero::after {
                content: "";
                position: absolute;
                width: 240px;
                height: 240px;
                border-radius: 50%;
                background: rgba(56, 189, 248, 0.10);
                right: -85px;
                top: -135px;
            }

            .eden-hero-content {
                position: relative;
                z-index: 2;
            }

            .eden-user-mark {
                position: absolute;
                z-index: 1;
                width: min(330px, 32vw);
                height: min(330px, 32vw);
                object-fit: cover;
                left: 0;
                top: 50%;
                transform: translateY(-50%);
                opacity: 0.48;
                border-radius: 28px;
                filter: saturate(0.9) contrast(1.08);
                box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.12);
            }

            .eden-hero-kicker {
                color: var(--eden-blue) !important;
                font-size: 0.74rem;
                font-weight: 800;
                letter-spacing: 0.13em;
                text-transform: uppercase;
                margin: 0 0 0.45rem 0;
            }

            .eden-hero h1 {
                color: var(--eden-text) !important;
                font-size: clamp(2rem, 3.1vw, 3.1rem) !important;
                line-height: 1.05 !important;
                margin: 0 !important;
            }

            .eden-hero-subtitle {
                color: var(--eden-muted) !important;
                font-size: 1rem;
                margin: 0.65rem 0 0 0;
            }

            @media (max-width: 700px) {
                .eden-welcome-stage {
                    min-height: 230px;
                }

                .eden-user-mark {
                    opacity: 0.18;
                    left: 0.65rem;
                    width: 150px;
                    height: 150px;
                }

            }

            .eden-project-bar {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                background: rgba(22, 62, 55, 0.54);
                border: 1px solid rgba(52, 211, 153, 0.32);
                border-radius: 14px;
                padding: 0.85rem 1rem;
                margin: 0.9rem 0 1.35rem 0;
            }

            .eden-project-label {
                color: #93E5C2 !important;
                font-size: 0.7rem;
                font-weight: 800;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                margin-bottom: 0.18rem;
            }

            .eden-project-name {
                color: var(--eden-text) !important;
                font-size: 1.05rem;
                font-weight: 750;
            }

            .eden-status-pill {
                color: #BCEAD5 !important;
                background: rgba(16, 95, 69, 0.45);
                border: 1px solid rgba(110, 231, 183, 0.25);
                border-radius: 999px;
                padding: 0.35rem 0.68rem;
                font-size: 0.76rem;
                font-weight: 700;
                white-space: nowrap;
            }

            .eden-feature-card {
                height: 100%;
                background: linear-gradient(145deg, rgba(18, 38, 58, 0.94), rgba(12, 21, 33, 0.94));
                border: 1px solid rgba(56, 189, 248, 0.38);
                border-radius: 16px;
                padding: 1.25rem;
                box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04), 0 14px 28px rgba(0, 0, 0, 0.14);
            }

            .eden-feature-label {
                color: var(--eden-blue) !important;
                font-size: 0.7rem;
                font-weight: 800;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                margin: 0 0 0.35rem 0;
            }

            .eden-feature-title {
                color: var(--eden-text) !important;
                font-size: 1.2rem;
                font-weight: 800;
                margin: 0 0 0.42rem 0;
            }

            .eden-feature-copy {
                color: var(--eden-muted) !important;
                line-height: 1.55;
                margin: 0;
            }

            .eden-splash {
                position: fixed;
                z-index: 999999;
                inset: 0;
                width: 100vw;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                background: #000000;
                padding: 2rem;
            }

            .eden-splash-logo {
                display: block;
                width: min(1120px, 94vw);
                max-height: 72vh;
                object-fit: contain;
                margin: 0 auto;
                border: none;
                border-radius: 0;
                box-shadow: none;
            }

            .eden-splash-tagline {
                color: #FFFFFF !important;
                font-size: 0.95rem;
                font-weight: 800;
                letter-spacing: 0.16em;
                text-transform: uppercase;
                margin: 0.9rem 0 0 0;
            }

            .eden-splash-loading {
                color: var(--eden-muted) !important;
                font-size: 0.82rem;
                font-weight: 700;
                letter-spacing: 0.12em;
                text-transform: uppercase;
            }

            .eden-splash-loading::after {
                content: "";
                display: inline-block;
                width: 1.5em;
                animation: eden-loading-dots 1.2s steps(4, end) infinite;
            }

            @keyframes eden-loading-dots {
                0% { content: ""; }
                25% { content: "."; }
                50% { content: ".."; }
                75%, 100% { content: "..."; }
            }

            hr {
                border-color: var(--eden-border);
            }
        </style>
        """,
        unsafe_allow_html=True
    )
