import cv2
import mediapipe as mp
import pyautogui as gui
import keyboard

import gesture_detector

gui.FAILSAFE = False

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

gd = gesture_detector.GestureDetector(5)
hd = gesture_detector.HandShapeDetector("data")
hands = gesture_detector.MPHands(buffer_size=100)

# hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    results = hands.run(image)

    if hands.history:
        # get hand shape
        hshape = hd.get_handshape(hands.history[-1])
        gd.run(hshape, hands.history[-1])
        print(gd.state, gd.is_click, hshape)
        if gd.state == "mouse":
            fingertip = hands.history[-1][gesture_detector.LANDMARK.INDEX_FINGER_TIP]
            SENSE = 1.5
            relativeX = int(fingertip[0] * gui.size()[0] * SENSE)
            relativeY = int(fingertip[1] * gui.size()[1] * SENSE)
            gui.moveTo(relativeX, relativeY, _pause=False)
        if gd.is_click:
            gui.click()

        # print(fingertip)

    if cv2.waitKey(5) & 0xFF == 27:
        break

    # if keyboard.is_pressed('a'):
    # print("pressed a")
    # break

    # Draw the hand annotations on the image.
    # image.flags.writeable = True
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # if results.multi_hand_landmarks:
    #   for hand_landmarks in results.multi_hand_landmarks:
    #     mp_drawing.draw_landmarks(
    #         image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    # cv2.imshow('MediaPipe Hands', image)

cv2.destroyAllWindows()
hands.close()
cap.release()
