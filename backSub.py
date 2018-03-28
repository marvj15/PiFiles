import argparse
import datetime
import imutils
import time
from time import sleep
from threading import Thread
import thread
import cv2


class Detection:

    number = 0
    firstFrame = None
    gray = 0

    def __init__(self):
        return

    def numofitems(self):
        x = self.number
        return x

    def startdetection(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video", help="path to the video file")
        ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
        args = vars(ap.parse_args())

        if args.get("video", None) is None:
            camera = cv2.VideoCapture(0)
            time.sleep(0.25)

        else:
            camera = cv2.VideoCapture(args["video"])

        self.firstFrame = None

        while True:
            (grabbed, frame) = camera.read()
            text = "Unoccupied"

            if not grabbed:
                break

            frame = imutils.resize(frame, width=500)
            self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.gray = cv2.GaussianBlur(self.gray, (21, 21), 0)

            if self.firstFrame is None:
                self.setfirstframe()
                continue

            frameDelta = cv2.absdiff(self.firstFrame, self.gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

            thresh = cv2.dilate(thresh, None, iterations=2)
            (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            tempc = 0
            for c in cnts:
                if cv2.contourArea(c) < args["min_area"]:
                    tempc = tempc +1
                    continue

                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                self.number = len(cnts)-tempc
                text = "Occupied :" + str(self.numofitems())

            cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            cv2.imshow("Security Feed", frame)
            cv2.imshow("Thresh", thresh)
            cv2.imshow("Frame Delta", frameDelta)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("n"):
                self.setfirstframe()
            if key == ord("q"):
                break

        camera.release()
        cv2.destroyAllWindows()
        return

    def setfirstframe(self):
        self.firstFrame = self.gray
        return

def tf(det):
    while True:
        print(det.number)
        sleep(1)



def startmultithread():
    det = Detection()
    #thread.start_new_thread(det.startdetection, ())
    thread = Thread(target = tf, args=(det,))
    thread.start()
    return det


newdet = startmultithread()

newdet.startdetection()