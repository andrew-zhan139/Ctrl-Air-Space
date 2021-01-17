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
from sklearn import neighbors
import pickle
import os

# Enum that can be used as numbers (e.g. LANDMARK.WRIST is 0)
LANDMARK  = mp.solutions.hands.HandLandmark  


class SwipeDetector:
    def __init__(self, window, main_axis_thresh, cross_axis_thresh, cooldown):
        self.window = window
        self.main_axis_thresh = main_axis_thresh # Relative coords
        self.cross_axis_thresh = cross_axis_thresh # Relative coords
        self.cooldown = cooldown # Number of seconds

        self.previous_swipe_time = -np.inf

    def get_swipe(self, axis, history):
        """Getting swipe direction
        For axis=0: -1 is left, 1 is right, 0 is no swipe 
        For axis=1: -1 is up, 1 is down, 0 is no swipe
        """
        if time.time() - self.previous_swipe_time < self.cooldown:
            return 0
        else:
            main_axis = axis
            cross_axis = 0 if axis == 1 else 1
            main = history[-1][LANDMARK.INDEX_FINGER_TIP, main_axis] - history[-int(self.window)][LANDMARK.INDEX_FINGER_TIP, main_axis] 
            cross = history[-1][LANDMARK.INDEX_FINGER_TIP, cross_axis] - history[-int(self.window)][LANDMARK.INDEX_FINGER_TIP, cross_axis]
            if abs(main) > self.main_axis_thresh and abs(cross) < self.cross_axis_thresh:
                self.previous_swipe_time = time.time()
                return -1 if main < 0 else 1 
            else:
                return 0


class HandShapeDetector:
    def __init__(self, data_folder, n_neighbours=15):
        self.labels = []

        # Get training set
        training_x = []
        training_y = []
        for i, datafile in enumerate(os.listdir(data_folder)): 
            print(f"Loading {datafile}")
            with open(os.path.join(data_folder, datafile), 'rb') as f:
                self.labels.append(datafile[5:-2])
                data = pickle.load(f)
                for hand in data:
                    training_x.append(self.process_input(hand))
                    training_y.append(i)
        training_x = np.array(training_x)

        # Train the KNN classifier
        self.clf = neighbors.KNeighborsClassifier(n_neighbours)
        self.clf.fit(training_x, training_y)
    
    def process_input(self, hand):
        """ Normalized about the wrist and flatten """
        return (hand - hand[0]).flatten()
  
    def get_handshape(self, hand):
        prediction = self.clf.predict(np.expand_dims(self.process_input(hand), 0))
        return self.labels[int(prediction)]



def relative_to_absolute(relative, img_width, img_height):
    return relative @ np.diag([img_height, img_width])

def landmark_to_array(multi_hand_landmark):
    """ e.g. multi_hand_landmark = results.multi_hand_landmarks[0]"""
    # return np.asarray([[pt.x, pt.y, pt.z] for pt in multi_hand_landmark.landmark])
    return np.asarray([[pt.x, pt.y] for pt in multi_hand_landmark.landmark])

class MPHands:
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
    mp_hands = MPHands(buffer_size=buffer_size)
    swipe_detector = SwipeDetector(
        window=0.5 / frame_delay, 
        main_axis_thresh=0.5, 
        cross_axis_thresh=0.2,
        cooldown=1
    )
    handshape_detector = HandShapeDetector("data")
    curr_colour = np.random.uniform(0, 255, 3)

    previous_swipe_time = -100000 
    try:
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            w, h, _ = image.shape
            results = mp_hands.run(image)

            # Showing the results
            img = mp_hands.render(image, results)
            text = ""
            if mp_hands.history:
                # print("Gesture:", gesture_detector.history[-1][8])
                try:
                    h_swipe = swipe_detector.get_swipe(0, mp_hands.history)
                    v_swipe = swipe_detector.get_swipe(1, mp_hands.history)
                    if h_swipe != 0:
                        print(f"SWIPED {'left' if h_swipe == -1 else 'right'}!!!!!!!!!!!!")
                        curr_colour = np.random.uniform(0, 255, 3)
                        previous_swipe_time = time.time()
                    elif v_swipe != 0:
                        print(f"SWIPED {'up' if v_swipe == -1 else 'down'}!!!!!!!!!!!!")
                        curr_colour = np.random.uniform(0, 255, 3)
                        previous_swipe_time = time.time()
                except IndexError:
                    continue

                # Outputting picture
                text = handshape_detector.get_handshape(mp_hands.history[-1])
                pts = np.int32(relative_to_absolute(np.asarray(mp_hands.history)[:, 8], w, h))
                img = cv2.polylines(img, [pts.reshape((-1, 1, 2))], isClosed=False, color=curr_colour)
            
            cv2.putText(img, text, (10,450), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow('MediaPipe Hands', img)

            if cv2.waitKey(5) & 0xFF == 27:
                break

            time.sleep(frame_delay)

    except:  
        mp_hands.close()
        cap.release()
        raise