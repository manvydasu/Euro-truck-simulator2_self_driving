import pandas
import constants
import cv2


def transform_image(image):
    image = image[int(768 * 0.4):768, :]  # cutting top of image since we can't learn anything from clouds anyway
    image = cv2.resize(image, (constants.IMAGE_WIDTH, constants.IMAGE_HEIGHT))
    return image

def transform_axis_input(input):
    """
    function for transforming input from PyGame format to VJOY format
    :param input:
    :return:
    """

    # sometimes input is not zero, but very very close to it, we have to find such cases and treat them like they are 0
    tempInput = input
    if(tempInput < 0):
        tempInput= -tempInput

    if(tempInput < 0.001):
        return int(constants.MAX_VJOY/2)


    if(input < 0):
        input=(1 + input) * int(constants.MAX_VJOY/2)
    else:
        input = int(constants.MAX_VJOY/2) + (input *  int(constants.MAX_VJOY/2))

    return int(input)



def transform_output(output):
    output = transform_axis_input(output) # transforming from pyGame to vJoy format
    return output / constants.MAX_VJOY # squishing to [0;1] interval



def transform_output_labels(data):
    data[0] = transform_output(data[0])
    data[1] = transform_output(data[1])
    return data








