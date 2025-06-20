import os
import json
import subprocess
import customtkinter as ctk
from tkinter import filedialog, simpledialog

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".slicerdhub", "config.json")
os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
ctk.set_appearance_mode("System")

from PIL import Image
import win32gui
import win32ui
import win32con

def extract_icon_from_exe(exe_path):
    try:
        large, small = win32gui.ExtractIconEx(exe_path, 0)
        hicon = large[0] if large else small[0] if small else None
        if not hicon:
            return None

        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, 64, 64)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        win32gui.DrawIconEx(hdc.GetHandleOutput(), 0, 0, hicon, 64, 64, 0, None, win32con.DI_NORMAL)

        bmpinfo = hbmp.GetInfo()
        bmpstr = hbmp.GetBitmapBits(True)
        image = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        return image.resize((48, 48))
    except Exception as e:
        print(f"Error loading icon: {e}")
        return None

class SlicerHubApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ico_path = os.path.join(os.path.dirname(__file__), "SlicerDHub.ico")
        if os.path.exists(ico_path):
            try:
                self.iconbitmap(ico_path)
            except Exception as e:
                print(f"Failed to set icon: {e}")

        self.title("SlicerDHub")

        self.settings = self.load_settings()

        self.update_idletasks()
        self.resizable(False, False)

        self.settings = self.load_settings()
        ctk.set_appearance_mode(self.settings.get("theme", "System"))

        self.slicers = self.load_slicers()
        self.edit_mode = False

        self.label = ctk.CTkLabel(self, text="Make the choice", font=("Segoe UI", 18))
        self.label.pack(pady=10)

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid_columnconfigure((0,1), weight=1)
        self.button_frame.pack(expand=True, fill="both", pady=20)

        self.render_buttons()

        button_panel = ctk.CTkFrame(self)
        button_panel.pack(pady=10)

        edit_button = ctk.CTkButton(button_panel, text="✏️ Edit", command=self.toggle_edit_mode)
        edit_button.pack(side="left", padx=5)

        self.submenu_frame = ctk.CTkFrame(button_panel)
        self.submenu_frame.pack_forget()

        self.add_button = ctk.CTkButton(self.submenu_frame, text="➕ Add slicer", command=self.add_slicer)
        self.add_button.pack(padx=5, pady=2)

        self.save_button = ctk.CTkButton(self.submenu_frame, text="💾 Add save", command=self.add_save_button)
        self.save_button.pack(padx=5, pady=2)

        settings_button = ctk.CTkButton(button_panel, text="⚙️ Settings", command=self.open_settings)
        settings_button.pack(side="left", padx=5)

        donate_button = ctk.CTkButton(self, text="Buy Me a Coffee ☕", command=self.open_donate)
        donate_button.pack(pady=(0, 5))

        author_label = ctk.CTkLabel(self, text="HDaveSoft  |  Version 0.33")
        author_label.pack(pady=(0, 10))

        self.after(100, self.center_window)

    def save_settings(self):
        try:
            data = {"settings": self.settings, "slicers": self.slicers}
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving settings.json: {e}")

    def load_slicers(self):
        return self.slicers

    def save_slicers(self):
        self.save_settings()

    def add_save_button(self):
        dialog = ctk.CTkInputDialog(text="Enter name for save:", title="Save name")
        dialog.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        win_width = 400
        win_height = 160
        x = int((screen_width - win_width) / 2)
        y = int((screen_height - win_height) / 2)
        dialog.geometry(f"{win_width}x{win_height}+{x}+{y}")
        name = dialog.get_input()
        if name:
            self.slicers.append({"name": name, "path": "__save__"})
            self.save_slicers()
            self.render_buttons()

    def render_buttons(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        cols = 2
        rows = (len(self.slicers) + 1) // 2
        height = max(320, 180 + rows * 140)
        self.minsize(500, height + 130)
        total_height = height + 100
        self.geometry(f"500x{total_height}")
        for idx, slicer in enumerate(self.slicers):
            row, col = divmod(idx, cols)
            icon_image = extract_icon_from_exe(slicer["path"])
            ctk_img = ctk.CTkImage(dark_image=icon_image, size=(48, 48)) if icon_image else None

            frame = ctk.CTkFrame(self.button_frame, width=130, height=130)
            frame.grid(row=row, column=col, padx=20, pady=20, sticky="n")
            frame.grid_propagate(False)

            btn = ctk.CTkButton(
                master=frame,
                font=("Segoe UI", 12),
                text=slicer["name"],
                image=ctk_img,
                compound="top",
                width=120,
                height=120,
                command=lambda p=slicer["path"]: self.launch_slicer(p)
            )
            btn.pack()

            if self.edit_mode:
                delete_btn = ctk.CTkButton(
                    master=frame,
                    text="✕",
                    width=24,
                    height=24,
                    fg_color="red",
                    hover_color="#aa0000",
                    font=("Segoe UI", 12, "bold"),
                    command=lambda i=idx: self.delete_slicer(i)
                )
                delete_btn.place(x=95, y=0)

    def delete_slicer(self, index):
        del self.slicers[index]
        self.save_slicers()
        self.render_buttons()

    def add_slicer(self):
        path = filedialog.askopenfilename(title="Select .exe file of slicer", filetypes=[("Executable Files", "*.exe")])
        if path:
            dialog = ctk.CTkInputDialog(text="Enter slicer name:", title="Slicer name")
            dialog.geometry("400x160")
            name = dialog.get_input()
            if name:
                self.slicers.append({"name": name, "path": path})
                self.save_slicers()
                self.render_buttons()

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        if self.edit_mode:
            self.submenu_frame.pack(side="left")
        else:
            self.submenu_frame.pack_forget()
        self.render_buttons()

    def launch_slicer(self, path):
        import sys
        if len(sys.argv) > 1:
            export_file = sys.argv[1]
            if path == "__save__":
                save_path = filedialog.asksaveasfilename(
                    title="Save file as",
                    initialfile=os.path.basename(export_file),
                    defaultextension=os.path.splitext(export_file)[1],
                    filetypes=[("All files", "*.*")]
                )
                if save_path:
                    try:
                        with open(export_file, "rb") as src, open(save_path, "wb") as dst:
                            dst.write(src.read())
                    except Exception as e:
                        print(f"Error saving file: {e}")
            else:
                subprocess.Popen([path, export_file], shell=True)
                if self.settings.get("close_on_launch", True):
                    self.destroy()

    def center_window(self):
        self.update_idletasks()
        width = 500
        height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def open_settings(self):
        settings_window = ctk.CTkToplevel(self)
        self.settings_window = settings_window
        settings_window.title("Settings")
        settings_window.geometry("300x200")
        settings_window.resizable(False, False)
        settings_window.transient(self)
        settings_window.grab_set()

        checkbox = ctk.CTkCheckBox(
            master=settings_window,
            text="Close SlicerDHub after slicer launch",
            command=lambda: self.toggle_close_on_launch(var.get())
        )
        var = ctk.BooleanVar(value=self.settings.get("close_on_launch", True))
        checkbox.configure(variable=var)
        checkbox.pack(pady=10)

        theme_label = ctk.CTkLabel(settings_window, text="Theme:")
        theme_label.pack(pady=(10, 2))
        theme_option = ctk.CTkOptionMenu(settings_window, values=["System", "Light", "Dark"], command=self.set_theme)
        theme_option.set(self.settings.get("theme", "System"))
        theme_option.pack()

    def set_theme(self, value):
        self.settings["theme"] = value
        self.save_settings()
        self.settings_window.destroy()
        ctk.set_appearance_mode(value)

    def toggle_close_on_launch(self, value):
        self.settings["close_on_launch"] = value
        self.save_settings()

    def open_donate(self):
        import webbrowser
        webbrowser.open("https://coff.ee/hdavesoft")

    def load_settings(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.slicers = data.get("slicers", [])
                    return data.get("settings", {})
            except Exception as e:
                print(f"Error loading config.json: {e}")
        self.slicers = []
        return {"close_on_launch": True, "theme": "System"}

if __name__ == "__main__":
    app = SlicerHubApp()
    app.mainloop()
