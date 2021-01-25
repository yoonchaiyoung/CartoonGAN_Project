def discriminator_optimizer():

    d_train_opt = tf.train.AdamOptimizer(learning_rate=0.02).maximize(adversarial_loss + content_loss, var_list=d_vars)

    return d_train_opt