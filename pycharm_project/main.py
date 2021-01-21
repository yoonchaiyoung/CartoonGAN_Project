

# 실행 코드
if __name__ == "__main__":
    import os, sys, cv2, PIL
    import matplotlib.pyplot as plt
    from matplotlib.image import imread
    from PIL import Image
    import numpy as np
    import tensorflow as tf
    from keras import layers
    from keras.layers import Input, Conv2D, BatchNormalization, Activation, Dropout, ReLU, Softmax, LeakyReLU, UpSampling2D, Conv2DTranspose
    from keras.models import Model
    from keras.losses import BinaryCrossentropy
    from keras.metrics import Accuracy, CategoricalCrossentropy, MeanSquaredError
    from keras.optimizers import Adam, Optimizer, RMSprop, SGD
    from keras.regularizers import l1, l2
    from keras.applications.vgg19 import VGG19, preprocess_input, decode_predictions
    from tensorflow.keras.callbacks import ModelCheckpoint
    import flickrapi
    import requests
    from io import BytesIO
    from datauri import DataURI
    import json



    print("정상작동")
    print(np.array([0, 0]))
    print(tf.__version__)
    from tensorflow.python.client import device_lib
    print(device_lib.list_local_devices())
    import tensorflow as tf
    tf.debugging.set_log_device_placement(True)


