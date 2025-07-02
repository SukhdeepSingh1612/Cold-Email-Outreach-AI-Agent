
# Visexa AI Cold Email Outreach App

### Deployed on streamlit : https://cold-email-outreach-ai-agent-xxnxjfw6acarjsjansrkvb.streamlit.app/

This is a Streamlit-based AI-powered tool for generating and sending professional cold emails for Visexa AI. The app uses multiple AI agents to:
- Write personalized cold emails
- Craft subject lines
- Format emails into beautiful HTML
- Send the emails via SendGrid

## 🧠 Features

- Multiple AI agents simulate different email writing styles
- Subject line and HTML email formatting agents
- Auto-selection of the best email
- Emails sent using SendGrid
- Responsive UI built with Streamlit

## 📦 Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt` (you must create one, see below)
- `.env` file with SendGrid API key and OPENAI API key

## 🔐 Environment Variables

Create a `.env` file with:

```
SENDGRID_API_KEY=your_sendgrid_api_key
OPENAI_API_KEY=your_openai_api_key
```

## 🚀 Running the App

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run app.py
```

## 🧰 Required Files

- `app.py`: Main Streamlit app file (your code above)
- `agents.py`: Should contain the Agent, Runner, trace, function_tool definitions

## 📄 requirements.txt (example)

```
streamlit
python-dotenv
openai
sendgrid
```

## ✉️ Output

The app:
- Gathers sender and recipient details
- Creates 3 email drafts via AI agents
- Picks the best one based on clarity, tone, CTA
- Generates a subject line and HTML version
- Sends the final email using SendGrid

---

Made with ❤️ by the Visexa AI team
