import streamlit as st
import os
import assemblyai as aai

# --- 1. SYSTEM CONFIGURATION ---
aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")

def transcribe_assembly(audio_file):
    """Nova uses AssemblyAI Universal-3-Pro for high-accuracy Clean Verbatim."""
    try:
        # Using the direct string 'universal_3_pro' to prevent attribute errors
        config = aai.TranscriptionConfig(
            speech_model="universal_3_pro", 
            speaker_labels=True,
            punctuate=True,
            format_text=True,
            filter_profanity=False
        )
        
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file, config)
        
        if transcript.status == aai.TranscriptStatus.error:
            return f"Neural Error: {transcript.error}"
            
        formatted_text = ""
        for utterance in transcript.utterances:
            start_min = int(utterance.start / 60000)
            start_sec = int((utterance.start % 60000) / 1000)
            formatted_text += f"[{start_min:02d}:{start_sec:02d}] Speaker {utterance.speaker}: {utterance.text}\n\n"
            
        return formatted_text
    except Exception as e:
        return f"System Link Error: {str(e)}"

# --- 2. INTERFACE DESIGN ---
st.set_page_config(page_title="Nova Scribe | Assembly Edition", page_icon="🌌")

st.markdown("<h1 style='color:#D4AF37; text-align: center;'>🌌 NOVA SCRIBE | ASSEMBLY AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#00FFFF; text-align: center;'><b>Engine: Universal-3-Pro | Status: Online</b></p>", unsafe_allow_html=True)

st.divider()

uploaded_file = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a", "flac"])

if uploaded_file:
    st.success(f"File '{uploaded_file.name}' is ready for analysis.")
    
    if st.button("🚀 Start Professional Transcription"):
        with st.spinner("🧠 Nova is analyzing frequencies and identifying speakers..."):
            result = transcribe_assembly(uploaded_file)
            
            if "Error" in result:
                st.error(result)
            else:
                st.divider()
                st.subheader("📜 Generated Transcript")
                st.text_area("Final Output", result, height=500)
                st.download_button("📥 Download Transcript", result, file_name=f"Nova_{uploaded_file.name}.txt")
