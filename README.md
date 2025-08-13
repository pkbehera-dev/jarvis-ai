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
    - Create a file named `.env` in the root directory of the project.
    - Add the following line to the `.env` file, replacing `YOUR_GOOGLE_API_KEY` with your actual API key:
      ```
      GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
      ```

2.  **Custom Commands (Optional):**
    - Edit `commands.json` to add or modify custom commands for Jarvis. This file defines phrases for opening applications, searching websites, etc.

## Usage

### Local Development (Windows)

For local development on Windows, it is recommended to use the `waitress` server.

1.  **Run the application with Waitress:**

    ```bash
    waitress-serve --host 127.0.0.1 --port 5000 app:app
    ```

2.  **Access Jarvis:**

    - Open your web browser and navigate to `http://127.0.0.1:5000/`.

### Local Development (macOS/Linux)

On macOS and Linux, you can use the Flask development server or Gunicorn.

1.  **Run with Flask development server:**

    ```bash
    python app.py
    ```

2.  **Run with Gunicorn:**

    ```bash
    gunicorn --bind 127.0.0.1:5000 app:app
    ```

## Deploying to Production

This project is configured to be deployed to services like Render or Heroku.

1.  **Procfile:** The `Procfile` in the root of the repository tells the hosting service how to run the application using Gunicorn:
    ```
    web: gunicorn app:app
    ```

2.  **Environment Variables:** As mentioned in the configuration section, do not upload your `.env` file. Instead, set the `GOOGLE_API_KEY` as an environment variable in your hosting provider's dashboard.
