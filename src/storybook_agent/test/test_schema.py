
import pytest
from pydantic import ValidationError

from storybook_agent.schema.schemas import (
    CharacterBible,
    StoryPage,
    StoryBook,
)


def make_story(page_count=5):
    character = CharacterBible(
        name="Milo",
        age="8 years",
        appearance="Small brown bear wearing a blue scarf",
        personality="Curious and kind",
        visual_style="Colorful children's book illustration",
    )

    pages = [
        StoryPage(
            page_number=i,
            title=f"Page {i}",
            story_text=f"Milo's adventure continues on page {i}.",
            illustration_prompt=f"Milo explores scene {i}.",
        )
        for i in range(1, page_count + 1)
    ]

    return {
        "book_title": "Milo's Adventure",
        "target_age": "5-8 years",
        "requested_page_count": page_count,
        "character": character,
        "pages": pages,
    }


def test_default_five_pages():
    data = make_story()
    data.pop("requested_page_count")

    story = StoryBook(**data)

    assert story.requested_page_count == 5
    assert len(story.pages) == 5


@pytest.mark.parametrize("count", [1, 3, 5, 8, 15])
def test_custom_page_count(count):
    story = StoryBook(**make_story(count))

    assert len(story.pages) == count
    assert story.pages[-1].page_number == count


def test_rejects_wrong_page_count():
    data = make_story(3)
    data["requested_page_count"] = 5

    with pytest.raises(ValidationError):
        StoryBook(**data)


def test_rejects_non_sequential_page_numbers():
    data = make_story(3)
    data["pages"][1].page_number = 3

    with pytest.raises(ValidationError):
        StoryBook(**data)
