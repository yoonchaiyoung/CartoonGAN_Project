def adversarial_loss(disc_c, disc_e, disc_p):
    """
    ----------------------------------------------
    파라미터 설명
    ----------------------------------------------
    disc_c : 만화 이미지가 discriminator를 통과해서 얻은 출력값(예측값)
    disc_e : 엣지 smoothing된 만화 이미지가 discriminator를 통과해서 얻은 출력값(예측값)
    disc_p : 카툰화된 사진이 discriminator를 통과해서 얻은 출력값(예측값)
    ----------------------------------------------
    """

    # binary cross entropy 객체
    bce = keras.losses.BinaryCrossentropy()

    one_c = np.ones_like(disc_c, dtype=tf.float32)
    zero_e = np.zeros_like(disc_e, dtype=tf.float32)
    zero_p = np.zeros_like(disc_p, dtype=tf.float32)

    # binary cross entropy (실제값, 예측값)
    cartoon_error = bce(one_c, disc_c).numpy()
    edge_smooth_cartoon_error = bce(zero_e, disc_e).numpy()
    photo_error = bce(zero_p, disc_p).numpy()

    adv_loss = cartoon_error + edge_smooth_cartoon_error + photo_error

    return adv_loss