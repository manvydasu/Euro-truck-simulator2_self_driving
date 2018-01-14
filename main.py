from PIL import ImageGrab
import numpy as np
import cv2
import pyvjoy


import data_manager
import constants
import cnn_model
import data_preprocessing


def deploy_model():
    """
    Test model in real time
    we will be getting screenshots and sending joystick input straight to the game
    and see how it goes
    :return:
    """

    # getting the saved model
    model = cnn_model.get_model()
    model.summary()


    j = pyvjoy.VJoyDevice(1) # this should be set according your device num

    #running the infinite loop
    while(True):
        screenshot = np.array(ImageGrab.grab(bbox=(0, 40, 1024, 768)))
        screenshot = data_preprocessing.transform_image(screenshot)

        prediction = model.predict(np.array([screenshot]))
        j.data.wAxisX = int(prediction[0][0] * constants.MAX_VJOY)
        j.data.wAxisY = int(prediction[0][1] * constants.MAX_VJOY)
        j.update()
        print(prediction)





if __name__ == "__main__":

    #data_manager.record_screen(0, 40, 1024, 768)  # passing 4 coordinates of screen to the game window which is on top left corner

    #model = cnn_model.get_model()
    #cnn_model.train_model(model)

    deploy_model()

    #data_manager.display_data()





