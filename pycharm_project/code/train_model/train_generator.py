def train_generator(generator, batch_size, resizing_photo, epochs):
  valid = np.ones((batch_size, 1))

  generator.fit(resizing_photo, valid, batch_size = batch_size, epochs = epochs, shuffle = True)

  return