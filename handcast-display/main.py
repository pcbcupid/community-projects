import cv2
import control as cnt
from cvzone.HandTrackingModule import HandDetector
import numpy as np

detector = HandDetector(detectionCon=0.8, maxHands=1)
video = cv2.VideoCapture(0)

min_distance = 15
max_distance = 200

def draw_dotted_line(img, pt1, pt2, color=(255, 255, 255), thickness=2, gap=5):
    dist = int(np.linalg.norm(np.array(pt2) - np.array(pt1)))
    for i in range(0, dist, gap * 2):
        start = (
            int(pt1[0] + (pt2[0] - pt1[0]) * i / dist),
            int(pt1[1] + (pt2[1] - pt1[1]) * i / dist)
        )
        end = (
            int(pt1[0] + (pt2[0] - pt1[0]) * (i + gap) / dist),
            int(pt1[1] + (pt2[1] - pt1[1]) * (i + gap) / dist)
        )
        cv2.line(img, start, end, color, thickness)

while True:
    success, frame = video.read()
    frame = cv2.flip(frame, 1)
    hands, _ = detector.findHands(frame, draw=False)  

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]

        x1, y1 = lmList[4][0:2]   # Thumb tip
        x2, y2 = lmList[8][0:2]   # Index tip

        # Dotted white line
        draw_dotted_line(frame, (x1, y1), (x2, y2), color=(222, 222, 222), thickness=2)

        # Draw small white circles
        cv2.circle(frame, (x1, y1), 15, (222, 222, 222))
        cv2.circle(frame, (x2, y2), 15, (222, 222, 222))        
        cv2.circle(frame, (x1, y1), 7, (200, 200, 200), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 7, (200, 200, 200), cv2.FILLED)

        # Measure distance b/w points
        distance = int(np.linalg.norm(np.array([x2 - x1, y2 - y1])))

        # Map to the brightness to distance 
        brightness = np.interp(distance, [min_distance, max_distance], [0, 255])

        # Display the val on screen
        cv2.putText(frame, f'Brightness: {int(brightness)}', (10, 460),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (252, 252, 252), 1)

        # Send brightness to glyph
        cnt.send_brightness(brightness)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) == ord('k'):
        break

video.release()
cv2.destroyAllWindows()
