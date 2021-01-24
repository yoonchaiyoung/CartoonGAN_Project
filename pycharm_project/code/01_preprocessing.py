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

    for imageName in imageName_list[0]:
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

def preprocessing(typeOfImage, image_path="", crop_path="", edge_smoothing_path="", resizing_path=""):
    """
    ------------------------------------------------------
    파라미터 설명
    ------------------------------------------------------
    typeOfImage : 사진 or 만화 이미지(photo or cartoon 입력)
    image_path : 이미지가 저장되어있는 디렉토리 위치
    ------------------------------------------------------
    함수 설명
    ------------------------------------------------------
    return 할 것들
    - 전처리 작업이 끝난 이미지(resizing된 사진, 엣지 smoothing이 된 만화 이미지)
    - original_size : 원본 이미지(후에 web에 올라가는 generator에서 이미지 resizing을 거친 후 다시 원본 사이즈로 돌려주어야하기 때문)
    """
    if typeOfImage == "photo":
        # 사진 -> resizing
        original_size = resizing(image_path, resizing_path)

        print("사진 전처리 작업 완료")
        print("원본 사진 -> resizing된 사진")

        return original_size
    elif typeOfImage == "cartoon":
        # 만화 이미지 -> crop -> edge_smoothing
        crop(image_path, crop_path)
        edge_smoothing(crop_path, edge_smoothing_path)

        print("만화 이미지 전처리 작업 완료")
        print("원본 만화 이미지 -> 엣지 smoothing된 만화 이미지")

if __name__ == "main":
    # 만화 이미지일 경우
    original_size = preprocessing(typeOfImage="cartoon", image_path="C:/Users/USER/Desktop/CartoonGAN_pycharm/data/cartoon_img/슈렉", crop_path="C:/Users/USER/Desktop/CartoonGAN_pycharm/data/cartoon_img_crop/슈렉", edge_smoothing_path="C:/Users/USER/Desktop/CartoonGAN_pycharm/data/cartoon_img_edge_smoothing/슈렉")

    # 사진일 경우
    # original_size = preprocessing(typeOfImage="photo", image_path="", crop_path="", resizing_path="")
