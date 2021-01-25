def generator_web():
    """
    저장된 모델의 가중치를 넣은 모델 만들기
    """
    # 학습된 모델 가중치 저장한 것 불러오기
    model = generator()
    model.load_weights(checkpoint_path)

    # 최고 성능을 냈던 가중치를 담은 모델 저장
    model.save("mymodel.h5")

    return model