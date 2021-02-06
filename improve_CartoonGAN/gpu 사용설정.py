import tensorflow as tf
device_name = tf.test.gpu_device_name()  # gpu 이름 설정
# print(device_name)

with tf.device(device_name):
    hello = tf.constant("hello, world!")
    print(hello)