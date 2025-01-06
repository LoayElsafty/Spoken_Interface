import speech_recognition as sr
import pyttsx3
import datetime
import math
import webbrowser
import random
import tkinter as tk
from tkinter import ttk
import threading

# Initialize speech recognition and text-to-speech
recognizer = sr.Recognizer()
tts = pyttsx3.init()

# Responses and keywords
responses = {
    "hello": "Hello! How can I help you today?",
    "exit": "Goodbye! Have a great day!",
}

# Operator mapping for math calculations
operator_mapping = {
    "plus": "+",
    "minus": "-",
    "times": "*",
    "multiplied by": "*",
    "divided by": "/",
}

# Get current time
def get_time():
    now = datetime.datetime.now()
    return f"The time is {now.strftime('%I:%M %p')}"

# Perform calculations
def calculate(expression):
    try:
        for word, symbol in operator_mapping.items():
            expression = expression.replace(word, symbol)
        result = eval(expression, {"__builtins__": None}, math.__dict__)
        return f"The result is {result}"
    except Exception:
        return "Sorry, I couldn't calculate that."

# Open websites
def open_website(command):
    if "open youtube" in command:
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        return "Of course, promise I won’t rickroll you."
    elif "open a christmas song" in command:
        webbrowser.open("https://www.youtube.com/watch?v=E8gmARGvPlI")
        return "Playing a Christmas song."
    return "Sorry, I don't know that website."

# Tell a joke
def tell_joke():
    jokes = [
        "What’s a robotics student’s favorite exercise? Circuit training!",
        "Why did the robotics student take a screwdriver to the party? To loosen up!",
    ]
    return random.choice(jokes)

# Provide a weather report
def weather_report():
    weather_conditions = [
        "Expect some rain today, so don't forget your umbrella!",
    ]
    return random.choice(weather_conditions)

# Handle user input
def respond_to_input(input_text):
    if "what is the time" in input_text:
        return get_time()
    elif "calculate" in input_text:
        expression = input_text.replace("calculate", "").strip()
        return calculate(expression)
    elif "open" in input_text:
        return open_website(input_text)
    elif "tell me a joke" in input_text:
        return tell_joke()
    elif "weather report" in input_text:
        return weather_report()
    elif "hello" in input_text:
        return responses["hello"]
    else:
        return "Sorry, I don't have a response for that."

# Text-to-speech
def speak_response(response_text):
    tts.say(response_text)
    tts.runAndWait()

# Listen for audio
def listen_for_audio():
    with sr.Microphone() as source:
        display_message("Listening...", "input")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio).lower()
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None

# Tkinter GUI setup
def setup_gui():
    global root, input_label, response_label, wave_canvas, wave_animation_running
    root = tk.Tk()
    root.title("AI Speech Assistant")

    # Styling
    root.geometry("600x400")
    root.configure(bg="#2b2b2b")

    # Input Label
    input_label = ttk.Label(root, text="", font=("Helvetica", 14), foreground="white", background="#2b2b2b")
    input_label.pack(pady=20)

    # Response Label
    response_label = ttk.Label(root, text="", font=("Helvetica", 14), foreground="white", background="#2b2b2b", wraplength=550)
    response_label.pack(pady=20)

    # Wave Animation Canvas
    wave_canvas = tk.Canvas(root, width=500, height=100, bg="#2b2b2b", highlightthickness=0)
    wave_canvas.pack(pady=20)

    # Quit Button
    quit_button = ttk.Button(root, text="Quit", command=root.quit)
    quit_button.pack(pady=20)

    # Wave animation control
    wave_animation_running = False

# Display messages
def display_message(message, label_type):
    if label_type == "input":
        input_label.config(text=f"You: {message}")
    elif label_type == "response":
        response_label.config(text=f"Assistant: {message}")

# Wave animation
def start_wave_animation():
    global wave_animation_running
    wave_animation_running = True
    animate_wave()

def stop_wave_animation():
    global wave_animation_running
    wave_animation_running = False

def animate_wave():
    if not wave_animation_running:
        return

    wave_canvas.delete("all")
    for i in range(0, 500, 20):
        height = random.randint(10, 50)
        wave_canvas.create_line(i, 50 - height, i, 50 + height, fill="#00FF7F", width=2)
    root.after(100, animate_wave)

# Main function
def main_loop():
    while True:
        start_wave_animation()
        user_input = listen_for_audio()
        stop_wave_animation()

        if user_input:
            display_message(user_input, "input")
            if "exit" in user_input:
                response = responses["exit"]
                display_message(response, "response")
                speak_response(response)
                root.quit()
                break

            response = respond_to_input(user_input)
            display_message(response, "response")
            speak_response(response)

# Run the program
setup_gui()
threading.Thread(target=main_loop, daemon=True).start()
root.mainloop()
