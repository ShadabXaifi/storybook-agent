
from pydantic import BaseModel, Field, model_validator


class CharacterBible(BaseModel):
    name: str
    age: str
    appearance: str
    personality: str
    visual_style: str = "Detailed children's picture-book illustration"
    clothing: str = "As described in the character appearance"
    distinctive_features: list[str] = Field(
        default_factory=lambda: ["Consistent face and body proportions"]
    )


class VisualBible(BaseModel):
    art_style: str = "Detailed children's picture-book illustration"
    color_palette: list[str] = Field(
        default_factory=lambda: ["warm amber", "forest green", "sky blue"]
    )
    lighting_style: str = "Soft cinematic storybook lighting"
    world_description: str = "A richly detailed storybook world"
    consistency_rules: list[str] = Field(
        default_factory=lambda: [
            "Keep character appearance consistent",
            "Keep illustration style consistent",
            "Keep the color palette consistent",
        ]
    )


class CoverPage(BaseModel):
    title: str
    illustration_prompt: str


class StoryPage(BaseModel):
    page_number: int = Field(ge=1)
    title: str
    story_text: str
    scene_description: str = ""
    character_actions: list[str] = Field(default_factory=list)
    illustration_prompt: str


class StoryBook(BaseModel):
    book_title: str
    target_age: str
    requested_page_count: int = Field(default=5, ge=1)

    character: CharacterBible

    visual_bible: VisualBible = Field(default_factory=VisualBible)

    cover: CoverPage = Field(
        default_factory=lambda: CoverPage(
            title="Storybook",
            illustration_prompt="A colorful children's storybook cover"
        )
    )

    pages: list[StoryPage] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_story_pages(self):
        if len(self.pages) != self.requested_page_count:
            raise ValueError(
                f"Expected {self.requested_page_count} pages, "
                f"received {len(self.pages)}."
            )

        expected = list(range(1, self.requested_page_count + 1))
        actual = [page.page_number for page in self.pages]

        if actual != expected:
            raise ValueError(
                "Page numbers must be sequential, starting from 1."
            )

        return self