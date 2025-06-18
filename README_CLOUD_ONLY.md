☁️ Boone Quote Assistant – Cloud-Only Workflow Guide

This project is designed to always run on Streamlit Cloud, regardless of what computer you're using. This guide outlines the proper workflow for editing and deploying updates.

✅ Project URL

Live app: https://quotebot-d3abkea5apc34xk4bfa3dj.streamlit.app/

GitHub repo: https://github.com/bobtucker1129/Quote_Bot

🧩 How to Make Updates (from any machine)

1. Open the Project Folder

Use your Google Shared Drive if synced

Or clone from GitHub:

git clone https://github.com/bobtucker1129/Quote_Bot.git
cd Quote_Bot

2. Make Changes in Cursor

Open quote_bot.py, boone_print_knowledge.md, or any logic files

Edit, test logic, and save

You do not need to run locally

You do not need a .env file

3. Push Changes to GitHub

git add .
git commit -m "Describe what you changed"
git push origin main

4. Your App Updates Automatically

Streamlit Cloud watches the main branch

Your app will reflect the latest commit

Visit: https://quotebot-d3abkea5apc34xk4bfa3dj.streamlit.app/

🔐 API Key Setup (one-time)

In Streamlit Cloud:

Go to your app dashboard

Click ⋯ > Settings > Secrets

Add:

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

This will remain private and available only to your Streamlit Cloud app.

🚫 What You Don’t Need to Do

Don’t run streamlit run quote_bot.py locally

Don’t manage .env on different machines

Don’t push .env to GitHub (ever)

Don’t worry about API key rotation locally — it’s handled in Cloud Secrets

✅ Summary Workflow

Step

Tool

Edit code

Cursor (anywhere)

Commit + push to GitHub

Terminal/Cursor

App updates live

Streamlit Cloud

API key stored

Streamlit Secrets

You're all set to work from any device — Streamlit will always serve the latest version.
