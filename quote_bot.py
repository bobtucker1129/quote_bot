import streamlit as st
import openai
import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
from datetime import datetime
import re

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

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
INTERNAL_RECIPIENTS = ["state@boonegraphics.net", "elemire@boonegraphics.net"]

st.set_page_config(page_title="Boone Quote Assistant", page_icon="📄")
st.title("Boone Quote Assistant")

if "conversation" not in st.session_state:
    st.session_state.conversation = []
    # Add system prompt only once, not to display
    st.session_state.system_prompt = {
        "role": "system",
        "content": (
            "You are a smart, helpful, and sales-oriented print quoting assistant trained on Boone Graphics' print production, mailing, and compliance capabilities, referencing boone_print_knowledge.md and boone_envelope_knowledge.md.\n\n"
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
            "- Color per side (1-sided or 2-sided, and ink colors: CMYK, black only, spot colors, etc.)\n"
            "- Delivery date (when they need the product completed and delivered)\n"
            "- Delivery method: ALWAYS ask 'Will you be picking up or do you need delivery?' If they say delivery, ALWAYS ask for their address\n\n"
            "Additional specifications based on product type:\n"
            "- Folding: Ask what type (tri-fold, z-fold, half-fold, etc.). If they're unsure, mention you'll show them a visual reference.\n"
            "- Binding: For booklets, ask about binding type (saddle stitch, perfect bound, coil bound, etc.)\n"
            "- Envelopes: If they need envelopes, ask about size, stock, and ink colors\n"
            "- Mailing: If they mention mailing or USPS, ALWAYS ask these two questions:\n"
            "  * 'Do you need extras beyond your mailing list?'\n"
            "  * 'If you need extras, should those be delivered back to you or will you pick them up?'\n"
            "- Posters/Signage: If they ask for posters or signage, ask if they want flexible or rigid:\n"
            "  * Flexible: Recommend '14mil Double White Popup'\n"
            "  * Rigid: Offer these 5 options:\n"
            "    - PVC Board - Durable for indoor and short term outdoor use\n"
            "    - Styrene - Semi-rigid, flexible, and curveable\n"
            "    - Foam Board - Lightweight poster board, for indoor use only\n"
            "    - GatorFoam - Extra heavy-duty surface, Lightweight, indoor use only - Comes in these thicknesses 3/16\" White, 1/2\" White, 3/16\" Black, 1/2\" Black\n"
            "    - Coroplast - 4mm coroplast with H-Stake option, Custom size, indoor/outdoor use\n"
            "- Banners: If they ask for banners, offer these options:\n"
            "  * 13 oz Matte Scrim Banner - Full color UV printed - Indoor and outdoor ready, Single or double sided\n"
            "  * 18 oz matte blockout banner - Full color UV printed - Indoor and outdoor ready, Single or double sided\n"
            "  * For ALL banners, ask if they want: Hemming the edges, Pole Pockets, Grommets\n"
            "  * If grommets, ask which option: Every 2' All Sides, Every 2' Top & Bottom, Every 2' Left & Right, 4 Corner Only\n"
            "- Other products: If they ask for anything outside these options, note their request so our estimator can see if we can do that\n\n"
            "BOOKLET BINDING LOGIC:\n"
            "- Saddle Stitch: Page count MUST be divisible by 4. Always 2-sided (no need to ask). If invalid page count, suggest adding blank pages on inside covers.\n"
            "- Perfect Bound/Coil Bound: Page count MUST be divisible by 2. Ask about 1-sided vs 2-sided. If invalid page count, suggest adding blank page at the end.\n"
            "- For ALL booklets, ask about paper stock: 'Will you be using the same paper stock throughout (self cover) or do you want a different, thicker stock for the cover?'\n"
            "- Use 'same paper throughout' in conversation, but understand 'self cover' terminology.\n"
            "- Page count validation examples:\n"
            "  * Saddle stitch 10 pages → 'For saddle stitch, we need the page count to be divisible by 4. Your 10-page booklet would need 2 additional pages (making it 12 pages total). Would you like to add 2 blank pages on the inside covers?'\n"
            "  * Perfect bound 15 pages → 'For perfect bound, we need an even page count. Your 15-page booklet would need 1 additional page (making it 16 pages total). Would you like to add a blank page?'\n\n"
            "ENVELOPE KNOWLEDGE & LOGIC:\n"
            "- PROACTIVE ENVELOPE DETECTION: When users mention 'letter', 'mailing', 'appeal', 'kit', 'billing', 'statement', 'donation', or 'membership campaign' → ask 'Would you like to quote envelopes as a separate item?'\n"
            "- SIZE VALIDATION: Insert must be 1/2\" narrower and 1/4\" shorter than envelope. Common patterns: trifold letter (8.5x11) fits #10 envelope, larger folded pieces need 9x12 or 10x13 envelopes.\n"
            "- STOCK RESTRICTIONS: NEVER recommend glossy or cover-weight envelopes unless specifically requested. Default to uncoated text or standard envelope stock.\n"
            "- USPS COMPLIANCE: Smallest mailable size 3.5\"x5\", max 6.125\"x11.5\". Square envelopes require extra postage but may have better open rates.\n"
            "- WINDOW ENVELOPES: Suggest window envelopes for personalized mail to avoid addressing mismatches and save money.\n"
            "- REMITTANCE ENVELOPES: For reply/donation scenarios, recommend #6-3/4 or #9 remittance envelopes with printable flaps.\n"
            "- ENVELOPE TYPES: Use both technical names (#10, A2, etc.) and simple explanations. Ask if customers need clarification.\n"
            "- SELF-MAILER AWARENESS: Understand self-mailers (no envelope needed, address/postage printed directly on piece) and their benefits (cost-effective, immediate impact, design flexibility) but don't necessarily suggest unless relevant.\n"
            "- ENVELOPE PAPER OPTIONS: Wove (smooth, white, economical), Recycled (sustainable, earthy), Smooth (non-textured), plus texture options: Linen, Laid, Felt, Embossed, Metallic/Foil.\n"
            "- CONVERSATIONAL TRIGGERS:\n"
            "  * 'folded letter into envelope' or #10 window → suggest envelope quote\n"
            "  * 'reply/donation' → recommend remittance envelopes\n"
            "  * 'security envelope' → offer window security with tinted interior\n"
            "  * 'wedding/invite' → suggest A-series envelopes (A6, A7)\n"
            "  * 'personalized' → suggest window envelopes\n"
            "  * 'cost-effective' → mention self-mailer options if relevant\n\n"
            "PRINTING TERMINOLOGY:\n"
            "- Page = one side of a sheet\n"
            "- Sheet = one piece of paper (2 pages)\n"
            "- Signature = large sheet folded to create multiple pages (multiples of 4)\n\n"
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
            "- IMPORTANT: After collecting all item specifications, ALWAYS ask about delivery method before ending\n"
            "- IMPORTANT: If they mention mailing, USPS, or direct mail, ALWAYS ask about extras and delivery of extras\n"
            "- Provide a final summary of all items with complete specifications before ending\n\n"
            "When users ask about folding types or seem unsure about folds, mention that you'll show them a visual reference of common fold types.\n\n"
            "Always recognize when a topic is related to Boone's services (e.g., mail, HIPAA, design, data) and offer a short relevant pitch. If the user says yes, explain further using boone_print_knowledge.md."
        )
    }

