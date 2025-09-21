# microphone_diagnostic.py
import speech_recognition as sr
import pyaudio

print("=== Microphone Diagnostic Tool ===")

# 1. Check PyAudio installation
try:
    p = pyaudio.PyAudio()
    print("✅ PyAudio is installed correctly")
    p.terminate()
except Exception as e:
    print(f"❌ PyAudio error: {e}")

# 2. List available microphones
print("\nAvailable microphones:")
try:
    mic_list = sr.Microphone.list_microphone_names()
    for i, mic in enumerate(mic_list):
        print(f"{i}: {mic}")
    
    # 3. Test each microphone
    print("\nTesting microphones (say 'test' after each prompt):")
    for i, mic_name in enumerate(mic_list):
        try:
            print(f"\nTesting microphone {i}: {mic_name}")
            with sr.Microphone(device_index=i) as source:
                recognizer = sr.Recognizer()
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Please say 'test' now...")
                audio = recognizer.listen(source, timeout=3)
                text = recognizer.recognize_google(audio).lower()
                if 'test' in text:
                    print(f"✅ WORKING: Heard '{text}'")
                else:
                    print(f"⚠️  Heard something else: '{text}'")
                    
        except sr.WaitTimeoutError:
            print("⏰ No sound detected")
        except sr.UnknownValueError:
            print("❌ Sound detected but not understood")
        except Exception as e:
            print(f"❌ Error with mic {i}: {e}")
            
except Exception as e:
    print(f"❌ Failed to list microphones: {e}")

print("\n=== Diagnostic Complete ===")