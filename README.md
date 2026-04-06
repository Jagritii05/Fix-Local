# Fix-Local

A privacy-focused code assistant built to run completely offline on your own hardware using Ollama. No cloud APIs, no data leaving your machine.

I built this because I wanted a way to get solid code reviews and debug tracebacks without having to paste my source code into ChatGPT every time. It comes with a command-line interface for quick checks in the terminal, and a Gradio web app when you want an actual UI.

## Features

- **Code Review**: Point it at a file, and it'll flag bugs, security risks, or logic errors.
- **Debug Session Mode**: The most useful part. If your code crashes, you give it the buggy file and the exact traceback. Instead of generic "make sure you installed X" advice, it cross-references the error with your file and gives you a ranked diagnosis and the exact code patch to fix it.
- **Dual Interface**: Use the terminal (`cli.py`) or the web UI (`app.py`).

## Setup

You'll need Python and [Ollama](https://ollama.com/) installed.

1. Clone the repo and install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: You might also need `rich` and `gradio` if they aren't in your environment).*

2. Make sure Ollama is running and has the model pulled. By default, the app uses `codellama`, but you can pass whatever model you want via flags or the UI.
   ```bash
   ollama pull codellama
   ```

## How to use it

### The Web App
Just run the app file. It'll pop open a browser tab on port 7860.
```bash
python app.py
```
There's a standard chat tab, and a dedicated "Debug Session" tab where you can upload a file and paste your error logs.

### The CLI
If you prefer staying in your terminal:

**To review a file:**
```bash
python cli.py review core.py
```

**To debug a crash:**
You can either paste the traceback directly, or point to an error log file if it's too long.
```bash
python cli.py debug your_script.py --logfile error.log
```
_Or inline:_
```bash
python cli.py debug your_script.py --log "NameError: name 'x' is not defined..."
```

