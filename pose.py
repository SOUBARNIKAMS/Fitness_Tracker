import cv2
import math
import numpy as np
import cvzone
from cvzone.PoseModule import PoseDetector

msg = ""

def findAngle(lmList, img, p1, p2, p3):
    x1, y1 = lmList[p1][1:3]
    x2, y2 = lmList[p2][1:3]
    x3, y3 = lmList[p3][1:3]
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -math.atan2(y1 - y2, x1 - x2))
    if angle < 0:
        angle += 360

    return angle
def WarriorPose(img, lmList):
    angle1 = findAngle(lmList, img, 11, 13, 15)
    angle2 = findAngle(lmList, img, 12, 14, 16)
    angle3 = findAngle(lmList, img, 24, 26, 28)
    angle4 = findAngle(lmList, img, 23, 25, 27)
    if (206 <= angle1 <= 290 and 180 <= angle2 <= 197):
        if (227 <= angle3 <= 251 or 280 <= angle4 <= 290):
                return True
    return False


def TreePose(img, lmList):
    angle1 = findAngle(lmList, img, 24, 26, 28)  # Angle between landmarks 24, 26, 28
    angle2 = findAngle(lmList, img, 23, 25, 27)  # Angle between landmarks 23, 25, 27
    if(196 <= angle1 <= 258 or 212 <= angle2 <= 347):
        if (212 <= angle1 <= 347 or 196 <= angle2 <= 258):
            return True
    return False

def TPose(img, lmList):
    angle1 = findAngle(lmList, img, 11, 13, 15)
    angle2 = findAngle(lmList, img, 12, 14, 16)
    angle3 = findAngle(lmList, img, 24, 26, 28)
    angle4 = findAngle(lmList, img, 23, 25, 27)
    if (178 <= angle3 <= 184 and 190 <= angle4 <= 232):
        if (30 <= angle1 <= 42 or 165 <= angle2 <= 184):
            return True

    return False

def capture(ch):
    try:
        global msg
        ch = int(ch)
        l = ["Tree Pose Yoga", "T Pose Yoga", "Warrior Pose Yoga", "Biceps Curl Workout", "Push Ups Workout"]
        path = "Images/" + str(ch) + ".mp4"
        cap = cv2.VideoCapture(path)
        detector = PoseDetector()
        counter = -1
        count = 0
        dir = 0
        displayText = "Invalid Pose"

        while True:
            success, img = cap.read()
            if success:
                img = cv2.resize(img, (1280, 720))
                imgDraw = detector.findPose(img)
                lmlist, _ = detector.findPosition(img)

                if len(lmlist) != 0:
                    if ch == 1:
                        if TreePose(img, lmlist):
                            if counter == -1:
                                counter = 0
                            else:
                                counter += 1
                    elif ch == 2:
                        if TPose(img, lmlist):
                            if counter == -1:
                                counter = 0
                            else:
                                counter += 1
                    elif ch == 3:
                        if WarriorPose(img, lmlist):
                            if counter == -1:
                                counter = 0
                            else:
                                counter += 1
                    elif ch == 4:
                        angle = findAngle(lmlist, img, 11, 13, 15)
                        per = np.interp(angle, (95, 200), (0, 100))
                        if per >= 99.5 and dir == 0:
                            count += 0.5
                            dir = 1
                        elif per <= 0.5 and dir == 1:
                            count += 0.5
                            dir = 0

                    elif ch == 5:
                        angle = findAngle(lmlist, img, 11, 13, 15)
                        per = np.interp(angle, (190, 240), (0, 100))
                        if per == 100 and dir == 0:
                            count += 0.5
                            dir = 1
                        elif per < 10 and dir == 1:
                            count += 0.5
                            dir = 0

                    if ch in [1, 2, 3]:
                        if counter == -1:
                            displayText = "Invalid Pose"
                        else:
                            displayText = "No of seconds=" + str(counter // 60)
                    elif ch in [4, 5]:
                        displayText = "No of Times=" + str(int(count))

                    cvzone.putTextRect(img, displayText, (50, 50))
                    ret, buffer = cv2.imencode('.jpg', img)

                    if ret:
                        img = buffer.tobytes()
                        yield (b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + img + b'\r\n')

            else:
                msg = "Today's workout pose is " + l[ch - 1] + ".\n" + displayText + "."
    except Exception as e:
        print(f"Error: {str(e)}")
