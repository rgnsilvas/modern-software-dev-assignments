import re

_ACTION_RE = re.compile(r"^(must|need to|should)\b", re.IGNORECASE)


def extract_action_items(text: str) -> list[str]:
    lines = [line.strip("- ") for line in text.splitlines() if line.strip()]
    results: list[str] = []
    for line in lines:
        normalized = line.lower()
        if normalized.startswith("todo:") or normalized.startswith("action:"):
            results.append(line)
        elif _ACTION_RE.search(line):
            results.append(line)
        elif line.endswith("!"):
            results.append(line)
    return results


