GROUPS = (("present", "challenge", "foundation", "recent past"),
          ("possibility", "near future", "your stance"),
          ("environment", "hopes and fears", "likely outcome"))


def paginate(sections, limit=2000):
    if limit <= 0:
        raise ValueError("Limit must be positive")
    expected = {name for group in GROUPS for name in group}
    if set(sections) != expected or any(not isinstance(value, str) or not value.strip() for value in sections.values()):
        raise ValueError("All ten nonempty sections are required")
    messages = ["\n".join(sections[name] for name in group) for group in GROUPS]
    if any(len(message) > limit for message in messages):
        raise ValueError("Regenerate a shorter reading before sending any part")
    return messages
