def generator_optimizer():

    g_train_opt = tf.train.AdamOptimizer(learning_rate=0.02).minimize(adversarial_loss + content_loss, var_list=g_vars)

    return g_train_opt