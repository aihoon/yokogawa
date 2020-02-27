import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' #surpress tensorflow log

import ssl
ssl._create_default_https_context = ssl._create_unverified_context #for ignore TLS verify

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, MobileNetV2
import numpy as np
import tensorflow as tf
from sample_utils import *

classes = load_class_labels("imagenet_classes.txt")

model = MobileNetV2(weights='imagenet', include_top=True)

print("loading model has completed")

for img_path in get_image_pathes("classification_images"):
    print("file: %s"%img_path)

    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    infer_time = performance_count()

    features = model.predict(x)

    print("  infer time: %f[ms]"%convert_to_ms(performance_count() - infer_time))

    print("  class label: " + classes[features[0].argmax()])