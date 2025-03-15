import streamlit as st
import google.generativeai as genai

# Google AI API config
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Call the gemini endpoint for gpt usage
def ask_ai(question):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Create response
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

def show_ai():
    st.markdown("## Ask the AI 🤖")
    # Input box for questions
    user_question = st.text_area("Write your prompt here:", placeholder="What is RSA encryption in depth?")

    if st.button("Submit"):
        if user_question.strip():
            with st.spinner("Thinking..."):
                ai_response = ask_ai(user_question)
                st.success("Response:")
                st.write(ai_response)
        else:
            st.warning("Please enter a question before pressing Submit")