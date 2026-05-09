import streamlit as st
import os
import assemblyai as aai

# --- 1. SYSTEM CONFIGURATION ---
# This pulls your key safely from Render's Environment Variables
aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")

def transcribe_assembly(audio_file):
    """Nova uses 0.7 speech_threshold for stable, high-accuracy QC labeling."""
    try:
        config = aai.TranscriptionConfig(
            speech_models=["universal-3-pro", "universal-2"], 
            speaker_labels=True,
            # 0.7 makes the AI more conservative to prevent 'phantom' speakers
            speech_threshold=0.7, 
            punctuate=True,
            format_text=True,
            filter_profanity=False
        )
        
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file, config)
        
        if transcript.status == aai.TranscriptStatus.error:
            return f"Neural Error: {transcript.error}"
            
        formatted_text = f"*** Processed via {getattr(transcript, 'speech_model_used', 'universal-3-pro')} ***\n\n"
        
        for utterance in transcript.utterances:
            seconds = int(utterance.start / 1000)
            hh = seconds // 3600
            mm = (seconds % 3600) // 60
            ss = seconds % 60
            
            # Simple conversion: A=1, B=2, C=3...
            speaker_num = ord(utterance.speaker) - 64 
            
            formatted_text += f"{hh:02d}:{mm:02d}:{ss:02d} S{speaker_num}: {utterance.text}\n\n"
            
        return formatted_text
    except Exception as e:
        return f"System Link Error: {str(e)}"
            
        formatted_text = f"*** Processed via {getattr(transcript, 'speech_model_used', 'universal-3-pro')} ***\n\n"
        
        for utterance in transcript.utterances:
            # Precise HH:MM:SS formatting
            seconds = int(utterance.start / 1000)
            hh = seconds // 3600
            mm = (seconds % 3600) // 60
            ss = seconds % 60
            
            # Labeling as S1, S2, etc.
            speaker_num = ord(utterance.speaker) - 64 
            
            formatted_text += f"{hh:02d}:{mm:02d}:{ss:02d} S{speaker_num}: {utterance.text}\n\n"
            
        return formatted_text
    except Exception as e:
        return f"System Link Error: {str(e)}"
            
        formatted_text = f"*** Processed via {getattr(transcript, 'speech_model_used', 'universal-3-pro')} ***\n\n"
        
        for utterance in transcript.utterances:
            seconds = int(utterance.start / 1000)
            hh = seconds // 3600
            mm = (seconds % 3600) // 60
            ss = seconds % 60
            
            # Labeling as S1, S2, etc.
            speaker_num = ord(utterance.speaker) - 64 
            
            formatted_text += f"{hh:02d}:{mm:02d}:{ss:02d} S{speaker_num}: {utterance.text}\n\n"
            
        return formatted_text
    except Exception as e:
        return f"System Link Error: {str(e)}"
        formatted_text = f"*** Processed via {getattr(transcript, 'speech_model_used', 'universal-3-pro')} ***\n\n"
        
        for utterance in transcript.utterances:
            # Precise math for HH:MM:SS format
            seconds = int(utterance.start / 1000)
            hh = seconds // 3600
            mm = (seconds % 3600) // 60
            ss = seconds % 60
            
            # Shortening 'Speaker A' to 'S1', 'Speaker B' to 'S2', etc.
            # AssemblyAI uses letters (A, B, C), so we convert them to numbers
            speaker_num = ord(utterance.speaker) - 64 
            
            formatted_text += f"{hh:02d}:{mm:02d}:{ss:02d} S{speaker_num}: {utterance.text}\n\n"
            
        return formatted_text
    except Exception as e:
        return f"System Link Error: {str(e)}"
            
        formatted_text = ""
        # Check which model was actually used for your legal file
        model_used = getattr(transcript, 'speech_model_used', 'Universal-3-Pro')
        formatted_text += f"--- Processed via {model_used} ---\n\n"
        
        for utterance in transcript.utterances:
            start_min = int(utterance.start / 60000)
            start_sec = int((utterance.start % 60000) / 1000)
            formatted_text += f"[{start_min:02d}:{start_sec:02d}] Speaker {utterance.speaker}: {utterance.text}\n\n"
            
        return formatted_text
    except Exception as e:
        return f"System Link Error: {str(e)}"
# --- 2. INTERFACE DESIGN ---
st.set_page_config(page_title="Nova Scribe | Assembly Edition", page_icon="🌌")

# Custom Styling for the Nova Brand
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
st.markdown("<p style='color:#00FFFF; text-align: center;'><b>Engine: Universal | Status: High-Priority Active</b></p>", unsafe_allow_html=True)

st.divider()

# File Uploader
uploaded_file = st.file_uploader("Upload Audio for Professional Transcription", type=["mp3", "wav", "m4a", "flac"])

if uploaded_file:
    st.success(f"File '{uploaded_file.name}' is ready for analysis.")
    
    if st.button("🚀 Start Professional Transcription"):
        with st.spinner("🧠 Nova is analyzing frequencies and identifying speakers..."):
            
            # Run the transcription engine
            result = transcribe_assembly(uploaded_file)
            
            if "Error" in result:
                st.error(result)
            else:
                st.divider()
                st.subheader("📜 Generated Transcript")
                
                # Display result in a scrollable area for easy QC
                st.text_area("Final Output", result, height=500)
                
                # Download Button for the final TXT file
                st.download_button(
                    label="📥 Download Transcript as TXT",
                    data=result,
                    file_name=f"Nova_QC_{uploaded_file.name}.txt",
                    mime="text/plain"
                )

# Sidebar System Info
st.sidebar.title("🛠 System Diagnostics")
st.sidebar.info("""
- **Model**: Universal Stable
- **Diarization**: Enabled
- **Formatting**: Clean Verbatim
""")
