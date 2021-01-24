# 순서 1
# model.compile

# 순서 2
# checkpoint 설정
checkpoint_path = "my_chkpoint.ckpt"
checkpoint = ModelCheckpoint(filepath=checkpoint_path,
                             save_weights_only=True,
                             save_best_only=True,
                             monitor="val_loss",
                             verbose=1)

# 순서 3
# model.fit

# 순서 4
# 저장된 모델의 가중치 불러오기
model.load_weights(checkpoint_path)

# 순서 5
# 저장된 모델의 가중치를 넣은 모델 만들기
model = solution_model()  # solution_model : 모델 만든 함수. 위의 1 ~ 4까지의 과정이 다 들어있고 맨 마지막에 return model)
model.save("mymodel.h5")  # <------ 최고 성능을 냈던 가중치를 담은 모델