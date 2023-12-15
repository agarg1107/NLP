import os

import pyttsx3

import webbrowser
import pywhatkit
import serial
import speech_recognition as sr

import datetime

from googletrans import Translator



Assistant = pyttsx3.init('sapi5')

voices = Assistant.getProperty('voices')

Assistant.setProperty('voice',voices[0].id)
Assistant.setProperty('rate', 180)
a = 1
cr = 0

k = len(voices);

def time():
    time = datetime.datetime.now().strftime("%H:%M")
    speak(time);

def web():
    speak("Which website i can open for you sir")
    query = take_command()

    if(query == "None"):
        speak("unable to open website")
        return
    print(query)
    no_spaces_string = query.replace(" ", "")
    print(no_spaces_string)
    web = "https://www."+no_spaces_string+".com"
    print(web)
    webbrowser.open(web)
    speak("Done")
def youtube_search():
    speak("What i can search for you sir")
    query = take_command()
    if (query == "None"):
        speak("unable to open youtube")
        return
    web = "https://www.youtube.com/results?search_query="+query
    webbrowser.open(web)
    speak("Done sir")
def googele_search():
    speak("What i can search for you sir")
    query = take_command()
    if (query == "None"):
        speak("unable to open Google")
        return
    no_string = query.replace(" ", "")
    pywhatkit.search(no_string)
    speak("Done sir")
def change_voice():
    global cr
    for i in range(k):
        if(i != cr):
            Assistant.setProperty('voice',voices[i].id)
            Assistant.setProperty('rate', 180)
            speak("Is it ok sir")
            val = take_command();
            if "ok" or "done" or "thik h" in val:
                cr = i;
                speak("Done sir")
                break;
            if(i == k-1 and val != "ok"):
                Assistant.setProperty('voice',voices[cr].id)
                Assistant.setProperty('rate', 180)
                speak("There is no more voice in the system");
                break;
        if(i == k-1):
                Assistant.setProperty('voice',voices[cr].id)
                Assistant.setProperty('rate', 180)
                speak("There is no more voice in the system");   
def speak(audio):
    print("  ")
    Assistant.say(audio)
    print(f"JARVIS: {audio}")
    print("  ")
    Assistant.runAndWait()
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        try:
            audio = recognizer.listen(source, timeout=9, phrase_time_limit=6)
            print("Recognizing...")
            command = recognizer.recognize_google(audio).lower()
            print(f"User said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not hear your request. Please try again.")
            return ""
        except Exception as Error:

            return "None"



def light_func(a):
    try:
        s = serial.Serial('com6', 9600)
        if (a == '1'):
            s.write(bytes('1', 'utf-8'))
        if (a == '0'):
            s.write(bytes('0', 'utf-8'))
    except:
        speak("Please connect the Audrino with computer")

def wishme():
    speak("Welcome back sir")

    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Good morning")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon")
    elif hour >= 18 and hour <= 24:
        speak("Good evening")

    speak("how can i help you")

def translatorhtoe():
    speak("Speake the sentence in Hindi")
    text = take_command()
    line = str(text)
    trans = Translator()
    result = trans.translate(line)
    data = result.text
    speak(data)
    print(data)

def browser():
    os.startfile("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
