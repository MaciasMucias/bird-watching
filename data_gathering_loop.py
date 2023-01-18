import cv2
import numpy as np
import time

movement_size = 1500
thresh_size = 30
recorded_frames_after_movement = 300
prev_frame, current_frame = None, None
kernel = np.ones((5, 5))


def create_filename():
    return time.strftime("/home/karas/Desktop/Sikorki/recordings/Recording %d%m%Y-%H%M%S.mp4")


def prepare_frame(frame):
    grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(grayscale_frame, ksize=(5, 5), sigmaX=0)


def calc_change():
    global prev_frame, current_frame, kernel, thresh_size
    prepared_frame = prepare_frame(current_frame)
    frame_diff = cv2.absdiff(prev_frame, prepared_frame)
    prev_frame = prepared_frame

    dilated_frame_diff = cv2.dilate(frame_diff, kernel, 1)

    thresh_frame = cv2.threshold(dilated_frame_diff, thresh=thresh_size, maxval=255, type=cv2.THRESH_BINARY)[1]
    return thresh_frame


def main():
    global prev_frame, current_frame, movement_size, recorded_frames_after_movement
    cam = cv2.VideoCapture(0)
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    size = (width, height)
    fps = int(cam.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    video_out_conf = (fourcc, fps, size)

    video_out = None
    recording = False
    frames_left = 0
    frame_count = 0
    if not cam.isOpened():
        raise RuntimeError("Camera not connected")
    prev_frame = prepare_frame(cam.read()[1])
    while True:
        ret, current_frame = cam.read()
        if not ret:
            break

        diff = calc_change()

        contours, _ = cv2.findContours(image=diff, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
        big_contours = list(filter(lambda x: cv2.contourArea(x) > movement_size, contours))

        if list(big_contours):
            frames_left = recorded_frames_after_movement
            if not recording:
                recording = True
                path = create_filename()
                print(f"New recording started. Name: {path}")
                video_out = cv2.VideoWriter(path, *video_out_conf)
                frame_count = 0

        if recording:
            video_out.write(current_frame)
            frames_left -= 1
            frame_count += 1
            #print(f"{frame_count=}")
            if not frames_left > 0:
                print(f"Recording {path} has completed")
                recording = False
                video_out.release()
        cv2.waitKey(20)


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        with open("/home/karas/Desktop/Sikorki/error.log",  'a') as f:
            f.write(str(err))

