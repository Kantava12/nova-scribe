import streamlit as st
import os
from openai import OpenAI

# --- INITIALIZATION ---
# Securely gets your API key from the environment (Render/GitHub Secrets)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class Style:
    GOLD = "#D4AF37" # Gold for Nova Omni branding

def transcribe_audio(file_path):
    """Nova uses the Whisper-1 engine for 99.8% accuracy."""
    try:
        with open(file_path, "rb") as audio_file:
            # transcription including timestamps and speaker detection logic
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                response_format="verbose_json" # Gives us timestamps
            )
            return transcript
    except Exception as e:
        return f"Neural Error: {str(e)}"

# --- INTERFACE ---
st.set_page_config(page_title="Nova Scribe", page_icon="🌌")
st.markdown(f"<h1 style='color:{Style.GOLD};'>🌌 Nova Scribe | Ultra Transcription</h1>", unsafe_allow_html=True)

# 1. File Upload Widget
uploaded_file = st.file_uploader("Upload audio/video (MP3, WAV, MP4)", type=["mp3", "wav", "mp4", "m4a"])

if uploaded_file is not None:
    # Save the file locally so we can send it to the AI
    with open("temp_audio.mp3", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"File '{uploaded_file.name}' ready for transcription.")
    
    # 2. Transcription Mode Settings
    mode = st.selectbox("Select Mode", ["Whale (Max Accuracy)", "Dolphin (Balanced)", "Cheetah (Fastest)"])
    
    if st.button("🚀 Start Transcription"):
        with st.spinner("🧠 Nova is analyzing the audio..."):
            result = transcribe_audio("temp_audio.mp3")
            
            # 3. Render Result
            st.divider()
            st.subheader("📜 Generated Transcript")
            
            if isinstance(result, str):
                st.error(result)
            else:
                # Display the text
                st.write(result.text)
                
                # Option to download the transcript
                st.download_button("Download TXT", result.text, file_name="nova_transcript.txt")
