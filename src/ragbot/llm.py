def call_llm(prompt: str) -> str:
    raise RuntimeError("Real API Call! This must never run in tests.")


def summarize(text: str) -> str:
    response = call_llm(f"Summarize: {text}")
    return response.upper()


def summarize_with_retry(text: str, attempts: int = 3) -> str:
    for attempt in range(attempts):
        try:
            return summarize(text)
        except TimeoutError:
            if attempt == attempts - 1:  # last attempt → give up
                raise
