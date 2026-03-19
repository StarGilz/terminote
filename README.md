# TermiNote v1.5 🚀

A terminal-style encrypted memo pad built with Python & Tkinter. 
Designed for those who love the CLI experience and need a secure space for quick notes.

## ✨ Key Features
- **File Browser**: Open files with arrow keys and Enter inside the browser mode (`:ls`).
- **Grep Search**: Instant keyword search across all encrypted notes (`:grep keyword`).
- **File Management**: 
  - **Rename**: Change filenames easily using the `:mv <old> <new>` command.
  - **Delete**: Remove notes via `:rm <name>` or by pressing `DEL` in the browser.
- **Smart Input**: Automatically converts Korean keyboard inputs to English commands (e.g., `;ㅈ` -> `:w`).
- **Real-time Status**: Displays `EDITING (*)` when there are unsaved changes.
- **Encryption**: All notes are stored in Base64 format for basic privacy.

## ⌨️ Command Reference
| Command | Action | Korean Input Support |
| :--- | :--- | :--- |
| `:w` | Save current file | `:ㅈ` |
| `:ls` | Open File Browser | `:ㅣㄴ` |
| `:e <name>` | Edit or create a new file | `:ㄷ` |
| `:mv <o> <n>` | Rename file | `:ㅡㅍ` |
| `:rm <name>` | Delete a file | `:ㄱㅡ` |
| `:grep <str>` | Search for keyword | `:ㅎㄱ데` |
| `:h` | Show help menu | `:ㅎ` |
| `:q` | Quit editor | `:ㅂ` |

## 🚀 How to Run
1. Ensure Python 3.x is installed.
2. Run the application:
   ```bash
   python main.py