import sys

from Computer import speak
from Computer import take_command
import Computer
import random
import json
import torch
import serial
from brain import NeuralNet
from NeuralNet import bag_of_words , tokenize
received_data = sys.argv[1]
print("Received Data:", received_data)


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open("intend.json",'r') as json_data:
    intents = json.load(json_data)
try:
    s = serial.Serial('COM5', 9600)
except:
    print("error")
# if received_data == '2':
#     print("yup its 2")
#     s.write(bytes('0', 'utf-8'))
# elif received_data == '1':
#     print("yup its 1")
#     s.write(bytes('8', 'utf-8'))

FILE = 'TrainData.pth'
data = torch.load(FILE)

input_size = data["input_size"]
output_size = data["output_size"]
hidden_size = data["hidden_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size,hidden_size,output_size).to(device)
model.load_state_dict(model_state)
model.eval()


#-------------------

def Main():
    sentence = take_command()


    sentence = tokenize(sentence)
    x = bag_of_words(sentence,all_words)
    x = x.reshape(1,x.shape[0])
    x = torch.from_numpy(x).to(device)

    output = model(x)
    _,predicted = torch.max(output,dim =1)
    tag = tags[predicted.item()]
    probs = torch.softmax(output,dim =1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                reply = random.choice(intent["responses"])
                if "time" in reply:
                    Computer.time()
                elif "web" in reply:
                    Computer.web()
                elif "youtube" in reply:
                    Computer.youtube_search()
                elif "google" in reply:
                    Computer.googele_search()
                elif "voice" in reply:
                    Computer.change_voice()
                elif "translate" in reply:
                    Computer.translatorhtoe()
                elif "Browser" in reply:
                    Computer.browser()
                elif "wish" in reply:
                    Computer.wishme()
                elif "onlight" in reply:
                    if received_data == "1":
                        s.write(bytes('1', 'utf-8'))
                    elif received_data == "2":
                        s.write(bytes('9', 'utf-8'))
                    else:
                        s.write(bytes('1', 'utf-8'))
                        s.write(bytes('9', 'utf-8'))

                elif "offlight" in reply:
                    if received_data == "1":
                        s.write(bytes('0', 'utf-8'))
                    elif received_data == "2":
                        s.write(bytes('8', 'utf-8'))
                    else:
                        s.write(bytes('0', 'utf-8'))
                        s.write(bytes('8', 'utf-8'))

                elif "secure" in reply:
                    s.write(bytes('2', 'utf-8'))
                    s.write(bytes('0', 'utf-8'))
                    s.write(bytes('8', 'utf-8'))
                    s.write(bytes('4', 'utf-8'))
                    s.write(bytes('5', 'utf-8'))
                    speak("Room is now secured")
                    sys.exit()
                else:
                    speak(reply)

while(True):

    Main()



