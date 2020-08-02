"""
pip3 install speechRecognition
    dep - pyaudio
        brew install portaudio
        sudo pip3 install pyaudio
pip3 install pyttsx3
pip3 install selenium
    Download chromewebdriver from https://chromedriver.chromium.org and save it to /usr/local/bin
/Users/hdivine/Documents/py/MrRobot_personal_assistent/main.py
"""

import re, random
import speech_recognition as sp_recog
import pyttsx3
import datetime
import pyautogui as pag
import os
# defined tasks
import tasks
# knowledge
import json

# load v simple neural net ################################################################################################################################################

# change me here - change the name of knowledge.json file path
with open("/Users/hdivine/Documents/GitHub/Personal-Assistent/knowledge.json") as file:
    knowledge = json.load(file)

#  listening once ################################################################################################################################################
recognize = sp_recog.Recognizer()
def listen_once():
    # os.system("clear")
    print("listening")
    with sp_recog.Microphone() as source:
        audio = recognize.listen(source, timeout=5*60)
        txt = recognize.recognize_google(audio).lower()
        print(txt)
        return txt

# listen till not get text input without errors ###############################################################################################################################################
def listen():
    while 1:
        try:
            txt = listen_once()
            if txt == "stop listening":
                return ""
            elif txt != "":
                return txt
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            print(e)
            continue

# speak ################################################################################################################################################
speech_engine = pyttsx3.init()
# speech_engine.setProperty("voice", speech_engine.getProperty("voices")[28].id)

def speak(msg):
    speech_engine.say(msg)
    speech_engine.runAndWait()

# main processing ################################################################################################################################################
def process(msg):
    # chrome
    if "open chrome" in msg:
        other_process = tasks.open_chrome()
        if other_process:
            process(other_process)

    # chrome
    elif re.match(r"play music .*", msg):
        tasks.play_music(msg[11:])

    # open any file 
    elif re.match(r"open .*", msg):
        tasks.open_me(msg[5:])

    # wiki
    elif re.match(r"what is .*", msg):
        tasks.search_wiki(msg[8:])
    
    elif re.match(r".*click.*", msg):
        pag.click()
        return
    
    elif re.match(r"type .*", msg):
        tasks.type(msg)
        return
    
    # elif "dynamic click" == msg:
    #     tasks.dynamic()

    elif re.match(r"close current .*", msg):
        pag.hotkey("command","q")

    # exit
    elif msg == "exit":
        speak("good bye! have a nice day...")
        exit()

    else:
        speak(random.choice(knowledge["listen"]["error"]))

# main #########################//*[@id="video-title"]######################################################################################################################

def main():

    # greet
    hour = int(datetime.datetime.now().strftime("%H")) 
    speak("Good Morning Sir") if hour >= 0 and hour <= 12 else speak("good afternoon sir") if hour > 12 and hour <= 17 else   speak("Hello sir") 

    # listen & process
    txt = ""
    while 1:
        # os.system("clear")
        if not re.match(r".*click.*", txt):
            speak(random.choice(knowledge["help"]))
        txt = listen()
        process(txt)

################################################################################################################################################
if __name__ == "__main__":
    main()