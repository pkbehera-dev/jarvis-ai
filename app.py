import html
from flask import Flask, render_template, request, jsonify
import json
import system_commands
import os
from dotenv import load_dotenv
import requests
import re
import time # Import time module

load_dotenv()

app = Flask(__name__)

# Hardcoded permanent memory
memory = {
    "AI_NAME": "Jarvis",
    "OWNER_CREATOR": "Pradyumna"
}

# In-memory chat history
chat_history = []

# Define the Gemini API endpoint
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def get_gemini_response(user_query, chat_history):
    headers = {
        "Content-Type": "application/json"
    }
    messages = []
    for entry in chat_history:
        messages.append({"role": entry["role"], "parts": [{"text": entry["content"]}]})
    
    messages.append({"role": "user", "parts": [{"text": user_query}]})

    data = {
        "contents": messages
    }
    
    try:
        response = requests.post(f'{GEMINI_API_URL}?key={os.getenv("GOOGLE_API_KEY")}', headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        
        gemini_text = "No response from Gemini API."
        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            for part in response_json["candidates"][0]["content"]["parts"]:
                if "text" in part:
                    gemini_text = part["text"]
                    break # Take the first text part

        # Regex to find code blocks: ```[language]\n[code]```
        # It captures the optional language and the code content
        code_block_pattern = re.compile(r"```(?P<lang>\w+)?\n(?P<code>.*?)\n```", re.DOTALL)

        def replace_code_block(match):
            lang = match.group("lang") if match.group("lang") else "python" # Default to python
            code = match.group("code")
            # Escape HTML characters in the code to prevent XSS and ensure correct rendering
            escaped_code = html.escape(code)
            return f"<pre><code class=\"language-{lang}\">{escaped_code}</code></pre>"

        # Replace all found code blocks with HTML wrapped versions
        formatted_response = code_block_pattern.sub(replace_code_block, gemini_text)
        
        return formatted_response

    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return f"Error communicating with AI: {e}"
    except json.JSONDecodeError:
        print(f"Error decoding JSON response from Gemini API: {response.text}")
        return "Error processing AI response."

@app.route('/')
def index():
    return render_template('index.html', chat_history=chat_history)

@app.route('/chat', methods=['POST'])
def chat():
    global memory, chat_history
    user_input = request.form['user_input']
    
    # Add user message to chat history
    chat_history.append({"role": "user", "content": user_input})
    
    start_time = time.time() # Record start time

    # Try to execute a system command first
    response, save_required = system_commands.execute_command(user_input, memory, chat_history)
    
    
            
    if not response:
        # If no system command was triggered, call the Gemini API
        response = get_gemini_response(user_input, chat_history)

    end_time = time.time() # Record end time
    response_time = round(end_time - start_time, 2) # Calculate response time, round to 2 decimal places

    # Add assistant message to chat history
    chat_history.append({"role": "assistant", "content": response})
    
    return jsonify({"response": response, "chat_history": chat_history, "response_time": response_time}) # Include response_time

if __name__ == '__main__':
    app.run(debug=True)