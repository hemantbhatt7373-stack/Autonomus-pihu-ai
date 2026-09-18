import sys
import os
from pathlib import Path

# 🔒 STEP 0: Force-load root directory & .env before any imports
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from dotenv import load_dotenv
    env_paths = [BASE_DIR / ".env", BASE_DIR / "brain" / ".env", Path.cwd() / ".env"]
    for ep in env_paths:
        if ep.exists():
            load_dotenv(dotenv_path=ep, override=True)
            break
except Exception:
    pass

import time
import math
import random
import threading
import json
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import pygame

try:
    pygame.mixer.pre_init(24000, -16, 2, 512)
    pygame.init()
    pygame.mixer.init()
except Exception:
    pass

import core.voice
from core.voice import speak
from core.listener import listen

# ⚡ Asli Automation Brain Link
from brain.offline_brain import engine, get_offline_response

CURRENT_USER = "Hemant"
SUB_USER = "..."
SUB_PIHU = "Standby"

CURRENT_MODE = "STANDBY"
orb_window = None
canvas_orb = None
orb_anim_angle = 0
is_active_listening = False

def get_path(relative_path):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    elif getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# --- 1. USER DATA LOGIC ---
DATA_FILE = get_path('data/pihu_memory.json')

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}}
    try:
        with open(DATA_FILE, 'r', encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {"users": {}}

def save_data(data):
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except Exception:
        pass

# --- 2. INTRO & LAUNCHER SCREEN ---
def show_intro_screen():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Pihu AI - System Launcher (Astra Edition)")
    try:
        app.iconbitmap(get_path("logo.ico"))
    except Exception:
        pass
    app.geometry("850x600")
    app.resizable(False, False)

    data = load_data()
    default_name = data.get('last_user', "Hemant")
    if not default_name:
        existing_users = list(data.get('users', {}).keys())
        default_name = existing_users[-1] if existing_users else "Hemant"

    left_frame = ctk.CTkFrame(app, corner_radius=0, fg_color="transparent")
    left_frame.pack(side="left", fill="y", padx=40, pady=40)

    try:
        img_path = get_path("assets/avatar/idle.png")
        avatar_img = ctk.CTkImage(light_image=Image.open(img_path), dark_image=Image.open(img_path), size=(150, 150))
        ctk.CTkLabel(left_frame, image=avatar_img, text="").pack(pady=(10, 10))
    except Exception:
        ctk.CTkLabel(left_frame, text="[Pihu Neural Core]", font=("Arial", 16, "bold"), text_color="#00FFFF").pack(pady=(20, 10))

    ctk.CTkLabel(left_frame, text="PIHU AI SYSTEM", font=("Arial", 26, "bold"), text_color="#00FFFF").pack(pady=5)
    ctk.CTkLabel(left_frame, text="Autonomous Desktop Co-Pilot", font=("Arial", 12), text_color="gray").pack(pady=(0, 15))
    ctk.CTkLabel(left_frame, text=f"Welcome Back, {default_name}! 👋", font=("Arial", 14), text_color="lightgreen").pack(pady=5)

    name_entry = ctk.CTkEntry(left_frame, placeholder_text="Enter your name...", width=250, height=45, corner_radius=10, font=("Arial", 15))
    name_entry.pack(pady=10)
    name_entry.insert(0, default_name)

    def save_and_start():
        global CURRENT_USER
        user_name = name_entry.get().strip()
        if not user_name:
            user_name = "Hemant"
        CURRENT_USER = user_name
        try:
            engine.curr_user = user_name
        except Exception:
            pass
        data['last_user'] = user_name
        save_data(data)
        
        # Clean Shutdown to prevent Tkinter update callback errors
        app.withdraw()
        app.after(100, app.destroy)
        start_agent_runtime()

    start_btn = ctk.CTkButton(
        left_frame, 
        text="🚀 START PIHU AGENT", 
        command=save_and_start, 
        width=250, 
        height=50,
        corner_radius=25, 
        fg_color="#00FFFF", 
        text_color="black", 
        hover_color="#00CCCC", 
        font=("Arial", 15, "bold")
    )
    start_btn.pack(pady=25)

    right_frame = ctk.CTkScrollableFrame(app, corner_radius=15, fg_color="#1e1e24", width=420)
    right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
    ctk.CTkLabel(right_frame, text="⚡ Active Capabilities & Demo", font=("Arial", 20, "bold"), text_color="#FFB6C1").pack(pady=(10, 15))

    def add_section(title, cmds):
        ctk.CTkLabel(right_frame, text=title, font=("Arial", 15, "bold"), text_color="#00FFFF", anchor="w").pack(fill="x", padx=10, pady=(10, 3))
        for c in cmds:
            ctk.CTkLabel(right_frame, text=f"• {c}", font=("Arial", 13), text_color="white", anchor="w", justify="left").pack(fill="x", padx=18, pady=2)

    add_section("🔮 Siri Neon Glow Mode:", [
        "Say 'Hey Pihu' -> Glowing Orb pops up & listens",
        "'open youtube and play song'",
        "'Back karo' / 'Pura desktop par aao'"
    ])
    add_section("💬 Agentic WhatsApp Execution:", [
        "'Nihal bro ke hello message send kar do'",
        "Physical flow: Search bar -> Select chat -> Paste message -> Enter"
    ])
    add_section("👁️ Active Vision & Screen Debugging:", [
        "'Screen par dekh kahan galti hai'",
        "Scans IDE error and executes autonomous file patching"
    ])
    add_section("🎭 Fullscreen Avatar Mode:", [
        "Say 'Hey Pihu, screen par aao' -> Full Avatar",
        "Say 'Pihu screen se jao' -> Standby (Background)"
    ])
    
    app.mainloop()

# --- 3. COMPACT & PROFESSIONAL SIRI NEON GLOW ORB ---
def create_orb_ui():
    global orb_window, canvas_orb
    orb_window = tk.Tk()
    orb_window.title("Pihu Siri Orb")
    orb_window.overrideredirect(True)
    orb_window.attributes("-topmost", True)
    
    TRANS_COLOR = "#000002"
    orb_window.attributes("-transparentcolor", TRANS_COLOR)

    screen_w = orb_window.winfo_screenwidth()
    screen_h = orb_window.winfo_screenheight()
    
    orb_w, orb_h = 160, 160
    x = (screen_w - orb_w) // 2
    y = screen_h - orb_h - 35
    orb_window.geometry(f"{orb_w}x{orb_h}+{x}+{y}")
    orb_window.configure(bg=TRANS_COLOR)

    canvas_orb = tk.Canvas(orb_window, width=orb_w, height=orb_h, bg=TRANS_COLOR, highlightthickness=0)
    canvas_orb.pack(fill="both", expand=True)
    orb_window.withdraw()

def show_orb_safe():
    if orb_window:
        orb_window.deiconify()
        orb_window.lift()
        orb_window.attributes("-topmost", True)

def hide_orb_safe():
    if orb_window:
        orb_window.withdraw()

def animate_procedural_orb():
    global orb_anim_angle, is_active_listening
    if orb_window and canvas_orb:
        canvas_orb.delete("all")
        cx, cy = 80, 80
        
        active = is_active_listening or core.voice.is_speaking
        pulse = math.sin(orb_anim_angle * 2.8) * (8 if active else 3)
        base_r = 28 + pulse
        
        aura_r = base_r + 16
        canvas_orb.create_oval(cx - aura_r, cy - aura_r, cx + aura_r, cy + aura_r, fill="#07101e", outline="")

        colors = ["#00f5d4", "#4361ee", "#7209b7", "#f72585"]
        for i, color in enumerate(colors):
            offset = orb_anim_angle + (i * (math.pi / 2))
            ox = math.cos(offset) * (8 if active else 4)
            oy = math.sin(offset) * (8 if active else 4)
            r = base_r + (math.sin(orb_anim_angle * 3.2 + i) * 4)
            canvas_orb.create_oval(cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r, fill=color, outline="")

        inner_r = max(16, int(base_r * 0.72))
        canvas_orb.create_oval(cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r, fill="#4cc9f0", outline="")

        core_r = max(8, int(base_r * 0.38))
        canvas_orb.create_oval(cx - core_r, cy - core_r, cx + core_r, cy + core_r, fill="#ffffff", outline="")

        orb_anim_angle += 0.07 if not active else 0.15
        orb_window.after(25, animate_procedural_orb)

# --- 4. FULLSCREEN PYGAME AVATAR ---
def run_avatar_fullscreen():
    global CURRENT_MODE, SUB_USER, SUB_PIHU
    
    pygame.display.init()
    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Pihu AI")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("segoeui", 22, bold=True)

    def load_avatar_image(filename):
        try:
            path = get_path(f"assets/avatar/{filename}.png")
            img = pygame.image.load(path).convert_alpha()
            orig_w, orig_h = img.get_size()
            scale = min((WIDTH * 0.85) / orig_w, (HEIGHT * 0.90) / orig_h)
            new_w, new_h = int(orig_w * scale), int(orig_h * scale)
            return pygame.transform.smoothscale(img, (new_w, new_h)), new_w, new_h
        except Exception:
            return pygame.Surface((350, 450)), 350, 450

    idle, av_w, av_h = load_avatar_image("idle")
    blink, _, _ = load_avatar_image("blink")
    talk1, _, _ = load_avatar_image("talk1")
    talk2, _, _ = load_avatar_image("talk2")
    talk_frames = [talk1, talk2]
    talk_idx = 0
    talk_timer = time.time()
    blink_timer = time.time()

    true_black = (0, 0, 0)
    av_x = (WIDTH - av_w) // 2
    av_y = (HEIGHT - av_h) // 2 - 20

    while CURRENT_MODE == "AVATAR":
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                CURRENT_MODE = "STANDBY"
                break

        if CURRENT_MODE != "AVATAR":
            break

        screen.fill(true_black)

        if core.voice.is_speaking:
            if time.time() - talk_timer > 0.12:
                talk_idx = (talk_idx + 1) % len(talk_frames)
                talk_timer = time.time()
            current_avatar = talk_frames[talk_idx]
        else:
            current_avatar = idle
            if time.time() - blink_timer > 3.8:
                current_avatar = blink
                if time.time() - blink_timer > 4.0:
                    blink_timer = time.time()

        screen.blit(current_avatar, (av_x, av_y))

        overlay = pygame.Surface((WIDTH, 80))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, HEIGHT - 80))

        u_txt = font.render(f"🗣️ You: {SUB_USER[:65]}", True, (0, 255, 255))
        p_txt = font.render(f"🤖 Pihu: {SUB_PIHU[:75]}", True, (255, 255, 0))
        screen.blit(u_txt, (30, HEIGHT - 70))
        screen.blit(p_txt, (30, HEIGHT - 35))

        pygame.display.flip()
        clock.tick(30)

    try:
        pygame.display.quit()
    except Exception:
        pass

