import streamlit as st
import os
from google import genai

# --- INITIALIZATION ---
# Connects to your GOOGLE_API_KEY from Render Environment
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

def transcribe_keyless(file_path, mime_type):
    """Nova uses Gemini's internal engine (No OpenAI key needed)."""
    try:
        with open(file_path, "rb") as f:
            audio_data = f.read()
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                "Transcribe this audio with speaker labels and timestamps.",
                {"mime_type": mime_type, "data": audio_data}
            ]
        )
        return response.text
    except Exception as e:
        return f"Neural Error: {str(e)}"

st.title("🌌 Nova Scribe | Omni Edition")
st.info("System: Using Gemini Engine (Keyless Mode)")

uploaded_file = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a"])

if uploaded_file:
    if st.button("🚀 Start Transcription"):
        with st.spinner("Processing..."):
            # Determine mime type and transcribe
            m_type = f"audio/{uploaded_file.name.split('.')[-1]}"
            with open("temp_file", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            result = transcribe_keyless("temp_file", m_type)
            st.write(result)
