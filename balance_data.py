import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
import cv2

train_data = np.load('training_data.npy')

df = pd.DataFrame(train_data)
print(df.head())
print(Counter(df[1].apply(str)))

up = []
down = []

shuffle(train_data)

for data in train_data:
    img = data[0]
    choice = data[1]

    if choice == [1]:
        up.append([img,choice])
    elif choice == [0]:
        down.append([img,choice])
    else:
        print('No Matchessssss!!!!!!!!!!!!!')

down = down[:len(up)]
final_data = up + down
shuffle(final_data)
print('len of ups')
print(len(up))
# print(len(final_data))
np.save('training_data_v2.npy', train_data)


# for data in train_data:
#     img = data[0]
#     choice = data[1]
#     cv2.imshow('test', img)
#     print(choice)
#     if cv2.waitKey(25) & 0xFF == ord('q'):
#         cv2.destroyAllWindows()
#         break