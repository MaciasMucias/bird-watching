import imageio.v3 as iio
from glob import glob
import numpy as np
import cv2
import json
import ctypes
import time
import copy
import os
import tqdm

local_path = r"D:\Informatyka\Sikorki"
file_suffix = "MOV"

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
dataset_path = local_path + r"\recordings"
excluded_path = local_path + r"\excluded_files"
large_path = local_path + r"\large_files"
dict_path = local_path + r"\clips_wroble_move.json"


class safemutable:
    def __init__(self, path, obj):
        self.path = path
        self.obj = obj
        super().__init__()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.path, 'w+') as f:
            json.dump(self.obj, f)


def create_pairs(array):
    if len(array) % 2 == 0:
        offset = 1
    else:
        offset = 2

    return [(array[i], array[i + 1]) for i in range(0, len(array) - offset, 2)]


def prepare_img(frame):
    rotated_frame = frame[..., ::-1]
    return rotated_frame


def border(frame, color):
    frame[:10, :] = color
    frame[-11:, :] = color
    frame[:, :10] = color
    frame[:, -11:] = color


def imshow(winname, img):
    cv2.namedWindow(winname)
    cv2.moveWindow(winname, 0, 0)
    cv2.imshow(winname, img)


if __name__ == '__main__':
    dataset = glob(dataset_path + r"\*")
    with open(dict_path, 'r') as f:
        clips = json.load(f)

    clips_amount = 0
    for clip in clips:
        clips_amount += len(clips[clip])

    with safemutable(dict_path, clips):
        for path in dataset:
            large = False
            path_name = path[path.rfind('\\') + 1:]
            if path_name in clips:  # Already marked in a previous session
                continue
            print(f"{path} {clips_amount}")

            fps = iio.immeta(path, plugin='pyav')['fps']
            ms = int(1000 // fps)
            key = 0
            skip = False
            finish = False

            clips_mark = []
            restart = False
            clip_beginning = True
            try:
                movie = iio.imread(path, plugin='pyav')
            except MemoryError:
                print(f"File {path} too large to load into memory")
                os.replace(path, f"{large_path}\\{path_name}")
                continue
            freeze_frame = 0
            for frame_number, frame in enumerate(movie):
                if frame_number < freeze_frame:
                    continue
                start = time.time()
                finished_img = prepare_img(frame)
                imshow("Slice video", finished_img)
                end = time.time()
                key = cv2.waitKey(max(1, ms - int((end - start) * 1000)))

                if key == ord(' '):
                    freeze_frame = frame_number
                    frame_offset = 0
                    last_frame = len(movie) - 1

                    cancel = False
                    while True:
                        frozen_frame = copy.copy(movie[freeze_frame])
                        finished_img = prepare_img(frozen_frame)

                        imshow("Slice video", finished_img)
                        key = cv2.waitKey()
                        if key == ord(' '):
                            clips_mark.append(freeze_frame)
                            clips_amount += 1
                            border(movie[freeze_frame], (255, 0, 0))
                            break
                        elif key == 27:
                            key = None
                            break
                        elif key == ord('a'):
                            frame_offset = -1
                        elif key == ord('d'):
                            frame_offset = 1
                        else:
                            continue
                        freeze_frame += frame_offset
                        if freeze_frame < 0:
                            freeze_frame = 0
                        elif freeze_frame > last_frame:
                            freeze_frame = last_frame

                if key == 8:
                    skip = True
                    break

                if key == 27:
                    finish = True
                    break

            if finish:
                quit()

            clips[path_name] = clips_mark

            if skip:
                continue

            finished_img = prepare_img(frame)
            border(finished_img, [0, 255, 0])
            imshow("Slice video", finished_img)
            key = cv2.waitKey()
            if key == 27:
                finish = True

            cv2.destroyWindow("Slice video")

            if finish:
                quit()
