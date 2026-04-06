import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "codellama"


def _call_ollama(prompt, model=DEFAULT_MODEL):
    """Internal helper: sends a prompt to Ollama and returns the response text."""
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(
            OLLAMA_URL,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data)
        )
        if response.status_code == 200:
            return json.loads(response.text)['response']
        else:
            return f"Error from Ollama API: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Failed to connect to local Ollama server: {str(e)}"


def analyze_code(file_content, model=DEFAULT_MODEL):
    """
    Sends the file content to Ollama with a system prompt asking for a code review.
    """
    prompt = f"""You are an expert AI Code Reviewer. Please review the following code carefully.
Identify any bugs, potential security issues, or logic errors, and suggest improvements.
Format your response using Markdown with clear headings and bullet points.

Code to review:
```python
{file_content}
```
"""
    return _call_ollama(prompt, model)


def debug_code(file_content, traceback_log, model=DEFAULT_MODEL):
    """
    Correlates a real error traceback/log with the provided source file.
    Returns a ranked root-cause diagnosis and a concrete patch plan.
    """
    prompt = f"""You are an expert debugger. A developer is facing a runtime error and needs precise help.

Do NOT give generic advice. Every observation must reference the specific code below.

---
**Source Code:**
```python
{file_content}
```

---
**Error Traceback / Log:**
```
{traceback_log}
```

---
Your response MUST follow this exact structure in Markdown:

## 1. Root Cause Triage
Identify the exact line number(s) and function(s) responsible for the failure. Explain *why* they fail.

## 2. Ranked Diagnosis
If multiple causes are possible, list them ranked from most to least likely. For each:
- **Cause**: what is wrong
- **Evidence**: which line / which part of the traceback points to it
- **Likelihood**: High / Medium / Low

## 3. Patch Plan
Show the exact code changes needed. Use a before/after diff format:
```python
# BEFORE
...

# AFTER
...
```

## 4. Prevention Tips
Briefly mention how to avoid this class of bug in the future.
"""
    return _call_ollama(prompt, model)
