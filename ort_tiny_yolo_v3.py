import onnxruntime
import numpy as np
import onnxruntime.backend as backend
import numpy as np
from PIL import Image, ImageDraw
from sample_utils import *

def letterbox_image(image, size):
    '''resize image with unchanged aspect ratio using padding'''
    iw, ih = image.size
    w, h = size
    scale = min(w/iw, h/ih)
    nw = int(iw*scale)
    nh = int(ih*scale)

    image = image.resize((nw,nh), Image.BICUBIC)
    new_image = Image.new('RGB', size, (128,128,128))
    new_image.paste(image, ((w-nw)//2, (h-nh)//2))
    return new_image

def preprocess(img):
    model_image_size = (416, 416)
    boxed_image = letterbox_image(img, tuple(reversed(model_image_size)))
    image_data = np.array(boxed_image, dtype='float32')
    image_data /= 255.
    image_data = np.transpose(image_data, [2, 0, 1])
    image_data = np.expand_dims(image_data, 0)
    return image_data

# main

input_dir = 'object_detection_images'
output_dir = 'outputs_ort_yolo'

print("device: %s" % onnxruntime.get_device())

model = onnxruntime.InferenceSession('model/tiny-yolov3-11.onnx')
sess = backend.prepare(model)

classes = load_class_labels("coco_classes.txt")

for image_path in get_image_pathes(input_dir):
    print("*** image: %s ***"%image_path)

    # load input image
    load_time = performance_count()

    image = Image.open(image_path)
    image_data = preprocess(image)
    image_size = np.array([image.size[1], image.size[0]], dtype=np.float32).reshape(1, 2)
    inputs = [image_data, image_size]

    load_time = convert_to_ms(performance_count() - load_time)

    # execute inference
    infer_time = performance_count()

    results = sess.run(inputs)

    infer_time = convert_to_ms(performance_count() - infer_time)

    print(" performance: image_load: %.0f[ms] infer: %.0f[ms]"%(load_time, infer_time))

    # output results
    boxes = results[0]
    scores = results[1]
    indices = results[2][0]

    bbox_text = []
    for idx_ in indices:
        print("  class: %s"%classes[idx_[1]])
        print("    score: %s"%scores[tuple(idx_)])
        idx_1 = (idx_[0], idx_[2])
        print("    bbox: %s"%boxes[idx_1])
        bbox_text.append((boxes[idx_1], classes[idx_[1]] + ": " + str(scores[tuple(idx_)])))

    draw_bboxes_with_texts(image, bbox_text)

    image.save(str(image_path).replace(input_dir, output_dir).replace('.', '_bbox.'))