import streamlit as st
import os
import assemblyai as aai

# --- 1. SYSTEM CONFIGURATION ---
# Make sure you have 'ASSEMBLYAI_API_KEY' set in your Render Environment Variables
aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")

def transcribe_assembly(audio_file):
    """Nova uses AssemblyAI Universal-3-Pro for high-accuracy Clean Verbatim."""
    try:
        config = aai.TranscriptionConfig(
            # Explicitly setting the model to satisfy the API requirements
            speech_model=aai.SpeechModel.universal_3_pro,
            speaker_labels=True,      # Identifies different voices
            punctuate=True,           # Adds commas and periods
            format_text=True,         # Capitalizes sentences
            filter_profanity=False    # Vital for accurate legal/medical QC
        )
        
        transcriber = aai.Transcriber()
        
        # AssemblyAI can handle the Streamlit UploadedFile object directly
        transcript = transcriber.transcribe(audio_file, config)
        
        if transcript.status == aai.TranscriptStatus.error:
            return f"Neural Error: {transcript.error}"
            
        # Building the final text with timestamps and speaker labels
        formatted_text = ""
        for utterance in transcript.utterances:
            # Format time from milliseconds to MM:SS
            start_min = int(utterance.start / 60000)
            start_sec = int((utterance.start % 60000) / 1000)
            formatted_text += f"[{start_min:02d}:{start_sec:02d}] Speaker {utterance.speaker}: {utterance.text}\n\n"
            
        return formatted_text
    except Exception as e:
        return f"System Link Error: {str(e)}"

# --- 2. INTERFACE DESIGN ---
st.set_page_config(page_title="Nova Scribe | Assembly Edition", page_icon="🌌")

# Custom Styling for Nova
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #D4AF37;
        color: black;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='color:#D4AF37; text-align: center;'>🌌 NOVA SCRIBE | ASSEMBLY AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#00FFFF; text-align: center;'><b>Engine: Universal-3-Pro | Mode: Clean Verbatim</b></p>", unsafe_allow_html=True)

st.divider()

# File Uploader
uploaded_file = st.file_uploader("Upload Audio for Professional Transcription", type=["mp3", "wav", "m4a", "flac"])

if uploaded_file:
    st.success(f"File '{uploaded_file.name}' is ready for analysis.")
    
    if st.button("🚀 Start Professional Transcription"):
        with st.spinner("🧠 Nova is analyzing frequencies and identifying speakers..."):
            
            # Run the transcription
            result = transcribe_assembly(uploaded_file)
            
            if "Error" in result:
                st.error(result)
            else:
                st.divider()
                st.subheader("📜 Generated Transcript")
                
                # Display in a scrollable text area
                st.text_area("Final Output", result, height=500)
                
                # Download Button
                st.download_button(
                    label="📥 Download Transcript as TXT",
                    data=result,
                    file_name=f"Nova_QC_{uploaded_file.name}.txt",
                    mime="text/plain"
                )

# Sidebar Info
st.sidebar.title("🛠 System Diagnostics")
st.sidebar.info("""
- **Model**: Universal-3-Pro
- **Diarization**: Enabled (Speaker Labels)
- **Verbatim**: Clean Verbatim Settings
""")
