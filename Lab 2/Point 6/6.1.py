# Modify the code to identify certain words in the generated (predicted text) which can form the basis for 'wake word' based system control (e.g. Ok Google, Alexa or Siri)

#!/usr/bin/env python3
# Refer to https://github.com/Uberi/speech_recognition?tab=readme-ov-file#readme
# Demo for speech recognition. You need to speak only after it says Say something
#%% import all necessary libraries
import speech_recognition as sr
import time
import os

#%% Recording from microphone
# obtain audio from the microphone
r = sr.Recognizer() #Initializing the Recognizer class
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source) #Important step to identify the ambient noise and hence be silent during this phase
    os.system('clear') 
    print("Say something!")
    audio = r.listen(source) # Listening from microphone

# recognize speech using Google Speech Recognition
start_time=time.time()  # start time
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")
    # instead of r.recognize_google(audio)
    google_text = r.recognize_google(audio)
    print("Google Speech Recognition thinks you said " + google_text)
except sr.UnknownValueError:
    google_text = ""
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    google_text = ""
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
print('Time for Google Speech Recognition recognition = {:.0f} seconds'.format(time.time()-start_time))

# recognize speech using Sphinx
start_time=time.time()  # start time
try:
     sphinx_text = r.recognize_sphinx(audio)
     print("Sphinx thinks you said " + sphinx_text)    
except sr.UnknownValueError:
    sphinx_text = ""
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    sphinx_text = ""
    print("Sphinx error; {0}".format(e))
print('Time for Sphinx recognition = {:.0f} seconds'.format(time.time()-start_time))


# Wake Word Check
wake_words = ["hey google", "alexa", "ok google", "hi siri"]
for phrase in wake_words:
    # Check if recognized text from any engine contains the phrase
    if phrase in google_text.lower() or phrase in sphinx_text.lower():
        print(f"Wake word '{phrase}' detected! Trigger your action here.")
        # e.g., call a function to handle the command, break out, etc.
        break