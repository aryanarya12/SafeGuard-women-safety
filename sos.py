import time
import os
import pygame  # Install with 'pip install pygame'
import numpy as np
import sounddevice as sd
import requests
import speech_recognition as sr

def send_emergency_alert():
    location_api = "https://ipinfo.io/loc"
    try:
        location = requests.get(location_api).text.strip()
        emergency_message = f"EMERGENCY! I am in danger. My location: {location}"
        print(emergency_message)
        # You can integrate an SMS or email API here to send the message
    except Exception as e:
        print("Failed to get location:", e)

def play_beep(frequency=1000, duration=0.3, use_file=True):
    if use_file and os.path.exists("sos.wav"):
        pygame.mixer.init()
        beep = pygame.mixer.Sound("sos.wav")
        beep.play()
        time.sleep(duration)
    else:
        samplerate = 44100
        t = np.linspace(0, duration, int(samplerate * duration), False)
        wave = 0.5 * np.sin(2 * np.pi * frequency * t)
        sd.play(wave, samplerate)
        sd.wait()

def play_sos():
    send_emergency_alert()
    dot_duration = 0.2
    dash_duration = dot_duration * 3
    gap_duration = dot_duration
    letter_gap = dot_duration * 3

    sos_pattern = [dot_duration, dot_duration, dot_duration,  
                   dash_duration, dash_duration, dash_duration,
                   dot_duration, dot_duration, dot_duration]

    for duration in sos_pattern:
        play_beep(duration=duration, use_file=True)
        time.sleep(gap_duration)
    
    time.sleep(letter_gap)

def listen_for_activation():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say 'hello' to activate SOS...")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            if "hello" in command:
                print("Activation detected! Starting SOS...")
                play_sos()
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError:
            print("Error with the speech recognition service.")

if __name__ == "__main__":
    listen_for_activation()
