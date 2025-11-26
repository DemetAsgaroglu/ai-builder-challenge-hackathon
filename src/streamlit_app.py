import streamlit as st
import asyncio
import os
import sys

# Add the project root to the python path to ensure imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.agent import GeminiAgent
from src.utils.logger import setup_logger

# Page Configuration
st.set_page_config(
    page_title="AI Calculator Agent",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #e6f3ff;
    }
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background-color: #f0f2f6;
    }
    h1 {
        color: #4F8BF9;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = GeminiAgent()

# Sidebar
with st.sidebar:
    st.title("🧮 AI Calculator")
    st.markdown("---")
    st.markdown("### 📚 Özellikler")
    st.markdown("- **Matematik**: `2 + 2`, `sqrt(16)`")
    st.markdown("- **Kalkülüs**: `x^2 türevi`, `integral x`")
    st.markdown("- **Lineer Cebir**: `[[1,2],[3,4]] det`")
    st.markdown("- **Finans**: `1000 TL %10 faiz`")
    st.markdown("- **İstatistik**: `[1,2,3] ortalama`")
    st.markdown("- **Grafik**: `sin(x) çiz`")
    st.markdown("---")
    if st.button("🗑️ Geçmişi Temizle"):
        st.session_state.messages = []
        st.rerun()

# Main Chat Interface
st.title("💬 AI Calculator Agent")
st.caption("Google Gemini destekli akıllı hesaplama asistanı")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"])

# Handle User Input
if prompt := st.chat_input("Bir işlem yazın (örn: x^2 grafiğini çiz)..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Hesaplanıyor..."):
            try:
                # Create a new event loop for this thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response_data = loop.run_until_complete(st.session_state.agent.process_command(prompt))
                loop.close()
                
                # Extract result and steps
                result_text = response_data.get("result", "İşlem tamamlandı.")
                steps = response_data.get("steps", [])
                
                # Format output
                output_text = f"**Sonuç:** `{result_text}`\n\n"
                if steps:
                    output_text += "**Adımlar:**\n"
                    for step in steps:
                        output_text += f"- {step}\n"
                
                st.markdown(output_text)
                
                # Check for graph image
                image_path = None
                # Check if result looks like a file path to a png
                if isinstance(result_text, str) and result_text.endswith(".png") and "cache" in result_text:
                     # Fix path for display if needed, or just use it if absolute/relative works
                     if os.path.exists(result_text):
                         st.image(result_text)
                         image_path = result_text
                
                # Add assistant message to history
                message_data = {"role": "assistant", "content": output_text}
                if image_path:
                    message_data["image"] = image_path
                st.session_state.messages.append(message_data)

            except Exception as e:
                error_msg = f"❌ Hata: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

