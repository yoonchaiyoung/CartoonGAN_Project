def train_generator(train_type, generator, batch_size, resizing_photo, epochs):
  """
  train_type : initialization, train_generator, train_discriminator
  """
  # fit
  valid = np.ones((batch_size, 1))
  generator.fit(resizing_photo, valid, batch_size = batch_size, epochs = epochs, shuffle = True)

  return