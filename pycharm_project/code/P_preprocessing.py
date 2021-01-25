# 다른 파일의 함수들 import
from P_crop import crop
from P_edge_smoothing import edge_smoothing
from P_resizing import resizing

def preprocessing(typeOfImage="photo", image_path="", crop_path="", edge_smoothing_path="", resizing_path=""):
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

if __name__ == "__main__":
    # 만화 이미지일 경우
    original_size = preprocessing(typeOfImage="cartoon", image_path="C:/Users/USER/Desktop/CartoonGAN_pycharm/data/cartoon_img/shrek", crop_path="C:/Users/USER/Desktop/CartoonGAN_pycharm/data/cartoon_img_crop/shrek", edge_smoothing_path="C:/Users/USER/Desktop/CartoonGAN_pycharm/data/cartoon_img_edge_smoothing/shrek", resizing_path="")

    # 사진일 경우
    # original_size = preprocessing(typeOfImage="photo", image_path="", crop_path="", resizing_path="")
