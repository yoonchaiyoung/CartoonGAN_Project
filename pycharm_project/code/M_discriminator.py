def discriminator():
    """
    discriminator 모델 구조만 존재
    """
    # tf.variable_scope 사용하여 dVar이라고 지정하게 디면
    # 범위 내에서 생성되는 모든 변수는 맨 앞에 dVar이 붙게 된다.
    with tf.variable_scope("dVar", reuse=reuse):
        input_shape = (300, 300, 3)
        input_layer = Input(input_shape)

        net = Conv2D(kernel_size=3,
                     filters=32,
                     strides=1,
                     padding="same"
                     )(input_layer)
        net = LeakyReLU(alpha=0.2)(net)

        net = Conv2D(kernel_size=3,
                     filters=64,
                     strides=2,
                     padding="same"
                     )(net)
        net = LeakyReLU(alpha=0.2)(net)
        net = Conv2D(kernel_size=3,
                     filters=128,
                     strides=1,
                     padding="same"
                     )(net)
        net = BatchNormalization()(net)
        net = LeakyReLU(alpha=0.2)(net)

        net = Conv2D(kernel_size=3,
                     filters=128,
                     strides=2,
                     padding="same"
                     )(net)
        net = LeakyReLU(alpha=0.2)(net)
        net = Conv2D(kernel_size=3,
                     filters=256,
                     strides=1,
                     padding="same"
                     )(net)
        net = BatchNormalization()(net)
        net = LeakyReLU(alpha=0.2)(net)

        net = Conv2D(kernel_size=3,
                     filters=256,
                     strides=1,
                     padding="same"
                     )(net)
        net = BatchNormalization()(net)
        net = LeakyReLU(alpha=0.2)(net)

        net = Conv2D(kernel_size=3,
                     filters=1,
                     strides=1,
                     padding="same"
                     )(net)

        # disciminator 완성
        # d = Model(inputs=input_layer,
        #               outputs=net,
        #               name="discriminator"
        #               )

    return d