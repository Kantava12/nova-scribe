import streamlit as st
import os
import assemblyai as aai

# --- CONFIGURATION ---
aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")

def transcribe_assembly(audio_file):
    """Nova uses AssemblyAI for professional Clean Verbatim."""
    try:
        config = aai.TranscriptionConfig(
            speaker_labels=True,      # Identifies Speaker A, Speaker B
            punctuate=True,
            format_text=True,
            filter_profanity=False    # Good for legal/QC files
        )
        
        transcriber = aai.Transcriber()
        # Uploads directly from the Streamlit file buffer
        transcript = transcriber.transcribe(audio_file, config)
        
        if transcript.status == aai.TranscriptStatus.error:
            return f"Neural Error: {transcript.error}"
            
        # Format the output with Speaker Labels and Timestamps
        formatted_text = ""
        for utterance in transcript.utterances:
            start_min = int(utterance.start / 60000)
            start_sec = int((utterance.start % 60000) / 1000)
            formatted_text += f"[{start_min:02d}:{start_sec:02d}] Speaker {utterance.speaker}: {utterance.text}\n\n"
            
        return formatted_text
    except Exception as e:
        return f"System Link Error: {str(e)}"

# --- INTERFACE ---
st.set_page_config(page_title="Nova Scribe | Assembly Edition", page_icon="🌌")
st.markdown("<h1 style='color:#D4AF37;'>🌌 NOVA SCRIBE | ASSEMBLY AI</h1>", unsafe_allow_html=True)
st.info("System: Using AssemblyAI Professional Engine (Clean Verbatim Enabled)")

uploaded_file = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a"])

if uploaded_file:
    if st.button("🚀 Start Transcription"):
        with st.spinner("🧠 Nova is analyzing voices..."):
            # We pass the file object directly to AssemblyAI
            result = transcribe_assembly(uploaded_file)
            
            st.divider()
            st.subheader("📜 Professional Transcript")
            st.text_area("Transcript Output", result, height=400)
            st.download_button("📥 Download Transcript", result, file_name="Nova_QC_Transcript.txt")
