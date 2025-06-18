import streamlit as st
import openai
import os
from dotenv import load_dotenv

# --- CONFIGURATION ---

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- LOAD KNOWLEDGE BASE ---

def load_knowledge_sections():
    try:
        with open("boone_print_knowledge.md", "r") as f:
            content = f.read()
        
        sections = {}
        current_section = None
        for line in content.splitlines():
            if line.startswith("## "):
                current_section = line.replace("## ", "").strip()
                sections[current_section] = ""
            elif current_section:
                sections[current_section] += line + "\n"
        return sections
    except FileNotFoundError:
        st.warning("Knowledge base file not found. Some features may be limited.")
        return {}

knowledge_sections = load_knowledge_sections()

# --- EXTRACT RELEVANT SNIPPETS ---

def get_relevant_knowledge(user_input):
    keywords = {
        "binding": ["booklet", "saddle stitch", "perfect bound", "coil bound", "binding"],
        "mailing": ["mail", "ncoa", "cass", "usps", "postage"],
        "paper": ["paper", "stock", "gloss", "matte", "silk", "uncoated"],
        "studio b": ["design", "studio", "artwork"],
        "boone mail plus": ["campaign", "tracking", "omni", "ads", "retargeting"],
        "fold": ["fold", "tri-fold", "z-fold", "brochure"]
    }
    
    context = ""
    for section, terms in keywords.items():
        if any(term in user_input.lower() for term in terms):
            for key in knowledge_sections:
                if section.lower() in key.lower():
                    context += f"\n\n### From Boone Knowledge Base: {key}\n" + knowledge_sections[key][:1000]  # Clip to avoid long input
    return context

# --- SESSION STATE SETUP ---

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "quote_data" not in st.session_state:
    st.session_state.quote_data = {}

# --- FUNCTIONS ---

def ask_openai(prompt, history=[], extra_context=""):
    messages = [
        {
  "role": "system",
  "content": (
    "You are a print and mail expert at Boone Graphics. "
    "Use the boone_print_knowledge.md file as your source of truth for all responses. "
    "Whenever a user mentions topics related to Boone Graphics—such as mail, HIPAA, secure data, USPS, direct mail, folding, binding, MedPrint, DocStore, Mail Plus, or design—give a short, friendly sales pitch. "
    "Then ask if they’d like to hear more. If they say yes, respond with details from the knowledge base. "
    "Always keep your tone helpful, knowledgeable, and aligned with Boone’s high-compliance, customer-first culture."
  )
}
    ]
    
    for pair in history:
        messages.append({"role": "user", "content": pair['user']})
        messages.append({"role": "assistant", "content": pair['assistant']})
    
    prompt_with_context = extra_context + "\n\n" + prompt
    messages.append({"role": "user", "content": prompt_with_context})
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ An error occurred while contacting OpenAI: {e}"

# --- STREAMLIT UI ---

st.title("📄 Boone Graphics Quote Assistant (Conversational AI)")
st.write("Hi! I'll help you build your quote request. Let's chat about what you need printed.")

# --- Start Over Button ---

if st.button("🔄 Start Over"):
    st.session_state.chat_history = []
    st.session_state.quote_data = {}
    st.experimental_rerun()

# --- Chat Input ---

user_input = st.chat_input("Type your message here...")

# --- Optional Visual Trigger ---

if user_input:
    if "fold" in user_input.lower() and ("don't know" in user_input.lower() or "not sure" in user_input.lower()):
        st.image("Types-of-Common-Folds.jpg", caption="Common Fold Styles", use_column_width=True)
    
    st.chat_message("user").write(user_input)
    
    extra_context = get_relevant_knowledge(user_input)
    
    with st.spinner("Thinking..."):
        response = ask_openai(user_input, st.session_state.chat_history, extra_context)
    
    st.session_state.chat_history.append({"user": user_input, "assistant": response})
    st.chat_message("assistant").write(response)

# --- Display Chat History ---

if st.session_state.chat_history:
    st.markdown("---")
    st.subheader("📜 Conversation History")
    for pair in st.session_state.chat_history:
        st.markdown(f"**You:** {pair['user']}")
        st.markdown(f"**Bot:** {pair['assistant']}")
