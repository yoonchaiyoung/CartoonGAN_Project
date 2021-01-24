def train_CartoonGAN(epochs, batch_size, cartoon_path, photo_path):

    # 순서 1. initialization
    # 모델 구조 로드
    g = generator()
    d = discriminator()

    # 전처리 작업이 끝난 사진(resizing된 사진) 담은 리스트 생성
    photoName_list = os.listdir(photo_path)
    photo_list = []
    for photoName in photoName_list:
        photo_bgr = cv2.imread(photo_path + '/' + photoName)
        photo = cv2.cvtColor(photo_bgr, cv2.COLOR_BGR2RGB)
        photo_list.append(photo)

    # 모델 compile
    g.compile(loss=content_loss, optimizer="adam", metrics=["acc"])
    d.compile(loss=adversarial_loss + content_loss, optimizer="adam", metrics=["acc"])

    # 가중치를 pickle로 저장
    checkpoint_path = "my_chkpoint.ckpt"
    checkpoint = ModelCheckpoint(filepath=checkpoint_path,
                                 save_weights_only=True,
                                 save_best_only=True,
                                 monitor="val_loss",
                                 verbose=1)
    # generator 10 epoch만큼 훈련
    for epoch in range(10):
        valid = np.ones((batch_size, 1))
        g.fit(photo_list, valid, batch_size=batch_size, shuffle=True)

    # -------------------------------------------------------------------------
    # 순서 2. discriminator 훈련 -> discriminator 훈련 반복
    for epoch in range(epochs):
        train_discriminator(discriminator, batch_size, cartoon_img, edge_smoothing_img, cartoonized_photo)
        train_generator(generator, batch_size, resizing_photo, epochs)

    return 