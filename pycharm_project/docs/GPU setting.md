# window 10 tensorflow-gpu 환경 설정
- anaconda prompt
    - 참고 : tf_GPU : 냬가 설정한 가상환경 이름
    - conda create -n tf_GPU python==3.7
    - conda activate tf_GPU
    - conda install tensorflow-gpu==2.0.0



- CUDA toolkit 10.0 버전 설치
    - 다운로드 링크 : https://developer.nvidia.com/cuda-toolkit-archive



- cuDNN 7.4.2 for CUDA 10.0 버전 설치
    - 다운로드 링크 : https://developer.nvidia.com/rdp/cudnn-archive   
    - 로그인 후 다운로드
    - zip 파일 압축해제 후 bin, include, lib 폴더를
    - C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0
    - 디렉터리에 덮어씌우기
    - 참고 : 해당 디렉토리는 위의 CUDA toolkit 을 설치한 디렉토리임



- 시스템 환경 변수 설정
    - tf_GPU(C:\Users\USER\anaconda3\envs\tf_GPU)
    - CUDA_PATH (C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0)
    - CUDA_PATH_V10_0 (C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0)
    - 추가하기
    


- pycharm python interpreter 설정
    - pycharm settings
    - Project: CartoonGAN_pycharm
    - Python Interpreter
    - Existing environment
    - Interpreter: C:\Users\USER\anaconda3\envs\tf_GPU\python.exe
        - 참고 : 이 디렉토리 위치는 anaconda 가상환경 속의 python
    - Python 3.7 (tf_GPU) C:\Users\USER\anaconda3\envs\tf_GPU-python.exe 로 뜨는 지 확인



- pycharm 껐다가 다시 켜고 pycharm Terminal에서 PATH 설정
    - SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\bin;%PATH%
    - SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\extras\CUPTI\libx64;%PATH%
    - SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\include;%PATH%
    - SET PATH=C:\tools\cuda\bin;%PATH%


- 참고 사항
    - tensorflow-gpu, CUDA, cuDNN 버전은 서로 호환이 되는 버전으로 설치해야한다.
    - 버전 확인 링크 : https://www.tensorflow.org/install/source_windows#tested_build_configurations
    - GPU 사용중인지 확인하는 코드 확인 -> useGPUtest.py 확인
    - 사진 참고 -> docs/GPU 설정완료 확인 모습.png 참고


