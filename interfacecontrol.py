import cv2
#from VideoStream import VideoStream
import mediapipe as mp

import pyautogui as gui
import keyboard

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# For webcam input:
hands = mp_hands.Hands(min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)
# vs = VideoStream(src=3).start()
cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, image = cap.read() #vs.grabbed, vs.read()
    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)
  # Draw the hand annotations on the image.
    # image.flags.writeable = True
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # if results.multi_hand_landmarks:
    #   for hand_landmarks in results.multi_hand_landmarks:
    #     mp_drawing.draw_landmarks(
    #         image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    # cv2.imshow('MediaPipe Hands', image)

    if(results.multi_hand_landmarks):
        fingertip = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        #print(fingertip)
        relativeX = int(fingertip.x * gui.size()[0])
        relativeY = int(fingertip.y * gui.size()[1])
        gui.moveTo(relativeX, relativeY, _pause=False)

    # if keyboard.is_pressed('a'):
    #     print("pressed a")
    #     break

    if cv2.waitKey(5) & 0xFF == 27:
        break

cv2.destroyAllWindows()
hands.close()
cap.release()


