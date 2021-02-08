"""
credit to https://github.com/taki0112/CartoonGAN-Tensorflow/blob/master/edge_smooth.py
LICENSE for this script: https://github.com/taki0112/CartoonGAN-Tensorflow/blob/master/LICENSE
"""
import os
import numpy as np
import cv2
from glob import glob
from tqdm import tqdm

import tensorflow as tf
os.environ["CUDA_VISIBLE_DEVICES"] = '0'

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session (config = config)

def make_edge_smooth(path):
    file_list = glob(os.path.expanduser(os.path.join(path, 'trainB', '*')))
    save_dir = os.path.expanduser(os.path.join(path, 'trainB_smooth'))
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    kernel_size = 5
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    gauss = cv2.getGaussianKernel(kernel_size, 0)
    gauss = gauss * gauss.transpose(1, 0)

    for f in tqdm(file_list):
        file_name = os.path.basename(f)

        bgr_img = cv2.imread(f)
        gray_img = cv2.imread(f, 0)
        pad_img = np.pad(bgr_img, ((2, 2), (2, 2), (0, 0)), mode='reflect')
        edges = cv2.Canny(gray_img, 100, 200)
        dilation = cv2.dilate(edges, kernel)

        gauss_img = np.copy(bgr_img)
        idx = np.where(dilation != 0)
        for i in range(np.sum(dilation != 0)):
            gauss_img[idx[0][i], idx[1][i], 0] = np.sum(np.multiply(
                pad_img[idx[0][i]:idx[0][i] + kernel_size, idx[1][i]:idx[1][i] + kernel_size, 0],
                gauss))
            gauss_img[idx[0][i], idx[1][i], 1] = np.sum(np.multiply(
                pad_img[idx[0][i]:idx[0][i] + kernel_size, idx[1][i]:idx[1][i] + kernel_size, 1],
                gauss))
            gauss_img[idx[0][i], idx[1][i], 2] = np.sum(np.multiply(
                pad_img[idx[0][i]:idx[0][i] + kernel_size, idx[1][i]:idx[1][i] + kernel_size, 2],
                gauss))

        cv2.imwrite(os.path.join(save_dir, file_name), gauss_img)


def main(path):
    make_edge_smooth(path)

# def make_edge_smooth(path):
#     crop_path = path + '/' + 'trainB' + '*'
#     edge_smoothing_path = path + 'trainB_smooth'
#
#     # crop된 이미지 파일명을 담은 리스트 생성
#     cropImageName_list = os.listdir(crop_path)
#
#     # edge smoothing된 이미지를 저장할 디렉토리 생성 : 디렉토리가 없으면 생성, 디렉토리가 존재하면 아무것도 하지 않음.
#     os.makedirs(edge_smoothing_path, exist_ok=True)
#
#     for cropImageName in cropImageName_list:
#         img_bgr = cv2.imread(crop_path + '/' + cropImageName)  # OpenCV는 이미지를 저장할 때 색상을 BGR 순서로 저장 -> RGB로 바꿔주어야 함
#         img_gray = cv2.imread(crop_path + '/' + cropImageName, 0)
#         img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
#
#         # 1. canny edge detector로 엣지 검출
#         edges = cv2.Canny(img_gray, 100, 200)
#
#         # 2. 엣지 영역 확장(dilation)
#         # dilation용 커널 생성
#         dilation_kernel = np.ones((5, 5), np.uint8)
#
#         # 엣지 영역 확장
#         dilation = cv2.dilate(edges, dilation_kernel)
#
#         # 3. gaussian filter를 이용하여 엣지 smoothing
#         # 이미지 패딩(padding)
#         img_padding = np.pad(img, ((2, 2), (2, 2), (0, 0)), mode="reflect")
#
#         # 엣지 영역 index
#         idx = np.where(dilation != 0)
#
#         # gaussian kernel 1D 생성
#         # cv2.getGaussianKernel(커널 사이즈, sigma)
#         gaussian1D = cv2.getGaussianKernel(5, 0)
#
#         # gaussian kernel 2D 생성 : gaussian filter 1D를 외적
#         # np.outer(가우시안 1D 커널, 가우시안 1D 커널.transpose())
#         gaussian2D = np.outer(gaussian1D, gaussian1D.transpose())
#
#         # 엣지 smoothing할 이미지 : 원본 이미지 복사
#         img_edge_smoothing = np.copy(img)
#
#         # 패딩한 이미지, 가우시안 2D 커널 합성곱
#         for i in range(np.sum(dilation != 0)):
#             img_edge_smoothing[idx[0][i], idx[1][i], 0] = np.sum(np.multiply(img_padding[idx[0][i]: idx[0][i] + 5,
#                                                                              idx[1][i]: idx[1][i] + 5,
#                                                                              0],
#                                                                              gaussian2D))
#             img_edge_smoothing[idx[0][i], idx[1][i], 1] = np.sum(np.multiply(img_padding[idx[0][i]: idx[0][i] + 5,
#                                                                              idx[1][i]: idx[1][i] + 5,
#                                                                              1],
#                                                                              gaussian2D))
#             img_edge_smoothing[idx[0][i], idx[1][i], 2] = np.sum(np.multiply(img_padding[idx[0][i]: idx[0][i] + 5,
#                                                                              idx[1][i]: idx[1][i] + 5,
#                                                                              2],
#                                                                              gaussian2D))
#
#         # 엣지 smoothing한 사진 저장
#         # OpenCV는 이미지를 저장할 때 색상을 BGR 순서로 저장 -> RGB로 바꿔주어야 함
#         cv2.imwrite(os.path.join(edge_smoothing_path, cropImageName[0:-4] + "_edge_smoothing" + '.png'),
#                     cv2.cvtColor(img_edge_smoothing, cv2.COLOR_BGR2RGB))
#
#     print("엣지 smoothing된 사진 저장 완료")

def main(path):
    make_edge_smooth(path)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, help='path to your dataset')
    args = parser.parse_args()
    main(args.path)
