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

def edge_smoothing(crop_path, edge_smoothing_path):
    """
    -----------------------------------------
    파라미터 설명
    crop_path : crop된 사진이 있는 디렉토리 위치
    edge_smoothing_path : edge smoothing을 한 사진을 넣을 디렉토리 위치
    -----------------------------------------
    함수 설명
    -----------------------------------------
    """
    # crop된 이미지 파일명을 담은 리스트 생성
    cropImageName_list = os.listdir(crop_path)

    # edge smoothing된 이미지를 저장할 디렉토리 생성 : 디렉토리가 없으면 생성, 디렉토리가 존재하면 아무것도 하지 않음.
    os.makedirs(edge_smoothing_path, exist_ok=True)

    for cropImageName in cropImageName_list:
        img_bgr = cv2.imread(crop_path + '/' + cropImageName)  # OpenCV는 이미지를 저장할 때 색상을 BGR 순서로 저장 -> RGB로 바꿔주어야 함
        img_gray = cv2.imread(crop_path + '/' + cropImageName, 0)
        img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

        # 1. canny edge detector로 엣지 검출
        edges = cv2.Canny(img_gray, 100, 200)

        # 2. 엣지 영역 확장(dilation)
        # dilation용 커널 생성
        dilation_kernel = np.ones((5, 5), np.uint8)

        # 엣지 영역 확장
        dilation = cv2.dilate(edges, dilation_kernel)

        # 3. gaussian filter를 이용하여 엣지 smoothing
        # 이미지 패딩(padding)
        img_padding = np.pad(img, ((2, 2), (2, 2), (0, 0)), mode="reflect")

        # 엣지 영역 index
        idx = np.where(dilation != 0)

        # gaussian kernel 1D 생성
        # cv2.getGaussianKernel(커널 사이즈, sigma)
        gaussian1D = cv2.getGaussianKernel(5, 0)

        # gaussian kernel 2D 생성 : gaussian filter 1D를 외적
        # np.outer(가우시안 1D 커널, 가우시안 1D 커널.transpose())
        gaussian2D = np.outer(gaussian1D, gaussian1D.transpose())

        # 엣지 smoothing할 이미지 : 원본 이미지 복사
        img_edge_smoothing = np.copy(img)

        # 패딩한 이미지, 가우시안 2D 커널 합성곱
        for i in range(np.sum(dilation != 0)):
            img_edge_smoothing[idx[0][i], idx[1][i], 0] = np.sum(np.multiply(img_padding[idx[0][i]: idx[0][i] + 5,
                                                                             idx[1][i]: idx[1][i] + 5,
                                                                             0],
                                                                             gaussian2D))
            img_edge_smoothing[idx[0][i], idx[1][i], 1] = np.sum(np.multiply(img_padding[idx[0][i]: idx[0][i] + 5,
                                                                             idx[1][i]: idx[1][i] + 5,
                                                                             1],
                                                                             gaussian2D))
            img_edge_smoothing[idx[0][i], idx[1][i], 2] = np.sum(np.multiply(img_padding[idx[0][i]: idx[0][i] + 5,
                                                                             idx[1][i]: idx[1][i] + 5,
                                                                             2],
                                                                             gaussian2D))

        # 엣지 smoothing한 사진 저장
        # OpenCV는 이미지를 저장할 때 색상을 BGR 순서로 저장 -> RGB로 바꿔주어야 함
        cv2.imwrite(os.path.join(edge_smoothing_path, cropImageName[0:-4] + "_edge_smoothing" + '.png'),
                    cv2.cvtColor(img_edge_smoothing, cv2.COLOR_BGR2RGB))

    print("엣지 smoothing된 사진 저장 완료")