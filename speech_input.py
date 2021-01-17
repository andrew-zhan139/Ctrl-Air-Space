import azure.cognitiveservices.speech as speechsdk
import pyautogui

#pip install azure-cognitiveservices-speech
key = "5a27343dbaca46059d48a0f8a23bd905" # For example
def from_mic():
    speech_config = speechsdk.SpeechConfig(subscription=key, region="eastus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    
    print("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()
    pyautogui.typewrite(result.text)
    pyautogui.typewrite('\n')
    #return(result.text)

if __name__ == "__main__":
    from_mic()
    
#from_mic()
