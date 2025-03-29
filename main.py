import mediapipe as mp
import cv2
import numpy as np
import uuid
import os
import matplotlib as plt
import time


result=None
num1 = None
num2 = None
operation = None
is_waiting_for_num2 = False
input_time_limit = 8  # Time limit for each input in seconds 
last_input_time = time.time()  # Initialize timer
input_state = "waiting_for_num1"  # Track the current input state

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)
hands_videos = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

def detectHandsLandmarks(frame, hands, display=False):
    
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
   
    image = cv2.flip(image, 1)

    
    image.flags.writeable = False
    
    
    results = hands.process(image)
    
    
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Render the landmarks on the image
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2)
            )
    
   
    if display:
        cv2.imshow('Hand Landmarks', image)
    
    return image, results


def countFingers(image, results, draw=True, display=True):
    
    height, width, _ = image.shape
    
    
    output_image = image.copy()
    
    
    count = {'RIGHT': 0, 'LEFT': 0}
    
    #Indexes of the tips landmarks of each finger of a hand 
    fingers_tips_ids = [mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                        mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]
    
    # True for finger raised and False for not raised of each finger of both hands.
    fingers_statuses = {'RIGHT_THUMB': False, 'RIGHT_INDEX': False, 'RIGHT_MIDDLE': False, 'RIGHT_RING': False,
                        'RIGHT_PINKY': False, 'LEFT_THUMB': False, 'LEFT_INDEX': False, 'LEFT_MIDDLE': False,
                        'LEFT_RING': False, 'LEFT_PINKY': False}
    
    
    
    for hand_index, hand_info in enumerate(results.multi_handedness):
        
        hand_label = hand_info.classification[0].label
        hand_landmarks =  results.multi_hand_landmarks[hand_index]
        
        for tip_index in fingers_tips_ids:
            
            finger_name = tip_index.name.split("_")[0]
            
            # Checking if the finger is up by comparing the y-coordinates of the tip and pip landmarks.
            if (hand_landmarks.landmark[tip_index].y < hand_landmarks.landmark[tip_index - 2].y):
                fingers_statuses[hand_label.upper()+"_"+finger_name] = True
                count[hand_label.upper()] += 1
        
        # y-coordinates of the tip and mcp landmarks of the thumb of the hand.
        thumb_tip_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
        thumb_mcp_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP - 2].x
        
        # Checking if the thumb is up by comparing the hand label and the x-coordinates of the retrieved landmarks.
        if (hand_label=='Right' and (thumb_tip_x < thumb_mcp_x)) or (hand_label=='Left' and (thumb_tip_x > thumb_mcp_x)):
            fingers_statuses[hand_label.upper()+"_THUMB"] = True
            count[hand_label.upper()] += 1
     
    if display:
        plt.figure(figsize=[10,10])
        plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
    
    
    else:
        return output_image,sum(count.values())
    
def detect_operation(fingers_up):
# Define operations based on number of fingers
    if fingers_up == 0:
        return "+"  # Closed fist (addition)
    elif fingers_up == 1:
        return "-"  # Thumbs down (subtraction)
    elif fingers_up == 2:
        return "*"  # Peace sign (multiplication)
    elif fingers_up == 5:
        return "/"  # Open palm (division)
    else:
        return None  # No gesture
        
# Function to display elapsed time in seconds
def display_timer(frame, x, y, last_input_time, input_time_limit):
    elapsed_time = int(time.time() - last_input_time)
    remaining_time = input_time_limit - elapsed_time
    if remaining_time > 0:
        cv2.putText(frame, f"Time left: {remaining_time}s", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(frame, f"Time's up!", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

#To display the captured values as a reference
def display_captured_values(frame):
    y_pos = 100
    key_value_pairs = [
        ("Num1", num1),
        ("Operation", operation),
        ("Num2", num2),
        ("Result", result),
    ]

    for key, value in key_value_pairs:
        if value is not None:
            cv2.putText(frame, f"{key}: {value}", (frame.shape[1] - 250, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            y_pos += 50 

    

cap = cv2.VideoCapture(0)
cap.set(3, 800)
cap.set(4, 500)

while cap.isOpened():
    ok, frame = cap.read()
    
    if not ok:
        continue
    
    # Perform Hands landmarks detection on the frame
    frame, results = detectHandsLandmarks(frame, hands_videos, display=False)

    if results.multi_hand_landmarks:
        # Count fingers raised in real-time
        frame, detected_fingers = countFingers(frame, results, display=False)

        if input_state == "waiting_for_num1":
            cv2.putText(frame, f"Num1: {detected_fingers}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if time.time() - last_input_time > input_time_limit:
                num1 = detected_fingers
                input_state = "waiting_for_operation"
                last_input_time = time.time()

        elif input_state == "waiting_for_operation":
            operation = detect_operation(detected_fingers)
            if operation:
                cv2.putText(frame, f"Operation: {operation}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if time.time() - last_input_time > input_time_limit:
                input_state = "waiting_for_num2"
                last_input_time = time.time()

        elif input_state == "waiting_for_num2":
            frame, num2_detected = countFingers(frame, results, display=False)
            cv2.putText(frame, f"Num2: {num2_detected}", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if time.time() - last_input_time > input_time_limit:
                num2 = num2_detected
                input_state = "waiting_for_result"
                last_input_time = time.time()

        elif input_state == "waiting_for_result":
            # Perform calculation
            if operation == "+":
                result = num1 + num2
            elif operation == "-":
                result = num1 - num2
            elif operation == "*":
                result = num1 * num2
            elif operation == "/":
                result = num1 / num2 if num2 != 0 else "Error"

            input_state = "display_result"

        elif input_state == "display_result":
            # Waiting until user presses 'r' to reset
            cv2.putText(frame, "Press 'R' to reset", (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the captured values on the right
    display_captured_values(frame)

    # Display the timer
    display_timer(frame, 10, 50, last_input_time, input_time_limit)
    
    # Show the frame with updates
    cv2.imshow('Finger Based Calculator', frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):  # Reset all values when 'r' is pressed
        num1 = num2 = operation = result = None
        input_state = "waiting_for_num1"
        last_input_time = time.time()

# Release resources
cap.release()
cv2.destroyAllWindows()


