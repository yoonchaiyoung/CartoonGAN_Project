def train_discriminator(discriminator, batch_size, cartoon_img, edge_smoothing_img, cartoonized_photo):
    valid = np.ones((batch_size, 1))
    fake = np.zeros((batch_size, 1))

    idx_1 = np.random.randint(0, cartoon_img.shape[0], batch_size)
    cartoon_imgs = cartoon_img[idx_1]
    discriminator.trainable = True  # discriminator 파라미터 업데이트되어야함
    d_losses = discriminator.train_on_batch(cartoon_imgs, valid)

    idx_2 = np.random.randint(0, edge_smoothing_img.shape[0], batch_size)
    edge_smoothing_imgs = edge_smoothing_img[idx_2]
    discriminator.trainable = True  # discriminator 파라미터 업데이트되어야함
    d_losses = discriminator.train_on_batch(edge_smoothing_imgs, fake)

    idx_3 = np.random.randint(0, cartoonized_photo.shape[0], batch_size)
    cartoonized_photos = cartoonized_photo[idx_3]
    discriminator.trainable = True  # discriminator 파라미터 업데이트되어야함
    d_losses = discriminator.train_on_batch(cartoonized_photos, fake)

    return d_losses