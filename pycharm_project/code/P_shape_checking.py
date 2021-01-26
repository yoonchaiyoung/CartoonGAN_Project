import os, cv2
import numpy as np

def shape_checking(movie_name):
    file_path = 'C:/Users/USER/Desktop/CartoonGAN_pycharm/data/cartoon_img/' + movie_name
    fileName_list = os.listdir(file_path)
    img_bgr = cv2.imread(file_path + '/' + fileName_list[0])
    print("{} 이미지의 shape : {}".format(movie_name, img_bgr.shape))
    return img_bgr.shape

coco = shape_checking("coco")
frozen2 = shape_checking("frozen2")
minions = shape_checking("minions")
ponyo = shape_checking("ponyo")
shrek = shape_checking("shrek")

print(min(coco, frozen2, minions, ponyo, shrek))

# ponyo의 이미지 사이즈인 336x640이 제일 작은 사이즈
# 나머지는 1000x1920의 언저리 사이즈

# ponyo 이미지 -> 기존 방식대로 3개 crop(맨왼쪽위, 가운데, 맨오른쪽아래)
# 나머지 애니메이션 이미지 -> 가운데 부분(가로와 세로를 4등분했을 때 가운데 2칸씩)에서 random crop으로 5장 crop하기
