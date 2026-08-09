from datetime import datetime
from pathlib import Path
from uuid import uuid4


PHOTO_ROOT = Path(__file__).with_name("uploads") / "daily_logs"
ALLOWED_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


def _project_folder_name(project_name):
    safe_name = "".join(
        character if character.isalnum() else "_"
        for character in str(project_name)
    )
    return safe_name.strip("_") or "project"


def save_daily_log_photos(project_name, uploaded_files):
    """Save uploaded field photos locally and return JSON-safe metadata."""
    project_folder = PHOTO_ROOT / _project_folder_name(project_name)
    project_folder.mkdir(parents=True, exist_ok=True)
    photos = []

    for uploaded_file in uploaded_files or []:
        original_name = Path(uploaded_file.name).name
        suffix = Path(original_name).suffix.lower()

        if suffix not in ALLOWED_SUFFIXES:
            continue

        stored_name = f"{uuid4().hex}{suffix}"
        destination = project_folder / stored_name
        destination.write_bytes(uploaded_file.getvalue())
        photos.append(
            {
                "path": str(destination.relative_to(Path(__file__).parent)),
                "name": original_name,
                "uploaded_at": datetime.now().isoformat(
                    timespec="seconds"
                )
            }
        )

    return photos


def get_daily_log_photo_path(photo):
    relative_path = Path(photo.get("path", ""))
    resolved_path = (Path(__file__).parent / relative_path).resolve()

    try:
        resolved_path.relative_to(PHOTO_ROOT.resolve())
    except ValueError:
        return None

    return resolved_path if resolved_path.exists() else None
