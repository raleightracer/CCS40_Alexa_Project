import speech_recognition as rt
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import subprocess

# Initialize recognizer and voice engine
listener = rt.Recognizer()
engine = pyttsx3.init()

# Configure voice settings
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # 0 = male, 1 = female (depends on OS)
engine.setProperty('rate', 170)
engine.setProperty('volume', 1)

# Text-to-speech function
def talk(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# Listen and recognize speech
def take_command():
    command = ""
    try:
        with rt.Microphone() as source:
            print("\nListening...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'jarvis' in command:
                command = command.replace('jarvis', '').strip()
                print("Command:", command)
    except rt.UnknownValueError:
        print("Jarvis could not understand.")
    except rt.RequestError:
        print("Network error — check your internet connection.")
    except Exception as e:
        print("Error:", e)
    return command

# Main logic
def run_jarvis():
    command = take_command()

    if command == "":
        return  # Skip empty input

    if 'play' in command:
        song = command.replace('play', '').strip()
        talk('Playing ' + song)
        pywhatkit.playonyt(song)

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk('The current time is ' + current_time)

    elif 'who is' in command:
        person = command.replace('who is', '').strip()
        try:
            info = wikipedia.summary(person, 2)
            talk(info)
        except wikipedia.exceptions.DisambiguationError:
            talk("There are multiple results, sir. Please be more specific.")
        except Exception as e:
            talk("Sorry sir, I couldn't find information about that.")
            print("Wikipedia error:", e)

    elif 'open face recognition' in command or ('face' in command and 'recognition' in command):
        talk("Opening Face Recognition system.")
        subprocess.Popen(['python', 'face_recognition_app_1.py'])

    elif 'date' in command:
        talk("Sorry sir, I'm not feeling well today.")

    elif 'what are you' in command:
        talk("I am your personal AI assistant, sir.")

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        talk(joke)

    elif 'stop' in command or 'goodbye' in command or 'exit' in command or 'yamete' in command:
        talk("Goodbye sir. Shutting down systems.")
        exit()

    else:
        talk("Please say that command again.")

# Keep Jarvis running
while True:
    run_jarvis()