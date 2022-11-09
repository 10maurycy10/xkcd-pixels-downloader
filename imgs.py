"""
XKCD "pixels" #1416 Downloader

A script to download ever image from xkcd #1416 "pixels".
"""
import requests
import json
import time
import zipfile
from PIL import Image
import io
import tqdm

ImgEndpoint = "https://imgs.xkcd.com/"
DataEndpoint = 'https://c.xkcd.com/turtle/'
output = "turtles.zip"

def get_img_url(imgid):
    return f"{ImgEndpoint}turtledown/{imgid}-tiled.png"

def get_data_url(imgid):
    return f"{DataEndpoint}{imgid}"


################################
# Enumerate all images         #
################################

print("* Enumerating Images")

found_imgs = []
queue = ["evolution"]

def add_img(imgid):
    if imgid in queue or imgid in found_imgs:
        return
    queue.append(imgid)
    found_imgs.append(imgid)

while len(queue) > 0:
    current = queue.pop()
    url = get_data_url(current)
    print(url)
    get = requests.get(url)
    get.raise_for_status()
    img_json = get.json()
    for imgid in (img_json["white"] + img_json["black"]):
        add_img(imgid)
    time.sleep(0.25)

print("Found ",len(found_imgs), " Images")

#######################
# Downlowd all images #
#######################

def resize(img):

    img = Image.open(io.BytesIO(img))
    img = img.crop(box=(0,0,600,600))
    output = io.BytesIO()
    img.save(output, format='PNG')
    return output.getvalue()

print("* Downloading images")

with zipfile.ZipFile(output, 'w') as outzip:
    for imgid in tqdm.tqdm(found_imgs):
        r = requests.get(get_img_url(imgid))
        r.raise_for_status()
        with outzip.open(f"{imgid}.png", "w", force_zip64=True) as inzip:
            inzip.write(resize(r.content))
        time.sleep(0.25)

