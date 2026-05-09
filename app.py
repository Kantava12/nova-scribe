def transcribe_assembly(audio_file):
    """Nova uses AssemblyAI Universal-3-Pro for high-accuracy QC work."""
    try:
        config = aai.TranscriptionConfig(
            # This line specifically fixes the "speech_models" error
            speech_model=aai.SpeechModel.universal_3_pro, 
            speaker_labels=True,
            punctuate=True,
            format_text=True
        )
        
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file, config)
        
        if transcript.status == aai.TranscriptStatus.error:
            return f"Neural Error: {transcript.error}"
            
        formatted_text = ""
        for utterance in transcript.utterances:
            # Converting milliseconds to MM:SS format
            start_min = int(utterance.start / 60000)
            start_sec = int((utterance.start % 60000) / 1000)
            formatted_text += f"[{start_min:02d}:{start_sec:02d}] Speaker {utterance.speaker}: {utterance.text}\n\n"
            
        return formatted_text
    except Exception as e:
        return f"System Link Error: {str(e)}"
