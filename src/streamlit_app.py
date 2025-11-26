import streamlit as st
import asyncio
import os
import sys

# Add the project root to the python path to ensure imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import CalculatorAgent

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
                # Define a wrapper to run the agent in the new loop
                async def run_agent_task(user_prompt):
                    # Instantiate agent HERE so it binds to the correct loop
                    agent = CalculatorAgent()
                    return await agent.process_command(user_prompt)

                # Run the wrapper
                response_data = asyncio.run(run_agent_task(prompt))
                
                # Extract result and steps
                output_text = response_data
                
                st.markdown(output_text)
                
                # Check for graph image in the output text
                image_path = None
                if "[GRAFIK]:" in output_text:
                    parts = output_text.split("[GRAFIK]:")
                    if len(parts) > 1:
                        potential_path = parts[1].strip()
                        if os.path.exists(potential_path):
                            st.image(potential_path)
                            image_path = potential_path
                
                # Add assistant message to history
                message_data = {"role": "assistant", "content": output_text}
                if image_path:
                    message_data["image"] = image_path
                st.session_state.messages.append(message_data)

            except Exception as e:
                error_msg = f"❌ Hata: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
