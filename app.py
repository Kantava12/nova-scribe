import streamlit as st
import os
from google import genai
from google.genai import types

# --- NEURAL CONFIGURATION ---
# This pulls your free key from the Render Environment Variables
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

class Style:
    GOLD = "#D4AF37"
    CYAN = "#00FFFF"

def transcribe_keyless(audio_bytes, mime_type):
    """Nova uses Gemini 2.0 Flash to transcribe without external keys."""
    try:
        # We wrap the data in types.Part to satisfy all 18 validation rules
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Part.from_bytes(
                    data=audio_bytes,
                    mime_type=mime_type
                ),
                "Role: Professional Transcriptionist. "
                "Task: Provide a 'Clean Verbatim' transcript of this audio. "
                "Format: Include speaker labels (e.g., Speaker 1, Speaker 2) and timestamps. "
                "Rules: Fix stutters and filler words (um, uh) but keep all legal/technical terminology intact."
            ]
        )
        return response.text
    except Exception as e:
        return f"Neural Link Error: {str(e)}"

# --- INTERFACE DESIGN ---
st.set_page_config(page_title="Nova Scribe Omni", page_icon="🌌")

st.markdown(f"""
    <h1 style='color:{Style.GOLD}; text-align: center;'>🌌 NOVA SCRIBE | OMNI EDITION</h1>
    <p style='color:{Style.CYAN}; text-align: center;'><b>Status: Keyless Mode Active | Engine: Gemini 2.0 Flash</b></p>
    """, unsafe_allow_html=True)

st.divider()

# File Uploader
uploaded_file = st.file_uploader("Drop your audio file here (MP3, WAV, M4A)", type=["mp3", "wav", "m4a"])

if uploaded_file:
    st.success(f"File '{uploaded_file.name}' loaded into the swarm.")
    
    # Determine the correct MIME type for Gemini
    file_ext = uploaded_file.name.split('.')[-1].lower()
    if file_ext == "m4a":
        mime_type = "audio/m4a"
    elif file_ext == "wav":
        mime_type = "audio/wav"
    else:
        mime_type = "audio/mp3"

    if st.button("🚀 Start God-Mode Transcription"):
        with st.spinner("🧠 Nova is analyzing the neural frequencies..."):
            # Convert the uploaded file to bytes
            audio_bytes = uploaded_file.getvalue()
            
            # Call the transcription function
            result = transcribe_keyless(audio_bytes, mime_type)
            
            st.divider()
            st.subheader("📜 Transcription Results")
            st.write(result)
            
            # Download Button
            st.download_button(
                label="📥 Download Transcript as TXT",
                data=result,
                file_name=f"Nova_{uploaded_file.name}.txt",
                mime="text/plain"
            )

st.sidebar.markdown(f"""
    ### 🛠 System Info
    - **QC Ready**: Clean Verbatim enabled
    - **Cost**: $0.00 (Free Tier)
    - **Limit**: ~1 hour per file
    """)
