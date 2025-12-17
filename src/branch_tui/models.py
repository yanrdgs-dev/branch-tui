import re
import unicodedata


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lower()

    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text).strip("-")
    return text


def format_branch_name(label: str, number: int, title: str) -> str:
    mapping = {
        "bug": "fix",
        "enhancement": "feat",
        "feature": "feat",
        "documentation": "docs",
        "refactor": "refactor",
        "chore": "chore",
    }

    prefix = mapping.get(label.lower(), "issue")

    clean_title = slugify(title)

    return f"{prefix}/{number}-{clean_title}"
