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
LANDMARK = mp.solutions.hands.HandLandmark

def get_centroid(hand):
    return np.mean(hand, axis=0)

def get_click_approx(hand):
    return (hand[0] + hand[5]) / 2

class SwipeDetector:
    def __init__(self, window, main_axis_thresh, cross_axis_thresh, cooldown):
        self.window = window
        self.main_axis_thresh = main_axis_thresh  # Relative coords
        self.cross_axis_thresh = cross_axis_thresh  # Relative coords
        self.cooldown = cooldown  # Number of seconds
        self.vicinity_thresh = main_axis_thresh * 0.25

        self.previous_swipe_time = -np.inf
        self.previous_location = [-1, -1]

    def get_swipe(self, axis, history):
        """Getting swipe direction
        For axis=0: -1 is left, 1 is right, 0 is no swipe
        For axis=1: -1 is up, 1 is down, 0 is no swipe
        """

        if time.time() - self.previous_swipe_time < self.cooldown:  # Check cooldown
            return 0
        elif np.linalg.norm(
            self.previous_location - history[-1][LANDMARK.INDEX_FINGER_TIP]
        ) < self.vicinity_thresh:  # Check if swipe registered yet
            return 0
        # elif np.linalg.norm(
        #     history[-int(self.window)][LANDMARK.INDEX_FINGER_TIP] - history[-int(self.window* 0.25)][LANDMARK.INDEX_FINGER_TIP]
        # ) < self.vicinity_thresh: # Check for jumps
        #     return 0
        else:
            main_axis = axis
            cross_axis = 0 if axis == 1 else 1
            main = history[-1][LANDMARK.INDEX_FINGER_TIP, main_axis] - \
                history[-int(self.window)
                        ][LANDMARK.INDEX_FINGER_TIP, main_axis]
            cross = history[-1][LANDMARK.INDEX_FINGER_TIP, cross_axis] - \
                history[-int(self.window)
                        ][LANDMARK.INDEX_FINGER_TIP, cross_axis]
            if abs(main) > self.main_axis_thresh and abs(cross) < self.cross_axis_thresh:
                self.previous_swipe_time = time.time()
                self.previous_location = history[-1][LANDMARK.INDEX_FINGER_TIP]
                return -1 if main < 0 else 1
            else:
                return 0


def is_hand(hand_of_interest, history, window):
    if type(hand_of_interest) != list:
        hand_of_interests = [hand_of_interest]
    else:
        hand_of_interests = hand_of_interest
    history_array = np.asarray(history)
    return all(hand in hand_of_interests for hand in history_array[-int(window):])


class GestureDetector:
    """ Will encompass point, swipe, etc."""

    def __init__(self, window):
        self.state = "none"
        self.is_click = False
        self.scroll_height = -1 # Relative (Only use when state is "scroll" or "volume")
        self.history = collections.deque(maxlen=100)
        self.swipe_detector = SwipeDetector(
            window=10,
            main_axis_thresh=0.45,
            cross_axis_thresh=0.2,
            cooldown=1.0
        )

    def run(self, hand, landmarks, i_history):
        self.is_click = False
        self.history.append(hand)
        # Two-finger ================================
        if is_hand("peace", self.history, 8) and not self.state == "volume":
            self.state = "scroll"
        elif is_hand("spiderman", self.history, 8) and not self.state == "scroll":
            self.state = "volume"
        elif is_hand("call", self.history, 8):
            self.state = "audio"

        if self.state == "scroll" or self.state == "volume":
            self.scroll_height = 1 - landmarks[LANDMARK.MIDDLE_FINGER_MCP][1]
            if is_hand(["palm-open", "palm-closed"], self.history, 5): # Only palm can deactivate
                self.state = "none"
                self.scroll_height = -1
        elif self.state == "audio":
            pass
        else:
            # Swipe ====================================
            try:
                h_swipe = self.swipe_detector.get_swipe(0, i_history)
                v_swipe = self.swipe_detector.get_swipe(1, i_history)
            except IndexError:
                h_swipe = 0
                v_swipe = 0
            if h_swipe != 0:
                direction = 'left' if h_swipe == -1 else 'right'
                print(f"SWIPED {direction}!")
                self.state = f"swipe-{direction}"
            elif v_swipe != 0:
                direction = 'up' if v_swipe == -1 else 'down'
                print(f"SWIPED {direction}!")
                self.state = f"swipe-{direction}"
            
            # Mouse ============================================
            elif is_hand(["palm-open", "palm-closed"], self.history, 5):
                self.state = "mouse"
            elif is_hand("fist", self.history, 5):
                self.is_click = True
            else:
                self.state = "none"
                #print(landmarks[LANDMARK.INDEX_FINGER_TIP], landmarks[LANDMARK.THUMB_TIP])
                # if np.linalg.norm(landmarks[LANDMARK.INDEX_FINGER_TIP] - landmarks[LANDMARK.THUMB_TIP]) < 0.03:
        



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
        prediction = self.clf.predict(
            np.expand_dims(self.process_input(hand), 0))
        return self.labels[int(prediction)]


