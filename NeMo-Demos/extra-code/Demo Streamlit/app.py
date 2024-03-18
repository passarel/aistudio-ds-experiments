import streamlit as st
from AudioToTextService.audio_to_text_service import AudioToTextService
import tempfile


MODEL_SERVICE_URL = "https://localhost:63361"


audio_to_text_service = AudioToTextService(MODEL_SERVICE_URL)

def main():
    st.title("English to Spanish Translator")

    uploaded_file = st.file_uploader("Choose an audio file (.mp3 only)", type="mp3")
    
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(uploaded_file.getvalue())
            st.write("Converting audio to text...")
            text = audio_to_text_service.mp3_to_text(tmp.name)
            
            if text:
                st.text_area("Text converted from audio:", text, height=150)
                
                if st.button("Send for Translation"):
                    st.write("Sending audio and text for translation....")
                    response = audio_to_text_service.send_audio_for_translation(tmp.name)
                    if 'error' in response:
                        st.error(response['message'])
                    else:
                        st.success("Translation received successfully!")
                        st.json(response)  

if __name__ == "__main__":
    main()