# --- 5. MASTER BACKGROUND INTELLIGENCE LOOP ---
def master_background_brain():
    global CURRENT_MODE, SUB_USER, SUB_PIHU, is_active_listening

    time.sleep(1)
    speak("Pihu background system active hai.")

    WAKE_WORDS = [
        "hey pihu", "pihu", "hello pihu", "sun pihu", "piyush", "hello piyush",
        "pehu", "pyari pihu", "hey pi", "view"
    ]

    while True:
        raw_input = listen()
        if not raw_input:
            time.sleep(0.1)
            continue

        q = raw_input.lower().strip()

        if any(k in q for k in [
            "chali jao", "fir se chali jao", "screen se jao", "screen se wapas jao",
            "screen se fir se chali jao", "hide ho jao", "minimize avatar",
            "screen se hato", "standby par jao", "standby"
        ]):
            SUB_PIHU = "Thik hai boss, main background me hu."
            speak(SUB_PIHU)
            CURRENT_MODE = "STANDBY"
            continue

        if any(k in q for k in [
            "screen per aao", "screen par aao", "samne aao", "full screen",
            "avatar aao", "screen par aana", "screen per aana",
            "puri screen per a jao", "puri screen par a jao", "puri screen per aana"
        ]):
            SUB_PIHU = "Ji boss, main screen par aa gayi hu."
            speak(SUB_PIHU)
            CURRENT_MODE = "AVATAR"
            threading.Thread(target=run_avatar_fullscreen, daemon=True).start()
            continue

        matched_wake = None
        for w in WAKE_WORDS:
            if w in q:
                matched_wake = w
                break

        if matched_wake or CURRENT_MODE == "AVATAR":
            if CURRENT_MODE != "AVATAR":
                orb_window.after(0, show_orb_safe)
            is_active_listening = True

            command = q
            if matched_wake:
                command = q.replace(matched_wake, "").strip()

            if len(command) <= 2:
                speak("Ji boss?")
                SUB_USER = "Listening..."
                cmd = listen()
                if cmd:
                    SUB_USER = cmd
                    is_active_listening = False
                    cmd_lower = cmd.lower().strip()

                    if any(k in cmd_lower for k in [
                        "chali jao", "fir se chali jao", "screen se jao",
                        "screen se wapas jao", "hide ho jao", "screen se hato"
                    ]):
                        SUB_PIHU = "Thik hai boss, main background me hu."
                        speak(SUB_PIHU)
                        CURRENT_MODE = "STANDBY"
                        continue

                    if any(k in cmd_lower for k in [
                        "screen per aao", "screen par aao", "samne aao", "avatar aao",
                        "puri screen per a jao", "puri screen par a jao"
                    ]):
                        if CURRENT_MODE != "AVATAR":
                            orb_window.after(0, hide_orb_safe)
                        SUB_PIHU = "Ji boss, main screen par aa gayi hu."
                        speak(SUB_PIHU)
                        CURRENT_MODE = "AVATAR"
                        threading.Thread(target=run_avatar_fullscreen, daemon=True).start()
                        continue

                    reply = get_offline_response(cmd)
                    if reply:
                        SUB_PIHU = reply
                        speak(reply)
            else:
                SUB_USER = command
                is_active_listening = False
                reply = get_offline_response(command)
                if reply:
                    SUB_PIHU = reply
                    speak(reply)

            time.sleep(0.8)
            if CURRENT_MODE != "AVATAR":
                orb_window.after(0, hide_orb_safe)
            is_active_listening = False

        time.sleep(0.1)

# --- 6. AGENT RUNTIME EXECUTION ---
def start_agent_runtime():
    create_orb_ui()
    threading.Thread(target=master_background_brain, daemon=True).start()
    animate_procedural_orb()
    orb_window.mainloop()

# --- 7. ENTRY POINT ---
if __name__ == "__main__":
    try:
        show_intro_screen()
    except KeyboardInterrupt:
        sys.exit(0)