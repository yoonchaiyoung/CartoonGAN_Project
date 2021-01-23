import tensorflow as tf
# tensorflow가 잘 깔렸는 지 확인
print('tensorflow가 지금 깔린 버전 : ', tf.__version__)

# gpu를 사용하고 있는 지 확인한다.
from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())

