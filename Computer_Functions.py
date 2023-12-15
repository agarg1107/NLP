import speech_recognition as sr
from googletrans import Translator
import serial

def take_command():
    command = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening")
        command.pause_threshold = 1
        audio = command.listen(source,0,3)
        try:
            print("Recognizing........")
            query = command.recognize_google(audio,language='hi')
            print(f"you said : {query}")
        except Exception as Error:
            return "None"

        return query.lower();

def translatorhtoe(text):
    line = str(text)
    trans = Translator()
    result = trans.translate(line)
    data = result.text
    print(data)
    return data

data = take_command()
print(data)
