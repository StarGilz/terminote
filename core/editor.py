import tkinter as tk
from tkinter import font, messagebox

class TerminalEditor:
    def __init__(self, root, callbacks):
        self.root = root
        self.callbacks = callbacks
        self.current_file = "vault.txt"
        self.mode = "EDIT"
        self.is_modified = False
        self.file_list = []
        self.selected_idx = 0
        self.custom_font = font.Font(family="Consolas", size=12)
        
        self.text_area = tk.Text(
            self.root, bg="#0D0D0D", fg="#00FF00", 
            insertbackground="#00FF00", font=self.custom_font,
            relief="flat", padx=10, pady=10, undo=True
        )
        self.text_area.pack(expand=True, fill='both')
        
        self.status_bar = tk.Label(
            self.root, text="",
            bg="#1A1A1A", fg="#888888", font=("Consolas", 9), anchor="w"
        )
        self.status_bar.pack(side="bottom", fill="x")

        self.cmd_line = tk.Entry(
            self.root, bg="#1A1A1A", fg="#FFFF00", 
            insertbackground="#FFFF00", font=self.custom_font,
            relief="flat", borderwidth=0
        )
        self.cmd_line.pack(side="bottom", fill="x")
        
        self.cmd_line.bind("<Return>", self.execute_command)
        self.root.bind("<Escape>", self.focus_editor)
        self.root.bind("<F1>", self.focus_command_line)
        self.root.bind("<Up>", self.navigate_browser)
        self.root.bind("<Down>", self.navigate_browser)
        self.root.bind("<Delete>", self.delete_file_in_browser)
        self.text_area.bind("<Return>", self.select_file_in_browser)
        self.text_area.bind("<KeyPress>", self.on_key_press)
        
        self.update_status("READY")

    def on_key_press(self, event=None):
        if self.mode == "EDIT" and event.keysym not in ["Escape", "F1", "Control_L", "Control_R", "Shift_L", "Shift_R"]:
            self.is_modified = True
            self.update_status("EDITING (*)")

    def focus_command_line(self, event=None):
        if self.mode in ["BROWSER", "HELP"]: return "break"
        self.cmd_line.delete(0, tk.END)
        self.cmd_line.insert(0, ":")
        self.cmd_line.focus_set()
        return "break"

    def focus_editor(self, event=None):
        if self.mode in ["BROWSER", "HELP"]:
            self.mode = "EDIT"
            content = self.callbacks['load'](self.current_file)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", content)
            self.is_modified = False
        
        self.cmd_line.delete(0, tk.END)
        self.text_area.focus_set()
        status_msg = "EDITING (*)" if self.is_modified else "IDLE"
        self.update_status(status_msg)
        return "break"

    def execute_command(self, event=None):
        raw_cmd = self.cmd_line.get().strip()
        if not raw_cmd: 
            self.focus_editor()
            return "break"
        parts = raw_cmd.split()
        cmd = parts[0]

        if cmd == ":h":
            self.show_help()
            self.cmd_line.delete(0, tk.END)
            return "break"

        elif cmd == ":ls":
            self.cmd_line.delete(0, tk.END)
            self.enter_browser_mode()
            return "break"

        elif cmd == ":rm" and len(parts) > 1:
            target = parts[1]
            if messagebox.askyesno("Delete", f"Delete {target}?"):
                if self.callbacks['delete'](target):
                    self.update_status(f"DELETED: {target}")
                else:
                    self.update_status(f"FAILED TO DELETE: {target}")
            self.cmd_line.delete(0, tk.END)
            return "break"

        elif cmd == ":grep" and len(parts) > 1:
            keyword = parts[1]
            matching_files = self.callbacks['search'](keyword)
            if matching_files:
                self.mode = "BROWSER"
                self.file_list = matching_files
                self.selected_idx = 0
                self.draw_browser()
                self.cmd_line.delete(0, tk.END)
                self.text_area.focus_set()
                self.update_status(f"SEARCH: {keyword}")
            else:
                self.update_status("NO MATCH FOUND")
                self.cmd_line.delete(0, tk.END)
            return "break"

        elif cmd == ":w":
            content = self.text_area.get("1.0", tk.END).strip()
            self.callbacks['save'](self.current_file, content)
            self.is_modified = False
            self.update_status(f"SAVED '{self.current_file}'")
            self.cmd_line.delete(0, tk.END)
            self.text_area.focus_set()
            return "break"

        elif cmd == ":q":
            self.root.destroy()
            return "break"

        elif cmd == ":wq":
            content = self.text_area.get("1.0", tk.END).strip()
            self.callbacks['save'](self.current_file, content)
            self.root.destroy()
            return "break"

        elif cmd == ":e" and len(parts) > 1:
            self.current_file = parts[1]
            content = self.callbacks['load'](self.current_file)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", content)
            self.is_modified = False
            self.update_status(f"OPENED: {self.current_file}")

        self.focus_editor()
        return "break"

    def show_help(self):
        self.mode = "HELP"
        self.text_area.delete("1.0", tk.END)
        help_text = (
            "--- COMMAND HELP (Press ESC to return) ---\n\n"
            ":w           - Save current file\n"
            ":q           - Quit editor\n"
            ":wq          - Save and Quit\n"
            ":ls          - Open File Browser\n"
            ":rm <name>   - Delete a file\n"
            ":e <name>    - Edit or create a new file\n"
            ":grep <word> - Search for files containing keyword\n"
            ":h           - Show this help menu\n\n"
            "F1           - Focus command line\n"
            "ESC          - Return to editor / Cancel mode\n"
            "DEL (in ls)  - Delete selected file"
        )
        self.text_area.insert(tk.END, help_text)
        self.text_area.focus_set()
        self.update_status("MODE: HELP")

    def enter_browser_mode(self):
        self.mode = "BROWSER"
        self.file_list = self.callbacks['list']()
        self.selected_idx = 0
        self.draw_browser()
        self.text_area.focus_set()

    def draw_browser(self):
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, "--- BROWSER (Up/Down: Move, Enter: Open, DEL: Delete, ESC: Exit) ---\n\n")
        if not self.file_list:
            self.text_area.insert(tk.END, "   (No files found)")
        else:
            for i, filename in enumerate(self.file_list):
                if i == self.selected_idx:
                    self.text_area.insert(tk.END, f" > {filename}\n", "highlight")
                else:
                    self.text_area.insert(tk.END, f"   {filename}\n")
        self.text_area.tag_configure("highlight", foreground="black", background="#00FF00")
        self.update_status("MODE: BROWSER")

    def navigate_browser(self, event):
        if self.mode != "BROWSER": return
        if event.keysym == "Up":
            self.selected_idx = max(0, self.selected_idx - 1)
        elif event.keysym == "Down":
            self.selected_idx = min(len(self.file_list) - 1, self.selected_idx + 1)
        self.draw_browser()
        return "break"

    def delete_file_in_browser(self, event):
        if self.mode != "BROWSER" or not self.file_list: return
        target = self.file_list[self.selected_idx]
        if messagebox.askyesno("Delete", f"Confirm deletion of {target}?"):
            if self.callbacks['delete'](target):
                self.file_list = self.callbacks['list']()
                self.selected_idx = min(self.selected_idx, len(self.file_list) - 1) if self.file_list else 0
                self.draw_browser()
                self.update_status(f"DELETED: {target}")
        return "break"

    def select_file_in_browser(self, event):
        if self.mode != "BROWSER": return
        if self.file_list:
            self.current_file = self.file_list[self.selected_idx]
            content = self.callbacks['load'](self.current_file)
            self.mode = "EDIT"
            self.is_modified = False
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", content)
            self.update_status(f"OPENED: {self.current_file}")
            self.text_area.focus_set()
        return "break"

    def update_status(self, message):
        self.status_bar.config(text=f" {message} | FILE: {self.current_file} ")