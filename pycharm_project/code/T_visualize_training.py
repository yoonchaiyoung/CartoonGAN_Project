def visualize_training(epochs, g_losses, d_losses, photo_list, sample_num):
    """
    1. loss 함수 변화 시각화
    2. 카툰화된 사진 시각화
    - sample_num 갯수만큼 photo_list에서 랜덤으로 꺼내서
    - generator를 돌려서 나온 카툰화된 사진을 시각화
    """
    plt.figure(figsize=(8, 4))
    plt.plot(g_losses, label="Generator Loss")
    plt.plot(d_losses, label="Discriminator Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.show()

    print("epoch : {}, Generator Loss : {}, Discriminator Loss : {}".format(epochs, np.asarray(g_losses).mean(), np.asarray(d_losses).mean()))

    idx = np.random.normal(0, photo_list.shape[0], sample_num)
    generated_images = generator,predict(selected_photo)
    generated_images = generated_images.reshape(300, 300, 3)

    plt.figure(figsize=(10, 10))
    for i in range(generated_images.shape[0]):
        plt.subplot(sample_num, 1, i+1)
        plt.imshow(generated_images[i], interpolation="nearest", cmap="gray")
        plt.axis("off")
    plt.tight_layout()
    plt.show()
