import imageio.v3 as iio
from glob import glob
from multiprocessing import Pool, Manager
import json
from tqdm import tqdm
from PIL import Image


local_path = r"D:\Informatyka\Sikorki"


dataset_path = local_path + r"\recordings"
target_path = local_path + r"\still_frames"
dict_path = local_path + r"\clips.json"


def _cut_videos(clip_path, clip_marks, clips_counter):
    global target_path
    if not clip_marks:
        return
    frames = iter(clip_marks)
    movie = iio.imiter(clip_path, plugin='pyav')

    current_frame = next(frames)

    for n, frame in enumerate(movie):
        if n < current_frame:
            continue
        PIL_image = Image.fromarray(frame.astype('uint8'), 'RGB')
        PIL_image.save(f"{target_path}/{clips_counter.count}.png")
        clips_counter.count += 1
        current_frame = next(frames, False)
        if not current_frame:
            break


def cut_videos(args):
    return _cut_videos(*args)


if __name__ == '__main__':
    manager = Manager()
    clips_counter = manager.Namespace()
    clips_counter.count = 0
    with open(dict_path, 'r') as f:
        clips = json.load(f)

    args_list = [(f"{dataset_path}\\{clip}", data, clips_counter) for clip, data in clips.items()]
    for args in tqdm(args_list):
        cut_videos(args)
