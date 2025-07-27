import random
import sys

from PIL import Image
import numpy as np

from stylize import wektoruj


def is_valid_pixel(pixel):
    r, g, b, a = pixel
    return a > 0 and not (r == 0 and g == 0 and b == 0)
def pixel_state(pixel):
    r, g, b, a = pixel
    if (a==0):
        return True
    if (r == 0 and g == 0 and b == 0):
        return False
    return True

def find_rectangles(image_path):
    img = Image.open(image_path).convert("RGBA")
    data = np.array(img)
    height, width = data.shape[:2]
    visited = np.zeros((height, width), dtype=bool)

    rectangles = []

    for y in range(height):
        for x in range(width):
            if visited[y, x]:
                continue

            pixel = tuple(data[y, x])
            if not is_valid_pixel(pixel):
                continue

            # Expand rectangle
            max_w, max_h = 0, 0

            # Determine width
            for w in range(x, width):
                if tuple(data[y, w]) == pixel and not visited[y, w]:
                    max_w += 1
                else:
                    break

            # Determine height
            done = False
            for h in range(y, height):
                for w in range(x, x + max_w):
                    if tuple(data[h, w]) != pixel or visited[h, w]:
                        done = True
                        break
                if done:
                    break
                max_h += 1

            # Mark visited
            for j in range(y, y + max_h):
                for i in range(x, x + max_w):
                    visited[j, i] = True

            # Determine cutoff

            rect = {
                "color": '{:02x}{:02x}{:02x}'.format(*[int(i) for i in pixel[:3]]),
                "min": (x, height - (y + max_h - 1)),
                "max": (x + max_w - 1, height - y),
                "width": max_w,
                "height": max_h
            }
            rectangles.append(rect)
    return rectangles



import re
import os
def check_if_exists(width, height, dir):
    def get_next_filename(folder_path, base_name):
        pattern = re.compile(rf'{re.escape(base_name)}-(\d+)\.txt$')
        max_number = -1
        os.makedirs(folder_path, exist_ok=True)

        for filename in os.listdir(folder_path):
            match = pattern.match(filename)
            if match:
                number = int(match.group(1))
                if number > max_number:
                    max_number = number

        next_number = max_number
        if (next_number == -1):
            return -1
        next_filename = f"{base_name}-{random.randint(0,next_number)}.txt"
        return next_filename
    return get_next_filename(dir+"building_blocks/", str(width)+"x"+str(height))


def get_next_number(folder_path, base_name):
    pattern = re.compile(rf'{re.escape(base_name)}-(\d+)\.txt$')
    max_number = -1
    os.makedirs(folder_path, exist_ok=True)

    for filename in os.listdir(folder_path):
        match = pattern.match(filename)
        if match:
            number = int(match.group(1))
            if number > max_number:
                max_number = number

    next_number = max_number + 1
    return next_number

def write_rectangles_to_file(rectangles, sceneWidth, SceneHeight, dir, filepath="rectangles.txt"):
    with open(filepath, "w") as f:
        f.write(f"SceneWidth: {sceneWidth}\n")
        f.write(f"SceneHeight: {SceneHeight}\n")
        f.write(f"RectCount: {len(rectangles)}\n")
        for i, r in enumerate(rectangles):
            f.write(f"Rect: {i}:\n")
            f.write(f"  color: {r['color']}\n")
            f.write(f"  min: {r['min']}\n")
            f.write(f"  max: {r['max']}\n")
            filename = check_if_exists(r['width'], r['height'], dir)
            if filename == -1 or get_next_number(dir+"building_blocks", str(r['width'])+"x"+str(r['height'])) <2:
                wektoruj(r['width'], r['height'], tuple(int(r['color'][i:i+2], 16) for i in (0, 2, 4)), dir)
            f.write(f"  file: {check_if_exists(r['width'], r['height'], dir)}\n")
def createScene(png_name, scene_name, objects_filename):
    filename = png_name
    rectangles = find_rectangles(filename + ".png")
    width, height = Image.open(filename + ".png").size
    rfct_dir = "C:/Users/Natal/Documents/games/reflect/assets/"
    write_rectangles_to_file(rectangles, width, height, rfct_dir,  rfct_dir+"scenes/" + scene_name +".txt")

    with open(objects_filename+".txt", 'r') as src_file:
        content = src_file.read()
    with open(rfct_dir+"scenes/" + scene_name +".txt", 'a') as dest_file:
        dest_file.write(content)
try:
    createScene(sys.argv[1], sys.argv[3], sys.argv[2])
except Exception as e:
    print(e)