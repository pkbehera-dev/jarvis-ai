import subprocess
import webbrowser
import json
import re
from datetime import datetime
import random
import sys # Import sys module
import os # Import os module

def load_commands(filename="commands.json"):
    """
    Loads application commands from a JSON file.
    """
    try:
        # Explicitly specify UTF-8 encoding
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found. Please create it.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: The file '{filename}' is not a valid JSON file.")
        return {}
    except UnicodeDecodeError:
        print(f"Error decoding '{filename}' with UTF-8. It may be corrupted.")
        return {}


def handle_memory_command(query, memory):
    """
    Handles user commands to remember specific information.
    """
    query_lower = query.lower()

    # Ensure user_info dictionary exists in memory
    if "user_info" not in memory:
        memory["user_info"] = {}

    # Pattern for "remember that X is Y" or "my X is Y"
    match = re.search(r"(?:remember that\s+)?(?:my\s+)?(.+?)\s+is\s+(.+)", query_lower)
    if match:
        key = match.group(1).strip()
        value = match.group(2).strip()
        
        # List of common question words
        question_words = ["who", "what", "where", "when", "why", "how"]

        # If the key is a question word, it's likely not a memory command
        if key in question_words:
            return None, False # Let the Gemini API handle this

        # Avoid remembering "what" as a key, e.g. "what is my name"
        if key == "what":
            return None, False
        
        # Map common keys to structured user_info
        if key == "name":
            memory["user_info"]["name"] = value
            return f"Okay, I will remember that your name is {value}.", True
        elif key == "gender":
            memory["user_info"]["gender"] = value
            return f"Okay, I will remember that your gender is {value}.", True
        elif key == "birthday":
            memory["user_info"]["birthday"] = value
            return f"Okay, I will remember that your birthday is {value}.", True
        else:
            # For other "X is Y" facts, store directly in memory for now
            memory[key] = value
            return f"Okay, I will remember that your {key} is {value}.", True

    # Pattern for "I have X Ys" (keep as is for now, not directly user_info)
    match = re.search(r"i have (\d+)\s+(.+?)s?", query_lower)
    if match:
        number = match.group(1)
        item = match.group(2).strip()
        memory[f"number of {item}s"] = number
        return f"Okay, I will remember that you have {number} {item}s.", True

    # Pattern for "I am from X"
    match = re.search(r"i am from\s+(.+)", query_lower)
    if match:
        location = match.group(1).strip() # Corrected from match(1)
        memory["user_info"]["location"] = location
        return f"Okay, I will remember that you are from {location}.", True

    # Pattern for "I am a/an X" (keep as is for now, not directly user_info)
    match = re.search(r"i am an?\s+(.+)", query_lower)
    if match:
        role = match.group(1).strip()
        memory["role"] = role
        return f"Okay, I will remember that you are a {role}.", True

    # Generic "remember that" for facts without "is" (keep as is for now)
    if "remember that" in query_lower:
        fact = query_lower.split("remember that")[-1].strip()
        if fact and " is " not in fact:
            i = 0
            while f"fact_{i}" in memory:
                i += 1
            memory[f"fact_{i}"] = fact
            return f"Okay, I will remember that: {fact}.", True

    return None, False


def handle_identity_command(query, memory):
    """
    Handles user queries about their own or the assistant's identity.
    """
    query_lower = query.lower()
    user_info = memory.get("user_info", {})

    # Handle "who are you", "what is your name", "who is your owner"
    if "who are you" in query_lower or "what is your name" in query_lower or "who is your owner" in query_lower:
        ai_name = memory.get("AI_NAME")
        owner_creator = memory.get("OWNER_CREATOR")
        if ai_name and owner_creator:
            return f"I am {ai_name}, created by {owner_creator}."
        elif ai_name:
            return f"I am {ai_name}."
        return None # Let Gemini handle if no specific identity is found in memory
    
    # Handle "did you know me" or "do you know me"
    elif "did you know me" in query_lower or "do you know me" in query_lower:
        if "name" in user_info:
            return f"Yes, I know your name is {user_info['name']}."
        else:
            return "I don't have your name stored in my memory."
            
    # Handle "who is [user's name]"
    match = re.search(r"who is (.+)", query_lower)
    if match:
        queried_name = match.group(1).strip()
        if "name" in user_info and queried_name == user_info["name"].lower():
            return f"That's you, {user_info['name']}."
    
    return None


