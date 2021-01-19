""" 
Adapted from https://google.github.io/mediapipe/solutions/hands#python-solution-api 

The point of the Gesture Detector is to  get gesture from video feed.
"""

import cv2
import time
import gesture_detector as gd
import numpy as np
import pickle


if __name__ == "__main__":
    frame_delay = 0.05
    history_window = 5 # Num seconds of history to save
    buffer_size = int(history_window / frame_delay) 
    mp_hands = gd.MPHands(buffer_size=buffer_size)

    data = {}
    current_shape_id = 0
    num_data_points_per_shape = 200
    hand_shapes = ["spiderman"]
    pause_time = 5
    for shape in hand_shapes:
        data[shape] = []

    try:
        cap = cv2.VideoCapture(0)
        print(f"Get ready for '{hand_shapes[current_shape_id]}'")
        time.sleep(pause_time)
        while cap.isOpened():
            # Get image
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue
            w, h, _ = image.shape

            # Get mediapipe features
            results = mp_hands.run(image)

            # Storing the data
            current_shape = hand_shapes[current_shape_id]
            try:
                data[current_shape].append(mp_hands.history[-1])
            except IndexError:
                continue

            # Showing the results
            img = mp_hands.render(image, results)            
            cv2.imshow('MediaPipe Hands', img)
            if cv2.waitKey(5) & 0xFF == 27:
                break

            print(len(data[current_shape]))
            if len(data[current_shape]) == num_data_points_per_shape:
                current_shape_id += 1
                if current_shape_id == len(hand_shapes):
                    raise AssertionError
                else:
                    print(f"Get ready for '{hand_shapes[current_shape_id]}'")
                    time.sleep(pause_time)
            else:
                time.sleep(frame_delay)
    except:  
        for shape in hand_shapes:
            data_array = np.asarray(data[shape])
            print(f"{data_array.shape[0]} data points for {shape}")
            with open(f"data_{shape}.p", 'wb') as f:
                pickle.dump(data_array, f)
        print("Now move the .p files to Server/data")
        mp_hands.close()
        cap.release()
        raise