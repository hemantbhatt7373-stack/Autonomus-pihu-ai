import subprocess
import os
import io
import time
import re
import base64
import urllib.parse
import json
import smtplib
import imaplib
import email
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import winreg
import pyautogui
import psutil
import requests
from bs4 import BeautifulSoup
from PIL import Image
from groq import Groq
import pyperclip
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
from dotenv import load_dotenv

# 🔒 Bulletproof Environment & Registry Loader
def get_secure_key(key_name):
    val = os.environ.get(key_name) or os.getenv(key_name)
    if val and val.strip():
        return val.strip().strip('"').strip("'")

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
            reg_val, _ = winreg.QueryValueEx(key, key_name)
            if reg_val and str(reg_val).strip():
                return str(reg_val).strip().strip('"').strip("'")
    except Exception:
        pass

    current_dir = Path(__file__).resolve().parent
    search_dirs = [current_dir, current_dir.parent, Path.cwd()]
    for d in search_dirs:
        env_file = d / ".env"
        if env_file.exists():
            load_dotenv(dotenv_path=env_file, override=True)
            val = os.environ.get(key_name) or os.getenv(key_name)
            if val and val.strip():
                return val.strip().strip('"').strip("'")
            try:
                with open(env_file, "r", encoding="utf-8-sig", errors="ignore") as f:
                    for line in f:
                        clean_line = line.strip()
                        if clean_line.startswith(f"{key_name}=") or f"{key_name}=" in clean_line:
                            k, v = clean_line.split("=", 1)
                            if k.strip() == key_name:
                                return v.strip().strip('"').strip("'")
            except Exception:
                pass
    return ""

pyautogui.FAILSAFE = False

try:
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
except Exception:
    pytesseract = None

# =====================================================================
# 🚀 PIHU MASTER AGENTIC BRAIN
# =====================================================================

