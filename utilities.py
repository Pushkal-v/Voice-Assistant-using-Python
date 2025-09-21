# utilities.py
import time
import datetime
import threading
import json
import os

class Utilities:
    def __init__(self):
        self.reminders_file = "reminders.json"
        self.timers = {}
        self.stopwatch_start = None
        self.load_reminders()
    
    def load_reminders(self):
        
        try:
            if os.path.exists(self.reminders_file):
                with open(self.reminders_file, 'r') as f:
                    self.reminders = json.load(f)
            else:
                self.reminders = []
        except:
            self.reminders = []
    
    def save_reminders(self):
        
        try:
            with open(self.reminders_file, 'w') as f:
                json.dump(self.reminders, f)
        except:
            pass
    

    def set_reminder(self, reminder_text, reminder_time):
        
        try:
            reminder = {
                'text': reminder_text,
                'time': reminder_time,
                'created': datetime.datetime.now().isoformat()
            }
            self.reminders.append(reminder)
            self.save_reminders()
            return f"Reminder set for {reminder_time} to {reminder_text}"
        except:
            return "Sorry, I couldn't set the reminder"
    
    def get_due_reminders(self):
        """Check for due reminders"""
        current_time = datetime.datetime.now().strftime("%H:%M")
        due_reminders = []
        
        for reminder in self.reminders[:]: 
            if reminder['time'] == current_time:
                due_reminders.append(reminder['text'])
                self.reminders.remove(reminder)
        
        if due_reminders:
            self.save_reminders()
        
        return due_reminders
    
    def list_reminders(self):
        """List all active reminders"""
        if not self.reminders:
            return "You have no active reminders"
        
        response = "Your reminders: "
        for i, reminder in enumerate(self.reminders, 1):
            response += f"{i}. {reminder['text']} at {reminder['time']}. "
        
        return response
    
    
    def start_timer(self, seconds, timer_name="default"):
        """Start a countdown timer"""
        def timer_callback(secs, name):
            time.sleep(secs)
            if name in self.timers:
                del self.timers[name]
            
        
        if timer_name in self.timers:
            return f"Timer '{timer_name}' is already running"
        
        self.timers[timer_name] = {
            'end_time': time.time() + seconds,
            'thread': threading.Thread(target=timer_callback, args=(seconds, timer_name))
        }
        self.timers[timer_name]['thread'].start()
        
        return f"Timer '{timer_name}' set for {seconds} seconds"
    
    def check_timer(self, timer_name="default"):
        """Check time remaining on timer"""
        if timer_name not in self.timers:
            return f"No timer named '{timer_name}'"
        
        remaining = self.timers[timer_name]['end_time'] - time.time()
        if remaining <= 0:
            return "Timer has ended"
        
        return f"Time remaining: {int(remaining)} seconds"
    
    
    def start_stopwatch(self):
        """Start the stopwatch"""
        self.stopwatch_start = time.time()
        return "Stopwatch started!"
    
    def check_stopwatch(self):
        """Check stopwatch elapsed time"""
        if not self.stopwatch_start:
            return "Stopwatch not started"
        
        elapsed = time.time() - self.stopwatch_start
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        
        return f"Elapsed time: {hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def stop_stopwatch(self):
        """Stop and reset stopwatch"""
        if not self.stopwatch_start:
            return "Stopwatch not started"
        
        elapsed = self.check_stopwatch()
        self.stopwatch_start = None
        return f"Stopwatch stopped. {elapsed}"
    def delete_reminder(self, keyword):
        """Delete a reminder by keyword (text or time)"""
        keyword = keyword.lower().strip()
        deleted = []

        new_reminders = []
        for r in self.reminders:
            text_match = keyword in r["text"].lower()
            time_match = keyword in r["time"].lower()
            full_match = keyword in f"{r['text'].lower()} {r['time'].lower()}"

            if text_match or time_match or full_match:
                deleted.append(f"{r['text']} at {r['time']}")
            else:
                new_reminders.append(r)

        self.reminders = new_reminders
        self.save_reminders()

        if deleted:
            return f"Deleted reminder(s): {', '.join(deleted)}"
        else:
            return f"No reminders found matching '{keyword}'"

# Test function
def test_utilities():
    print("Testing Utilities...")
    util = Utilities()
    
    # Test reminders
    print(util.set_reminder("Call mom", "15:30"))
    print(util.list_reminders())
    
    # Test timer
    print(util.start_timer(5, "test_timer"))
    print(util.check_timer("test_timer"))
    
    # Test stopwatch
    print(util.start_stopwatch())
    time.sleep(2)
    print(util.check_stopwatch())

if __name__ == "__main__":
    test_utilities()