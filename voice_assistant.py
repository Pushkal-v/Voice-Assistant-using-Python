from text_assistant import TextAssistant
from news_reader import NewsReader 
from utilities import Utilities  # Import the Utilities class
import speech_recognition as sr
import pyttsx3
import time
import threading
import datetime



class Voice_assistant(TextAssistant):
    def __init__(self):
        super().__init__()
        
        self.active_timer = None
        self.utils = Utilities()  # Create Utilities instance
        self.news_reader = NewsReader()
        
        self.recognizer = sr.Recognizer()
        try:
            self.microphone = sr.Microphone(device_index=0)
            self.has_microphone = True
            print("✅ Microphone ready!")
        except:
            self.has_microphone = False
            print("⚠️  Microphone not available - text mode")
        
        
        self.speak("Hello! I'm your voice assistant . How can I help you today?")  
    
    def speak(self, text):
        print(f"Assistant: {text}")
        try:
            tts = pyttsx3.init()
            tts.say(text)
            tts.runAndWait()
        except Exception as e:
            print(f" TTS Error: {e}")
    
    def listen(self):
        if not self.has_microphone:
            return input("You (type): ").strip().lower()
        
        print("🎤 Listening...")
        
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=6)
                text = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {text}")
                return text
                
        except sr.WaitTimeoutError:
            print("⏰ Timeout - no voice input")
            return None
        except sr.UnknownValueError:
            print(" Could not understand audio")
            return None
        except Exception as e:
            print(f" Error: {e}")
            return None
    
    def handle_command(self, command):  
        """Handle commands including NEWS"""
        command = command.lower().strip()
    
        if 'timer' in command and 'for' in command:
            try:
                # Extract seconds
                parts = command.split('for')
                time_str = parts[1].strip()
                
                if 'second' in time_str:
                    seconds = int(time_str.split()[0])
                elif 'minute' in time_str:
                    seconds = int(time_str.split()[0]) * 60
                else:
                    seconds = int(time_str.split()[0])  # Assume seconds
                    
                return self.start_timer(seconds)
            except:
                return "Say: 'set timer for 30 seconds' or 'timer for 2 minutes'"
        
        # REMINDER COMMANDS
        elif 'remind' in command:
            if 'list' in command:
                return self.utils.list_reminders()
            elif 'delete' in command:
                try:
                    keyword = command.replace('delete reminder', '').strip()
                    if not keyword:
                        return "Please say: 'delete reminder dance' or 'delete reminder at 14:30'"
                    return self.utils.delete_reminder(keyword)
                except:
                    return "Sorry, I couldn't delete the reminder"
            elif 'at' in command:
                try:
                    parts = command.split('at')
                    text_part = parts[0].replace('remind me to', '').strip()
                    time_part = parts[1].strip()[:5]  # Get only HH:MM
                    return self.utils.set_reminder(text_part, time_part)
                except:
                    return "Say: 'remind me to call mom at 14:30'"
        
        # NEWS COMMANDS
        if any(word in command for word in ['news', 'headlines', 'update']):
            topic = self.news_reader.extract_topic(command)
            print(f"🎯 News topic: {topic}")
            news_items = self.news_reader.get_news(topic=topic)
            return self.news_reader.format_news_response(news_items, topic)
        
        return super().handle_command(command)
    
    def get_input(self):
        """Get input with proper fallback to text"""        
        if self.has_microphone:
            command = self.listen()
            if command is not None:
                return command
        
        try:
            print("Type your command or press Enter to try voice again:")
            command = input().strip().lower()
            return command if command else None
        except:
            return None
    
    def run(self):
        """Main loop with news functionality"""
        while True:
            try:
                # Check for due reminders using Utilities
                self.check_notifications()
                
                # Get input (voice or text)                
                command = self.get_input()
                
                if command is None:
                    continue
                
                if any(word in command for word in ['exit', 'quit', 'goodbye']):
                    self.speak("Goodbye! Have a great day!")
                    break
                
                response = self.handle_command(command)
                self.speak(response)
                
                time.sleep(1)
                
            except KeyboardInterrupt:
                self.speak("Goodbye!")
                break
            except Exception as e:
                self.speak("Sorry, I encountered an error")
                print(f"Error: {e}")
    
    def start_timer(self, seconds):
        """Start a timer that speaks when done"""
        # Cancel any existing timer
        if self.active_timer:
            return "A timer is already running!"
        
        # Create timer thread
        def timer_complete():
            time.sleep(seconds)
            self.speak(f"⏰ Timer completed! {seconds} seconds are up!")
            self.active_timer = None
        
        self.active_timer = threading.Thread(target=timer_complete)
        self.active_timer.daemon = True  # Allows program to exit while timer runs
        self.active_timer.start()
        
        return f"Timer set for {seconds} seconds"
    
    def check_notifications(self):
        """Check for due reminders using Utilities"""
        due_reminders = self.utils.get_due_reminders()
        for reminder in due_reminders:
            self.speak(f"🔔 REMINDER: {reminder}")

if __name__ == "__main__":
    assistant = Voice_assistant()
    assistant.run()