import datetime
import os
from weather import get_weather, format_weather
from utilities import Utilities  
import re


class TextAssistant:
    def __init__(self):
        self.running = True
        self.utils = Utilities()

    def get_time(self):
        now= datetime.datetime.now()
        return now.strftime("Current time: %I:%M %p")

    def get_date(self):
        today=datetime.date.today()
        return today.strftime("Today's date: %B %d, %Y")

    def extract_city(self,command):
        words = command.split()
        if "in" in words:
            city_index = words.index("in") + 1
            if city_index < len(words):
                return ' '.join(words[city_index:])
            
    def handle_weather(self, command):
            """Handle weather requests"""
            city = self.extract_city(command)
            if not city:
                return "Please specify a city. Example: 'weather in london'"
            
            weather_data = get_weather(city)
            return format_weather(weather_data)    

    def show_help(self):
            """Show available commands"""
            return """
    Available commands:
    - time: Get current time
    - date: Get current date  
    - weather in [city]: Get weather for a city (e.g., 'weather in london')
    - commands: Show this help message
    - exit: Quit the assistant
    -"news" or "latest news"
    -"tech news" or "technology news"
    -"sports news" or "sports headlines"
    -"business news"
    -"health news"
    - "set a reminder to [task] at [HH:MM]"
    - "list my reminders"
    - "start a timer for [seconds/minutes/hours]"
    - start stopwatch
    - stop stopwatch

    """

    def handle_command(self, command):
            """Main command handler - YOU WILL EXPAND THIS"""
            command = command.lower().strip()

            
            if 'remind' in command or 'reminder' in command:
                return self.handle_reminder(command)
            
        
            elif 'timer' in command:
                return self.handle_timer(command)
            
            
            elif 'stopwatch' in command:
                return self.handle_stopwatch(command)
            
            if command == 'exit' or command == 'quit':
                self.running = False
                return "Goodbye!"
                
            elif command == 'help':
                return self.show_help()
                
            elif 'time' in command:
                return self.get_time()
                
            elif 'date' in command:
                return self.get_date()
                
            elif 'weather' in command:
                return self.handle_weather(command)
                
            else:
                return "Sorry, I don't understand that command. Type 'help' for options."
      
    def handle_reminder(self, command):
        """Handle reminder commands"""
        if 'list' in command or 'show' in command:
            return self.utils.list_reminders()
        
       
        time_match = re.search(r'at\s+(\d{1,2}:\d{2})', command)
        if time_match:
            reminder_time = time_match.group(1)
        
            text_match = re.search(r'(?:to|that|me)\s+(.+)', command)
            if text_match:
                reminder_text = text_match.group(1)
                return self.utils.set_reminder(reminder_text, reminder_time)
        
        return "Please specify time and reminder. Example: 'remind me to call mom at 15:30'"
    
    def handle_timer(self, command):
        """Handle timer commands"""
        if 'start' in command or 'set' in command:
          
            sec_match = re.search(r'(\d+)\s*(?:second|sec|minute|min|hour|hr)', command)
            if sec_match:
                seconds = int(sec_match.group(1))
              
                if 'min' in command:
                    seconds *= 60
                elif 'hour' in command or 'hr' in command:
                    seconds *= 3600
                return self.utils.start_timer(seconds)
            return "Please specify time. Example: 'set timer for 5 minutes'"
        
        elif 'check' in command or 'status' in command:
            return self.utils.check_timer()
        
        else:
            return self.utils.check_timer()
        
    def handle_stopwatch(self, command):
        """Handle stopwatch commands"""
        if 'start' in command:
            return self.utils.start_stopwatch()
        elif 'stop' in command or 'end' in command:
            return self.utils.stop_stopwatch()
        else:
            return self.utils.check_stopwatch()
    
    def check_reminders(self):
        """Check for due reminders (call this periodically)"""
        due_reminders = self.utils.get_due_reminders()
        if due_reminders:
            return "Reminder! " + ". ".join(due_reminders)
        return None
            
def main():
    assistant = TextAssistant()
    
    while assistant.running:
        try:
            command = input("\nYou: ").strip()
            if not command:
                continue
                
            response = assistant.handle_command(command)
            print(f"Assistant: {response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()