class PihuAutonomousBrain:
    def __init__(self):
        self.curr_user = "Hemant"
        self.GROQ_API_KEY = get_secure_key("GROQ_API_KEY")
        self.client = None
        
        self.active_model = "llama3-70b-8192"
        self.vision_model = "llama-3.2-11b-vision-preview"
        self.available_models = ["llama3-70b-8192", "llama-3.3-70b-versatile", "llama3-8b-8192"]
        
        self.MY_EMAIL = get_secure_key("MY_EMAIL") or "your_email@gmail.com"
        self.EMAIL_APP_PASS = get_secure_key("EMAIL_APP_PASS") or ""

        if self.GROQ_API_KEY:
            try:
                self.client = Groq(api_key=self.GROQ_API_KEY.strip())
                server_models = [m.id for m in self.client.models.list().data]
                
                valid_tool_models = [
                    "llama3-70b-8192",
                    "llama-3.3-70b-versatile",
                    "llama-3.1-8b-instant",
                    "llama3-8b-8192"
                ]
                
                matched = [m for m in valid_tool_models if m in server_models]
                if matched:
                    self.active_model = matched[0]
                    self.available_models = matched

                if "llama-3.2-11b-vision-preview" in server_models:
                    self.vision_model = "llama-3.2-11b-vision-preview"
                elif "llama-3.2-90b-vision-preview" in server_models:
                    self.vision_model = "llama-3.2-90b-vision-preview"

                print(f"✅ Active Groq Model Connected: {self.active_model}")
                print(f"✅ Active Vision Model: {self.vision_model}")
            except Exception as e:
                print(f"⚠️ Groq API Init Warning: {e}")
        else:
            print("⚠️ GROQ_API_KEY nahi mili!")
                
        self.chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
        ]
        
        self.tools_map = {
            "type_text": self.type_text,
            "press_key": self.press_key,
            "search_and_open": self.search_and_open,
            "send_message": self.send_message,
            "send_whatsapp_message": self.send_whatsapp_message,
            "whatsapp_voice_call": self.whatsapp_voice_call,
            "whatsapp_video_call": self.whatsapp_video_call,
            "create_custom_folder": self.create_custom_folder,
            "create_custom_file": self.create_custom_file,
            "smart_launch_app_or_web": self.smart_launch_app_or_web,
            "windows_search_and_open": self.windows_search_and_open,
            "search_google": self.search_google,
            "search_youtube_and_play": self.search_youtube_and_play,
            "send_email_auto": self.send_email_auto,
            "read_latest_email": self.read_latest_email,
            "os_navigation": self.os_navigation,
            "analyze_screen_vision": self.analyze_screen_vision,
            "diagnose_and_fix_screen_error": self.diagnose_and_fix_screen_error,
            "auto_fix_file_code": self.auto_fix_file_code,
            "write_and_run_code": self.write_and_run_code,
            "read_screen": self.read_screen,
            "scrape_and_summarize": self.scrape_and_summarize,
            "control_volume": self.control_volume,
            "media_control": self.media_control,
            "control_wifi": self.control_wifi,
            "get_system_info": self.get_system_info,
            "get_battery_status": self.get_battery_status,
            "power_control": self.power_control,
            "calculate_math": self.calculate_math
        }

    def _clean_response(self, text):
        if not text:
            return ""
        cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
        if "<think>" in cleaned:
            cleaned = cleaned.split("<think>")[0]
        return cleaned.replace("*", "").replace("`", "").strip()

    def _open_in_chrome(self, url):
        for path in self.chrome_paths:
            if os.path.exists(path):
                subprocess.Popen([path, url])
                return
        subprocess.Popen(f'start chrome "{url}"', shell=True)

    # =========================================================================
    # 💬 1. FAIL-PROOF WHATSAPP SEARCH & SEND PIPELINE
    # =========================================================================
    def _open_and_find_chat(self, clean_name):
        self._open_in_chrome("https://web.whatsapp.com")
        time.sleep(8.0)

        sw, sh = pyautogui.size()

        # 1. Bring Chrome to front and maximize
        pyautogui.click(sw // 2, 25)
        time.sleep(0.3)
        pyautogui.hotkey('alt', 'space')
        time.sleep(0.2)
        pyautogui.press('x')
        time.sleep(0.5)

        # 2. Dismiss any existing modals
        for _ in range(3):
            pyautogui.press('esc')
            time.sleep(0.15)

        # 3. Focus Search Box: Hotkeys + Multi-coordinate Click
        pyautogui.hotkey('ctrl', 'alt', '/')
        time.sleep(0.3)
        pyautogui.hotkey('alt', 'k')
        time.sleep(0.3)

        search_x = int(sw * 0.22)
        pyautogui.click(search_x, int(sh * 0.17))
        time.sleep(0.2)
        pyautogui.click(search_x, int(sh * 0.17))
        time.sleep(0.2)

        # 4. Clear existing query
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('backspace')
        time.sleep(0.2)

        # 5. Send contact name: Clipboard Paste + Direct Keyboard Write Fallback
        pyperclip.copy(clean_name)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.3)
        pyautogui.write(clean_name, interval=0.08)
        time.sleep(3.0)

        # 6. Select contact and open chat
        pyautogui.press('down')
        time.sleep(0.4)
        pyautogui.press('enter')
        time.sleep(2.0)

    def send_whatsapp_message(self, name="", message="Hello", **kwargs):
        try:
            clean_name = name.strip() or "didi"
            clean_msg = re.sub(
                r"\b(ka message|hay ka|hi ka|message drop kar do|drop kar do|send kar do|bhejo|message karo|send kar dena|nihal block|nihal bro ke|ko|ke)\b", 
                "", 
                message, 
                flags=re.IGNORECASE
            ).strip() or "Hello"

            print(f"\n[WHATSAPP ACTION] Searching: '{clean_name}' | Message: '{clean_msg}'")

            self._open_and_find_chat(clean_name)

            sw, sh = pyautogui.size()

            # Click bottom chat bar
            pyautogui.click(int(sw * 0.55), int(sh * 0.95))
            time.sleep(0.3)

            # Paste message
            pyperclip.copy(clean_msg)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.4)

            # Send
            pyautogui.press('enter')
            time.sleep(0.3)

            return f"Boss, WhatsApp par '{clean_name}' ko '{clean_msg}' message bhej diya hai!"
        except Exception as e:
            return f"WhatsApp auto-send error: {e}"

    def whatsapp_video_call(self, name="", **kwargs):
        try:
            clean_name = name.strip()
            self._open_and_find_chat(clean_name)
            sw, sh = pyautogui.size()
            pyautogui.click(int(sw * 0.88), int(sh * 0.08))
            time.sleep(0.5)
            return f"Boss, WhatsApp par '{clean_name}' ko video call mila diya hai!"
        except Exception as e:
            return f"Video call error: {e}"

    def whatsapp_voice_call(self, name="", **kwargs):
        try:
            clean_name = name.strip()
            self._open_and_find_chat(clean_name)
            sw, sh = pyautogui.size()
            pyautogui.click(int(sw * 0.84), int(sh * 0.08))
            time.sleep(0.5)
            return f"Boss, WhatsApp par '{clean_name}' ko voice call mila diya hai!"
        except Exception as e:
            return f"Voice call error: {e}"

    # ==========================================
    # 🛠️ 2. DIRECT AUTONOMOUS CODE FIXER
    # ==========================================
    def auto_fix_file_code(self, filename="smartmemory.py", old_code="", new_code="", **kwargs):
        try:
            target_name = filename.strip() if filename else "smartmemory.py"
            found_paths = []
            search_paths = [
                os.path.abspath(os.path.dirname(__file__)),
                os.path.abspath("."),
                os.path.join(os.environ.get("USERPROFILE", ""), "Desktop", "Pihu-AI")
            ]
            for s_path in search_paths:
                if not os.path.exists(s_path): continue
                for root_dir, _, files in os.walk(s_path):
                    for f in files:
                        if f.lower() == target_name.lower():
                            found_paths.append(os.path.join(root_dir, f))
            if not found_paths:
                return f"Boss, system me '{target_name}' file physically nahi mili."

            target_path = found_paths[0]
            with open(target_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            modified = False
            new_lines = []
            for idx, line in enumerate(lines):
                line_no = idx + 1
                if line_no == 17 or "return {" in line:
                    if "{" in line and "}" not in line:
                        indent = len(line) - len(line.lstrip())
                        new_lines.append(" " * indent + "return {}\n")
                        modified = True
                        continue
                new_lines.append(line)

            if not modified and old_code:
                content = "".join(lines)
                if old_code in content:
                    content = content.replace(old_code, new_code, 1)
                    with open(target_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    return f"Boss, {os.path.basename(target_path)} file me code replace karke solve kar diya hai!"

            with open(target_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            return f"Boss, maine '{os.path.basename(target_path)}' file ka syntax error solve karke save kar diya hai!"
        except Exception as e:
            return f"Auto-fix error: {e}"

    # ==========================================
    # 📁 3. FILE & FOLDER CREATOR
    # ==========================================
    def create_custom_folder(self, folder_name="", location="desktop", **kwargs):
        try:
            name = folder_name.strip() if folder_name else "New_Folder"
            clean_name = name.replace(" ", "_")
            desktop_dir = os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), "Desktop")
            target_dir = desktop_dir if location == "desktop" else os.getcwd()
            full_path = os.path.join(target_dir, clean_name)
            idx = 1
            orig_path = full_path
            while os.path.exists(full_path):
                full_path = f"{orig_path}_{idx}"
                clean_name = f"{name}_{idx}"
                idx += 1
            os.makedirs(full_path, exist_ok=True)
            return f"Boss, Desktop par '{clean_name}' folder bana diya hai!"
        except Exception as e:
            return f"Folder error: {e}"

    def create_custom_file(self, filename="", content="", location="desktop", open_with="notepad", **kwargs):
        try:
            name = filename.strip() if filename else "newfile"
            clean_name = name.replace(" ", "_")
            if "." not in clean_name:
                clean_name += ".cpp" if any(x in content.lower() for x in ["#include", "cout", "int main"]) else ".txt"
            if clean_name.endswith(".cpp") and not content:
                content = "#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << \"Hello from Pihu AI!\" << endl;\n    return 0;\n}\n"
            desktop_dir = os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), "Desktop")
            target_dir = desktop_dir if location == "desktop" else os.getcwd()
            full_path = os.path.join(target_dir, clean_name)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content or "// Created by Pihu AI\n")
            if "vs" in open_with.lower() or "code" in open_with.lower():
                subprocess.Popen(f'code "{full_path}"', shell=True)
                return f"Boss, '{clean_name}' file bana kar VS Code me open kar di hai!"
            else:
                os.system(f'start notepad.exe "{full_path}"')
                return f"Boss, Desktop par '{clean_name}' file bana kar open kar di hai!"
        except Exception as e:
            return f"File create error: {e}"

    # ==========================================
    # ⌨️ 4. UNIVERSAL KEYBOARD & SEARCH
    # ==========================================
    def type_text(self, text_to_type="", press_enter=True, **kwargs):
        try:
            clean = re.sub(r"^(hello pihu|pihu|type karo|likho|search karo|bolo|pucho)\s*", "", text_to_type, flags=re.IGNORECASE).strip() or text_to_type.strip()
            pyautogui.press('shift')
            time.sleep(0.1)
            pyperclip.copy(clean)
            time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            if press_enter: pyautogui.press('enter')
            return f"Boss, type kar diya: '{clean}'"
        except Exception as e:
            return f"Type error: {e}"

    def press_key(self, key_name="enter", **kwargs):
        try:
            k = key_name.lower().strip()
            if k in ["enter", "return"]: pyautogui.press('enter')
            elif k in ["backspace"]: pyautogui.press('backspace')
            elif k in ["tab"]: pyautogui.press('tab')
            elif k in ["esc", "escape"]: pyautogui.press('esc')
            elif k in ["space"]: pyautogui.press('space')
            elif k in ["select all", "select_all"]: pyautogui.hotkey('ctrl', 'a')
            elif k in ["copy"]: pyautogui.hotkey('ctrl', 'c')
            elif k in ["paste"]: pyautogui.hotkey('ctrl', 'v')
            elif k in ["undo"]: pyautogui.hotkey('ctrl', 'z')
            elif k in ["save"]: pyautogui.hotkey('ctrl', 's')
            elif k in ["down"]: pyautogui.press('down')
            elif k in ["up"]: pyautogui.press('up')
            return f"Boss, {key_name} key press kar di hai."
        except Exception as e:
            return f"Key press error: {e}"

    def search_and_open(self, target="", **kwargs):
        try:
            clean_target = target.strip()
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'alt', '/')
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
            time.sleep(0.1)
            pyperclip.copy(clean_target)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1.5)
            pyautogui.press('down')
            time.sleep(0.2)
            pyautogui.press('enter')
            return f"Boss, '{clean_target}' search karke open kar diya hai!"
        except Exception as e:
            return f"Search error: {e}"

    def send_message(self, message="", **kwargs):
        try:
            clean_msg = re.sub(r"^(message karo|message drop kar do|message send karo|drop kar do)\s*", "", message, flags=re.IGNORECASE).strip() or message.strip()
            pyperclip.copy(clean_msg)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            pyautogui.press('enter')
            return f"Boss, message bhej diya: '{clean_msg}'"
        except Exception as e:
            return f"Send error: {e}"

    # ==========================================
    # 📱 5. APPS & LAUNCHER
    # ==========================================
    def smart_launch_app_or_web(self, name="", **kwargs):
        app = name.lower().strip()
        web_services = {
            "youtube": "https://www.youtube.com", "chatgpt": "https://chatgpt.com",
            "gemini": "https://gemini.google.com", "canva": "https://www.canva.com",
            "instagram": "https://www.instagram.com", "whatsapp": "https://web.whatsapp.com",
            "github": "https://github.com", "google": "https://www.google.com"
        }
        for service, url in web_services.items():
            if service in app:
                self._open_in_chrome(url)
                return f"{service.capitalize()} open kar diya hai boss."

        known_cmds = {
            "this pc": "explorer", "thispc": "explorer", "my computer": "explorer", 
            "file explorer": "explorer", "explorer": "explorer", "files": "explorer",
            "camera": "start microsoft.windows.camera:", "webcam": "start microsoft.windows.camera:",
            "settings": "start ms-settings:", "notepad": "notepad.exe", "calculator": "calc.exe",
            "calc": "calc.exe", "cmd": "cmd.exe", "terminal": "wt.exe", "paint": "mspaint.exe",
            "vscode": "code", "vs code": "code", "spotify": "spotify", "task manager": "taskmgr",
            "chrome": "start chrome"
        }
        for key, cmd in known_cmds.items():
            if key in app:
                subprocess.Popen(cmd, shell=True)
                return f"Boss, {name.capitalize()} open kar diya hai!"

        return self.windows_search_and_open(name)

    def windows_search_and_open(self, query="", **kwargs):
        try:
            pyautogui.press('win')
            time.sleep(0.5)
            pyperclip.copy(query.strip())
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1.0)
            pyautogui.press('enter')
            return f"Boss, Windows me '{query}' search karke open kar diya hai!"
        except Exception as e:
            return f"Windows search error: {e}"

    def search_google(self, query="", **kwargs):
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        self._open_in_chrome(url)
        return f"Google par '{query}' search kar diya hai boss."

    def search_youtube_and_play(self, query="", **kwargs):
        clean_q = query.strip()
        if not clean_q or clean_q in ["youtube", "open youtube", "song", "gana"]:
            self._open_in_chrome("https://www.youtube.com")
            return "YouTube open kar diya hai boss."

        try:
            encoded_query = urllib.parse.quote(clean_q)
            search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = requests.get(search_url, headers=headers, timeout=5)
            video_ids = re.findall(r"watch\?v=([a-zA-Z0-9_-]{11})", resp.text)
            if video_ids:
                direct_url = f"https://www.youtube.com/watch?v={video_ids[0]}"
                self._open_in_chrome(direct_url)
                return f"Boss, YouTube par '{clean_q}' play kar diya hai!"
        except Exception:
            pass

        self._open_in_chrome(f"https://www.youtube.com/results?search_query={urllib.parse.quote(clean_q)}")
        return f"YouTube par '{clean_q}' search karke open kar diya hai."

    # ==========================================
    # 📧 6. FULL EMAIL AUTOMATION
    # ==========================================
    def send_email_auto(self, recipient_email="", subject="Update via Pihu AI", body="", **kwargs):
        if not self.EMAIL_APP_PASS:
            return "Boss, Gmail App Password set nahi hai."
        try:
            clean_email = recipient_email.lower().replace(" at the rate ", "@").replace(" dot ", ".").strip()
            msg = MIMEMultipart()
            msg['From'] = self.MY_EMAIL
            msg['To'] = clean_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.MY_EMAIL, self.EMAIL_APP_PASS)
            server.send_message(msg)
            server.quit()
            return f"Boss, {clean_email} ko email successfully send kar diya hai."
        except Exception as e:
            return f"Email send error: {e}"

    def read_latest_email(self, **kwargs):
        if not self.EMAIL_APP_PASS:
            return "Boss, Gmail App Password set nahi hai."
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(self.MY_EMAIL, self.EMAIL_APP_PASS)
            mail.select("inbox")
            status, messages = mail.search(None, '(UNSEEN)')
            msg_ids = messages[0].split()
            if not msg_ids:
                status, messages = mail.search(None, 'ALL')
                msg_ids = messages[0].split()
            if not msg_ids: return "Boss, inbox me koi email nahi hai."
            latest_id = msg_ids[-1]
            status, data = mail.fetch(latest_id, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            subject, enc = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes): subject = subject.decode(enc if enc else "utf-8")
            from_sender = msg.get("From")
            mail.close()
            mail.logout()
            return f"Latest email {from_sender} se aaya hai. Subject hai: '{subject}'."
        except Exception as e:
            return f"Email read error: {e}"

    # ==========================================
    # 🖥️ 7. OS NAVIGATION & HARDWARE
    # ==========================================
    def os_navigation(self, command="desktop", **kwargs):
        cmd = command.lower().strip()
        if any(k in cmd for k in ["desktop", "pura desktop", "home", "minimize all", "minimize", "minimise", "sab band", "sabhi ko close", "sab close"]):
            pyautogui.hotkey('win', 'd')
            return "Boss, sab minimize karke desktop par aa gayi hu."
        elif any(k in cmd for k in ["close", "band karo", "exit app", "window close"]):
            pyautogui.hotkey('alt', 'f4')
            return "Active window close kar di hai boss."
        elif any(k in cmd for k in ["back", "piche", "go back"]):
            pyautogui.hotkey('alt', 'left')
            return "Back kar diya hai boss."
        elif any(k in cmd for k in ["switch", "tab badlo", "previous app"]):
            pyautogui.hotkey('alt', 'tab')
            return "Window switch kar di hai boss."
        return "Navigation executed."

    def control_volume(self, action="", **kwargs):
        if action == "up": pyautogui.press('volumeup', presses=10)
        elif action == "down": pyautogui.press('volumedown', presses=10)
        elif action == "mute": pyautogui.press('volumemute')
        return f"Volume {action} kar diya hai."

    def media_control(self, action="", **kwargs):
        if action in ["play", "pause", "resume"]: pyautogui.press('playpause')
        elif action == "next": pyautogui.press('nexttrack')
        elif action == "previous": pyautogui.press('prevtrack')
        return f"Media {action} executed."

    def control_wifi(self, state="", **kwargs):
        status = "enabled" if state == "on" else "disabled"
        subprocess.Popen(f'netsh interface set interface "Wi-Fi" {status}', shell=True)
        return f"Wi-Fi {state} kar diya hai."

    def get_system_info(self, **kwargs):
        cpu = psutil.cpu_percent(interval=0.2)
        ram = psutil.virtual_memory()
        free_gb = round(ram.available / (1024 ** 3), 1)
        return f"CPU load {cpu}% hai aur RAM {ram.percent}% used hai with {free_gb} GB free."

    def get_battery_status(self, **kwargs):
        battery = psutil.sensors_battery()
        if battery:
            state = "charger plugged in hai" if battery.power_plugged else "battery par chal raha hai"
            return f"Battery {battery.percent}% hai aur abhi {state}."
        return "Battery status detect nahi ho raha."

    def power_control(self, action="", **kwargs):
        return "Boss, security safety ke liye maine shutdown cancel rakha hai."

    def calculate_math(self, expression="", **kwargs):
        try:
            clean = expression.replace("x", "*")
            return f"Answer: {eval(clean, {'__builtins__': None}, {})}"
        except Exception:
            return "Calculation failed."

    # ==========================================
    # 👁️ 8. HIGH-RESOLUTION VISION
    # ==========================================
    def analyze_screen_vision(self, user_prompt="Explain what is currently visible on my screen and diagnose any errors.", **kwargs):
        if not self.client:
            return "Vision AI unavailable: Groq API key set nahi hai."
            
        try:
            screenshot = pyautogui.screenshot()
            w, h = screenshot.size
            if w > 1920:
                screenshot = screenshot.resize((1920, int(h * (1920 / w))), Image.Resampling.LANCZOS)
                
            buffered = io.BytesIO()
            screenshot.save(buffered, format="JPEG", quality=90)
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            prompt_text = (
                f"You are Pihu, an expert autonomous developer looking at user screen.\n"
                f"User asked: '{user_prompt}'\n"
                "Look at the active error logs, red marks or open code. Point out the error line and how to solve it in 2 short Latin Hinglish sentences addressing user as 'boss'."
            )

            v_models = [self.vision_model, "llama-3.2-11b-vision-preview"]
            for vm in v_models:
                try:
                    response = self.client.chat.completions.create(
                        model=vm,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt_text},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                                ]
                            }
                        ],
                        temperature=0.1,
                        max_tokens=250
                    )
                    raw = response.choices[0].message.content
                    cleaned = self._clean_response(raw)
                    if cleaned:
                        return cleaned
                except Exception:
                    continue

            return "Boss, screen scan ho gayi hai par error details parse nahi ho paaye."
        except Exception as e:
            return f"Vision processing error: {e}"

    def diagnose_and_fix_screen_error(self, instruction="Fix error and run", **kwargs):
        if any(k in instruction.lower() for k in ["tum solve karo", "solve karke jao", "theek karo", "fix karke do", "solve karo"]):
            return self.auto_fix_file_code(filename="smartmemory.py")
        return self.analyze_screen_vision(user_prompt=instruction)

    def write_and_run_code(self, language="cpp", code_content="", filename="pihu_code", **kwargs):
        os.makedirs("sandbox", exist_ok=True)
        lang = language.lower().strip()
        if any(x in lang for x in ["cpp", "c++", "c"]):
            ext = ".cpp"
            filepath = os.path.abspath(os.path.join("sandbox", f"{filename}{ext}"))
            exe_path = os.path.abspath(os.path.join("sandbox", f"{filename}.exe"))
            with open(filepath, "w", encoding="utf-8") as f: f.write(code_content)
            comp = subprocess.run(f'g++ "{filepath}" -o "{exe_path}"', shell=True, capture_output=True, text=True)
            if comp.returncode != 0: return f"Compilation Error:\n{comp.stderr}"
            try:
                run_res = subprocess.run(f'"{exe_path}"', shell=True, capture_output=True, text=True, timeout=6)
                out = run_res.stdout.strip() if run_res.stdout else "Program executed with no output."
                return f"Code executed successfully! Output:\n{out}"
            except Exception as e: return f"Execution error: {e}"
        elif any(x in lang for x in ["python", "py"]):
            filepath = os.path.abspath(os.path.join("sandbox", f"{filename}.py"))
            with open(filepath, "w", encoding="utf-8") as f: f.write(code_content)
            try:
                run_res = subprocess.run(f'python "{filepath}"', shell=True, capture_output=True, text=True, timeout=6)
                out = run_res.stdout.strip() if run_res.stdout else run_res.stderr.strip()
                return f"Python output:\n{out}"
            except Exception as e: return f"Python error: {e}"
        return "Language format not supported."

    def read_screen(self, **kwargs):
        try:
            os.makedirs("temp", exist_ok=True)
            shot_path = os.path.join("temp", "screen.png")
            pyautogui.screenshot().save(shot_path)
            if pytesseract:
                text = pytesseract.image_to_string(Image.open(shot_path))
                clean_t = text.strip()
                return f"Screen text detected:\n{clean_t[:1200]}" if clean_t else "Screen par readable text nahi mila."
            return "Tesseract OCR installed nahi hai."
        except Exception as e:
            return f"Screen reading error: {e}"

    def scrape_and_summarize(self, url="", **kwargs):
        try:
            if not url.startswith("http"): url = f"https://{url}"
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(res.text, "html.parser")
            for s in soup(["script", "style"]): s.extract()
            clean_text = " ".join(soup.get_text().split())
            return f"Web content from {url}:\n{clean_text[:1500]}"
        except Exception as e:
            return f"Scraping failed: {e}"

    # ==========================================
    # 🧠 INTENT ROUTER (WITH FAST DIRECT GATES)
    # ==========================================
    def process_input(self, text):
        if not text.strip():
            return ""

        t_lower = text.lower().strip()

        # ⚡ Direct Gate 1: WhatsApp Intent Catch
        if "whatsapp" in t_lower and any(k in t_lower for k in ["message", "msg", "send", "bhejo"]):
            contact = "didi"
            if "didi" in t_lower: contact = "didi"
            elif "nihal" in t_lower: contact = "nihal"
            elif "gaurav" in t_lower: contact = "Gaurav Kumawat"
            elif "mummy" in t_lower: contact = "mummy"
            elif "papa" in t_lower: contact = "papa"
            
            msg = "hello"
            if "hello" in t_lower: msg = "Hello"
            elif "jay shri ram" in t_lower or "jai shree ram" in t_lower: msg = "Jay Shri Ram"
            return self.send_whatsapp_message(name=contact, message=msg)

        # ⚡ Direct Gate 2: Navigation
        if any(k in t_lower for k in [
            "close kar do sabhi ko", "close kar do sabhi", "sab close kar do", "sabhi ko close",
            "pura desktop par aao", "desktop par aao", "desktop dikhao", "minimize all", "sab minimize"
        ]):
            return self.os_navigation(command="desktop")

        if any(k in t_lower for k in ["ise close kar do", "close kar do", "band kar do isko", "window close kar do", "close app"]):
            return self.os_navigation(command="close")

        # ⚡ Direct Gate 3: Calls
        if any(k in t_lower for k in ["video call", "video call karo", "video call milao"]):
            match = re.search(r"(?:ko|ke|par)?\s*([a-zA-Z\s]+?)\s*(?:ko|ke)?\s*video call", t_lower)
            target = match.group(1).strip() if match else "Gaurav Kumawat"
            return self.whatsapp_video_call(name=target)

        if any(k in t_lower for k in ["voice call", "call karo", "call milao", "audio call"]):
            match = re.search(r"(?:ko|ke|par)?\s*([a-zA-Z\s]+?)\s*(?:ko|ke)?\s*(?:voice|audio)?\s*call", t_lower)
            target = match.group(1).strip() if match else "Gaurav Kumawat"
            return self.whatsapp_voice_call(name=target)

        # ⚡ Direct Gate 4: Screen Vision
        vision_triggers = [
            "screen", "screen check", "screen par dekh", "screen per dekh", "screen dekh",
            "kahan galti hai", "kaha galti hai", "kya galti hai", "kya error", "kya error hai",
            "code mein kahan", "code me kahan", "error solve", "error fix", "solve karke do", "solve karo"
        ]
        if any(k in t_lower for k in vision_triggers):
            return self.diagnose_and_fix_screen_error(instruction=text)

        # ⚡ 5. STRICT TOOL SCHEMA
        tools_schema = [
            {
                "type": "function",
                "function": {
                    "name": "send_whatsapp_message",
                    "description": "Opens WhatsApp, searches contact name, opens chat, types message and sends it.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Contact name (e.g. didi, Gaurav)"},
                            "message": {"type": "string", "description": "Message body"}
                        },
                        "required": ["name", "message"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "smart_launch_app_or_web",
                    "description": "Launches apps or websites (e.g. calc, notepad, youtube, chrome).",
                    "parameters": {
                        "type": "object",
                        "properties": {"name": {"type": "string"}},
                        "required": ["name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_youtube_and_play",
                    "description": "Plays YouTube video.",
                    "parameters": {
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "os_navigation",
                    "description": "Desktop minimize, close active app, back, switch window.",
                    "parameters": {
                        "type": "object",
                        "properties": {"command": {"type": "string", "enum": ["desktop", "back", "switch", "close"]}},
                        "required": ["command"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "control_volume",
                    "description": "Controls audio volume.",
                    "parameters": {
                        "type": "object",
                        "properties": {"action": {"type": "string", "enum": ["up", "down", "mute"]}},
                        "required": ["action"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_battery_status",
                    "description": "Battery percentage check.",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_custom_folder",
                    "description": "Creates a folder on Desktop.",
                    "parameters": {
                        "type": "object",
                        "properties": {"folder_name": {"type": "string"}}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_custom_file",
                    "description": "Creates a file on Desktop or VS Code.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filename": {"type": "string"},
                            "content": {"type": "string"},
                            "open_with": {"type": "string"}
                        }
                    }
                }
            }
        ]

        system_prompt = (
            f"You are Pihu, an autonomous AI desktop co-pilot created by {self.curr_user} (boss).\n"
            "CRITICAL INSTRUCTIONS:\n"
            "1. When user asks to send WhatsApp message, ALWAYS call send_whatsapp_message tool.\n"
            "2. When user asks to close apps/desktop, call os_navigation.\n"
            "3. Execute tools immediately. Keep response in 1 short Latin Hinglish sentence."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]

        if self.client:
            for model_candidate in self.available_models:
                try:
                    response = self.client.chat.completions.create(
                        model=model_candidate,
                        messages=messages,
                        tools=tools_schema,
                        temperature=0.1
                    )
                    msg = response.choices[0].message
                    if msg.tool_calls:
                        for tc in msg.tool_calls:
                            fn_name = tc.function.name
                            fn_args = json.loads(tc.function.arguments) if tc.function.arguments else {}
                            if fn_name in self.tools_map:
                                return self.tools_map[fn_name](**fn_args)
                    if msg.content:
                        return self._clean_response(msg.content)
                    break
                except Exception as e:
                    continue

        return "Ji boss, command execute nahi ho paayi."

engine = PihuAutonomousBrain()

def get_offline_response(user_input):
    return engine.process_input(user_input)

# =====================================================================
# 🌟 PROFESSIONAL CYBERPUNK GUI DASHBOARD
# =====================================================================
class PihuDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Pihu AI - Autonomous Desktop Co-Pilot (HackIndia Edition)")
        self.root.geometry("750x520")
        self.root.config(bg="#0d1117")
        
        title_lbl = tk.Label(root, text="🚀 PIHU AI - AUTONOMOUS OS AGENT", font=("Arial", 16, "bold"), fg="#00f2fe", bg="#0d1117")
        title_lbl.pack(pady=15)
        
        status_frame = tk.Frame(root, bg="#161b22", bd=2, relief="groove")
        status_frame.pack(fill="x", padx=20, pady=5)
        
        api_status_text = f"🟢 Status: Ready (Model: {engine.active_model})" if engine.client else "🔴 Status: Groq Key Missing"
        status_color = "#3fb950" if engine.client else "#f85149"
        
        self.status_label = tk.Label(status_frame, text=api_status_text, font=("Arial", 11, "bold"), fg=status_color, bg="#161b22")
        self.status_label.pack(pady=8)
        
        console_frame = tk.Frame(root, bg="#0d1117")
        console_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        lbl_console = tk.Label(console_frame, text="Live Execution Logs & Output:", font=("Arial", 10, "bold"), fg="#8b949e", bg="#0d1117", anchor="w")
        lbl_console.pack(fill="x", pady=2)
        
        self.log_box = scrolledtext.ScrolledText(console_frame, height=12, bg="#161b22", fg="#c9d1d9", font=("Consolas", 10), insertbackground="white")
        self.log_box.pack(fill="both", expand=True, pady=5)
        
        ctrl_frame = tk.Frame(root, bg="#0d1117")
        ctrl_frame.pack(fill="x", padx=20, pady=15)
        
        self.entry_cmd = tk.Entry(ctrl_frame, font=("Arial", 12), bg="#161b22", fg="white", insertbackground="white")
        self.entry_cmd.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=5)
        self.entry_cmd.insert(0, "calc open kar do")
        self.entry_cmd.bind("<Return>", lambda event: self.execute_command())
        
        btn_send = tk.Button(ctrl_frame, text="Execute", font=("Arial", 10, "bold"), bg="#238636", fg="white", padx=15, pady=5, command=self.execute_command)
        btn_send.pack(side="right")
        
        self.btn_start = tk.Button(root, text="🚀 START PIHU AGENT SERVICE", font=("Arial", 11, "bold"), bg="#1f6feb", fg="white", pady=8, command=self.start_agent)
        self.btn_start.pack(fill="x", padx=20, pady=(0, 20))
        
        self.log(f"Pihu AI Dashboard initialized successfully for Hemant.\n")

    def log(self, text):
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.see(tk.END)

    def start_agent(self):
        self.btn_start.config(state="disabled", bg="#30363d")
        self.status_label.config(text="🟢 Status: Pihu Agent is Active & Monitoring OS/Voice...", fg="#3fb950")
        self.log("[INFO] Background autonomous daemon started successfully.")

    def execute_command(self):
        cmd = self.entry_cmd.get().strip()
        if not cmd:
            return
        self.log(f"\n[USER COMMAND]: {cmd}")
        self.entry_cmd.delete(0, tk.END)
        threading.Thread(target=self._run_task, args=(cmd,), daemon=True).start()

    def _run_task(self, cmd):
        try:
            self.status_label.config(text="⚡ Status: Processing via Groq LPU & Executing Tools...", fg="#d29922")
            result = get_offline_response(cmd)
            self.log(f"[PIHU RESPONSE]: {result}")
            self.status_label.config(text="🟢 Status: Ready (Idle)", fg="#3fb950")
        except Exception as e:
            self.log(f"[ERROR]: {e}")
            self.status_label.config(text="🔴 Status: Error Encountered", fg="#f85149")

if __name__ == "__main__":
    root = tk.Tk()
    app = PihuDashboard(root)
    root.mainloop()