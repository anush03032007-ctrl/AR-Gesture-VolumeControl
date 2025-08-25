import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):

        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # Initialize MediaPipe Hands
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode,
                                        max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 0), cv2.FILLED)

        return lmList


def main():
    pTime = 0
    cTime = 0

    # Auto-detect the correct camera ID
    cap = None
    for i in range(4):  # Try camera IDs from 0 to 3
        try:
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                print(f"Successfully opened camera with ID: {i}")
                break
        except Exception:
            print(f"Failed to open camera with ID: {i}")
            cap = None
            continue

    if not cap or not cap.isOpened():
        print("Error: Could not open any camera. Exiting.")
        return

    detector = handDetector()

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read a frame from the camera.")
            break

        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        # Only print if a hand is detected to avoid IndexError
        if len(lmList) != 0:
            # Example: print the position of the thumb tip (landmark 4)
            print(lmList[4])

        # Calculate and display FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 0, 255), 3)

        # Display the image
        cv2.imshow("Hand Tracking", img)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('Q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()