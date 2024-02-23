from send import send_action



import numpy as np
import mediapipe as mp
import cv2
import time
import pyautogui


def main():    
    # tunnelUrl = input("Device URL : ")
    # username = input("username")
    # password = input("password")
    username = "master"
    password = "master123"
    # cred = {"tunnelUrl" : tunnelUrl , "username" : username , "password":password}

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    horizontal_split_left = 1/3
    horizontal_split_right = 2/3

    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.4,
        max_num_hands = 1,
        min_tracking_confidence=0.4) as hands:
        

        while cap.isOpened():   

            success, image = cap.read() 
            h, w, c = image.shape
            left_boundary = int(horizontal_split_left * w)
            right_boundary = int(horizontal_split_right * w)
            start = time.perf_counter()
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:

                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                    
                    index_finger_tip_up = hand_landmarks.landmark[8]
                    index_finger_tip_down = hand_landmarks.landmark[6]
                    middle_finger_tip_up = hand_landmarks.landmark[12]
                    middle_finger_tip_down = hand_landmarks.landmark[10] 
                    thumb_tip_up = hand_landmarks.landmark[4]

                    index_finger_up = index_finger_tip_up.y * h
                    index_finger_down = index_finger_tip_down.y * h 
                    middle_finger_up = middle_finger_tip_up.y * h
                    middle_finger_down = middle_finger_tip_down.y * h
                    thumb_tip_up = thumb_tip_up.y * h


                    # left side 
                    if (index_finger_tip_up.x * w < left_boundary):
                        print("L")
                    # right side 
                    elif (index_finger_tip_up.x * w > right_boundary):
                        print("R")

                    # palm close
                    if index_finger_up > index_finger_down and middle_finger_up > middle_finger_down:
                        cv2.putText(image, "palm close", (300,70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,0), 2)
                        # pyautogui.keyDown('left')
                        # pyautogui.keyUp('right')
                        # send_action(cred,"left")
                        print("PC")
                    # pinch
                    elif (thumb_tip_up - index_finger_up) < 30 :
                        cv2.putText(image, "pinch", (500,70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,0), 2)
                        print("P")
                    # palm open
                    elif index_finger_up < index_finger_down and middle_finger_up < middle_finger_down :
                        cv2.putText(image, "palm open", (300,70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)
                        # pyautogui.keyDown('right')
                        # pyautogui.keyUp('left')
                        # send_action(cred,"right")
                        print("PO")




            else :
                cv2.putText(image, "null", (500,70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,0), 2)
                # pyautogui.keyUp('left')
                # pyautogui.keyUp('right')


        # cv2.line(image, (int(w/2), 0), (int(w/2), h), (0, 255, 0), 2)
            end = time.perf_counter()
            totalTime = end - start
            fps = 1 / totalTime
            cv2.putText(image, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0),2)
            cv2.line(image, ( left_boundary, h), ( left_boundary, 0), (255,0,0), 6)
            cv2.line(image, ( right_boundary, h), ( right_boundary, 0), (255,0,0), 6)
            cv2.imshow('MediaPipe Hands', image)
            if cv2.waitKey(2) == ord('q'):
                break

    cap.release()



if __name__ == "__main__":
    main()





















