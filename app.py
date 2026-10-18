
import streamlit as st

from storybook_agent.services.storybook_generator import generate_storybook

st.set_page_config(
    page_title="AI Storybook Studio",
    page_icon="📚",
    layout="wide",
)

st.title("AI Storybook Studio")
st.write("Turn your story idea into an illustrated children's storybook.")

with st.form("storybook_form"):
    story_idea = st.text_area(
        "Your story idea",
        placeholder=(
            "Example: A little fox discovers a magical seed "
            "and helps a lonely dragon grow a garden."
        ),
        height=130,
    )

    page_count = st.slider(
        "Number of story pages",
        min_value=1,
        max_value=15,
        value=5,
    )

    submitted = st.form_submit_button(
        "Generate Storybook",
        type="primary",
    )

if submitted:
    if not story_idea.strip():
        st.error("Please enter a story idea.")
    else:
        try:
            with st.spinner(
                "Creating your story and illustrations... "
                "This may take several minutes."
            ):
                result = generate_storybook(
                    story_idea=story_idea.strip(),
                    page_count=page_count,
                )

            st.success("Your storybook is ready!")
            st.header(result["book_title"])

            cover_path = result["cover_path"]
            if cover_path.is_file():
                st.subheader("Cover")
                st.image(str(cover_path), use_container_width=True)

            st.subheader("Your Story")

            for page in result["pages"]:
                st.markdown(f"### Page {page['page_number']}: {page['title']}")
                image_path = page["image_path"]

                if image_path.is_file():
                    st.image(str(image_path), use_container_width=True)

                st.write(page["story_text"])
                st.divider()

            pdf_path = result["pdf_path"]

            if pdf_path.is_file():
                with pdf_path.open("rb") as pdf_file:
                    st.download_button(
                        label="Download Storybook PDF",
                        data=pdf_file.read(),
                        file_name=f"{result['book_title']}.pdf",
                        mime="application/pdf",
                        type="primary",
                    )

            st.caption(f"Saved locally in: {result['output_dir']}")

        except Exception as exc:
            st.error(f"Storybook generation failed: {exc}")
            st.exception(exc)
