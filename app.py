import requests
import json
import gradio as gr
from core import debug_code

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "codellama"
MAX_HISTORY = 5


def call_ollama(message, history):
    """
    Streaming chat handler.
    History is [[user_msg, ai_msg], ...] as provided by Gradio.
    """
    formatted_messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful, expert AI Coding Assistant running locally. "
                "Provide clear, concise, and accurate answers formatted in Markdown."
            )
        }
    ]

    recent_history = history[-MAX_HISTORY:] if len(history) > MAX_HISTORY else history
    for user_msg, ai_msg in recent_history:
        formatted_messages.append({"role": "user",      "content": user_msg})
        formatted_messages.append({"role": "assistant", "content": ai_msg})

    formatted_messages.append({"role": "user", "content": message})

    data = {"model": DEFAULT_MODEL, "messages": formatted_messages, "stream": True}

    try:
        response = requests.post(OLLAMA_CHAT_URL, json=data, stream=True)
        response.raise_for_status()
        partial_message = ""
        for line in response.iter_lines():
            if line:
                body = json.loads(line)
                content = body.get("message", {}).get("content", "")
                partial_message += content
                yield partial_message
    except requests.exceptions.RequestException as e:
        yield f"**Connection Error:** Could not connect to local Ollama server.\nError details: {e}"


chat_tab = gr.ChatInterface(
    fn=call_ollama,
    chatbot=gr.Chatbot(height=550, label="Chat"),
    textbox=gr.Textbox(placeholder="Ask me a coding question...", container=False, scale=7),
)


def run_debug_session(uploaded_file, traceback_text, model_choice):
    """
    Reads the uploaded source file, correlates it with the pasted traceback,
    and returns a ranked root-cause diagnosis + patch plan.
    """
    if uploaded_file is None:
        return "⚠️ Please upload a source file first."
    if not traceback_text or not traceback_text.strip():
        return "⚠️ Please paste an error traceback or log."

    try:
        with open(uploaded_file.name, "r", encoding="utf-8") as f:
            source_code = f.read()
    except Exception as e:
        return f"**Error reading file:** {e}"

    result = debug_code(source_code, traceback_text.strip(), model=model_choice)
    return result


with gr.Blocks() as debug_tab:
    gr.Markdown(
        """
        ## 🐛 Debug Session Mode
        Upload your source file and paste the error traceback below.
        The assistant will **correlate the error with your code**, rank the most likely root causes,
        and produce a concrete **patch plan** — no generic advice.
        """
    )
    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(
                label="📂 Upload Source File",
                file_types=[".py", ".js", ".ts", ".java", ".go", ".cpp", ".c", ".rb"],
            )
            model_dropdown = gr.Dropdown(
                choices=["codellama", "deepseek-coder", "llama3", "mistral"],
                value="codellama",
                label="🤖 Model",
            )
            run_btn = gr.Button("🔍 Analyse & Diagnose", variant="primary")
        with gr.Column(scale=2):
            traceback_input = gr.Textbox(
                label="📋 Paste Error Traceback / Log",
                placeholder="Traceback (most recent call last):\n  File \"app.py\", line 42, in ...\nNameError: name 'x' is not defined",
                lines=12,
            )

    gr.Markdown("---")
    debug_output = gr.Markdown(label="Debug Report")

    run_btn.click(
        fn=run_debug_session,
        inputs=[file_input, traceback_input, model_dropdown],
        outputs=debug_output,
    )


app = gr.TabbedInterface(
    interface_list=[chat_tab, debug_tab],
    tab_names=["💬 Chat", "🐛 Debug Session"],
    title="🤖 Local AI Code Assistant",
)

if __name__ == "__main__":
    app.launch(inbrowser=True, theme=gr.themes.Soft())