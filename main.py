import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "b04346bba52344e9b62bac7e42c5f970"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    #Initialize Pygame mixer
    pygame.mixer.init()

    #Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    #Play the MP3 file
    pygame.mixer.music.play()

    #Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    client = OpenAI(api_key="sk-_vssegvTrNczQ9_cbMYFFFeReTnGNgddvTY2Hj_tjST3BlbkFJtrbiHyQoR8a98lChcpTU99Np5qzN5avnTWSKSp3PAA",)

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user","content": command}
    ]
    )
 
    return (completion.choices[0].message.content)

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser("https://linkedin.com")
    elif "open hianime" in c.lower():
        webbrowser("https://hianime.com")
    elif "open spotify" in c.lower():
        webbrowser("https://spotify.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            #Parse the JSON response
            data = r.json()

            #Extract the articles
            articles = data.get('articles', [])

            #Print the headlines
            for article in articles:
                speak(article['title'])

        else:
            #Let OpenAi handle the request
            output = aiProcess(c)
            speak(output)



if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        #Listen for the wake up word "Jarvis"
        #obtain audio from the microphone
        r = sr.Recognizer()
      
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout = 2, phrase_time_limit = 1)
            word = r.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yo")
                #Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except sr.RequestError as e:
            print("Error; {0}".format(e))