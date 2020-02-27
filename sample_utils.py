from PIL import Image, ImageDraw
from pathlib import Path
from datetime import datetime

def performance_count():
    dt  = datetime.now()
    return  (dt.minute * 60 + dt.second) * 1000000 + dt.microsecond

def convert_to_ms(pfm_count):
    return pfm_count/1000

def get_image_pathes(dir_path):
    p = Path(dir_path)
    img_paths = []
    for ext in ['jpg', 'jpeg', 'JPG', 'JPEG']:
        img_paths.extend(list(p.glob('**/*.' + ext)))
    return sorted(img_paths)

def draw_bboxes_with_texts(image, bbox_text):
    for bbox, text in bbox_text:
        draw = ImageDraw.Draw(image)
        text_w, text_h = draw.textsize(text)
        draw.rectangle((bbox[1], bbox[0], bbox[3], bbox[2]), outline=(255,0,0))
        draw.rectangle((bbox[1], bbox[0], bbox[1]+text_w, bbox[0]+text_h), fill=(255,0,0))
        draw.text((bbox[1], bbox[0]),text, fill=(255,255,255))

def load_class_labels(filename):
    with open(filename, 'r') as f:
        classes =  [l[:-1] for l in f]
    return classes