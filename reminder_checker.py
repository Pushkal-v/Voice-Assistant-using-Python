import datetime
import time
import threading
import pyttsx3
import json

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def reminder_checker(reminders_file="reminders.json"):
    while True:
        try:
            # Load reminders from JSON file
            with open(reminders_file, "r") as f:
                reminders = json.load(f)

            now = datetime.datetime.now().strftime("%H:%M")

            for r in reminders[:]:
                if r["time"] == now:
                    print(f"🔔 Reminder: {r['task']} at {r['time']}")
                    speak(f"Reminder: {r['task']} at {r['time']}")

                    # remove reminder after alert
                    reminders.remove(r)

                    with open(reminders_file, "w") as f:
                        json.dump(reminders, f, indent=4)

        except (FileNotFoundError, json.JSONDecodeError):
            pass  # no reminders yet

        time.sleep(30)  # check every 30s

def start_checker():
    threading.Thread(target=reminder_checker, daemon=True).start()
