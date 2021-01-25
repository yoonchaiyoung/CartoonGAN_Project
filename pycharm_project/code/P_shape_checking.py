import os, cv2
import matplotlib.pyplot as plt

def shape_checking(movie_name):
    file_path = 'C:/Users/USER/Desktop/CartoonGAN_pycharm/data/cartoon_img/' + movie_name
    fileName_list = os.listdir(file_path)
    img_bgr = cv2.imread(file_path + '/' + fileName_list[0])
    print("{} 이미지의 shape : {}".format(movie_name, img_bgr.shape))

shape_checking("coco")
shape_checking("frozen2")
shape_checking("minions")
shape_checking("ponyo")
shape_checking("shrek")