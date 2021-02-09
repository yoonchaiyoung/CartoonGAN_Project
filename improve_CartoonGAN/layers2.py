import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Layer, InputSpec, DepthwiseConv2D
from tensorflow.keras.layers import Conv2D, BatchNormalization, Add
from tensorflow.keras.layers import ReLU, LeakyReLU, ZeroPadding2D
from keras_contrib.layers import InstanceNormalization
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


class ReflectionPadding2D_2(Layer):
    def __init__(self, padding=(1, 1), **kwargs):
        super(ReflectionPadding2D_2, self).__init__(**kwargs)
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
        return ReflectionPadding2D_2(padding)
    elif pad_type == "constant":
        return ZeroPadding2D(padding)
    else:
        raise ValueError(f"Unrecognized pad_type {pad_type}")


def get_norm(norm_type):
    if norm_type == "instance":
        return InstanceNormalization()
    elif norm_type == 'batch':
        return BatchNormalization()

    elif norm_type == "spectral":
        return SpectralNormalization()

    else:
        raise ValueError(f"Unrecognized norm_type {norm_type}")


class FlatConv_2(Model):
    def __init__(self,
                 filters,
                 kernel_size,
                 norm_type="spectral",
                 pad_type="constant",
                 **kwargs):
        super(FlatConv_2, self).__init__(name="FlatConv_2")
        padding = (kernel_size - 1) // 2
        padding = (padding, padding)
        self.model = tf.keras.models.Sequential()
        self.model.add(get_padding(pad_type, padding))
        self.model.add(Conv2D(filters, kernel_size))
        self.model.add(get_norm(norm_type))
        self.model.add(ReLU())

    def build(self, input_shape):
        super(FlatConv_2, self).build(input_shape)

    def call(self, x, training=False):
        return self.model(x, training=training)


class BasicShuffleUnitV2_2(Model):
    def __init__(self,
                 filters,  # NOTE: will be filters // 2
                 norm_type="spectral",
                 pad_type="constant",
                 **kwargs):
        super(BasicShuffleUnitV2_2, self).__init__()
        filters //= 2
        self.model = tf.keras.models.Sequential([
            Conv2D(filters, 1, use_bias=False),
            get_norm(norm_type),
            ReLU(),
            DepthwiseConv2D(3, padding='same', use_bias=False),
            get_norm(norm_type),
            Conv2D(filters, 1, use_bias=False),
            get_norm(norm_type),
            ReLU(),
        ])

    def build(self, input_shape):
        super(BasicShuffleUnitV2_2, self).build(input_shape)

    def call(self, x, training=False):
        xl, xr = tf.split(x, 2, 3)
        x = tf.concat((xl, self.model(xr)), 3)
        return channel_shuffle_2(x)


class DownShuffleUnitV2_2(Model):
    def __init__(self,
                 filters,  # NOTE: will be filters // 2
                 norm_type="spectral",
                 pad_type="constant",
                 **kwargs):
        super(DownShuffleUnitV2_2, self).__init__(name="DownShuffleUnitV2_2")
        filters //= 2
        self.r_model = tf.keras.models.Sequential([
            Conv2D(filters, 1, use_bias=False),
            get_norm(norm_type),
            ReLU(),
            DepthwiseConv2D(3, 2, 'same', use_bias=False),
            get_norm(norm_type),
            Conv2D(filters, 1, use_bias=False),
        ])
        self.l_model = tf.keras.models.Sequential([
            DepthwiseConv2D(3, 2, 'same', use_bias=False),
            get_norm(norm_type),
            Conv2D(filters, 1, use_bias=False),
        ])
        self.bn_act = tf.keras.models.Sequential([
            get_norm(norm_type),
            ReLU(),
        ])

    def build(self, input_shape):
        super(DownShuffleUnitV2_2, self).build(input_shape)

    def call(self, x, training=False):
        x = tf.concat((self.l_model(x), self.r_model(x)), 3)
        x = self.bn_act(x)
        return channel_shuffle_2(x)


class ConvBlock_2(Model):
    def __init__(self,
                 filters,
                 kernel_size,
                 stride=1,
                 norm_type="spectral",
                 pad_type="constant",
                 **kwargs):
        super(ConvBlock_2, self).__init__(name="ConvBlock_2")
        padding = (kernel_size - 1) // 2
        padding = (padding, padding)

        self.model = tf.keras.models.Sequential()
        self.model.add(get_padding(pad_type, padding))
        self.model.add(Conv2D(filters, kernel_size, stride))
        self.model.add(get_padding(pad_type, padding))
        self.model.add(Conv2D(filters, kernel_size))
        self.model.add(get_norm(norm_type))
        self.model.add(ReLU())

    def build(self, input_shape):
        super(ConvBlock_2, self).build(input_shape)

    def call(self, x, training=False):
        return self.model(x, training=training)


class ResBlock_2(Model):
    def __init__(self,
                 filters,
                 kernel_size,
                 idx,
                 norm_type="spectral",
                 pad_type="constant",
                 **kwargs):
        super(ResBlock_2, self).__init__(name="ResBlock_{}".format(idx))
        padding = (kernel_size - 1) // 2
        padding = (padding, padding)
        self.model = tf.keras.models.Sequential()
        self.model.add(get_padding(pad_type, padding))
        self.model.add(Conv2D(filters, kernel_size))
        self.model.add(get_norm(norm_type))
        self.model.add(ReLU())
        self.model.add(get_padding(pad_type, padding))
        self.model.add(Conv2D(filters, kernel_size))
        self.model.add(get_norm(norm_type))
        self.add = Add()

    def build(self, input_shape):
        super(ResBlock_2, self).build(input_shape)

    def call(self, x, training=False):
        return self.add([self.model(x, training=training), x])


class UpSampleConv_2(Model):
    def __init__(self,
                 filters,
                 kernel_size,
                 norm_type="spectral",
                 pad_type="constant",
                 light=False,
                 **kwargs):
        super(UpSampleConv_2, self).__init__(name="UpSampleConv_2")
        if light:
            self.model = tf.keras.models.Sequential([
                Conv2D(filters, 1),
                BasicShuffleUnitV2_2(filters, norm_type, pad_type)
            ])
        else:
            self.model = ConvBlock_2(
                filters, kernel_size, 1, norm_type, pad_type)

    def build(self, input_shape):
        super(UpSampleConv_2, self).build(input_shape)

    def call(self, x, training=False):
        x = tf.keras.backend.resize_images(x, 2, 2, "channels_last", 'bilinear')
        return self.model(x, training=training)


class StridedConv_2(Model):
    def __init__(self,
                 filters=64,
                 lrelu_alpha=0.2,
                 norm_type="spectral",
                 pad_type="constant",
                 **kwargs):
        super(StridedConv_2, self).__init__(name="StridedConv_2")

        self.model = tf.keras.models.Sequential()
        self.model.add(get_padding(pad_type, (1, 1)))
        self.model.add(Conv2D(filters, 3, strides=(2, 2)))
        self.model.add(LeakyReLU(lrelu_alpha))
        self.model.add(get_padding(pad_type, (1, 1)))
        self.model.add(Conv2D(filters * 2, 3))
        self.model.add(get_norm(norm_type))
        self.model.add(LeakyReLU(lrelu_alpha))

    def build(self, input_shape):
        super(StridedConv_2, self).build(input_shape)

    def call(self, x, training=False):
        return self.model(x, training=training)
