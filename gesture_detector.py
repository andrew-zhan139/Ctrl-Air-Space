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
    return relative @ np.diag([img_height, img_width])

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
    

    def update_history(self, array):
        # Need to readjust because image is flipped horizontally
        # readjusted_coords = np.array([1, 0]) - np.multiply(array, [1, -1]) 
        # self.history.append(readjusted_coords)
        self.history.append(array)


    def close(self):
        self.hands.close()

if __name__ == "__main__":
    frame_delay = 0.05

    history_window = 5 # Num seconds of history to save
    buffer_size = int(history_window / frame_delay) 
    gesture_detector = GestureDetector(buffer_size=buffer_size)
    try:
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            w, h, _ = image.shape
            results = gesture_detector.run(image)

            # Showing the results
            img = gesture_detector.render(image, results)

            if gesture_detector.history:
                print("Gesture:", gesture_detector.history[-1][8])
                pts = np.int32(relative_to_absolute(np.asarray(gesture_detector.history)[:, 8], w, h))
                img = cv2.polylines(img, [pts.reshape((-1, 1, 2))], isClosed=False, color=(0,255,255))
            
            cv2.imshow('MediaPipe Hands', img)

            if cv2.waitKey(5) & 0xFF == 27:
                break

            time.sleep(frame_delay)

    except:  
        gesture_detector.close()
        cap.release()

        all_coords = np.asarray(gesture_detector.history)
        coords = relative_to_absolute(all_coords[:, 8], w, h)
        plt.plot(coords[:, 0], coords[:, 1])
        axes = plt.gca()
        axes.set_xlim([0, w])
        axes.set_ylim([0, h])
        plt.show()
        raise