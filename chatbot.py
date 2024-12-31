import streamlit as st
import pandas as pd
import openai 

# Set your OpenAI API Key
openai.api_key = st.secrets["openai_api_key"]

def load_csv(file): 
    """Load the uploaded CSV file and return a DataFrame."""
    try: 
        data = pd.read_csv(file)
        if 'Question' in data.columns and 'Answer' in data.columns:
            return data
        else:
            st.error("CSV file must contain 'Question' and 'Answer' columns.")
            return None
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None

def get_openai_response(user_query, qa_data):
    """Generate a response using OpenAI API based on the user's query and CSV data."""
    context = "\n".join(
        [f"Q: {row['Question']}\nA: {row['Answer']}" for _, row in qa_data.iterrows()]
    )
    prompt = f"The following is a conversation with a chatbot. The chatbot uses the provided context to answer questions.\n\nContext:\n{context}\n\nUser: {user_query}\nChatbot:"

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        st.error(f"Error with OpenAI API: {e}")
        return "Sorry, there was an issue generating a response."

def main():
    st.title("CSV-Powered Chatbot with OpenAI")
    st.write("Upload a CSV file with 'Question' and 'Answer' columns to get started.")

    uploaded_file = st.file_uploader("Upload CSV", type="csv")

    if uploaded_file:
        qa_data = load_csv(uploaded_file)

        if qa_data is not None:
            st.success("CSV loaded successfully!")
            user_query = st.text_input("Ask a question:")

            if user_query:
                response = get_openai_response(user_query, qa_data)
                st.write("**Chatbot:**", response)

if __name__ == "__main__":
    main()
