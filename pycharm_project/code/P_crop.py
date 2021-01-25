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

def crop(image_path, crop_path):
    """
    ------------------------------------------------
    파라미터 설명
    image_path : 이미지 파일이 있는 디렉토리 위치
    crop_path : crop된 이미지를 넣을 디렉토리 위치
    ------------------------------------------------
    함수 설명

    이미지 불러와서 crop한 이미지 저장
    나중에는 이미지 return 하는걸로 바꾸기
    ------------------------------------------------
    """

    # 이미지 파일명을 담은 리스트 생성
    imageName_list = os.listdir(image_path)

    # crop된 이미지를 저장할 디렉토리 생성 : 디렉토리가 없으면 생성, 디렉토리가 존재하면 아무것도 하지 않음.
    os.makedirs(crop_path, exist_ok=True)

    for imageName in imageName_list:
        img_bgr = cv2.imread(image_path + '/' + imageName)  # OpenCV는 이미지를 저장할 때 색상을 BGR 순서로 저장 -> RGB로 바꿔주어야 함
        img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

        # 맨 왼쪽위부터 300x300 crop
        img_left_crop = img[0:0 + 300, 0:0 + 300]

        # 가운데 300x300 crop
        img_middle_crop = img[int(img.shape[0] / 2) - 150:int(img.shape[0] / 2) + 150,
                          int(img.shape[1] / 2) - 150:int(img.shape[1] / 2) + 150]

        # 맨 오른쪽 아래부터 300x300 crop
        img_right_crop = img[img.shape[0] - 300:img.shape[0], img.shape[1] - 300:img.shape[1]]

        # crop한 사진 저장  # OpenCV는 이미지를 저장할 때 색상을 BGR 순서로 저장 -> RGB로 바꿔주어야 함
        cv2.imwrite(os.path.join(crop_path, imageName[0:-4] + '_left_crop' + '.png'),
                    cv2.cvtColor(img_left_crop, cv2.COLOR_BGR2RGB))
        cv2.imwrite(os.path.join(crop_path, imageName[0:-4] + '_middle_crop' + '.png'),
                    cv2.cvtColor(img_middle_crop, cv2.COLOR_BGR2RGB))
        cv2.imwrite(os.path.join(crop_path, imageName[0:-4] + '_right_crop' + '.png'),
                    cv2.cvtColor(img_right_crop, cv2.COLOR_BGR2RGB))

    print("crop된 사진 저장 완료")
