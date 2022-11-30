# Importing Libraries
import cv2
import mediapipe as mp

# Used to convert protobuf message to a dictionary.
from google.protobuf.json_format import MessageToDict

# Initializing the Model
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
min_detection_confidence = 0.75,
                           min_tracking_confidence = 0.75,
                                                     max_num_hands = 2)


#TODO BUILD MY OWN HAND DETECTION!!!
# Start capturing video from webcam
# HAND ABOVE A CHESS BOARD CLASSIFICARE



cap = cv2.VideoCapture(0)

while True:
    # Read video frame by frame
    success, img = cap.read()

    # Flip the image(frame)
    img = cv2.flip(img, 1)

    # Convert BGR image to RGB image
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process the RGB image
    results = hands.process(imgRGB)

    # If hands are present in image(frame)
    if results.multi_hand_landmarks:
        print("KUSRABAKKKKK")
        x1 = 50
        x2 = 300
        y1 = 100
        y2 = 150

        image = cv2.arrowedLine(img, (x1, y1), (x2, y2), (233, 0, 55), 2)
        # image = cv2.line(img, (x1, y1), (x1-10, y1+30), (0, 0, 55), 2)
        # image = cv2.line(img, (x1, y1), (x1+30, y1+30), (0, 200, 55), 2)

    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break


