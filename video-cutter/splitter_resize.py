import imageio.v3 as iio
from glob import glob
import cv2
from multiprocessing import Pool
import json
import tqdm


local_path = r"D:\Informatyka\Sikorki"
scale = 4


large_path = local_path + r"\large_files"
cropped_path = local_path + r"\recordings"


def resize_video(path):
    file_name = path[path.rfind('\\')+1:]
    fps = iio.immeta(path, plugin='pyav')['fps']
    movie = iio.imiter(path, plugin='pyav')
    first_frame = next(movie)
    y, x, _ = first_frame.shape

    rotated_frame = first_frame.swapaxes(0, 1)
    cropped_frame = cv2.resize(rotated_frame, (y//4, x//4))

    with iio.imopen(f"{cropped_path}\\{file_name}", 'w', plugin='pyav') as out_file:
        out_file.init_video_stream('libx264', fps=fps)
        out_file.write_frame(cropped_frame)
        for frame in movie:
            rotated_frame = frame.swapaxes(0, 1)
            cropped_frame = cv2.resize(rotated_frame, (y // scale, x // scale))
            out_file.write_frame(cropped_frame)


if __name__ == '__main__':
    dataset = glob(large_path + r"\*")
    with Pool() as pool:
        for _ in tqdm.tqdm(pool.imap(resize_video, dataset), total=len(dataset)):
            pass


