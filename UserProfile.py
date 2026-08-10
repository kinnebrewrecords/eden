import json
from pathlib import Path

from WorkspaceFiles import workspace_file


def _profile_file():
    return workspace_file(__file__, "user_profile.json")

upload_folder = Path(__file__).with_name(
    "uploads"
)


def load_profile():
    profile_file = _profile_file()

    if not profile_file.exists():
        return {}

    with open(profile_file, "r") as file:
        return json.load(file)


def save_profile(
        name,
        company,
        phone="",
        email="",
        address="",
        default_region="",
        preferred_supplier="",
        pricing_setup_choice=""
):
    profile_file = _profile_file()
    existing_profile = load_profile()

    profile = {
        "name": name.strip(),
        "company": company.strip(),
        "phone": phone.strip(),
        "email": email.strip(),
        "address": address.strip(),
        "default_region": default_region.strip(),
        "preferred_supplier": preferred_supplier.strip(),
        "pricing_setup_choice": (
            pricing_setup_choice.strip()
            or existing_profile.get("pricing_setup_choice", "")
        ),
        "avatar_path": existing_profile.get(
            "avatar_path",
            ""
        ),
        "onboarding_complete": existing_profile.get(
            "onboarding_complete",
            False
        )
    }

    with open(profile_file, "w") as file:
        json.dump(
            profile,
            file,
            indent=4
        )

    return profile


def complete_onboarding():
    profile_file = _profile_file()
    profile = load_profile()

    profile["onboarding_complete"] = True

    with open(profile_file, "w") as file:
        json.dump(
            profile,
            file,
            indent=4
        )


def save_avatar(uploaded_file):
    upload_folder.mkdir(exist_ok=True)

    file_extension = Path(
        uploaded_file.name
    ).suffix.lower()

    if file_extension not in [
        ".png",
        ".jpg",
        ".jpeg"
    ]:
        return False

    avatar_file = upload_folder / (
        f"profile_avatar{file_extension}"
    )

    with open(avatar_file, "wb") as file:
        file.write(uploaded_file.getbuffer())

    profile_file = _profile_file()
    profile = load_profile()

    profile["avatar_path"] = str(
        Path("uploads") / avatar_file.name
    )

    with open(profile_file, "w") as file:
        json.dump(
            profile,
            file,
            indent=4
        )

    return True
