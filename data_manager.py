import win32api
from PIL import ImageGrab
import numpy as np
import cv2
import pygame
import time
import pickle

import constants
import data_preprocessing

def get_joystick_axis_values(joystick):
    """
     method for retrieving joystick analog values
    :param joystick:
    :return: an array of two elements (axis0  ( speed ) and axis1 (turn))
    """

    pygame.event.pump() # this has to be called in order to get most recent input from joystick
    axis0 = joystick.get_axis(0)
    axis1 = joystick.get_axis(1)
    return [axis0, axis1]

def display_data():
    """
    function which iterates through dataset
    :return:
    """
    data = read_data_from_file()
    data_size = len(data)
    print('Data size  -  ' + str(data_size))


    for i in range(data_size-1, 0, -1):
        image = data[i]
        cv2.imshow('window', image[0])
        print(str(image[1]))
        cv2.waitKey(50)




def record_screen(startX, startY, endX, endY):
    """
    function which runs infinite loop and takes screenshot + joystick input and saves that data to the file
    :param startX:
    :param startY:
    :param endX:
    :param endY:
    :return:
    """

    # some delay, which allows us to focus game window and  start driving
    print("Starting collecting data in...")
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)


    # initing joystick
    pygame.init()
    pygame.event.pump()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    with open(constants.DATA_FILENAME, 'ab') as f:



        data = []

        count = 0  # keeping a counter to know how much data we have collected in this run so far

        while (True):

            screenshot = ImageGrab.grab(bbox=(startX, startY, endX, endY))

            joystick_values = get_joystick_axis_values(joystick)
            joystick_values = data_preprocessing.transform_output_labels(joystick_values)

            screenshot = data_preprocessing.transform_image(np.array(screenshot))

            data.append([screenshot, joystick_values])

            # write to file every time we collect another 1000 data samples
            if (count % 1000 == 0 and count != 0):
                print('Collected data count - {0}.'.format(count))
                pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
                data = [] # clear the data from memory

            count += 1



def read_data_from_file(split=False):
    """
    returns an array of two elements (axis0  ( speed ) and axis1 (turn))
    :param split:  if split is set to True, returns two  numpy arrays - X_train, Y-train
    :return:
    """
    with open(constants.DATA_FILENAME, 'rb') as f:
        data = []
        while(True):
            try:
                temp = pickle.load(f)

                if type(temp) is not list:
                   temp = np.ndarray.tolist(temp)

                data = data + temp
            except EOFError:
                break
        if split:
            X_train = []
            Y_train = []

            for i in range (0, len(data)):
                X_train.append(data[i][0]) # image
                Y_train.append(data[i][1]) # corresponding joystick output

            return np.array(X_train), np.array(Y_train)
        else:
            return np.array(data)



def get_pressed_keys(self):
    """
    function for getting pressed keys
    this could be used for some other CNN which outputs more than a single value
    ! currently this is not used anywhere  !
    :param self:
    :return:
    """
    pressed_keys = np.empty(len(constants.POSSIBLE_KEYS))
    for index, key in enumerate(constants.POSSIBLE_KEYS):
        if((win32api.GetKeyState(ord(key)) & (1 << 7)) != 0):
            pressed_keys[index] = 1

    return pressed_keys