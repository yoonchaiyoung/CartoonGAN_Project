def train_CartoonGAN(epochs):
    for epoch in range(10):
        initialization(generator, resizing_photo, batch_size, epochs)

    for epoch in range(epochs):
        train_discriminator(discriminator, batch_size, cartoon_img, edge_smoothing_img, cartoonized_photo)
        train_generator(generator, batch_size, resizing_photo, epochs)

    return 