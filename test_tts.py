# test_tts.py
import pyttsx3

def test_text_to_speech():
    print("Testing text-to-speech...")
    
    # Initialize the engine
    engine = pyttsx3.init()
    
    # Test basic speech
    engine.say("Hello! I am your voice assistant. Can you hear me?")
    print("Speaking: Hello! I am your voice assistant.")
    
    # Run and wait for speech to finish
    engine.runAndWait()
    print("Test completed.")

if __name__ == "__main__":
    test_text_to_speech()