
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from storybook_agent.schema.schemas import StoryBook

load_dotenv()


def create_story(story_idea: str, page_count: int = 5) -> StoryBook:
    if not story_idea.strip():
        raise ValueError("Story idea cannot be empty.")

    if page_count < 1:
        raise ValueError("Page count must be at least 1.")

    api_key = os.getenv("GOOGLE_API_KEY")
    model_name = os.getenv("GEMINI_TEXT_MODEL")

    if not api_key:
        raise ValueError("GOOGLE_API_KEY missing in .env")
    if not model_name:
        raise ValueError("GEMINI_TEXT_MODEL missing in .env")

    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=0.7,
    )

    structured_llm = llm.with_structured_output(StoryBook)

    prompt = f"""
Create an original, complete illustrated children's storybook.

USER'S STORY IDEA:
{story_idea}

REQUIREMENTS:
- Target children aged 5-8.
- Generate exactly {page_count} story pages, excluding the cover.
- Create a suitable book title and a separate cover illustration prompt.
- Create a detailed CharacterBible for the main character.
- Define appearance, age, clothing, personality and distinctive features.
- Create a VisualBible for the entire book.
- Specify art style, at least three palette colors, lighting,
  world description and at least three visual consistency rules.
- Keep character anatomy, face, proportions, clothing, colors,
  accessories and art style consistent across every page.
- Change a character's appearance only when the story explicitly
  requires a change.
- Make every page advance the story naturally.
- Each page must include a scene_description and character_actions.
- Each illustration_prompt must be detailed and describe composition,
  foreground, background, environment, lighting, camera angle,
  character appearance, action, emotion, colors, textures and mood.
- Include the full relevant character appearance and visual style
  in each illustration prompt. Do not rely on previous prompts.
- Avoid text, letters, watermarks and logos inside illustrations.
- Use rich, polished, professional children's picture-book artwork.
- Make the cover visually appealing and related to the story.
- Use simple, age-appropriate story text.
- Number pages sequentially starting from 1.
- Return data matching the StoryBook schema.
  STORY SEQUENCE AND SCENE CONTINUITY:
- Create a chronological, cause-and-effect story.
- Every page must continue from the events of the previous page.
- Page 1 establishes the characters, location and initial situation.
- Each next page must show a new action or consequence.
- Do not repeat the same scene, pose, event or composition on multiple pages.
- Keep track of character location, clothing, carried objects and emotional state.
- If a character moves to a new place, show that transition in the story.
- Each illustration must depict the exact event described on its own page.
- Do not illustrate a future event before it happens in the story.
- The final page must resolve the main story problem.
- Write scene descriptions as specific visual moments, not general summaries.
- Include foreground, background, character positions, actions and expressions.
"""

    return structured_llm.invoke(prompt)
