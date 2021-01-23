import os, sys, cv2, PIL
import matplotlib.pyplot as plt
from matplotlib.image import imread
from PIL import Image
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras import layers
from tensorflow.keras.layers import Input, Conv2D, BatchNormalization, Activation, Dropout, ReLU, Softmax, LeakyReLU, UpSampling2D, Conv2DTranspose
from tensorflow.keras.models import Model
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.metrics import Accuracy, CategoricalCrossentropy, MeanSquaredError
from tensorflow.keras.optimizers import Adam, Optimizer, RMSprop, SGD
from tensorflow.keras.regularizers import l1, l2
from tensorflow.keras.applications.vgg19 import VGG19, preprocess_input, decode_predictions
from tensorflow.keras.callbacks import ModelCheckpoint
import flickrapi
import requests
from io import BytesIO
from datauri import DataURI
import json

import 01_crop
crop(dir1)