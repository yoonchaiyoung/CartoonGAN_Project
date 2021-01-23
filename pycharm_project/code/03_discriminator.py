def discriminator(loss, optimizer, metrics):
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
    model = Model(inputs=input_layer,
                  outputs=net,
                  name="discriminator"
                  )

    # compile
    model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
    model.trainable = False  # trainable 메소드는 compile할 때만 영향을 미친다

    return model