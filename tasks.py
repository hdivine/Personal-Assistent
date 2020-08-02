from main import speak, listen, listen_once
import re
import json

# change me here - change the name of cmds.json file path
with open("/Users/hdivine/Documents/GitHub/Personal-Assistent/cmds.json") as file:
    cmds = json.load(file)

# click ################################################################################################################################################

def click():
    pass

# check defined commands ########################################################################

def defined_cmd(txt):
    for cmd in cmds:
        if re.match(re.compile(cmd), txt):
            return txt
    
    speak("Sorry can you repeat that one")
    return False

# chrome ########################################################################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def chrome_subprocess(drive,txt):
    if re.match(r"search .*", txt):
        speak(f"searching {txt[7:]}")
        drive.find_element_by_name("q").clear()
        drive.find_element_by_name("q").send_keys(txt[7:])
        drive.find_element_by_name("q").send_keys(Keys.RETURN)
        # drive.clear()


        speak("these are some search results")
        return True, False

    elif txt == "close":
        drive.close()
        return False, False

    else:
        defined = defined_cmd(txt)
        if defined:
            return False, txt
        else: 
            return True, False

def open_chrome():
    speak("opening chrome")
    drive = webdriver.Chrome("/Users/hdivine/Documents/GitHub/Personal-Assistent/chromedriver")
    drive.get("https://google.com")  
    speak("would you like to search anything?")

    cont = True
    defined = ""
    while cont:
        txt = listen()
        cont, defined = chrome_subprocess(drive,txt)
    
    return defined

# play music ###################################################################################

from selenium.webdriver.chrome.options import Options

headless = Options()
headless.add_argument("--headless")

def play_music(mus):
    speak("searching "+mus)
    drive = webdriver.Chrome(executable_path="/Users/hdivine/Documents/GitHub/Personal-Assistent/chromedriver", chrome_options=headless)
    drive.get("https://www.youtube.com/results?search_query="+mus)
    drive.find_elements_by_id("video-title")[0].click()
    try:
        wait = drive.find_element_by_class_name("ytp-time-duration")[2]
    except Exception as e:
        print(e)



# wiki ###################################################################################

import wikipedia



def search_wiki(msg):
    speak(f"Searching results for {msg}")
    info = wikipedia.summary(msg)

    txt=""
    for i in range(0,len(info.split('.')), 3):
        if ((re.match(r".* ya|yes|ok|okay|continue .*", txt) or i==0) and i < len(info.split('.'))):
            fewInfo = ('.').join([m for m in info.split('.')[i:i+3]])
            speak(fewInfo)

            if  i+3 >= len(info.split('.')):
                speak("That's what i know!")
                break
                
        elif re.match(r".*no.*", txt):
            speak("Thanks for asking me, i hope it helped!")
            break


        speak("should i continue?")
        txt = listen()
    
    # wiki_subprocess(txt)




# open any software in applications folder ###################################################################################################################################
import os

def open_me(app_name):
    speak("finding "+app_name)

    for loc in ["/System/Applications/","/Applications/"] :
        files = os.listdir(loc)
        for file in files:
            regx = re.compile(".*"+app_name+".*")
            if re.match(regx, file.lower()):
                file = (r'\ ').join(file.split(' '))
                speak("here you go... ")
                os.system(f"open {loc+file}")
                return
    
    speak(f"Sorry sir I didnt found {app_name}")
    print("not found")

        

        


# mouse key board function ###################################################################################################################################
import pyautogui as pag

def type(msg):
    speak("here you go... ")
    pag.write(msg[5:], interval=0.01)

# dynamic clicks ###################################################################################################################################

# import time
# from threading import Thread as trd

# stop = "0"

# def input_timeout():
#     global stop
#     stop = input()
#     return

# def dynamic():
#     new_pos = 0
#     inptThrd = trd(target=input_timeout)
#     inptThrd.start()
#     while True:

#         curr_pos = pag.position()

#         if curr_pos == new_pos:
#             pass
        
        

#         if stop == "1":
#             inptThrd.join()
#             return
#         else:
#             print("would you like to stop\n1.yes\n2.no")

#             time.sleep(1)
#             if stop != "1":
#                 new_pos = pag.position()
#                 time.sleep(3)

###################################################################################################################################