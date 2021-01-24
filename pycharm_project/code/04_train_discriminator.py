def train_discriminator(batch_size, cartoon_img, edge_smoothing_img, cartoonized_photo):
    valid = np.ones((batch_size, 1))
    fake = np.zeros((batch_size, 1))

    idx_1 = np.random.randint(0, cartoon_img.shape[0], batch_size)
    cartoon_imgs = cartoon_img[idx_1]
    discriminator.fit(cartoon_imgs, valid, batch_size=batch_size, epochs=epochs, shuffle=True)

    idx_2 = np.random.randint(0, edge_smoothing_img.shape[0], batch_size)
    edge_smoothing_imgs = edge_smoothing_img[idx_2]
    discriminator.fit(edge_smoothing_imgs, fake, batch_size=batch_size, epochs=epochs, shuffle=True)

    idx_3 = np.random.randint(0, cartoonized_photo.shape[0], batch_size)
    cartoonized_photos = cartoonized_photo[idx_3]
    discriminator.fit(cartoonized_photos, fake, batch_size=batch_size, epochs=epochs, shuffle=True)

    return 