def change_file_name_simply(file_path, change_path, front_name, digits_num):
    """
    file_path : 이름을 변경할 파일이 있는 디렉토리 위치
    change_path : 이름변경한 파일을 저장할 디렉토리 위치 (만일 현재 디렉토리로 하고 싶다면 file_path와 동일한 디렉토리 경로 입력)
    front_name : 파일 맨 앞에 붙여주고 싶은 문자열
    digits_num : 자리수
    """
    import os
    fileName_list = os.listdir(file_path)
    for idx, name in enumerate(fileName_list):
        file_src = os.path.join(file_path, name)
        changeName = front_name + "_" + str(idx + 1).zfill(digits_num) + ".png"
        # zfill : 숫자의 자릿수를 맞추기 위해 앞에 0을 붙여준다.
        change_file_src = os.path.join(change_path, changeName)
        os.rename(file_src, change_file_src)

change_file_name_simply(file_path="C:/Users/USER/Desktop/CartoonGAN_pycharm/data/cartoon_img/frozen2",
                        change_path="C:/Users/USER/Desktop/CartoonGAN_pycharm/data/cartoon_img/frozen2",
                        front_name="frozen2",
                        digits_num=5)