def handle_datetime_command(query):
    """
    Handles user queries about the current date and time.
    """
    now = datetime.now()
    if "date" in query.lower():
        formatted_date = now.strftime("%A, %B %d, %Y")
        return f"Today's date is {formatted_date}."
    elif "time" in query.lower():
        formatted_time = now.strftime("%I:%M %p")
        return f"The current time is {formatted_time}."
    return None


def handle_age_command(query, memory):
    """
    Handles user commands about age, if the birthday is stored in memory.
    """
    if "age" in query.lower() and "dob" in memory:
        try:
            dob = datetime.strptime(memory["dob"], "%B %d, %Y") # Assuming this format
            today = datetime.now()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            return f"You are {age} years old.", False
        except ValueError:
            return "I remember your birthday, but I can't calculate your age with the format I have. Please tell me your birthday again in a full format like 'January 1, 1990'.", False
    return None, False


def execute_command(query, memory, chat_history):
    """
    Executes a system command based on the user's query.
    """
    commands = load_commands()
    query = query.lower()
    save_required = False
    
    # Check for memory and age commands
    memory_response, save_required = handle_memory_command(query, memory)
    if memory_response:
        return memory_response, save_required

    # Check for identity commands first
    identity_response = handle_identity_command(query, memory)
    if identity_response:
        return identity_response, False

    age_response, save_required = handle_age_command(query, memory)
    if age_response:
        return age_response, save_required

    # Check for the new date and time command
    datetime_response = handle_datetime_command(query)
    if datetime_response:
        return datetime_response, False

    # Open application
    open_app_phrase = commands.get("open_app_phrase", "")
    if open_app_phrase and query.startswith(open_app_phrase):
        app_name_to_open = query.replace(open_app_phrase, "").strip()
        # Try to open using platform-specific commands
        if sys.platform == "win32":
            try:
                subprocess.Popen(["start", "", app_name_to_open], shell=True, start_new_session=True)
                return f"Opening {app_name_to_open}.", False
            except Exception as e:
                return f"An error occurred while trying to open {app_name_to_open}: {e}", False
        elif sys.platform == "darwin": # macOS
            try:
                subprocess.Popen(["open", app_name_to_open], start_new_session=True)
                return f"Opening {app_name_to_open}.", False
            except Exception as e:
                return f"An error occurred while trying to open {app_name_to_open}: {e}", False
        elif sys.platform.startswith("linux"): # Linux
            try:
                subprocess.Popen(["xdg-open", app_name_to_open], start_new_session=True)
                return f"Opening {app_name_to_open}.", False
            except Exception as e:
                return f"An error occurred while trying to open {app_name_to_open}: {e}", False
        else:
            return f"Sorry, I don't know how to open applications on your operating system ({sys.platform}).", False
    
    # Search on a website
    search_phrase = commands.get("search_phrase", "")
    if search_phrase and query.startswith(search_phrase):
        search_query = query.replace(search_phrase, "").strip()
        search_url = commands.get("search_url", "").format(query=search_query)
        webbrowser.open(search_url)
        return f"Searching for {search_query}.", False
    
    # Greeting commands
    greetings = ["hello", "hi", "hey"]
    for greeting in greetings:
        if query.startswith(greeting) or query == greeting:
            return random.choice(["Hello!", "Hi there!", "Hey! How can I help?"]), False
    
    # Open website
    web_phrases = commands.get("web_phrases", {})
    if "open" in query and web_phrases:
        site = query.replace("open", "").strip().split(" ")[0]
        if site in web_phrases:
            webbrowser.open(web_phrases[site])
            return f"Opening {site}.", False
    
    # Default return for no command found
    return None, False