GROUPS = (("present", "challenge", "foundation", "recent past"),
          ("possibility", "near future", "your stance"),
          ("environment", "hopes and fears", "likely outcome"))


def paginate(sections, limit=2000):
    return ["\n".join(sections.values())[:limit]]
