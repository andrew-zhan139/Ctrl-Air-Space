# Ctrl+Air+Swipe

## Note
Note that Filip Jerga is listed as an author due to our usage of his boilerplate code (https://github.com/Jerga99/electron-react-boilerplate).

## Overview
A desktop application that allows users to execute computer commands with the use of air gestures through movement recognition models. Hack the North 2020++ 🏆!
Current iteration is not perfect, so use at your own risk 😎.

## Instructions for running
1. Set up Python (see below)
1. (Optional) If want to have voice recognition feature, follow instructions below.
1. Install ui dependencies: ```npm install``` </br>
1. In one terminal: ```npm run watch``` to compile react code <br/>
1. In another terminal: ```npm start``` to start Electron app

## Stuff to edit before running
- src\assets: Change the file paths for thepath1, ..., thepath6 (gesture demonstrations)
- src\components\GestureMatch.js: Change the file path for the logo

## Setting up Python
Libraries (which you may not have yet) to install:
- mediapipe
- opencv-python
- scikit-learn
- keyboard
- pyautogui
- azure-cognitiveservices-speech

To run just the python portion of the computer control, go to the Server folder and run the following: ```python hello.p ```

To run a demo of the gesture recognition without computer control, go to the Server folder and run the following: ```python gesture_detector.py```

## Setting up Azure Speech Service voice recognition
1. Create Azure Speech Service resource ([Speech Service setup example](https://github.com/MicrosoftDocs/ai-fundamentals/blob/master/02b%20-%20Speech.ipynb)). 
1. In the Server folder, create a copy of settings_template.json. Rename it to settings.json.
1. Add key into the json file.

## Improvements to be made
- Improve robustness and reliability of gesture detection
- Connect config settings from UI to Python
- Add an exit program feature
- Add post-hackathon comments/documentation
