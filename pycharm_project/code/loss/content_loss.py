def content_loss(photo_path, cartoonized_photo_path):
    # ------------------------------------------------------------------------------------------------------------------------------

    def vgg_transfer_model():
        """
        -------------------------------------
        함수 설명
        -------------------------------------
        VGG19 모델을 전이학습을 하기 위해서
        conv4_4 layer까지 불러온다.
        -------------------------------------
        """

        vgg19 = VGG19()
        input_shape = (224, 224, 3)
        input_layer = Input(shape=input_shape)
        net = vgg19.layers[0](input_layer)
        net = vgg19.layers[1](net)
        net = vgg19.layers[2](net)
        net = vgg19.layers[3](net)
        net = vgg19.layers[4](net)
        net = vgg19.layers[5](net)
        net = vgg19.layers[6](net)
        net = vgg19.layers[7](net)
        net = vgg19.layers[8](net)
        net = vgg19.layers[9](net)
        net = vgg19.layers[10](net)
        net = vgg19.layers[11](net)
        net = vgg19.layers[12](net)
        net = vgg19.layers[13](net)
        net = vgg19.layers[14](net)
        net = vgg19.layers[15](net)

        model = Model(inputs=input_layer,
                      outputs=net,
                      name="vgg_layer_0to15")

        return model

    # ------------------------------------------------------------------------------------------------------------------------------

    def vgg19_transfer_learning(img_path, model):
        """
        --------------------------------------------------
        파라미터 설명
        --------------------------------------------------
        img_path : 원본 사진 또는 카툰화된 사진이 저장된 디렉토리 경로
        model : VGG19 모델의 conv4_4 layer까지의 모델
        --------------------------------------------------
        함수 설명
        --------------------------------------------------
        VGG19 모델을 가져다가 conv4_4 layer까지 전이학습을 시키는 과정
        함수의 input : 원본 사진 또는 카툰화된 사진
        함수의 output : 원본 사진 또는 카툰화된 사진을 VGG19 모델에 통과시킨후
                        얻은 conv4_4 layer의 feature map
        --------------------------------------------------
        """

        imageName_list = os.listdir(img_path)

        feature_map_list = []
        # VGG19 모델의 conv4_4 layer의 feature map을 각각의 이미지에 대해 구한 후
        # 리스트에 순서대로 담는다.

        for imageName in imageName_list:
            # 이미지 전처리 과정
            img_bgr = cv2.imread(img_path + '/' + imageName)
            img = cv2.cvtCOLOR(img_bgr, cv2.COLOR_BGR2RGB)
            img_resizing = cv2.resize(img, dsize=(224, 224), interpolation=cv2.INTER_LINEAR)
            img_array = np.asarray(img_resizing)
            img_4D = img_array.reshape((1, img_array.shape[0], img_array.shape[1], img_array.shape[2]))
            img_preprocess_input = preprocess_input_img_4D
            img_float32 = tf.cast(img_preprocess_input, dtype=tf.float32)

            # VGG19 conv4_4 layer에 해당하는 feature map 추출하기
            vgg_conv4_4_output = model(img_float32)
            feature_map_list.append(vgg_conv4_4_output)

        return feature_map_list

    def l1_regularization(photo_feature_map_list, cartoonized_photo_feature_map_list):
        """
        ---------------------------------------
        파라미터 설명
        ---------------------------------------
        photo_feature_map_list : 원본 사진 모음의 VGG19 conv4_4 layer의
                                feature map이 담긴 리스트
        cartoonized_photo_feature_map_list : 카툰화된 사진 모음의 VGG19 conv4_4 layer의
                                feature map이 담긴 리스트
        ---------------------------------------
        함수 설명
        ---------------------------------------
        CartoonGAN의 content loss는 feature map에 추가로
        l1 규제를 취해준다.
        ---------------------------------------
        """
        n = photo_feature_map_list.shape[-1]
        bce = BinaryCrossentropy()
        error = bce(photo_feature_map_list, cartoonized_photo_feature_map_list).numpy()

        return error

    # ------------------------------------------------------------------------------------------------------------------------------
    # content_loss 함수 내용 부분

    model = vgg_transfer_model()
    photo_feature_map_list = vgg19_transfer_learning(photo_path, model)
    cartoonized_feature_map_list = vgg19_transfer_learning(cartoonized_photo_path, model)
    content_loss = l1_regularization(photo_feature_map_list, cartoonized_photo_feature_map_list)

    return content_loss