def train_generator(generator, batch_size, photo_list):
  # fit
  valid = np.ones((batch_size, 1))

  # 사진 중에서 랜덤으로 batch_size 갯수만큼 골라서 훈련시키기
  idx = np.random.normal(0, photo_list.shape[0], batch_size)
  selected_photo = photo_list[idx]
  discriminator.trainable = False  # discriminator 파라미터 업데이트되면 안됨
  g_losses = generator.train_on_batch(selected_photo, valid)

  return selected_photo, g_losses