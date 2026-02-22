import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pywhatkit

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        listener.adjust_for_ambient_noise(source)
        audio = listener.listen(source)
    try:
        command = listener.recognize_google(audio)
        command = command.lower()
        print("You said:", command)
    except:
        command = ""
    return command

def run_assistant():
    command = take_command()

    if "time" in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The current time is {time}")

    elif "who is" in command:
        person = command.replace("who is", "")
        info = wikipedia.summary(person, 1)
        speak(info)

    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")

    elif "play" in command:
        song = command.replace("play", "")
        pywhatkit.playonyt(song)
        speak("Playing on YouTube")

    elif "stop" in command:
        speak("Goodbye Lakshmi")
        exit()

    else:
        speak("Please say the command again")

if __name__ == "__main__":
    speak("Hello Lakshmi, I am your voice assistant. How can I help you?")
    while True:
        run_assistant()
