import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Latest version - Updated for Streamlit Cloud deployment
load_dotenv()

# Try to get API key from Streamlit secrets first, then environment variables
if hasattr(st, 'secrets') and st.secrets.get("OPENAI_API_KEY"):
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("""
    ⚠️ **OpenAI API Key Not Found!**

    Please set your OpenAI API key using one of these methods:

    1. **Streamlit Cloud Secrets:** Add to your app's secrets in the dashboard
    2. **Environment Variable:** `export OPENAI_API_KEY="your_api_key"`
    3. **Create a .env file** with: `OPENAI_API_KEY=your_api_key`

    Get your API key from: https://platform.openai.com/account/api-keys
    """)
    st.stop()

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

st.set_page_config(page_title="Boone Quote Assistant", page_icon="📄")
st.title("Boone Quote Assistant")

if "conversation" not in st.session_state:
    st.session_state.conversation = []
    # Add system prompt only once, not to display
    st.session_state.system_prompt = {
        "role": "system",
        "content": (
            "You are a smart, helpful, and sales-oriented print quoting assistant trained on Boone Graphics' print production, mailing, and compliance capabilities, referencing boone_print_knowledge.md.\n\n"
            "Your primary goal is to gather accurate, complete print quote requests in a warm, conversational, one-question-at-a-time flow while actively promoting Boone's services.\n\n"
            "CRITICAL: For EVERY item, you MUST collect these specifications:\n"
            "- Quantity (ask for ranges if unsure)\n"
            "- Size (flat dimensions - width x height)\n"
            "- Size folded (if applicable - width x height when folded)\n"
            "- Stock type, weight, AND texture/finish (be specific):\n"
            "  * Weight examples: 60#, 70#, 80#, 100#, 120#\n"
            "  * Type examples: Text, Cover, Writing\n"
            "  * Finish examples: Gloss, Matte, Satin, Uncoated, Linen, Laid\n"
            "  * Examples: '80# Gloss Text', '100# Matte Cover', '24# Uncoated Writing'\n"
            "- Color per side (1-sided or 2-sided, and ink colors: CMYK, black only, spot colors, etc.)\n\n"
            "Additional specifications based on product type:\n"
            "- Folding: Ask what type (tri-fold, z-fold, half-fold, etc.). If they're unsure, mention you'll show them a visual reference.\n"
            "- Binding: For booklets, ask about binding type (saddle stitch, perfect bound, coil bound, etc.)\n"
            "- Envelopes: If they need envelopes, ask about size, stock, and ink colors\n"
            "- Mailing: If it will be mailed, ask about mailing services needed\n\n"
            "SALES ORIENTATION:\n"
            "- Answer ANY questions about printing, mailing, design, or Boone's services\n"
            "- Actively promote Boone's services when relevant (MedPrint, Studio B, Mail Plus, etc.)\n"
            "- Reference boone_print_knowledge.md to explain services and offer upsells\n"
            "- Don't be afraid to sell! You're part salesperson, part assistant\n"
            "- If they mention medical/healthcare, pitch MedPrint and DataLock\n"
            "- If they need design help, recommend Studio B\n"
            "- If they mention mailing, suggest Boone Mail Plus\n"
            "- If they're unsure about paper, offer guidance and options\n\n"
            "Process:\n"
            "- Label each item (Item #1: Brochure, Item #2: Envelope, etc.)\n"
            "- Ask ONE question at a time and wait for their answer\n"
            "- Don't move to the next specification until the current one is confirmed\n"
            "- If they mention multiple items, collect ALL specifications for each item separately\n"
            "- Always collect Name and Email (mandatory). Recommend Company and Phone.\n"
            "- Provide a final summary of all items with complete specifications before ending\n\n"
            "When users ask about folding types or seem unsure about folds, mention that you'll show them a visual reference of common fold types.\n\n"
            "Always recognize when a topic is related to Boone's services (e.g., mail, HIPAA, design, data) and offer a short relevant pitch. If the user says yes, explain further using boone_print_knowledge.md."
        )
    }

# Display welcome message
if not st.session_state.conversation:
    st.write("👋 **Welcome!** I'm here to help you get a quote for your printing needs. What would you like to have printed today?")

user_input = st.chat_input("Tell me what you need printed! v19")
if user_input:
    # Check if we should show the fold image - make it more flexible
    user_input_lower = user_input.lower()
    fold_keywords = ["fold", "folding", "folded", "tri-fold", "z-fold", "half-fold", "folded", "folds"]
    unsure_keywords = ["don't know", "not sure", "unsure", "uncertain", "which", "what type", "show me", "help", "options", "types"]
    
    # Show image if they mention folding OR if they seem unsure about anything related to folding
    should_show_fold_image = (
        any(keyword in user_input_lower for keyword in fold_keywords) or
        ("fold" in user_input_lower and any(keyword in user_input_lower for keyword in unsure_keywords))
    )
    
    if should_show_fold_image:
        st.image("Types-of-Common-Folds.jpg", caption="Common Fold Types", use_container_width=True)
    
    st.session_state.conversation.append({"role": "user", "content": user_input})
    try:
        # Include system prompt in API call but not in display
        messages = [st.session_state.system_prompt] + st.session_state.conversation
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        assistant_reply = response.choices[0].message.content
        st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})
    except Exception as e:
        assistant_reply = f"⚠️ An error occurred: {e}"
        st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})

# Display conversation history (excluding system prompt)
for message in st.session_state.conversation:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

