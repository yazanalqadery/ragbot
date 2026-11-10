def chunk_text(text: str, size: int) -> list[str]:
    return [text[i : i + size + 1] for i in range(0, len(text), size)]
