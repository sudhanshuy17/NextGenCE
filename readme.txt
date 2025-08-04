# NextGenCE `Chatbot`

A powerful, customizable conversational AI app built with [Streamlit](https://streamlit.io/) and [Google Gemini](https://ai.google.dev/gemini-api/), featuring:

- **Persona Customization:** Choose from multiple expert personas for tailored responses.
- **Emotional Intelligence:** The bot analyzes and adapts to user emotions.
- **Long-Term Memory:** Uses vector memory to remember and reference past conversations.
- **(Optional) Voice Input/Output:** Easily extendable for speech-to-text and text-to-speech.

---

## 🚀 Features

- **Conversational AI** powered by Google Gemini (via LangChain).
- **Multiple Personas:** Switch between expert roles (Python Expert, ML Engineer, Consultant, etc.).
- **Emotion Analysis:** Detects user emotion and adapts responses.
- **Memory:** Remembers previous messages for context-aware replies.
- **Streamlit UI:** Clean, interactive chat interface.

---

## 🛠️ Setup Instructions

### 1. **Clone the Repository**
```bash
git clone https:REPO
cd gemini-app

### 2. Install Dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r [requirements.txt](http://_vscodecontentref_/0)

### 3. Configure API keys
Create a .streamlit/secrets.toml file:
GEMINI_API_KEY = "your_google_gemini_api_key_here"

### 4. Run the app
streamlit run [app.py](http://_vscodecontentref_/1)

----
## 🤖 File Structure 

gemini-app/
│
├──               # Main Streamlit app
├──          # Persona prompt definitions
├──             # (Optional) Voice input/output utilities
├──     # Python dependencies
└── .streamlit/
    └── secrets.toml    # API keys (not tracked by git)

----
## 📝 Customization
Add/Edit Personas:
Edit personas.py to add new expert roles or modify existing ones.

Change LLM Model:
To use OpenAI GPT-4o or another model, swap out the LangChain LLM and embedding classes in app.py.

Enable Voice:
Uncomment and use the VoiceSystem in voice.py and app.py for speech features.

----
🙏 Credits
Streamlit
LangChain
Google Gemini API
FAISS
OpenAI Whisper (for optional voice features)

----
Made with ❤️ by Sudhanshu Yadav

