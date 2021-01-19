def run():
    import cv2
    import mediapipe as mp
    import pyautogui as gui
    import keyboard

    import speech_input
    import gesture_detector

    gui.FAILSAFE = True
    is_show_video = True

    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    gd = gesture_detector.GestureDetector(5)
    hd = gesture_detector.HandShapeDetector("data")
    hands = gesture_detector.MPHands(buffer_size=100)

    try:
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            results = hands.run(image)
            hshape = ""
            if hands.history:
                # get hand shape
                hshape = hd.get_handshape(hands.history[-1])
                gd.run(hshape, hands.history[-1], hands.history)
                print(f"State={gd.state}, isClick={gd.is_click}, scrollHeight={gd.scroll_height}, hand={hshape}")
                if gd.state == "mouse":
                    point = hands.history[-1][gesture_detector.LANDMARK.INDEX_FINGER_TIP]
                    point = gesture_detector.get_centroid(hands.history[-1])
                    # point = gesture_detector.get_click_approx(hands.history[-1])  # This will give more accurate clicking
                    SENSE = 1.5
                    relativeX = int(point[0] * gui.size()[0] * SENSE)
                    relativeY = int(point[1] * gui.size()[1] * SENSE)
                    gui.moveTo(relativeX, relativeY, _pause=False)
                if gd.is_click:
                    gui.click()
                    gd.is_click = False

                if gd.state == "audio":
                    try:
                        speech_input.from_mic()
                    except AssertionError as e:
                        print(
                            "Speech recognition currently not available because " + str(e))
                    gd.state = "none"

                if gd.state == "volume":
                    if gd.scroll_height > 0.5:
                        gui.press('volumeup',  _pause=False)
                    else:
                        gui.press('volumedown', _pause=False)

                if gd.state == "scroll":
                    SCROLLSENSE = 38
                    if gd.scroll_height > 0.5:
                        gui.scroll(
                            int(gd.scroll_height * SCROLLSENSE), _pause=False)
                    else:
                        gui.scroll(int(gd.scroll_height * -
                                    SCROLLSENSE), _pause=False)

                if gd.state == "swipe-left" or gd.state == "swipe-right":
                    gui.hotkey('alt', 'tab')
                    gd.state = "none"

                if gd.state == "swipe-up" or gd.state == "swipe-down":
                    gui.hotkey('alt', 'shift', 'tab', _pause=False)
                    gd.state = "none"

            if is_show_video:
                # Overlaying the mediapipe "skeleton"
                img = hands.render(image, results)
                cv2.putText(img, hshape, (10, 450), cv2.FONT_HERSHEY_SIMPLEX,
                            3, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.imshow('Camera View :)', img)

            if cv2.waitKey(5) & 0xFF == 27:
                break
    except:        
        cv2.destroyAllWindows()
        hands.close()
        cap.release()
        print("\n>>> Error caught. Program closed gracefully. <<<\n")
        raise


if __name__ == "__main__":
    run()
