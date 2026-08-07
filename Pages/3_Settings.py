import streamlit as st

from Settings import Settings
from UserProfile import (
    load_profile,
    save_profile,
    save_avatar
)


st.set_page_config(
    page_title="Settings",
    layout="wide"
)

st.title("Settings")
st.caption(
    "Current estimating defaults from Settings.py."
)

profile = load_profile()

st.subheader("Company Profile")

with st.form("company_profile_form"):
    name = st.text_input(
        "Your name",
        value=profile.get("name", "")
    )

    company = st.text_input(
        "Company name",
        value=profile.get("company", "")
    )

    phone = st.text_input(
        "Phone",
        value=profile.get("phone", "")
    )

    email = st.text_input(
        "Email",
        value=profile.get("email", "")
    )

    address = st.text_area(
        "Business address",
        value=profile.get("address", "")
    )

    uploaded_avatar = st.file_uploader(
        "Upload profile avatar",
        type=["png", "jpg", "jpeg"]
    )

    save_company_profile = st.form_submit_button(
        "Save Company Profile"
    )

if save_company_profile:
    if name.strip() and company.strip():
        save_profile(
            name,
            company,
            phone,
            email,
            address
        )

        if uploaded_avatar:
            saved_avatar = save_avatar(
                uploaded_avatar
            )

            if not saved_avatar:
                st.error(
                    "Please upload a PNG or JPG image."
                )
                st.stop()

        st.success(
            "Company profile and avatar saved successfully."
        )

    else:
        st.error(
            "Your name and company name are required."
        )

st.divider()

all_settings = {}

for setting_name in dir(Settings):
    if setting_name.isupper():
        all_settings[setting_name] = getattr(
            Settings,
            setting_name
        )

categories = {
    "Concrete and Structural": [
        "CONCRETE",
        "REBAR",
        "GRAVEL",
        "FORM"
    ],
    "Lumber and Framing": [
        "LUMBER",
        "STUD",
        "JOIST",
        "RAFTER",
        "BLOCKING",
        "COLLAR"
    ],
    "Roofing": [
        "ROOFING",
        "SHINGLE",
        "UNDERLAYMENT",
        "ICE",
        "DRIP",
        "RIDGE"
    ],
    "Drywall and Paint": [
        "DRYWALL",
        "CORNER",
        "JOINT",
        "TEXTURE",
        "PRIMER",
        "PAINT",
        "DOORS"
    ],
    "Insulation": [
        "INSULATION",
        "BATT",
        "BATTS",
        "BLOWN",
        "SPRAY_FOAM"
    ],
    "Plumbing and HVAC": [
        "PLUMBING",
        "HVAC"
    ]
}

used_settings = set()

for category_name, keywords in categories.items():
    rows = []

    for setting_name, setting_value in all_settings.items():
        if any(
            keyword in setting_name
            for keyword in keywords
        ):
            rows.append(
                {
                    "Setting": setting_name.replace(
                        "_",
                        " "
                    ).title(),
                    "Value": setting_value
                }
            )

            used_settings.add(setting_name)

    if rows:
        with st.expander(category_name, expanded=True):
            st.dataframe(
                rows,
                use_container_width=True,
                hide_index=True
            )

general_rows = []

for setting_name, setting_value in all_settings.items():
    if setting_name not in used_settings:
        general_rows.append(
            {
                "Setting": setting_name.replace(
                    "_",
                    " "
                ).title(),
                "Value": setting_value
            }
        )

if general_rows:
    with st.expander("General", expanded=True):
        st.dataframe(
            general_rows,
            use_container_width=True,
            hide_index=True
        )