# import numpy as np
# from alexnet import alexnet

# WIDTH = 81
# HEIGHT = 73
# LR = 1e-3
# EPOCHS = 6
# MODEL_NAME = 'aprende-a-seguir-{}-{}-{}-epochs.model'.format(LR, 'alexnetv2',EPOCHS)

# model = alexnet(WIDTH, HEIGHT, LR)
# train_data = np.load('training_data_v2.npy')

# train = train_data[:-500]

# test = train_data[-500:]

# Y = np.array([i[0] for i in train]).reshape(-1, WIDTH, HEIGHT, 1)
# X = [i[1] for i in test]

# test_y = np.array([i[0]for i in test]).reshape(-1, WIDTH, HEIGHT, 1)
# test_x = [i[1] for i in test]

# model.fit({'input': X}, {'targets': Y}, n_epoch=EPOCHS, 
#             validation_set=({'input': test_x}, {'targets': test_y}),
#             snapshot_step=200, show_metric=True, run_id=MODEL_NAME)

# model.save(MODEL_NAME)

# train_model.py

# train_model.py

import numpy as np
from alexnet import alexnet
WIDTH = 160
HEIGHT = 120
LR = 1e-4
EPOCHS = 10
MODEL_NAME = 'aprende-a-seguir{}-{}-{}-el-pajarito-data.model'.format(LR, 'alexnetv2',EPOCHS)

model = alexnet(WIDTH, HEIGHT, LR)

for i in range(EPOCHS):

    train_data = np.load('training_data_v2.npy')

    train = train_data[:-850]
    test = train_data[-350:]

    X = np.array([i[0] for i in train]).reshape(-1,WIDTH,HEIGHT,1)
    Y = [i[1] for i in train]

    test_x = np.array([i[0] for i in test]).reshape(-1,WIDTH,HEIGHT,1)
    test_y = [i[1] for i in test]

    model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}), 
        snapshot_step=500, show_metric=True, run_id=MODEL_NAME)

    model.save(MODEL_NAME)



# tensorboard --logdir=foo:C:/path/to/log

