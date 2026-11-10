from unittest.mock import patch

import pytest

from ragbot.llm import summarize, summarize_with_retry


def test_summarize_uppercases_llm_reply():
    with patch("ragbot.llm.call_llm") as fake_llm:
        fake_llm.return_value = "short summary"  # script the answer
        result = summarize("long article")

    assert result == "SHORT SUMMARY"  # check YOUR logic
    fake_llm.assert_called_once_with("Summarize: long article")  # check what was sent


def test_summarize_sends_text_in_prompt():
    with patch("ragbot.llm.call_llm") as fake_llm:
        fake_llm.return_value = "hello world"
        result = summarize("doc")

    assert result == "HELLO WORLD"
    fake_llm.assert_called_once_with("Summarize: doc")


def test_retry_succeeds_after_one_timeout():
    with patch("ragbot.llm.call_llm") as fake_llm:
        fake_llm.side_effect = [TimeoutError(), "ok"]  # fail, then succeed
        result = summarize_with_retry("doc")

    assert result == "OK"
    assert fake_llm.call_count == 2  # it really retried


def test_retry_gives_up_after_three_timeouts():
    with patch("ragbot.llm.call_llm") as fake_llm:
        fake_llm.side_effect = TimeoutError()  # fail every time
        with pytest.raises(TimeoutError):  # we EXPECT it to raise
            summarize_with_retry("doc")

    assert fake_llm.call_count == 3  # tried exactly 3 times


def test_retry_succeeds_on_last_attempt():
    with patch("ragbot.llm.call_llm") as fake_llm:
        fake_llm.side_effect = [TimeoutError(), TimeoutError(), "done"]
        result = summarize_with_retry("doc")

    assert result == "DONE"
    assert fake_llm.call_count == 3

