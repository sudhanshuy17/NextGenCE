import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import streamlit as st
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.memory import VectorStoreRetrieverMemory
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.schema import Document
from personas import personas
#from voice import VoiceSystem

# Runtime error fix for asyncio event loop in Streamlit threads
import asyncio
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# ======================
# 1. Advanced Configuration
# ======================
@st.cache_resource
def setup_advanced_gemini():
    google_api_key = st.secrets.get("GEMINI_API_KEY")
    if not google_api_key:
        st.error("GEMINI_API_KEY not found in Streamlit secrets!")
        st.stop()
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=google_api_key,
        temperature=0.8,
        top_p=0.95,
        max_output_tokens=2048
    )

# ======================
# 2. Memory & Persona System
# ======================
class AdvancedChatSystem:
    def __init__(self):
        google_api_key = st.secrets.get("GEMINI_API_KEY")
        if not google_api_key:
            st.error("GEMINI_API_KEY not found in Streamlit secrets!")
            st.stop()
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=google_api_key
        )
        self.memory_store = None
        self.personas = personas
        self.emotion_history = []

    def update_memory(self, text):
        doc = Document(
            page_content=text,
            metadata={"timestamp": datetime.now().isoformat()}
        )
        if self.memory_store is None:
            self.memory_store = FAISS.from_documents([doc], self.embeddings)
        else:
            self.memory_store.add_documents([doc])

    def get_context(self, query):
        if self.memory_store is None:
            return []
        return self.memory_store.similarity_search(query, k=5)

# ======================
# 3. Emotional Intelligence Engine
# ======================
def analyze_emotion(prompt):
    emotion_prompt = f"""
    Analyze the emotional state in this message:
    "{prompt}"
    
    Respond ONLY with one of: happy, sad, angry, anxious, neutral
    """
    llm = setup_advanced_gemini()
    result = llm.invoke(emotion_prompt)
    if not result or not hasattr(result, "content") or result.content is None:
        return "neutral"
    result_text = result.content.lower().strip()
    if result_text not in {"happy", "sad", "angry", "anxious", "neutral"}:
        return "neutral"
    return result_text

# ======================
# 4. Streamlit UI Setup
# ======================
st.set_page_config(page_title="Advanced Chat AI", page_icon="🤖", layout="wide")
st.title("🧠 Next-Gen Chat Experience")
st.title("_Designed_ by :blue[Sudhanshu] :sunglasses:")
st.caption("Persona Customization | Emotional Intelligence | Long-Term Memory")

# @st.cache_resource
# def get_voice_system():
#     return VoiceSystem()

# voice = get_voice_system()

if "chat_system" not in st.session_state:
    st.session_state.chat_system = AdvancedChatSystem()

if "voice_muted" not in st.session_state:
    st.session_state.voice_muted = False

with st.sidebar:
    st.header("⚙️ Personality Settings")
    selected_persona = st.selectbox(
        "Choose Persona",
        options=list(st.session_state.chat_system.personas.keys()),
        index=0
    )
    emotion_enabled = st.checkbox("Enable Emotional AI", True)
    st.subheader("🧠 Memory Settings")
    memory_length = st.slider("Memory Context (messages)", 5, 50, 20)
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Chat cleared! I'm ready for a fresh start.",
            "emotion": "neutral"
        }]
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! I'm your adaptive AI companion. How can I assist you today?",
        "emotion": "neutral"
    }]

for msg in st.session_state.messages[-memory_length:]:
    emoji = {
        "happy": "😊", "sad": "😢", "angry": "😠", "anxious": "😰", "neutral": "😐"
    }.get(msg["emotion"], "🤖")
    with st.chat_message(msg["role"], avatar=emoji):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            st.caption(f"Persona: {selected_persona.capitalize()} | Emotion: {msg['emotion'].capitalize()}")

prompt = st.chat_input("Type your message...")

# audio_file = voice.record_audio(label="🎤 Upload/Record your message", key="audio_recorder")
# if audio_file:
#     user_voice_text = voice.speech_to_text(audio_file)
#     if user_voice_text:
#         prompt = user_voice_text
#         st.info(f"Recognized voice input: {user_voice_text}")

if prompt:
    current_emotion = analyze_emotion(prompt) if emotion_enabled else "neutral"
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "emotion": current_emotion
    })
    st.session_state.chat_system.update_memory(prompt)
    persona = st.session_state.chat_system.personas[selected_persona]
    context = st.session_state.chat_system.get_context(prompt)
    full_prompt = f"""
    {persona}
    
    Emotional Context: {current_emotion}
    
    Conversation History:
    {[msg['content'] for msg in st.session_state.messages[-memory_length:]]}
    
    Relevant Context:
    {[doc.page_content for doc in context]}
    
    Current Message: {prompt}
    
    Response:
    """
    llm = setup_advanced_gemini()
    with st.spinner("💭 Processing..."):
        try:
            response = llm.invoke(full_prompt)
            if not response or not hasattr(response, "content") or response.content is None:
                st.error("LLM did not return a valid response.")
            else:
                response_emotion = analyze_emotion(response.content) if emotion_enabled else "neutral"
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.content,
                    "emotion": response_emotion
                })
                st.rerun()
        except Exception as e:
            st.error(f"System Error: {str(e)}")