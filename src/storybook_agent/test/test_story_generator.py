
from unittest.mock import MagicMock, patch

import pytest

from storybook_agent.schema.schemas import (
    CharacterBible,
    StoryBook,
    StoryPage,
)
from storybook_agent.services.story_generator import create_story


def make_story(page_count=3):
    character = CharacterBible(
        name="Finley",
        age="6 years old",
        appearance="Small orange fox with a blue scarf",
        personality="Curious and helpful",
        visual_style="Whimsical watercolor illustration",
    )

    pages = [
        StoryPage(
            page_number=i,
            title=f"Page {i}",
            story_text=f"Finley's adventure, page {i}.",
            illustration_prompt=f"Finley explores scene {i}.",
        )
        for i in range(1, page_count + 1)
    ]

    return StoryBook(
        book_title="Finley's Adventure",
        target_age="5-8 years",
        requested_page_count=page_count,
        cover={
            "title": "Finley's Adventure",
            "illustration_prompt": "Finley under a magical starry sky.",
        },
        character=character,
        pages=pages,
    )



def test_create_story_returns_structured_story(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "test-key")
    monkeypatch.setenv("GEMINI_TEXT_MODEL", "test-model")

    expected_story = make_story(3)

    mock_chain = MagicMock()
    mock_chain.invoke.return_value = expected_story

    with patch(
        "storybook_agent.services.story_generator.ChatGoogleGenerativeAI"
    ) as mock_llm:
        mock_llm.return_value.with_structured_output.return_value = mock_chain

        result = create_story("A fox helps a lost star.", page_count=3)

    assert isinstance(result, StoryBook)
    assert result.requested_page_count == 3
    assert len(result.pages) == 3

    mock_llm.return_value.with_structured_output.assert_called_once_with(
        StoryBook
    )

    prompt = mock_chain.invoke.call_args.args[0]
    assert "A fox helps a lost star." in prompt
    assert "exactly 3 story pages" in prompt.lower()


def test_empty_story_idea_is_rejected():
    with pytest.raises(ValueError, match="Story idea cannot be empty"):
        create_story("   ")


def test_page_count_below_one_is_rejected():
    with pytest.raises(ValueError, match="Page count must be at least 1"):
        create_story("A fox finds a star.", page_count=0)
