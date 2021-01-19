import azure.cognitiveservices.speech as speechsdk
import pyautogui
import json
import os

# If want to use voice recognition feature, you must add your Azure Speech Service Key in the settings.json file
settings_path = "settings.json" if os.path.isfile("settings.json") else "Server/settings.json"
if os.path.isfile(settings_path):
    print("yaya")
    with open(settings_path) as f:
        settings = json.load(f)
        key = settings["AzureSpeechServiceKey"]

def from_mic():
    assert os.path.isfile(settings_path), "Server/settings.json file not found. Make a copy of settings_template.json, then rename it to settings.json"
    assert key != "INSERT KEY HERE", "Azure Speech Service key has not be added to Server/speech_input.py"
    speech_config = speechsdk.SpeechConfig(subscription=key, region="eastus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    
    print("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()
    assert result.reason != speechsdk.ResultReason.Canceled, "Azure Speech Service key may not be recognized."
    print("Detected:", result.text)
    pyautogui.typewrite(result.text)
    pyautogui.typewrite('\n')
    #return(result.text)

if __name__ == "__main__":
    from_mic()
