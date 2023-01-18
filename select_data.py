from collections import Counter
from operator import itemgetter
import json
import shutil

with open("Training.json", "r") as f:
    data = json.load(f)


classes_count = Counter()

for annotation in data["annotations"]:
    classes_count[annotation["category_id"]] += 1

classes_by_amount = sorted(classes_count.items(), key=lambda x: x[1])
print(classes_by_amount)

classes_count[2] = classes_count[1]
classes_count[3] = classes_count[1]

selected_images = []
selected_ids = []


def use_image(image_id):
    global classes_count, selected_images, selected_ids
    if image_id in selected_ids:
        return
    images: list = data["images"]
    image_ids = list(map(itemgetter("id"), images))
    index = image_ids.index(image_id)
    selected_images.append(images[index])
    selected_ids.append(image_id)
    for ind, annotation in enumerate(data["annotations"]):
        if annotation["image_id"] == image_id:
            classes_count[annotation["category_id"]] -= 1


for annotation in data["annotations"]:
    if classes_count[1] <= 0:
        break
    if annotation["category_id"] == 1:
        use_image(annotation["image_id"])

print(classes_count.items())

for annotation in data["annotations"]:
    if classes_count[3] <= 0:
        break
    if annotation["category_id"] == 3:
        use_image(annotation["image_id"])

print(classes_count.items())

for annotation in data["annotations"]:
    if classes_count[2] <= 0:
        break
    if annotation["category_id"] == 2:
        use_image(annotation["image_id"])

print(classes_count.items())

print(selected_images[0])
for i, img in enumerate(selected_images):
    img_w = img["width"]
    img_h = img["height"]
    file_name = img["file_name"]
    img_id = img["id"]
    shutil.copy2(rf"D:\Informatyka\Sikorki\still_frames\{file_name}", fr"D:\Informatyka\Sikorki\dataset\all\{i}.png")
    with open(rf"D:\Informatyka\Sikorki\dataset\all\{i}.txt", "w+") as f:
        for annotation in data["annotations"]:
            if annotation["image_id"] != img_id:
                continue
            current_category = annotation['category_id'] - 1  # As yolo format labels start from 0
            current_bbox = annotation['bbox']
            x = current_bbox[0]
            y = current_bbox[1]
            w = current_bbox[2]
            h = current_bbox[3]

            x_centre = (x + (x + w)) / 2
            y_centre = (y + (y + h)) / 2

            x_centre = x_centre / img_w
            y_centre = y_centre / img_h
            w = w / img_w
            h = h / img_h

            _centre = format(x_centre, '.6f')
            y_centre = format(y_centre, '.6f')
            w = format(w, '.6f')
            h = format(h, '.6f')

            f.write(f"{current_category} {x_centre} {y_centre} {w} {h}\n")

