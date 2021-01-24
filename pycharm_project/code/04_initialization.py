def initialization(generator, resizing_photo, batch_size, epochs):
    valid = np.ones((batch_size, 1))
    generator.fit(resizing_photo, valid, batch_size=batch_size, epochs=epochs, shuffle=True)

    return