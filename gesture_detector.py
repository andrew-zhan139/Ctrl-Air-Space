""" 
Adapted from https://google.github.io/mediapipe/solutions/hands#python-solution-api 

The point of the Gesture Detector is to  get gesture from video feed.
"""

import mediapipe as mp
import cv2
import collections
import numpy as np
import time
import matplotlib.pyplot as plt

# Enum that can be used as numbers (e.g. LANDMARK.WRIST is 0)
LANDMARK  = mp.solutions.hands.HandLandmark  

class Gestures:
    @staticmethod
    def is_swipe(history, threshold_occurance, threshold_deviation):
        return 

    @staticmethod
    def is_call(history):
        pass

def relative_to_absolute(relative, img_width, img_height):
    return relative @ np.diag([img_width, img_height])

def landmark_to_array(multi_hand_landmark):
    """ e.g. multi_hand_landmark = results.multi_hand_landmarks[0]"""
    # return np.asarray([[pt.x, pt.y, pt.z] for pt in multi_hand_landmark.landmark])
    return np.asarray([[pt.x, pt.y] for pt in multi_hand_landmark.landmark])

class GestureDetector:
    def __init__(self, buffer_size=None):
        self.hands = mp.solutions.hands.Hands(
            min_detection_confidence=0.75, 
            min_tracking_confidence=0.9
        )
        self.history = collections.deque(maxlen=buffer_size)
    
    def run(self, img):
        img_width, img_height, _ = img.shape

        # Flip horizontally, then BGR->RGB
        input_img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)

        # To improve performance, this will ensure image pass by reference.
        input_img.flags.writeable = False

        # Get mediapipe result 
        results = self.hands.process(input_img)

        # Processing results for history
        # (CURRENTLY DEALING WITH ONE HAND) <---------------
        if results.multi_hand_landmarks:
            results_array = landmark_to_array(results.multi_hand_landmarks[0]) # Relative coords
            # results_array = relative_to_absolute(results_array, img_width, img_height) # Absolute coords
            self.update_history(results_array)

        return results


    def render(self, image, results):
        # Showing results
        flipped = cv2.flip(image, 1) # Flipped to match the results
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    flipped, 
                    hand_landmarks, 
                    mp.solutions.hands.HAND_CONNECTIONS
                )
        return flipped
    

    def update_history(self, result):
        self.history.append(result)


    def close(self):
        self.hands.close()


if __name__ == "__main__":
    buffer_size = 1000 # Will depend on computer
    gesture_detector = GestureDetector(buffer_size=buffer_size)

    start = time.time()
    prev_time = start
    processing_rate = 20
    approx_window_length = 2
    record_start_time = 5
    x = collections.deque(maxlen=approx_window_length*processing_rate)
    y = collections.deque(maxlen=approx_window_length*processing_rate)
    try:
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue
            
            results = gesture_detector.run(image)
            img = gesture_detector.render(image, results)
            cv2.imshow('MediaPipe Hands', img)
            if cv2.waitKey(5) & 0xFF == 27:
                break
            
            if time.time() > record_start_time and time.time() - prev_time > 1 / processing_rate:
                prev_time = time.time()
                if gesture_detector.history:
                    print(gesture_detector.history)
                    x.append(gesture_detector.history[-1][8][0]) # Getting the most recent result
                    y.append(gesture_detector.history[-1][8][1])

    except:  
        gesture_detector.close()
        cap.release()
        plt.plot(list(x), list(y))
        plt.show()
        raise