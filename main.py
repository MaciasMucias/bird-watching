import cv2
import numpy as np


if __name__ == '__main__':
    cam = cv2.VideoCapture("./test.mp4v")
    frame_count = 0
    prev_frame = None
    prev_diff = np.zeros((int(cam.get(4)), (int(cam.get(3)))))
    i = 0
    while True:
        ret, frame = cam.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        preped_frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)
        preped_frame = cv2.GaussianBlur(preped_frame, ksize=(5, 5), sigmaX=0)

        if prev_frame is None:
            prev_frame = preped_frame
            continue

        frame_diff = cv2.absdiff(prev_frame, preped_frame)
        prev_frame = preped_frame

        kernel = np.ones((5, 5))
        frame_diff = cv2.dilate(frame_diff, kernel, 1)

        thresh_frame = cv2.threshold(frame_diff, thresh=30, maxval=255, type=cv2.THRESH_BINARY)[1]
        merge = thresh_frame+prev_diff
        prev_diff = thresh_frame

        cv2.putText(merge, str(i), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255), 3)
        cv2.imshow("test", merge)
        if i == 519:
            cv2.imshow("screen", frame)
            cv2.waitKey(0)
        cv2.waitKey(1)
        i += 1
