def generator():
    """
    generator 모델 구조만 존재
    """

    # ----------------------------------------------------------------------------------------------
    def generator_residual_block(x):
        """
        --------------------------------------------
        함수 설명
        --------------------------------------------
        residual block의 똑같은 구조가 generator안에 8번 반복되므로 따로 만듦.
        --------------------------------------------
        """
        shortcut = x
        x = Conv2D(kernel_size=3,
                   filters=256,
                   strides=1,
                   padding="same"
                   )(x)
        x = BatchNormalization()(x)
        x = ReLU()(x)
        x = Conv2D(kernel_size=3,
                   filters=256,
                   strides=1,
                   padding="same")(x)
        x = BatchNormalization()(x)
        x = layers.Add()([x, shortcut])  # identity shortcut connection  # elementwise sum

        return x

    # ----------------------------------------------------------------------------------------------
    # flat-convolution 영역
    input_shape = (300, 300, 3)
    input_layer = Input(shape=input_shape)
    net = Conv2D(kernel_size=7,
                 filters=64,
                 strides=1,
                 padding="same"
                 )(input_layer)
    net = BatchNormalization()(net)
    net = ReLU()(net)

    # down-convolution 영역
    net = Conv2D(kernel_size=3,
                 filters=128,
                 strides=2,
                 padding="same"
                 )(net)

    net = Conv2D(kernel_size=3,
                 filters=128,
                 strides=1,
                 padding="same"
                 )(net)
    net = BatchNormalization()(net)
    net = ReLU()(net)

    net = Conv2D(kernel_size=3,
                 filters=256,
                 strides=2,
                 padding="same"
                 )(net)
    net = Conv2D(kernel_size=3,
                 filters=256,
                 strides=1,
                 padding="same"
                 )(net)
    net = BatchNormalization()(net)
    net = ReLU()(net)

    # 8 residual block 영역
    net = generator_residual_block(net)
    net = generator_residual_block(net)
    net = generator_residual_block(net)
    net = generator_residual_block(net)
    net = generator_residual_block(net)
    net = generator_residual_block(net)
    net = generator_residual_block(net)
    net = generator_residual_block(net)

    # up-convolution 영역
    net = Conv2DTranspose(kernel_size=3,
                          filters=128,
                          strides=(2, 2),
                          padding="same"
                          )(net)
    net = Conv2D(kernel_size=3,
                 filters=128,
                 strides=1,
                 padding="same"
                 )(net)
    net = BatchNormalization()(net)
    net = ReLU()(net)

    net = Conv2DTranspose(kernel_size=3,
                          filters=64,
                          strides=(2, 2),
                          padding="same"
                          )(net)
    net = Conv2D(kernel_size=3,
                 filters=64,
                 strides=1,
                 padding="same"
                 )(net)
    net = BatchNormalization()(net)
    net = LeakyReLU()(net)

    # output layer 영역
    net = Conv2D(kernel_size=7,
                 filters=3,
                 strides=1,
                 padding="same"
                 )(net)

    # generator 완성
    g = Model(inputs=input_layer,
              outputs=net,
              name="generator"
              )

    return g