# Display welcome message
if not st.session_state.conversation:
    st.write("👋 **Welcome!** I'm here to help you get a quote for your printing needs. What would you like to have printed today?")

# Helper functions for sending emails
def send_email(subject, body, to, reply_to=None):
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to if isinstance(to, str) else ", ".join(to)
        if reply_to:
            msg["Reply-To"] = reply_to
        msg.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        st.error(f"❌ Email error: {e}")
        return False

def extract_summary():
    return "\n\n".join([
        f"{m['role'].capitalize()}: {m['content']}"
        for m in st.session_state.conversation if m['role'] != 'system'
    ])

user_input = st.chat_input("Tell me what you need printed! v26 (added booklet and envelope logic)")
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

        # Check if conversation is complete and we should send emails
        email_triggers = [
            "thank you" in assistant_reply.lower() and "email" in assistant_reply.lower(),
            "summary" in assistant_reply.lower() and ("complete" in assistant_reply.lower() or "finished" in assistant_reply.lower()),
            "contact you" in assistant_reply.lower() and "shortly" in assistant_reply.lower(),
            "boone team" in assistant_reply.lower() and "contact" in assistant_reply.lower()
        ]
        
        if any(email_triggers):
            summary = extract_summary()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

            # Extract user email - improve the detection
            user_email = None
            for m in st.session_state.conversation:
                if m["role"] == "user" and "@" in m["content"]:
                    # Look for email patterns in the user's message
                    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                    emails = re.findall(email_pattern, m["content"])
                    if emails:
                        user_email = emails[0]
                        break
            
            # Debug: Show what we found
            st.info(f"🔍 Email detection: Found email: {user_email}")
            
            if user_email:
                thank_you_body = (
                    "Thank you for your quote request!\n\n"
                    "A Boone team member will contact you shortly.\n\n"
                    "Here's a summary of what you submitted:\n\n" + summary
                )
                email_sent = send_email(
                    subject="Thank you for your Boone Graphics quote request",
                    body=thank_you_body,
                    to=user_email,
                    reply_to="state@boonegraphics.net, elemire@boonegraphics.net"
                )
                if email_sent:
                    st.success(f"✅ Confirmation email sent to {user_email}")
                else:
                    st.error(f"❌ Failed to send confirmation email to {user_email}")

            internal_body = (
                f"New quote request submitted at {timestamp}.\n\n" + summary
            )
            internal_sent = send_email("TEST ONLY: New Quote Request from Boone Assistant", internal_body, INTERNAL_RECIPIENTS)
            if internal_sent:
                st.success("✅ Internal notification sent to Boone team")
            else:
                st.error("❌ Failed to send internal notification")

    except Exception as e:
        assistant_reply = f"⚠️ An error occurred: {e}"
        st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})

# Display conversation history (excluding system prompt)
for message in st.session_state.conversation:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