def relative_to_absolute(relative, img_width, img_height):
    return relative @ np.diag([img_height, img_width])


def landmark_to_array(multi_hand_landmark):
    """ e.g. multi_hand_landmark = results.multi_hand_landmarks[0]"""
    # return np.asarray([[pt.x, pt.y, pt.z] for pt in multi_hand_landmark.landmark])
    return np.asarray([[pt.x, pt.y] for pt in multi_hand_landmark.landmark])


class MPHands:
    def __init__(self, buffer_size=None, track_missing_thresh=3):
        self.hands = mp.solutions.hands.Hands(
            min_detection_confidence=0.75,
            min_tracking_confidence=0.9
        )
        self.history = collections.deque(maxlen=buffer_size)

        self.track_missing_thresh = track_missing_thresh
        self.track_missing_number = 0

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
            results_array = landmark_to_array(
                results.multi_hand_landmarks[0])  # Relative coords
            self.history.append(results_array)
            self.track_missing_number = 0
        elif self.track_missing_number < self.track_missing_thresh:
            self.track_missing_number += 1
        else:
            self.history.clear()
            self.track_missing_number = 0
        # else:
        #     try:
        #         self._update_history(self.history[-1])
        #     except IndexError:
        #         pass

        return results

    def render(self, image, results):
        # Overlays the mediapipe "skeleton" onto the image
        flipped = cv2.flip(image, 1)  # Flipped to match the results
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    flipped,
                    hand_landmarks,
                    mp.solutions.hands.HAND_CONNECTIONS
                )
        return flipped

    def close(self):
        self.hands.close()


if __name__ == "__main__":
    frame_delay = 0.05

    swipe_duration = 0.5  # Approx num seconds for swipe to be valid
    history_window = 0.5  # Num seconds of history to save in the mphands object
    buffer_size = int(history_window / frame_delay)
    curr_colour = np.random.uniform(0, 255, 3)
    text = ""

    mp_hands = MPHands(buffer_size=buffer_size)
    swipe_detector = SwipeDetector(
        window=swipe_duration / frame_delay,
        main_axis_thresh=0.5,
        cross_axis_thresh=0.2,
        cooldown=0.5
    )
    handshape_detector = HandShapeDetector("data")
    gesture_detector = GestureDetector(5)

    try:
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            hand_shape = None
            # 1. Get image ====================================================
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            # 2. Run mediapipe ================================================
            w, h, _ = image.shape
            results = mp_hands.run(image)

            # 3. Detect gestures ==============================================
            if mp_hands.history:  # Ensures there is history available
                # Hand Shape -------------------------------
                hand_shape = handshape_detector.get_handshape(
                    mp_hands.history[-1])
                text = hand_shape

                # Gesture
                gesture_detector.run(hand_shape, mp_hands.history[-1], mp_hands.history)

                # # Hand Swipe -------------------------------
                # try:
                #     h_swipe = swipe_detector.get_swipe(0, mp_hands.history)
                #     v_swipe = swipe_detector.get_swipe(1, mp_hands.history)
                #     if h_swipe != 0:
                #         print(
                #             f"SWIPED {'left' if h_swipe == -1 else 'right'}!!!!!!!!!!!!")
                #         curr_colour = np.random.uniform(0, 255, 3)
                #         previous_swipe_time = time.time()
                #     elif v_swipe != 0:
                #         print(
                #             f"SWIPED {'up' if v_swipe == -1 else 'down'}!!!!!!!!!!!!")
                #         curr_colour = np.random.uniform(0, 255, 3)
                #         previous_swipe_time = time.time()
                # except IndexError:
                #     continue

            # 4. Showing the image result =====================================
            # Overlaying the mediapipe "skeleton"
            img = mp_hands.render(image, results)
            if mp_hands.history:
                # Drawing the finger path
                pts = np.int32(relative_to_absolute(np.asarray(
                    [get_click_approx(p) for p in mp_hands.history]), w, h))
                img = cv2.polylines(
                    img, [pts.reshape((-1, 1, 2))], isClosed=False, color=curr_colour)

            cv2.putText(img, text, (10, 450), cv2.FONT_HERSHEY_SIMPLEX,
                        3, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow('Swipe', img)

            # =================================================================
            print(f"State={gesture_detector.state}, isClick={gesture_detector.is_click}, scrollHeight={gesture_detector.scroll_height}, hand={hand_shape}")
            if cv2.waitKey(5) & 0xFF == 27:
                break

            #time.sleep(frame_delay)
    except:
        mp_hands.close()
        cap.release()
        raise
