import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv2D, Activation
from layers3 import FlatConv_3, ConvBlock_3, ResBlock_3, UpSampleConv_3
from layers3 import get_padding, DownShuffleUnitV2_3, BasicShuffleUnitV2_3


class Generator3(Model):
    def __init__(self,
                 # norm_type="instance",
                 gp_num=3003,  # 여기도 문제가 아니군
                 pad_type="constant",
                 base_filters=64,
                 num_resblocks=8,
                 light=False):
        super(Generator3, self).__init__(name="Generator3")
        if light:
            downconv = DownShuffleUnitV2_3
            resblock = BasicShuffleUnitV2_3
            base_filters += 32
            end_ksize = 5
        else:
            downconv = ConvBlock_3
            resblock = ResBlock_3
            end_ksize = 7
        upconv = UpSampleConv_3
        self.flat_conv1 = FlatConv_3(filters=base_filters,
                                   kernel_size=end_ksize,
                                   # norm_type=norm_type,
                                   gp_num=3,
                                   pad_type=pad_type)
        self.down_conv1 = downconv(mid_filters=base_filters,
                                   filters=base_filters * 2,
                                   kernel_size=3,
                                   gp_num=64,
                                   stride=2,
                                   # norm_type=norm_type,
                                   pad_type=pad_type)
        self.down_conv2 = downconv(mid_filters=base_filters,
                                   filters=base_filters * 4,
                                   kernel_size=3,
                                   stride=2,
                                   gp_num=128,
                                   # norm_type=norm_type,
                                   pad_type=pad_type)
        self.residual_blocks = tf.keras.models.Sequential([
            resblock(
                filters=base_filters * 4,
                kernel_size=3,
                gp_num=256) for _ in range(num_resblocks)])
        self.up_conv1 = upconv(filters=base_filters * 2,
                               kernel_size=3,
                               # norm_type=norm_type,
                               gp_num=64,
                               pad_type=pad_type,
                               light=light)
        self.up_conv2 = upconv(filters=base_filters,
                               kernel_size=3,
                               # norm_type=norm_type,
                               pad_type=pad_type,
                               gp_num=32,
                               light=light)

        end_padding = (end_ksize - 1) // 2
        end_padding = (end_padding, end_padding)
        self.final_conv = tf.keras.models.Sequential([
            get_padding(pad_type, end_padding),
            Conv2D(3, end_ksize)])
        self.final_act = Activation("tanh")

    def build(self, input_shape):
        super(Generator3, self).build(input_shape)

    def call(self, x, training=False):
        x = self.flat_conv1(x, training=training)
        x = self.down_conv1(x, training=training)
        x = self.down_conv2(x, training=training)
        x = self.residual_blocks(x, training=training)
        x = self.up_conv1(x, training=training)
        x = self.up_conv2(x, training=training)
        x = self.final_conv(x)
        x = self.final_act(x)
        return x

    def compute_output_shape(self, input_shape):
        return tf.TensorShape(input_shape)


if __name__ == "__main__":
    import numpy as np
    f = 3
    k = 3
    s = (1, 64, 64, 3)
    nx = np.random.rand(*s).astype(np.float32)

    custom_layers = [
        FlatConv_3(f, k),
        ConvBlock_3(f, k),
        ResBlock_3(f, k),
        UpSampleConv_3(f, k)
    ]

    for layer in custom_layers:
        tf.keras.backend.clear_session()
        out = layer(nx)
        layer.summary()
        print(f"Input  Shape: {nx.shape}")
        print(f"Output Shape: {out.shape}")
        print("\n" * 2)

    tf.keras.backend.clear_session()
    g3 = Generator3()
    shape = (1, 256, 256, 3)
    nx = np.random.rand(*shape).astype(np.float32)
    t = tf.keras.Input(shape=nx.shape[1:], batch_size=nx.shape[0])
    out = g3(t, training=False)
    g3.summary()
    print(f"Input  Shape: {nx.shape}")
    print(f"Output Shape: {out.shape}")
    assert out.shape == shape, "Output shape doesn't match input shape"
    print("Generator's output shape is exactly the same as shape of input.")
