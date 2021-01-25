def train_CartoonGAN(epochs, batch_size=0, photo_path, edge_smoothing_path, generated_list):

    # 모델 구조 로드
    g = generator()
    d = discriminator()

    # loss함수 로드
    content_loss = content_loss()
    adversarial_loss = adversarial_loss()

    # resizing된 사진을 담은 리스트 생성
    photoName_list = os.listdir(photo_path)
    photo_list = []  # 사진을 담은 리스트
    for photoName in photoName_list:
        photo_bgr = cv2.imread(photo_path + '/' + photoName)
        photo = cv2.cvtColor(photo_bgr, cv2.COLOR_BGR2RGB)
        photo_list.append(photo)

    # 엣지 smoothing된 만화 이미지를 담은 리스트 생성
    edgeCartoonName_list = os.listdir(edge_smoothing_path)
    edge_list = []  # 엣지 smothing된 만화 이미지를 담은 리스트
    for edgeCartoonName in edgeCartoonName_list:
        cartoon_bgr = cv2.imread(edge_smoothing_path + '/' + edgeCartoonName)
        cartoon = cv2.cvtColor(cartoon_bgr, cv2.COLOR_BGR2RGB)
        edge_list.append(cartoon)

    # 모델 compile
    g.compile(loss=content_loss, optimizer=generator_optimizer)
    d.compile(loss=adversarial_loss + content_loss, optimizer=discriminator_optimizer)



    # 변수 목록 생성
    total_vars = tf.trainable_variables()  # 선언한 모든 변수를 담은 리스트를 반환
    g_vars = [var for var in total_vars if var.name.startswith("gVar")]
    d_vars = [var for var in total_vars if var.name.startswith("dVar")]

    # optimizer 생성
    # G는 loss값을 최소로 만들어야하고
    # D는 loss값을 최대로 만들어야한다.
    g_train_opt = tf.train.AdamOptimizer(learning_rate=0.2).minimize(adversarial_loss + content_loss, var_list=g_vars)
    d_train_opt = tf.train.AdamOptimizer(learning_rate=0.2).maximize(adversarial_loss + content_loss, var_list=d_vars)


    # generator 10 epoch만큼 훈련
    # discriminator 파라미터 업데이트 안 되도록 고정
    saver = tf.train.Saver(var_list=g_vars)
    with tf.Session() as sess:  # 세션을 만들어서 연산그래프 실행
        sess.run(tf.global_variables_initializer())  # 모든 변수를 초기화
        for epoch in range(10):
            # optimizer 돌리기
            _ = sess.run()

        # 카툰화된 사진을 담은 리스트 생성
        cartoonized_photo_list = []
        cartoonized_photo = sess.run(generator(photo, reuse=True),
                                     feed_dict={photo : photo_list})  # photo_list에서 한개씩 꺼낸것을 photo라고 함
        cartoonized_photo_list.apend(cartoonized_photo)

        # 카툰화된 사진 저장
        for idx, photoName in enumerate(photoName_list):
            cv2.imwrite(os.path.join(generated_list, photoName[0:-4] + '_generated' + '.png'),
                        cv2.cvtColor(generated_list[idx], cv2.COLOR_BGR2RGB))

        # 가중치 저장 체크포인트 파일(.ckpt)로 저장
        saver.save(sess, './checkpoints_210125/generator.ckpt')

    # 가중치를 pickle로 저장
    # with open('train_samples_210125.pkl', 'wb') as f:
    #     pickle.dump(cartoonized_photo_list, f)

    # 가중치를 pickle로 저장
    checkpoint_path = "chkpoint_210125.ckpt"
    checkpoint = ModelCheckpoint(filepath=checkpoint_path,
                                 save_weights_only=True,
                                 save_best_only=True,
                                 monitor="val_loss",
                                 verbose=1)


    # -------------------------------------------------------------------------
    # 순서 2. discriminator 훈련 -> discriminator 훈련 설정한 epochs 수만큼 반복
    # generator 훈련할 때는 discriminator 파라미터 업데이트 안되도록 고정
    # discriminator 훈련할 때는 generator 파라미터 업데이트 안되도록 고정
    for epoch in range(epochs):
        train_discriminator()
        train_generator()


    return 