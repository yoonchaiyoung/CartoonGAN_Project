import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Layer, InputSpec, DepthwiseConv2D
from tensorflow.keras.layers import Conv2D, BatchNormalization, Add
from tensorflow.keras.layers import ReLU, LeakyReLU, ZeroPadding2D
from keras_contrib.layers import InstanceNormalization
from tensorflow_addons.layers import WeightNormalization, InstanceNormalization, SpectralNormalization, GroupNormalization
from switchnorm import SwitchNormalization


def channel_shuffle_2(x):
    dyn_shape = tf.shape(x)
    h, w = dyn_shape[1], dyn_shape[2]
    c = x.shape[3]
    x = K.reshape(x, [-1, h, w, 2, c // 2])
    x = K.permute_dimensions(x, [0, 1, 2, 4, 3])
    x = K.reshape(x, [-1, h, w, c])
    return x


class ReflectionPadding2D_3(Layer):
    def __init__(self, padding=(1, 1), **kwargs):
        super(ReflectionPadding2D_3, self).__init__(**kwargs)
        padding = tuple(padding)
        self.padding = ((0, 0), padding, padding, (0, 0))
        self.input_spec = [InputSpec(ndim=4)]

    def compute_output_shape(self, s):
        """ If you are using "channels_last" configuration"""
        return s[0], s[1] + 2 * self.padding[0], s[2] + 2 * self.padding[1], s[3]

    def call(self, x):
        return tf.pad(x, self.padding, "REFLECT")


def get_padding(pad_type, padding):
    if pad_type == "reflect":
        return ReflectionPadding2D_3(padding)
    elif pad_type == "constant":
        return ZeroPadding2D(padding)
    else:
        raise ValueError(f"Unrecognized pad_type {pad_type}")


# def get_norm(norm_type):
#     if norm_type == "instance":
#         return InstanceNormalization()
#     elif norm_type == 'batch':
#         return BatchNormalization()
#
#     elif norm_type == "weight":
#         return WeightNormalization()
#
#     elif norm_type == "spectral":
#         return SpectralNormalization()
#
#     elif norm_type == "switch":
#         return SwitchNormalization()
#
#     elif norm_type == "group":
#         return GroupNormalization()
#
#     else:
#         raise ValueError(f"Unrecognized norm_type {norm_type}")


class FlatConv_3(Model):
    def __init__(self,
                 filters,
                 kernel_size,
                 # norm_type="group",
                 gp_num=3,
                 pad_type="constant",
                 **kwargs):
        super(FlatConv_3, self).__init__(name="FlatConv_3")
        padding = (kernel_size - 1) // 2
        padding = (padding, padding)
        self.model = tf.keras.models.Sequential()
        self.model.add(get_padding(pad_type, padding))

        self.model.add(GroupNormalization(groups=gp_num, axis=-1))  # 추가

        self.model.add(WeightNormalization(Conv2D(filters, kernel_size, activation='relu')))
        # self.model.add(Conv2D(filters, kernel_size))
        # self.model.add(get_norm(norm_type))
        # self.model.add(ReLU())

    def build(self, input_shape):
        super(FlatConv_3, self).build(input_shape)

    def call(self, x, training=False):
        return self.model(x, training=training)


class BasicShuffleUnitV2_3(Model):
    def __init__(self,
                 filters,  # NOTE: will be filters // 2
                 # norm_type="group",
                 pad_type="constant",
                 gp_num=3000,  # 여기가 문제가 아니군
                 **kwargs):
        # super(BasicShuffleUnitV2_3, self).__init__(name="BasicShuffleUnitV2_3")
        super(BasicShuffleUnitV2_3, self).__init__()
        filters //= 2
        self.model = tf.keras.models.Sequential([
            GroupNormalization(groups=gp_num, axis=-1),  # 추가
            WeightNormalization(Conv2D(filters, 1, use_bias=False, activation='relu')),
            # Conv2D(filters, 1, use_bias=False),
            # get_norm(norm_type),
            # ReLU(),
            GroupNormalization(groups=gp_num, axis=-1),
            WeightNormalization(DepthwiseConv2D(3, padding='same', use_bias=False)),
            # DepthwiseConv2D(3, padding='same', use_bias=False),
            # get_norm(norm_type),
            GroupNormalization(groups=gp_num, axis=-1),
            WeightNormalization(Conv2D(filters, 1, use_bias=False, activation='relu')),
            # Conv2D(filters, 1, use_bias=False),
            # get_norm(norm_type),
            # ReLU(),
        ])

    def build(self, input_shape):
        super(BasicShuffleUnitV2_3, self).build(input_shape)

    def call(self, x, training=False):
        xl, xr = tf.split(x, 2, 3)
        x = tf.concat((xl, self.model(xr)), 3)
        return channel_shuffle_2(x)


class DownShuffleUnitV2_3(Model):
    def __init__(self,
                 filters,  # NOTE: will be filters // 2
                 # norm_type="group",
                 pad_type="constant",
                 gp_num=3001,  # 여기도 문제가 아니군
                 **kwargs):
        super(DownShuffleUnitV2_3, self).__init__(name="DownShuffleUnitV2_3")
        filters //= 2
        self.r_model = tf.keras.models.Sequential([
            # GroupNormalization(groups=256, axis=-1),
            GroupNormalization(groups=gp_num, axis=-1),
            WeightNormalization(Conv2D(filters, 1, use_bias=False, activation='relu')),
            # Conv2D(filters, 1, use_bias=False),
            # get_norm(norm_type),
            # ReLU(),
            GroupNormalization(groups=gp_num, axis=-1),
            # GroupNormalization(axis=-1),
            WeightNormalization(DepthwiseConv2D(3, 2, 'same', use_bias=False)),
            # DepthwiseConv2D(3, 2, 'same', use_bias=False),
            # get_norm(norm_type),
            GroupNormalization(groups=gp_num, axis=-1),
            # GroupNormalization(axis=-1),
            WeightNormalization(Conv2D(filters, 1, use_bias=False))
            # Conv2D(filters, 1, use_bias=False)
        ])
        self.l_model = tf.keras.models.Sequential([
            GroupNormalization(groups=gp_num, axis=-1),
            # GroupNormalization(axis=-1),
            WeightNormalization(DepthwiseConv2D(3, 2, 'same', use_bias=False)),
            DepthwiseConv2D(3, 2, 'same', use_bias=False),
            # get_norm(norm_type),
            GroupNormalization(groups=gp_num, axis=-1),
            # GroupNormalization(axis=-1),
            WeightNormalization(Conv2D(filters, 1, use_bias=False))
            # Conv2D(filters, 1, use_bias=False)
        ])
        self.bn_act = tf.keras.models.Sequential([
            GroupNormalization(groups=gp_num, axis=-1),
            # GroupNormalization(axis=-1),
            # get_norm(norm_type),
            ReLU(),
        ])

    def build(self, input_shape):
        super(DownShuffleUnitV2_3, self).build(input_shape)

    def call(self, x, training=False):
        x = tf.concat((self.l_model(x), self.r_model(x)), 3)
        x = self.bn_act(x)
        return channel_shuffle_2(x)


class ConvBlock_3(Model):
    def __init__(self,
                 filters,
                 kernel_size,
                 stride=1,
                 # norm_type="group",
                 gp_num=3,
                 pad_type="constant",
                 **kwargs):
        super(ConvBlock_3, self).__init__(name="ConvBlock_3")
        padding = (kernel_size - 1) // 2
        padding = (padding, padding)

        self.model = tf.keras.models.Sequential()
        self.model.add(get_padding(pad_type, padding))
        self.model.add(GroupNormalization(groups=gp_num, axis=-1))
        self.model.add(WeightNormalization(Conv2D(filters, kernel_size, stride)))
        # self.model.add(WeightNormalization(Conv2D(filters, kernel_size, stride)))
        self.model.add(get_padding(pad_type, padding))
        self.model.add(GroupNormalization(groups=gp_num, axis=-1))
        self.model.add(WeightNormalization(Conv2D(filters, kernel_size, activation='relu')))
        # self.model.add(WeightNormalization(Conv2D(filters, kernel_size)))
        # self.model.add(get_norm(norm_type))
        # self.model.add(ReLU())

    def build(self, input_shape):
        super(ConvBlock_3, self).build(input_shape)

    def call(self, x, training=False):
        return self.model(x, training=training)


class ResBlock_3(Model):
    def __init__(self,
                 filters,
                 kernel_size,
                 # idx=1,
                 # norm_type="group",
                 gp_num=3,
                 pad_type="constant",
                 **kwargs):
        # super(ResBlock_3, self).__init__(name="ResBlock_3_{}".format(idx))
        super(ResBlock_3, self).__init__()
        padding = (kernel_size - 1) // 2
        padding = (padding, padding)
        self.model = tf.keras.models.Sequential()
        self.model.add(get_padding(pad_type, padding))
        self.model.add(GroupNormalization(groups=gp_num, axis=-1))
        # self.model.add(GroupNormalization(axis=-1))
        self.model.add(WeightNormalization(Conv2D(filters, kernel_size, activation='relu')))
        # self.model.add(get_norm(norm_type))
        # self.model.add(ReLU())
        self.model.add(get_padding(pad_type, padding))
        self.model.add(GroupNormalization(groups=gp_num, axis=-1))
        # self.model.add(GroupNormalization(axis=-1))
        self.model.add(WeightNormalization(Conv2D(filters, kernel_size)))
        # self.model.add(get_norm(norm_type))
        self.add = Add()

    def build(self, input_shape):
        super(ResBlock_3, self).build(input_shape)

    def call(self, x, training=False):
        return self.add([self.model(x, training=training), x])


class UpSampleConv_3(Model):
    def __init__(self,
                 filters,
                 kernel_size,
                 # norm_type="group",
                 gp_num=3,
                 pad_type="constant",
                 light=False,
                 **kwargs):
        super(UpSampleConv_3, self).__init__(name="UpSampleConv_3")
        if light:
            self.model = tf.keras.models.Sequential([
                GroupNormalization(groups=gp_num, axis=-1),
                WeightNormalization(Conv2D(filters, 1)),
                # Conv2D(filters, 1),
                # BasicShuffleUnitV2_3(filters, norm_type, pad_type)
                BasicShuffleUnitV2_3(filters, pad_type)
            ])
        else:
            self.model = ConvBlock_3(
                # filters, kernel_size, 1, norm_type, pad_type)
                filters, kernel_size, 1, gp_num, pad_type)

    def build(self, input_shape):
        super(UpSampleConv_3, self).build(input_shape)

    def call(self, x, training=False):
        x = tf.keras.backend.resize_images(x, 2, 2, "channels_last", 'bilinear')
        return self.model(x, training=training)


class StridedConv_3(Model):
    def __init__(self,
                 filters=64,
                 lrelu_alpha=0.2,
                 pad_type="constant",
                 # norm_type="group",
                 gp_num=3002,  # 여기도 문제가 아니군
                 **kwargs):
        super(StridedConv_3, self).__init__(name="StridedConv_3")

        self.model = tf.keras.models.Sequential()
        self.model.add(get_padding(pad_type, (1, 1)))
        self.model.add(GroupNormalization(groups=gp_num, axis=-1))
        self.model.add(WeightNormalization(Conv2D(filters, 3, strides=(2, 2))))
        # self.model.add(Conv2D(filters, 3, strides=(2, 2)))
        self.model.add(LeakyReLU(lrelu_alpha))
        self.model.add(get_padding(pad_type, (1, 1)))

        self.model.add(GroupNormalization(groups=gp_num, axis=-1))
        self.model.add(WeightNormalization(Conv2D(filters * 2, 3)))
        # self.model.add(Conv2D(filters * 2, 3))
        # self.model.add(get_norm(norm_type))
        self.model.add(LeakyReLU(lrelu_alpha))

    def build(self, input_shape):
        super(StridedConv_3, self).build(input_shape)

    def call(self, x, training=False):
        return self.model(x, training=training)
