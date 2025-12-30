import customtkinter as ctk
from tkinter import messagebox
import shutil
import os
import subprocess

# ---------- APP SETUP ----------
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")  # closest purple-ish built-in theme

app = ctk.CTk()
app.geometry("640x480")
app.title("Buttered RAT Builder")
app.resizable(False, False)

# ---------- GLOBAL FONT ----------
FONT = ("Segoe UI", 20, "bold")  # bright, readable font

# ---------- FRAME FOR CENTERING ----------
frame = ctk.CTkFrame(app, corner_radius=15, fg_color="#2b2b2b")
frame.pack(padx=40, pady=40, fill="both", expand=True)

# ---------- LABELS & ENTRIES ----------
ctk.CTkLabel(frame, text="Discord Bot Token", font=FONT).pack(pady=(20, 5))
token_entry = ctk.CTkEntry(frame, width=400, placeholder_text="Enter your bot token...", font=FONT)
token_entry.pack(pady=5)

ctk.CTkLabel(frame, text="Guild ID", font=FONT).pack(pady=(20, 5))
guild_entry = ctk.CTkEntry(frame, width=400, placeholder_text="Enter the guild ID...", font=FONT)
guild_entry.pack(pady=5)

# ---------- FUNCTION ----------
def build_bot():
    token = token_entry.get().strip()
    guild_id = guild_entry.get().strip()

    if not token or not guild_id:
        messagebox.showerror("Error", "Please enter both token and guild ID")
        return

    try:
        # Ensure build folder exists
        os.makedirs("build", exist_ok=True)

        # Copy base.py to build/main.py
        shutil.copy("base.py", "build/main.py")

        # Replace placeholders
        main_file = "build/main.py"
        with open(main_file, "r", encoding="utf-8") as f:
            content = f.read()

        content = content.replace('thymainguildeid = 1', f'thymainguildeid = {guild_id}')
        content = content.replace('thyobftoketoke = "a"', f'thyobftoketoke = "{token}"')

        with open(main_file, "w", encoding="utf-8") as f:
            f.write(content)

        messagebox.showinfo("Success", f"build/main.py has been updated!\nOpening folder...")

        # Open Explorer at build folder
        subprocess.Popen(f'explorer "{os.path.abspath("build")}"')

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

# ---------- BUTTON ----------
build_button = ctk.CTkButton(frame, text="Build Bot (vibecoded af)", command=build_bot, font=FONT, hover_color="#6c4cff")
build_button.pack(pady=40)

# ---------- RUN APP ----------
app.mainloop()
