import azure.cognitiveservices.speech as speechsdk
#pip install azure-cognitiveservices-speech
def from_mic():
    speech_config = speechsdk.SpeechConfig(subscription="5a27343dbaca46059d48a0f8a23bd905", region="eastus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    
    print("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()
    return(result.text)

from_mic()