import os
import streamlit as st
from docx import Document
import openai

# Set your OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-key")
openai.api_key = OPENAI_API_KEY


def extract_questions_from_docx(file_path):
    """Extract questions from a Word document."""
    doc = Document(file_path)
    questions = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    return questions


def convert_to_gift_with_openai(questions):
    """Use OpenAI to convert questions to GIFT format."""
    prompt = (
        "Convert the following questions to GIFT format. Each question has a correct answer and "
        "multiple incorrect answers separated by '|'. Format: Question | Correct | Wrong1 | Wrong2...\n\n"
    )
    prompt += "\n".join(questions)
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1500,
            temperature=0
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"


# Streamlit App
st.title("Word to GIFT Converter with OpenAI")

uploaded_file = st.file_uploader("Upload a Word document", type="docx")

if uploaded_file:
    with open("temp.docx", "wb") as f:
        f.write(uploaded_file.read())

    questions = extract_questions_from_docx("temp.docx")
    if questions:
        st.write("Processing questions with OpenAI...")
        gift_format = convert_to_gift_with_openai(questions)
        st.text_area("GIFT Output", gift_format, height=400)
        st.download_button("Download GIFT File", gift_format, "questions.gift")
    else:
        st.warning("No questions found in the document.")

    os.remove("temp.docx")
