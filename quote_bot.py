import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Latest version - Updated for Streamlit Cloud deployment
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Boone Quote Assistant", page_icon="📄")
st.title("Boone Quote Assistant")

if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Enhanced system prompt
st.session_state.conversation.append({
    "role": "system",
    "content": (
        "You are a smart and helpful print quoting assistant trained on Boone Graphics' print production, mailing, and compliance capabilities, referencing boone_print_knowledge.md.\n\n"
        "Your primary goal is to gather accurate, complete print quote requests in a warm, conversational, one-question-at-a-time flow.\n\n"
        "Quote gathering must include:\n"
        "- Quantity (ask for ranges)\n"
        "- Stock type and weight (offer options or help if unsure)\n"
        "- Digital vs Offset printing (offer explanations if unsure)\n"
        "- Ink setup (CMYK, black only, spot, combo)\n"
        "- Sides printed (1 or 2)\n"
        "- Flat and finished size\n"
        "- Folding needed? Ask what type. If unsure, show image.\n"
        "- Ask if it needs to go into an envelope. If yes, suggest adding envelope as separate item.\n"
        "- Ask if they need design help. If yes, recommend Studio B.\n"
        "- Ask if this will be mailed. If yes, suggest Boone Mail Plus.\n"
        "- Ask if they will upload artwork or if it's pending.\n"
        "- Ask when the project must be completed.\n"
        "- Ask for Name and Email (mandatory). Recommend Company and Phone.\n\n"
        "Every item should be labeled (e.g., Item #1: Brochure), and a final summary shown before the conversation ends.\n"
        "Ask if there's anything else we can quote.\n\n"
        "Always recognize when a topic is related to Boone's services (e.g., mail, HIPAA, design, data) and offer a short relevant pitch. If the user says yes, explain further using boone_print_knowledge.md."
    )
})

user_input = st.chat_input("Tell me what you need printed!")
if user_input:
    st.session_state.conversation.append({"role": "user", "content": user_input})
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=st.session_state.conversation
        )
        assistant_reply = response["choices"][0]["message"]["content"]
        st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})
    except Exception as e:
        assistant_reply = f"⚠️ An error occurred: {e}"
        st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})

for message in st.session_state.conversation:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

