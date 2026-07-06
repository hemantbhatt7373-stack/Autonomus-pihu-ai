import webbrowser
import subprocess
import os
from datetime import datetime


def execute(command):

    command = command.lower()

    if "youtube" in command:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube."

    elif "google" in command:
        webbrowser.open("https://google.com")
        return "Opening Google."

    elif "notepad" in command:
        os.system("notepad")
        return "Opening Notepad."

    elif "calculator" in command:
        subprocess.Popen("calc.exe")
        return "Opening Calculator."

    elif "explorer" in command:
        os.system("explorer")
        return "Opening File Explorer."

    elif "time" in command:
        return datetime.now().strftime("Current time is %I:%M %p")

    return None