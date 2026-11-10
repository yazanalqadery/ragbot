from ragbot.text import chunk_text


def test_splits_evenly():
    assert chunk_text("abcdef", 2) == ["ab", "cd", "ef"]


def test_last_chunk_can_be_shorter():
    assert chunk_text("abcde", 2) == ["ab", "cd", "e"]
