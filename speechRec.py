import speech_recognition as sr
import database as db
import encryption
import windows
import pyaudio


# This code was heavily referenced from the official speech
# recognition package documentation because there's only so many ways
# someone can write the same code.


def listen():
    r = sr.Recognizer()

    print("Listening Loop")
    with sr.Microphone() as source:
        audio = r.listen(source)
        voiceData = ''
        try:
            voiceData = r.recognize_google(audio)
        except sr.UnknownValueError:
            print('Didn\'t understand')
        except sr.RequestError:
            print("Service down")
        print("Finished")
        return voiceData


# Method to find account or username in audio transcription.
def findAccountMatches(selectedList):
    windows.searchMode = False
    audioText = listen()
    print("AUDIO: " + audioText)
    matchList = []
    i = 0
    while i < len(selectedList):
        if encryption.decryptString(selectedList[i][1]) in audioText:
            matchList.append(selectedList[i])
        if encryption.decryptString(selectedList[i][2]) in audioText:
            matchList.append(selectedList[i])
        i = i + 1
    print(matchList)
    return matchList


# Method to find text in audio transcription.
def findTextMatches(selectedList):
    windows.searchMode = False
    audioText = listen()
    print("AUDIO: " + audioText)
    matchList = []
    i = 0
    while i < len(selectedList):
        if encryption.decryptString(selectedList[i][1]) in audioText:
            matchList.append(selectedList[i])
        i = i + 1
    print(matchList)
    return matchList

