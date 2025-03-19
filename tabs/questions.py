import streamlit as st
from utils.style_loader import load_css

def show_questions():
    load_css()

    # Header
    st.markdown("<div class='faq-header'>Frequently Asked Questions</div>", unsafe_allow_html=True)

    # FAQ 1
    st.markdown("<div class='faq-question'>1. What is this app about? 🤷‍♂️</div>", unsafe_allow_html=True)
    st.markdown("<div class='faq-answer'>This app helps you test and understand various protocols in a user-friendly way. "
        "It provides detailed explanations, visualizations, and tools to make protocol testing easier 🚚</div>",unsafe_allow_html=True,
    )

    # FAQ 2
    st.markdown("<div class='faq-question'>2. How do I get started? 🛠️</div>", unsafe_allow_html=True)
    st.markdown("<div class='faq-answer'>Simply navigate to the 'Testing' section, select a protocol, and follow the instructions. "
        "You'll be testing protocols like a pro in no time! 🎯</div>",unsafe_allow_html=True,
    )

    # FAQ 3
    st.markdown("<div class='faq-question'>3. Can I contribute to this project? 🤝</div>", unsafe_allow_html=True)
    st.markdown("<div class='faq-answer'>Future contributions will be accepted indeed. Check out the GitHub repository for more details "
        "and feel free to open new issues or suggest new features. 🛠️</div>",unsafe_allow_html=True,
    )

    # FAQ 4
    st.markdown("<div class='faq-question'>4. Where can I find documentation? 📚</div>", unsafe_allow_html=True)
    st.markdown("<div class='faq-answer'>You can find detailed documentation in the 'Documentation' section of the app or visit our "
        "GitHub repository for more technical details. 📖</div>",unsafe_allow_html=True,
    )

    # FAQ 5
    st.markdown("<div class='faq-question'>5. How can I contact the team? 📧</div>", unsafe_allow_html=True)
    st.markdown("<div class='faq-answer'>Luckly for you, it's just me! So you can reach out via email at <strong>a.garciasr.2018@alumnos.urjc.es</strong> or "
        "open an issue on my GitHub repository. Don't be too mean! 💌</div>",unsafe_allow_html=True,
    )

    # Contact Section
    st.markdown(
        """
        <div class='contact-section'>
            <h3>📬 Contact Us</h3>
            <p>Have more questions or feedback? Reach out to us!</p>
            <p>👉 <a href="https://github.com/XalbertoXX/agarcisr-TFG" target="_blank">Visit the GitHub Repository</a> 👈</p>
        </div>
        """,unsafe_allow_html=True,
    )