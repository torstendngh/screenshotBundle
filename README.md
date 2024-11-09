# 📸📦 ScreenshotBundle
I created ScreenshotBundle as a lightweight Python tool to quickly take and save screenshots into a designated folder. I made this tool because I wanted an easy way to gather visual references, capture moments from old games, or organize screenshots for creative inspiration.

### Features
- Simple and fast screenshot capture.
- Automatically saves screenshots to an organized, timestamped folder.
- Easy-to-use, with minimal setup required.
### My Use Cases
- Collecting visual references for art or game development.
- Archiving screenshots from classic or retro games.
- Quick documentation of screen activities for projects or tutorials.

## 🤔 Why I Built This
I often found myself needing a quick way to take screenshots while playing old games or working on projects where visual references were essential. ScreenshotBundle helps me gather these screenshots efficiently without manual sorting.

## 🎓 How To Use
1. Start `ScreenshotBundle.exe`:
    - Double-click `ScreenshotBundle.exe` to launch the application.
1. Press `Start` to begin the screenshotting session:
    - This action creates a new session folder.
    - Note: Screenshots cannot be taken until the session has started.
1. Take screenshots with `Ctrl + Space`:
    - Screenshots will be stored in the "Screenshots" folder within the session folder.
    - The tool captures screenshots of the monitor where the cursor is currently located.
    - Optionally, activate "Capture All Screens" to take a screenshot of all connected monitors simultaneously.
1. Press `Stop` when finished:
    - This will end the session and save all captured screenshots.

## 🏗️ Building the Executable
To convert the Python script into a standalone .exe file, follow these steps:

1. `pip install pyinstaller`
1. Navigate to the project directory in your command line or terminal.
1. Run the following command:
    ```bash
    pyinstaller --onefile --icon=icon.ico --name=ScreenshotBundle --noconsole main.py
    ```