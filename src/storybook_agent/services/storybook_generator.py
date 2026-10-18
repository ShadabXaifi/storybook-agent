
import re
from pathlib import Path

from storybook_agent.schema.schemas import StoryBook
from storybook_agent.services.image_generator import generate_image
from storybook_agent.services.story_generator import create_story
from storybook_agent.services.pdf_generator import create_storybook_pdf


def _safe_filename(value: str) -> str:
    filename = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", value)
    filename = re.sub(r"\s+", "_", filename.strip())
    return filename[:80] or "storybook"


def _build_image_prompt(
    story: StoryBook,
    scene_prompt: str,
) -> str:
    character = story.character
    visual = story.visual_bible

    return f"""
Create a polished, detailed children's picture-book illustration.

CHARACTER IDENTITY — KEEP CONSISTENT:
Name: {character.name}
Age: {character.age}
Appearance: {character.appearance}
Clothing: {character.clothing}
Distinctive features: {", ".join(character.distinctive_features)}
Personality: {character.personality}

GLOBAL VISUAL STYLE:
Art style: {visual.art_style}
Color palette: {", ".join(visual.color_palette)}
Lighting: {visual.lighting_style}
World: {visual.world_description}

VISUAL CONSISTENCY RULES:
{"; ".join(visual.consistency_rules)}

SCENE:
{scene_prompt}

Render the character with the same face, body proportions, fur/skin,
clothing, colors and distinctive features. Keep the art style and world
visually consistent. Use rich textures, detailed foreground and background,
clear composition, expressive emotions and professional picture-book quality.
No text, letters, watermark or logo.
SCENE CONTINUITY:
This image must depict ONLY the current page's event.
Follow the chronological story sequence.
Show the exact character actions described for this page.
Do not reuse a previous page's composition or show future events.
Preserve character identity, clothing, props and the established world.
The illustration must visually communicate this page's specific story moment.
""".strip()



def generate_storybook(story_idea: str, page_count: int = 5) -> dict:
    story: StoryBook = create_story(
        story_idea=story_idea,
        page_count=page_count,
    )

    project_root = Path(__file__).resolve().parents[2]
    book_dir = project_root / "outputs" / _safe_filename(story.book_title)
    book_dir.mkdir(parents=True, exist_ok=True)

    cover_path = generate_image(
        prompt=_build_image_prompt(
            story,
            f"Book cover composition. {story.cover.illustration_prompt}",
        ),
        filename=str(book_dir / "cover.png"),
    )

    page_results = []

    for page in story.pages:
        prompt = _build_image_prompt(
            story,
            (
                f"Scene description: {page.scene_description}\n"
                f"Character actions: {', '.join(page.character_actions)}\n"
                f"Illustration details: {page.illustration_prompt}"
            ),
        )

        image_path = generate_image(
            prompt=prompt,
            filename=str(book_dir / f"page_{page.page_number:02d}.png"),
        )

        page_results.append(
            {
                "page_number": page.page_number,
                "title": page.title,
                "story_text": page.story_text,
                "image_path": image_path,
            }
        )

        pdf_path = create_storybook_pdf(
        {
            "book_title": story.book_title,
            "target_age": story.target_age,
            "cover_path": cover_path,
            "pages": page_results,
            "output_dir": book_dir,
        }
    )

    return {
        "book_title": story.book_title,
        "target_age": story.target_age,
        "character": story.character,
        "visual_bible": story.visual_bible,
        "cover_path": cover_path,
        "pages": page_results,
        "output_dir": book_dir,
        "pdf_path": pdf_path,
    }
