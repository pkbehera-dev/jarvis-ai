# Jarvis AI Assistant

Jarvis is a personal AI assistant built using Flask and the Google Gemini API. It provides a conversational interface, allowing you to interact with an AI, execute system commands, and remember information.

## Features

- **Conversational AI:** Interact with Jarvis using natural language.
- **System Commands:** Execute predefined system commands (e.g., open applications, search the web, get date/time).
- **Memory:** Jarvis can remember specific information you tell it.
- **Web Interface:** A simple and intuitive web-based chat interface.
- **Syntax Highlighting:** Code blocks in responses are automatically highlighted.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **Git**

## Installation

Follow these steps to get Jarvis up and running on your local machine:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/Jarvis-AI.git
    cd Jarvis-AI
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

    - **Windows:**
      ```bash
      .\venv\Scripts\activate
      ```
    - **macOS/Linux:**
      ```bash
      source venv/bin/activate
      ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **Google Gemini API Key:**

    - Obtain a Google Gemini API key from the [Google AI Studio](https://aistudio.google.com/)
    - Open `config.py` and replace `"YOUR_GOOGLE_API_KEY"` with your actual API key:
      ```python
      # config.py
      GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
      ```
      Note: Create a config.py in your root directory.

2.  **Custom Commands (Optional):**
    - Edit `commands.json` to add or modify custom commands for Jarvis. This file defines phrases for opening applications, searching websites, etc.

## Usage

1.  **Run the Flask application:**

    ```bash
    python app.py
    ```

2.  **Access Jarvis:**

    - Open your web browser and navigate to `http://127.0.0.1:5000/`.

3.  **Interact:**
    - Type your commands or questions into the chat input and press Enter or click "Send".

## Customization

- **AI Identity:** The AI's name (Jarvis) and creator (Pradyumna) are hardcoded in `app.py`.
- **System Commands:** Modify `commands.json` to extend Jarvis's capabilities with new system commands.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details. (Note: A `LICENSE` file is not included in this project. You may want to create one.)

## Credits

- **Creator:** Pradyumna
