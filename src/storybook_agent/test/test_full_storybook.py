
from storybook_agent.services.storybook_generator import generate_storybook


def main():
    result = generate_storybook(
        story_idea=(
            "A little rabbit discovers a glowing seed in a forest "
            "and learns to help other animals."
        ),
        page_count=2,
    )

    print(f"\nBook: {result['book_title']}")
    print(f"Output folder: {result['output_dir']}")
    print(f"Cover: {result['cover_path']}")

    for page in result["pages"]:
        print(f"\nPage {page['page_number']}: {page['title']}")
        print(f"Text: {page['story_text']}")
        print(f"Image: {page['image_path']}")


if __name__ == "__main__":
    main()
