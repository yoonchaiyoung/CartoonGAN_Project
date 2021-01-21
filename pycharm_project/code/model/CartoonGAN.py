def CartoonGAN(generator, discriminator, loss, optimizer, metrics):
  """
  ------------------------------------
  함수 설명
  ------------------------------------
  CartoonGAN은 generator, discriminator가 합쳐진 모델
  ------------------------------------
  """
  # CartoonGAN 완성
  CartoonGAN = Sequential()
  CartoonGAN.add(generator)
  CartoonGAN.add(discriminator)

  # compile
  CartoonGAN.compile(loss = loss, optimizer = optimizer, metrics = metrics)
  CartoonGAN.trainable = False # trainable 메소드는 compile할 때만 영향을 미친다

  return CartoonGAN

