import tkinter as tk
from core import TerminalEditor, CryptoManager

class TermiNoteApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TermiNote v1.5")
        self.root.geometry("900x600")
        self.crypto = CryptoManager()
        
        callbacks = {
            'save': self.crypto.save_sealed,
            'load': self.crypto.load_unsealed,
            'list': self.crypto.get_file_list,
            'search': self.crypto.search_files,
            'delete': self.crypto.delete_file,
            'rename': self.crypto.rename_file
        }
        
        self.editor = TerminalEditor(self.root, callbacks)
        initial_content = self.crypto.load_unsealed("vault.txt")
        self.editor.text_area.insert("1.0", initial_content)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TermiNoteApp()
    app.run()