# 라이브러리 import
import os
import sys
import cv2
import PIL
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
from tensorflow.keras.callbacks import ModelCheckpoint
from keras.activations import sigmoid
import pickle

def resizing(image_path, resizing_path):
    """
    ------------------------------------------------
    파라미터 설명

    img_path : resizing 해줄 이미지 디렉토리 위치
    resizing_path : resizing된 이미지를 저장할 디렉토리 위치
    ------------------------------------------------
    함수 설명

    resizing할 사이즈를 변경하려면 dsize=(300, 300) 부분을 바꾸면 된다.
    ------------------------------------------------
    """
    # 이미지 파일명을 담은 리스트 생성
    imageName_list = os.listdir(image_path)

    # resizing된 이미지를 저장할 디렉토리 생성 : 디렉토리가 없으면 생성, 디렉토리가 존재하면 아무것도 하지 않음.
    os.makedirs(resizing_path, exist_ok=True)

    for imageName in imageName_list:
        img_bgr = cv2.imread(image_path + '/' + imageName)
        img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

        original_size = img.shape  # 원본 이미지의 shape 저장 -> 후에 원본 크기로 돌려줄 때 필요함

        # 이미지 300x300 사이즈로 resizing
        img_resizing = cv2.resize(img, dsize=(300, 300), interpolation=cv2.INTER_LINEAR)

        # resizing한 이미지 저장
        cv2.imwrite(os.path.join(resizing_path, imageName[0:-4] + '_resizing' + '.png'),
                    cv2.cvtColor(img_resizing, cv2.COLOR_BGR2RGB))

    print("resizing된 사진 저장 완료")

    return original_size