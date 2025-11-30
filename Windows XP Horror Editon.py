import tkinter as tk
from tkinter import messagebox
import sys
import os
import subprocess
import threading

# --- FIX: GET THE EXACT FOLDER PATH ---
# This forces Python to look in the folder where this script is saved
script_folder = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_folder, "Bsod.png")

# Check for Pillow Library
try:
    from PIL import Image, ImageTk
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

class HorrorOS:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Windows XP - Horror Edition")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="black")
        
        # Bind escape to exit
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        # Check for Pillow Library
        if not HAS_PILLOW:
            messagebox.showerror("Missing Library", "CRITICAL ERROR:\nYou are missing the 'Pillow' library.\n\nOpen CMD and type: pip install pillow")
            self.root.destroy()
            return

        # Check for Image File using the FIXED path
        if not os.path.exists(image_path):
            messagebox.showerror("Missing File", f"CRITICAL ERROR:\nCannot find 'Bsod.png'.\n\nI looked here:\n{image_path}\n\nMake sure the picture is named exactly 'Bsod.png'.")
            self.root.destroy()
            return

        self.boot_screen()
        self.root.mainloop()

    def boot_screen(self):
        self.boot_frame = tk.Frame(self.root, bg="black")
        self.boot_frame.pack(fill="both", expand=True)

        logo = tk.Label(self.boot_frame, text="Microsoft\nWindows XP", fg="white", bg="black", font=("Trebuchet MS", 40, "bold"))
        logo.pack(pady=(200, 20))
        
        sub = tk.Label(self.boot_frame, text="HORROR EDITION", fg="red", bg="black", font=("Courier", 20, "bold"))
        sub.pack(pady=10)

        self.loading_label = tk.Label(self.boot_frame, text="[                    ]", fg="blue", bg="black", font=("Courier", 20))
        self.loading_label.pack(pady=50)
        
        self.load_step = 0
        self.animate_boot()

    def animate_boot(self):
        if self.load_step < 20:
            bar = "[" + "=" * self.load_step + " " * (20 - self.load_step) + "]"
            self.loading_label.config(text=bar)
            self.load_step += 1
            self.root.after(200, self.animate_boot)
        else:
            self.boot_frame.destroy()
            self.lock_screen()

    def lock_screen(self):
        self.lock_frame = tk.Frame(self.root, bg="#003366")
        self.lock_frame.pack(fill="both", expand=True)

        top = tk.Frame(self.lock_frame, bg="black", height=100)
        top.pack(fill="x")
        
        top_lbl = tk.Label(top, text="Windows XP", fg="white", bg="black", font=("Trebuchet MS", 20, "italic"))
        top_lbl.pack(pady=30, padx=20, anchor="w")

        center_frame = tk.Frame(self.lock_frame, bg="#003399", bd=2, relief="ridge")
        center_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=200)

        user_lbl = tk.Label(center_frame, text="Unknown User", fg="#cccccc", bg="#003399", font=("Arial", 14))
        user_lbl.pack(pady=20)

        self.pw_entry = tk.Entry(center_frame, font=("Arial", 12), show="*")
        self.pw_entry.pack(pady=10)
        self.pw_entry.bind("<Return>", self.login)

        login_btn = tk.Button(center_frame, text="Log On", command=self.login, bg="green", fg="white")
        login_btn.pack(pady=10)

        hint = tk.Label(self.lock_frame, text="(Hint: Don't look behind you)", fg="gray", bg="#003366")
        hint.pack(side="bottom", pady=20)

    def login(self, event=None):
        self.lock_frame.destroy()
        self.desktop()

    def desktop(self):
        self.desk_frame = tk.Frame(self.root, bg="#550000")
        self.desk_frame.pack(fill="both", expand=True)

        taskbar = tk.Frame(self.desk_frame, bg="#1a1a1a", height=40)
        taskbar.pack(side="bottom", fill="x")

        start_btn = tk.Button(taskbar, text="DEAD", bg="green", fg="white", font=("Arial", 10, "bold", "italic"), width=10)
        start_btn.pack(side="left", padx=2, pady=2)

        time_lbl = tk.Label(taskbar, text="6:66 PM", bg="#1a1a1a", fg="red", font=("Arial", 10))
        time_lbl.pack(side="right", padx=10)

        self.create_icon("My Computer", 20, 20, self.my_computer_click)
        self.create_icon("Recycle Bin", 20, 100)
        self.create_icon("Do Not Open.txt", 20, 180)

        self.root.after(3000, self.scary_popup)

    def create_icon(self, name, x, y, command=None):
        f = tk.Frame(self.desk_frame, bg="#550000")
        f.place(x=x, y=y)
        icon_btn = tk.Button(f, text="[?]", fg="white", bg="#550000", font=("Arial", 20), borderwidth=0, command=command)
        icon_btn.pack()
        lbl = tk.Label(f, text=name, fg="white", bg="#550000")
        lbl.pack()

    def my_computer_click(self):
        response = messagebox.askyesno("My Computer", "Do you want to trash your computer forever?", icon="question")
        if response:
            self.play_scream_and_show_bsod()

    def play_scream_and_show_bsod(self):
        """Play scream.wav in wmplayer and show BSOD image"""
        # Play scream in separate thread
        threading.Thread(target=self._play_scream_in_wmplayer, daemon=True).start()
        # Show BSOD image
        self.root.after(500, self.show_bsod_image)
    
    def _play_scream_in_wmplayer(self):
        """Play scream.wav using wmplayer.exe"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        scream_path = os.path.join(script_dir, 'scream.wav')
        if os.path.exists(scream_path):
            try:
                subprocess.Popen(['wmplayer.exe', scream_path])
            except Exception:
                pass
    
    def show_bsod_image(self):
        """Display the BSOD image fullscreen"""
        try:
            if hasattr(self, 'desk_frame') and self.desk_frame.winfo_exists():
                self.desk_frame.destroy()
            self.bsod_frame = tk.Frame(self.root, bg="blue")
            self.bsod_frame.pack(fill="both", expand=True)
            
            # Load and display BSOD image
            image = Image.open(image_path)
            
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            image = image.resize((screen_width, screen_height), Image.LANCZOS)
            
            self.bsod_image = ImageTk.PhotoImage(image)
            img_label = tk.Label(self.bsod_frame, image=self.bsod_image, bg="blue")
            img_label.pack(fill="both", expand=True)
            
            # Auto-close after 10 seconds (press ESC to close early)
            self.root.after(10000, lambda: self.root.destroy())
        except Exception as e:
            messagebox.showerror("Image Error", f"Could not load Bsod.png:\n{e}")

    def red_screen_of_death(self):
        try:
            self.desk_frame.destroy()
            self.rsod_frame = tk.Frame(self.root, bg="red")
            self.rsod_frame.pack(fill="both", expand=True)
            
            # USE THE FIXED PATH HERE
            image = Image.open(image_path)
            
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            image = image.resize((screen_width, screen_height), Image.LANCZOS)
            
            self.rsod_image = ImageTk.PhotoImage(image)
            img_label = tk.Label(self.rsod_frame, image=self.rsod_image, bg="red")
            img_label.pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Image Error", f"Could not load Bsod.png:\n{e}")

    def scary_popup(self):
        if hasattr(self, 'desk_frame') and self.desk_frame.winfo_exists():
            box = tk.Toplevel(self.root)
            box.geometry("300x150")
            box.title("System Error")
            box.configure(bg="black")
            msg = tk.Label(box, text="Your soul is corrupted.\nCannot delete System32.", fg="red", bg="black", font=("Courier", 12))
            msg.pack(expand=True)
            btn = tk.Button(box, text="OK", command=box.destroy)
            btn.pack(pady=10)

if __name__ == "__main__":
    try:
        app = HorrorOS()
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Crash Report", f"The app crashed because:\n{e}")                              