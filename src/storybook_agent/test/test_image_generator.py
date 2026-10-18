
from storybook_agent.services.image_generator import generate_image


def test_generate_image():
    image_path = generate_image(
        prompt=(
            "A friendly little brown bear wearing a blue scarf, "
            "standing in a colorful storybook forest, "
            "children's picture book illustration"
        ),
        filename="comfyui_integration_test.png",
    )

    assert image_path.is_file()
    assert image_path.stat().st_size > 0
