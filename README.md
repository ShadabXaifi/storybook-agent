# Storybook Agent

An AI-powered children's storybook generator that creates a structured story from a user prompt, generates illustrations, and produces a downloadable PDF.

## Overview

Storybook Agent is a Python application designed to turn a story idea into an illustrated children's book. It uses Gemini for story generation, ComfyUI with Stable Diffusion 1.5 for image generation, and ReportLab for PDF creation.

The project provides a Streamlit interface for generating and downloading the storybook.

## Features

- **AI Story Generation:** Generates a structured children's story from a user-provided prompt.
- **Structured Output:** Uses Pydantic models to define and validate story data.
- **Character Consistency:** Uses character information and illustration prompts to guide image generation across story pages.
- **AI Image Generation:** Uses ComfyUI and Stable Diffusion 1.5 through an API workflow.
- **PDF Generation:** Creates a downloadable storybook PDF containing the generated content and illustrations.
- **Streamlit Interface:** Provides a user interface to generate and download the resulting storybook.

## Tech Stack

- **Language:** Python
- **AI Model Integration:** Google Gemini, LangChain
- **AI Workflow Framework:** LangGraph
- **Data Validation:** Pydantic
- **Image Generation:** ComfyUI, Stable Diffusion 1.5
- **PDF Generation:** ReportLab
- **User Interface:** Streamlit
- **Environment and Dependency Management:** uv
- **Configuration:** python-dotenv
- **Image Processing:** Pillow

## Project Structure

```text
storybook-agent/
├── app.py
├── pyproject.toml
├── uv.lock
├── .env.example
├── workflows/
│   └── sd15_txt2img_api.json
├── src/
│   └── storybook_agent/
│       ├── __init__.py
│       ├── schema/
│       │   └── schemas.py
│       └── services/
│           ├── story_generator.py
│           ├── image_generator.py
│           ├── storybook_generator.py
│           └── pdf_generator.py
├── tests/
└── outputs/
```

`outputs/` is used for generated storybook files and may be created at runtime.

## Prerequisites

- Python 3.14 or a compatible version supported by the project.
- [uv](https://docs.astral.sh/uv/)
- A Google Gemini API key.
- ComfyUI configured with the Stable Diffusion 1.5 workflow used by the project.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ShadabXaifi/storybook-agent.git
cd storybook-agent
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file using the provided example:

```bash
copy .env.example .env
```

Add the required API key and model configuration using the variable names specified in `.env.example`.

Keep your API keys private. Do not commit `.env` to version control.

### 4. Start ComfyUI

Start ComfyUI with the configuration required by the project's image-generation service. Ensure the configured API endpoint is accessible and the required Stable Diffusion 1.5 workflow is available.

### 5. Run the application

```bash
uv run streamlit run app.py
```

Open the local URL displayed by Streamlit in your browser.

## How It Works

1. **User Input:** The user provides a prompt describing the children's story.
2. **Story Generation:** Gemini generates the structured story content.
3. **Data Validation:** Pydantic models validate the story structure.
4. **Illustration Generation:** The image-generation service uses ComfyUI and the configured Stable Diffusion workflow to generate illustrations.
5. **Storybook Assembly:** The storybook generator coordinates the generation process.
6. **PDF Creation:** ReportLab generates the final PDF.
7. **Download:** The Streamlit interface provides the generated PDF for download.

## Output

Generated storybooks are organized by story title under the `outputs/` directory.

```text
outputs/
└── Story_Title/
    └── storybook.pdf
```

The exact output depends on the prompt and the configured generation services.

## Running Tests

Run the project's test suite with:

```bash
uv run pytest -v
```

## Configuration Notes

- Gemini API access is required for story generation.
- ComfyUI must be running and accessible for image generation.
- Image generation depends on the configured workflow and available model files.
- Generated files are stored locally in the project's output directory.

## License

No license has been specified for this project.
