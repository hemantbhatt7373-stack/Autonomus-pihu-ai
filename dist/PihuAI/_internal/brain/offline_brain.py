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
import pyautogui
import psutil
import requests
from bs4 import BeautifulSoup
from PIL import Image
from groq import Groq
import pyperclip

# OCR लाइब्रेरी
try:
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
except Exception:
    pytesseract = None

# =====================================================================
# 🚀 PIHU MASTER AGENTIC BRAIN (100% BULLETPROOF WHATSAPP & OS)
# =====================================================================

class PihuAutonomousBrain:
    def __init__(self):
        self.curr_user = "Hemant"
        
        # 🔑 अपनी Groq API Key यहाँ डालें
        self.GROQ_API_KEY = "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"
        self.client = None
        
        self.active_model = "openai/gpt-oss-20b"
        self.vision_model = "qwen/qwen3.6-27b"
        
        # 📧 ईमेल सेटिंग्स
        self.MY_EMAIL = "your_email@gmail.com"
        self.EMAIL_APP_PASS = "xxxx xxxx xxxx xxxx"

        if self.GROQ_API_KEY:
            try:
                self.client = Groq(api_key=self.GROQ_API_KEY.strip())
                server_models = [m.id for m in self.client.models.list().data]
                
                preferred_order = [
                    "openai/gpt-oss-20b",
                    "llama-3.1-8b-instant",
                    "llama-3.2-3b-preview",
                    "llama3-70b-8192",
                    "llama-3.3-70b-versatile"
                ]
                for candidate in preferred_order:
                    if candidate in server_models:
                        self.active_model = candidate
                        break

                vision_candidates = [
                    "qwen/qwen3.6-27b",
                    "llama-3.2-90b-vision-preview",
                    "meta-llama/llama-4-scout-17b-16e-instruct"
                ]
                for vc in vision_candidates:
                    if vc in server_models:
                        self.vision_model = vc
                        break

                print(f"✅ Active Groq Model Connected: {self.active_model}")
                print(f"✅ Active Vision Model: {self.vision_model}")
            except Exception as e:
                print(f"⚠️ Groq API Init Warning: {e}")
                    
        self.chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
        ]
        
        # 🛠️ सभी 24 टूल्स की पूरी मैपिंग
        self.tools_map = {
            "type_text": self.type_text,
            "press_key": self.press_key,
            "search_and_open": self.search_and_open,
            "send_message": self.send_message,
            "send_whatsapp_message": self.send_whatsapp_message,
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
        cleaned = cleaned.replace("*", "").replace("`", "").strip()
        return cleaned

    def _open_in_chrome(self, url):
        for path in self.chrome_paths:
            if os.path.exists(path):
                subprocess.Popen([path, url])
                return
        subprocess.Popen(f'start chrome "{url}"', shell=True)

    # ==========================================
    # 💬 1. 100% BULLETPROOF WHATSAPP AUTOMATION
    # ==========================================
    def send_whatsapp_message(self, name="", message="Hello", **kwargs):
        try:
            clean_name = name.strip() or "friend"
            
            # मैसेज में से बेकार वॉयस कमांड शब्द साफ़ करना
            clean_msg = re.sub(
                r"\b(ka message|hay ka|hi ka|message drop kar do|drop kar do|send kar do|bhejo|message karo|send kar dena|nihal block|nihal bro ke|ko|ke)\b", 
                "", 
                message, 
                flags=re.IGNORECASE
            ).strip()
            
            if not clean_msg or clean_msg.lower() == clean_name.lower():
                clean_msg = "Hello"

            # Chrome में WhatsApp Web खोलें
            self._open_in_chrome("https://web.whatsapp.com")
            time.sleep(7.5)

            sw, sh = pyautogui.size()

            # 1. Chrome को सबसे ऊपर लाने के लिए टॉप बार पर क्लिक
            pyautogui.click(sw // 2, 10)
            time.sleep(0.3)

            # 2. पुरानी खुली हुई चैट से फ़ोकस हटाने के लिए 2 बार Escape
            pyautogui.press('esc')
            time.sleep(0.2)
            pyautogui.press('esc')
            time.sleep(0.3)

            # 3. WhatsApp Web के सर्च बार को एक्टिवेट करने के 2 रास्ते:
            # रास्ता A: Ctrl + Alt + / दबाना
            pyautogui.hotkey('ctrl', 'alt', '/')
            time.sleep(0.4)

            # रास्ता B: सर्च बार के सही इनपुट एरिया (18% width, 18% height) पर सीधा क्लिक
            pyautogui.click(int(sw * 0.18), int(sh * 0.18))
            time.sleep(0.4)

            # 4. सर्च बॉक्स का पुराना टेक्स्ट साफ़ करना
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
            time.sleep(0.3)

            # 5. नाम क्लिपबोर्ड से पेस्ट करें
            pyperclip.copy(clean_name)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(2.8)  # WhatsApp को कॉन्टैक्ट फ़िल्टर करने का समय दें

            # 6. फ़िल्टर हुई चैट लिस्ट में सबसे पहली चैट पर जाने के लिए:
            # Enter दबाएं, फिर अगर चैट नहीं खुली तो Down Arrow दबाकर Enter
            pyautogui.press('enter')
            time.sleep(0.5)
            pyautogui.press('down')
            time.sleep(0.3)
            pyautogui.press('enter')
            time.sleep(1.8)  # चैट खुलने और कर्सर मैसेज बॉक्स में आने का इंतज़ार

            # 7. मैसेज पेस्ट करके सेंड करें
            pyperclip.copy(clean_msg)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(0.3)

            return f"Boss, WhatsApp par '{clean_name}' ko '{clean_msg}' message bhej diya hai!"
        except Exception as e:
            return f"WhatsApp auto-send error: {e}"

    # ==========================================
    # 📁 2. FILE & FOLDER CREATOR (SMART DEFAULT)
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
                if any(x in content.lower() for x in ["#include", "cout", "int main", "std::", "c++", "cpp"]):
                    clean_name += ".cpp"
                else:
                    clean_name += ".txt"
            
            if clean_name.endswith(".cpp") and not content:
                content = (
                    "#include <iostream>\n"
                    "using namespace std;\n\n"
                    "int main() {\n"
                    "    cout << \"Hello from Pihu AI!\" << endl;\n"
                    "    return 0;\n"
                    "}\n"
                )

            desktop_dir = os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), "Desktop")
            target_dir = desktop_dir if location == "desktop" else os.getcwd()
            full_path = os.path.join(target_dir, clean_name)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content or "// Created by Pihu AI\n")

            if "vs" in open_with.lower() or "code" in open_with.lower() or "vscode" in location.lower():
                subprocess.Popen(f'code "{full_path}"', shell=True)
                return f"Boss, '{clean_name}' file bana kar VS Code me open kar di hai!"
            else:
                os.system(f'start notepad.exe "{full_path}"')
                return f"Boss, Desktop par '{clean_name}' file bana kar open kar di hai!"
        except Exception as e:
            return f"File create error: {e}"

    # ==========================================
    # ⌨️ 3. UNIVERSAL KEYBOARD & SEARCH
    # ==========================================
    def type_text(self, text_to_type="", press_enter=True, **kwargs):
        try:
            clean = re.sub(
                r"^(hello pihu|pihu|gemini per|gemini mein|type karo|likho|search karo|bolo|pucho)\s*",
                "",
                text_to_type,
                flags=re.IGNORECASE
            ).strip()
            if not clean:
                clean = text_to_type.strip()
                
            pyautogui.press('shift')
            time.sleep(0.1)

            pyperclip.copy(clean)
            time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.4)

            if press_enter:
                pyautogui.press('enter')

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
            time.sleep(0.3)
            pyautogui.hotkey('ctrl', 'alt', '/')
            time.sleep(0.3)
            
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
            time.sleep(0.2)
            
            pyperclip.copy(clean_target)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(2.0)
            
            pyautogui.press('down')
            time.sleep(0.3)
            pyautogui.press('enter')
            return f"Boss, '{clean_target}' search karke open kar diya hai!"
        except Exception as e:
            return f"Search error: {e}"

    def send_message(self, message="", **kwargs):
        try:
            clean_msg = re.sub(r"^(message karo|message drop kar do|message send karo|drop kar do)\s*", "", message, flags=re.IGNORECASE).strip()
            if not clean_msg:
                clean_msg = message.strip()
            pyperclip.copy(clean_msg)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.4)
            pyautogui.press('enter')
            return f"Boss, message bhej diya: '{clean_msg}'"
        except Exception as e:
            return f"Send error: {e}"

    # ==========================================
    # 📱 4. APPS & WINDOWS LAUNCHER
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
            time.sleep(0.6)
            pyperclip.copy(query.strip())
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1.2)
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
    # 📧 5. FULL EMAIL AUTOMATION
    # ==========================================
    def send_email_auto(self, recipient_email="", subject="Update via Pihu AI", body="", **kwargs):
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
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(self.MY_EMAIL, self.EMAIL_APP_PASS)
            mail.select("inbox")

            status, messages = mail.search(None, '(UNSEEN)')
            msg_ids = messages[0].split()
            if not msg_ids:
                status, messages = mail.search(None, 'ALL')
                msg_ids = messages[0].split()

            if not msg_ids:
                return "Boss, inbox me koi naya email nahi hai."

            latest_id = msg_ids[-1]
            status, data = mail.fetch(latest_id, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])

            subject, enc = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(enc if enc else "utf-8")
            from_sender = msg.get("From")

            mail.close()
            mail.logout()
            return f"Latest email {from_sender} se aaya hai. Subject hai: '{subject}'."
        except Exception as e:
            return f"Email read error: {e}"

    # ==========================================
    # 🖥️ 6. OS CONTROLS & HARDWARE
    # ==========================================
    def os_navigation(self, command="desktop", **kwargs):
        cmd = command.lower().strip()
        if any(k in cmd for k in ["desktop", "pura desktop", "home", "minimize all", "minimize", "minimise"]):
            pyautogui.hotkey('win', 'd')
            return "Boss, sab minimize karke desktop par aa gayi hu."
        elif any(k in cmd for k in ["back", "piche", "go back"]):
            pyautogui.hotkey('alt', 'left')
            return "Back kar diya hai boss."
        elif any(k in cmd for k in ["switch", "tab badlo", "previous app"]):
            pyautogui.hotkey('alt', 'tab')
            return "Window switch kar di hai boss."
        elif any(k in cmd for k in ["close", "band karo", "exit app"]):
            pyautogui.hotkey('alt', 'f4')
            return "Active window close kar di hai."
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
        if action == "shutdown": os.system("shutdown /s /t 10")
        elif action == "restart": os.system("shutdown /r /t 10")
        return f"System 10 seconds me {action} ho jayega."

    def calculate_math(self, expression="", **kwargs):
        try:
            clean = expression.replace("x", "*")
            return f"Answer: {eval(clean, {'__builtins__': None}, {})}"
        except Exception:
            return "Calculation failed."

    # ==========================================
    # 👁️ 7. HIGH-RESOLUTION VISION & ERROR SOLVER
    # ==========================================
    def analyze_screen_vision(self, user_prompt="Explain what is currently visible on my screen and diagnose any errors.", **kwargs):
        if not self.client:
            return "Vision AI unavailable: Groq API key set nahi hai."
            
        try:
            screenshot = pyautogui.screenshot()
            screenshot.thumbnail((1280, 720))
            buffered = io.BytesIO()
            screenshot.save(buffered, format="JPEG", quality=90)
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            prompt_text = (
                "You are Pihu, an expert code debugger looking at user screen. "
                f"User asks: '{user_prompt}'. "
                "Examine any open code, terminal, red squiggly lines, or error stack traces carefully. "
                "DO NOT output <think> tags. Directly state: "
                "1. What is open and what the error/bug is (mention line number or function if visible). "
                "2. The exact quick fix. "
                "Answer in 2-3 concise Latin Hinglish sentences addressing user as boss."
            )

            response = self.client.chat.completions.create(
                model=self.vision_model,
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
                max_tokens=400
            )
            raw = response.choices[0].message.content
            cleaned = self._clean_response(raw)
            return cleaned if cleaned else "Boss, screen par code me koi obvious error nahi dikh raha hai."
        except Exception as e:
            return f"Vision processing error: {e}"

    def diagnose_and_fix_screen_error(self, instruction="Fix error and run", **kwargs):
        return self.analyze_screen_vision(user_prompt=instruction)

    def write_and_run_code(self, language="cpp", code_content="", filename="pihu_code", **kwargs):
        os.makedirs("sandbox", exist_ok=True)
        lang = language.lower().strip()
        
        if any(x in lang for x in ["cpp", "c++", "c"]):
            ext = ".cpp"
            filepath = os.path.abspath(os.path.join("sandbox", f"{filename}{ext}"))
            exe_path = os.path.abspath(os.path.join("sandbox", f"{filename}.exe"))

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code_content)

            comp = subprocess.run(f'g++ "{filepath}" -o "{exe_path}"', shell=True, capture_output=True, text=True)
            if comp.returncode != 0:
                return f"Compilation Error:\n{comp.stderr}"
            
            try:
                run_res = subprocess.run(f'"{exe_path}"', shell=True, capture_output=True, text=True, timeout=6)
                out = run_res.stdout.strip() if run_res.stdout else "Program executed with no output."
                return f"Code executed successfully! Output:\n{out}"
            except Exception as e:
                return f"Execution error: {e}"

        elif any(x in lang for x in ["python", "py"]):
            filepath = os.path.abspath(os.path.join("sandbox", f"{filename}.py"))
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code_content)

            try:
                run_res = subprocess.run(f'python "{filepath}"', shell=True, capture_output=True, text=True, timeout=6)
                out = run_res.stdout.strip() if run_res.stdout else run_res.stderr.strip()
                return f"Python output:\n{out}"
            except Exception as e:
                return f"Python error: {e}"

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
            if not url.startswith("http"):
                url = f"https://{url}"
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(res.text, "html.parser")
            for s in soup(["script", "style"]):
                s.extract()
            clean_text = " ".join(soup.get_text().split())
            return f"Web content from {url}:\n{clean_text[:1500]}"
        except Exception as e:
            return f"Scraping failed: {e}"

    # ==========================================
    # 🧠 THE COMPLETE UNCUT AGENTIC ROUTER
    # ==========================================
    def process_input(self, text):
        if not text.strip():
            return ""

        t_lower = text.lower().strip()

        # ⚡ 1. SCREEN VISION & ERROR DETECTION DIRECT DISPATCH
        if any(k in t_lower for k in [
            "kahan galti hai", "kaha galti hai", "kya galti hai", "kya error hai",
            "code mein kahan", "error solve", "error fix", "solve karke do", "solve karo",
            "kis code mein error", "solution dekar jao", "solution dekhe jao"
        ]):
            return self.diagnose_and_fix_screen_error(instruction=text)

        if any(k in t_lower for k in ["screen per dekh", "screen par dekh", "screen dekh"]):
            return self.analyze_screen_vision(user_prompt=text)

        # ⚡ 2. FULL 24 TOOLS SCHEMA
        tools_schema = [
            {
                "type": "function",
                "function": {
                    "name": "create_custom_folder",
                    "description": "Creates a folder on Desktop. Always create immediately with default name if user didn't specify one. Never ask follow-up questions.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "folder_name": {"type": "string", "description": "Folder name (e.g. Hemant, New_Folder)"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_custom_file",
                    "description": "Creates a file on Desktop or in VS Code with specific name and content. If user doesn't give a name, default to newfile.txt. Never ask follow-up questions.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filename": {"type": "string", "description": "Filename (e.g. notes.txt, main.cpp)"},
                            "content": {"type": "string", "description": "Text or code to write inside file"},
                            "open_with": {"type": "string", "description": "Set 'vscode' if user mentions vs code, else 'notepad'"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "type_text",
                    "description": "Types clean text in the active window (Gemini, Google, editor). Always sets press_enter=True to submit the query/text.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text_to_type": {"type": "string", "description": "The exact question or text to type without filler words"},
                            "press_enter": {"type": "boolean", "description": "Set True to submit the text by pressing Enter"}
                        },
                        "required": ["text_to_type"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "press_key",
                    "description": "Presses keyboard keys like enter, backspace, tab, esc, save, copy, paste.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "key_name": {"type": "string", "description": "Key name"}
                        },
                        "required": ["key_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_and_open",
                    "description": "Searches for a person's chat or file in currently open app and opens it.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "target": {"type": "string", "description": "Name of person or chat to search and open"}
                        },
                        "required": ["target"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "send_message",
                    "description": "Types and sends a message in the active chat box.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message": {"type": "string", "description": "Message content"}
                        },
                        "required": ["message"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "send_whatsapp_message",
                    "description": "Opens WhatsApp and sends message to a contact name.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Contact or person name (e.g. Mummy ji, Nihal bro)"},
                            "message": {"type": "string", "description": "Clean message body to send (e.g. hello, hay)"}
                        },
                        "required": ["name", "message"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "smart_launch_app_or_web",
                    "description": "Launches applications or websites (This PC, Camera, Chrome, WhatsApp, VS Code, Notepad, etc.).",
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
                    "name": "windows_search_and_open",
                    "description": "Opens Windows Start Menu, types query and presses Enter.",
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
                    "name": "search_google",
                    "description": "Performs Google search in Chrome browser.",
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
                    "name": "search_youtube_and_play",
                    "description": "Plays song or video on YouTube.",
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
                    "name": "send_email_auto",
                    "description": "Sends an email to any recipient email address.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "recipient_email": {"type": "string"},
                            "subject": {"type": "string"},
                            "body": {"type": "string"}
                        },
                        "required": ["recipient_email", "body"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_latest_email",
                    "description": "Reads latest unread or inbox emails.",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "os_navigation",
                    "description": "Desktop minimize, back, switch, close active window.",
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
                    "description": "Controls system audio volume.",
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
                    "name": "media_control",
                    "description": "Controls media playback (play, pause, next, previous).",
                    "parameters": {
                        "type": "object",
                        "properties": {"action": {"type": "string", "enum": ["play", "pause", "resume", "next", "previous"]}},
                        "required": ["action"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "control_wifi",
                    "description": "Enables or disables Wi-Fi interface.",
                    "parameters": {
                        "type": "object",
                        "properties": {"state": {"type": "string", "enum": ["on", "off"]}},
                        "required": ["state"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_system_info",
                    "description": "Checks CPU and RAM usage status.",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_battery_status",
                    "description": "Checks laptop battery percentage and plug status.",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "power_control",
                    "description": "Shuts down or restarts the computer.",
                    "parameters": {
                        "type": "object",
                        "properties": {"action": {"type": "string", "enum": ["shutdown", "restart"]}},
                        "required": ["action"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_and_run_code",
                    "description": "Compiles and executes C++ or Python code directly.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "language": {"type": "string", "enum": ["cpp", "python"]},
                            "code_content": {"type": "string"},
                            "filename": {"type": "string"}
                        },
                        "required": ["language", "code_content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "calculate_math",
                    "description": "Solves math calculations and arithmetic expressions.",
                    "parameters": {
                        "type": "object",
                        "properties": {"expression": {"type": "string"}},
                        "required": ["expression"]
                    }
                }
            }
        ]

        system_prompt = (
            f"You are Pihu, an autonomous AI desktop co-pilot created by {self.curr_user}. "
            f"The user speaking to you is {self.curr_user} (boss). "
            "You have direct execution control over files, folders, keyboard, apps, WhatsApp, and screen vision. "
            "CRITICAL WHATSAPP RULE:\n"
            "When user asks to send WhatsApp message to someone (e.g. 'Nihal bro ke hay ka message send kar do'):\n"
            "- name MUST be ONLY the contact name: 'Nihal bro'.\n"
            "- message MUST be ONLY the clean message text: 'hay'. NEVER include the contact name or command words in the message.\n"
            "- Call send_whatsapp_message(name='Nihal bro', message='hay').\n"
            "Always execute the tool immediately. Reply in 1 short Latin Hinglish sentence. Never output think tags."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]

        if self.client:
            models_to_try = [self.active_model, "llama-3.1-8b-instant"]
            for model_candidate in models_to_try:
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
                    print(f"Model error: {e}")
                    continue

        return "Ji boss, command samajh me nahi aayi."

engine = PihuAutonomousBrain()

def get_offline_response(user_input):
    return engine.process_input(user_input)