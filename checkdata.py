import numpy as np
import cv2

train_data = np.load('training_data.npy')

for data in train_data:
    img = data[0]
    choice = data[1]
    cv2.imshow('test',img)
    print(choice)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

# import keyboard #Using module keyboard
# while True:#making a loop
#     try: #used try so that if user pressed other than the given key error will not be shown
#         if keyboard.is_pressed('w'):#if key 'q' is pressed 
#             print('You Pressed A Key!')
#             #break#finishing the loop
#             keyboard.
#         else:
#             pass
#     except:
#         break