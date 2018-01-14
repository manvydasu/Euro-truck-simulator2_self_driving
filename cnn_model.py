from keras.models import Sequential
from keras.layers.core import Dense, Flatten, Dropout
from keras.layers.convolutional import Conv2D
import keras
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
import os

import constants
import data_manager


print (keras.__version__)

# paper link for the convolutional model  - https://arxiv.org/pdf/1604.07316.pdf

def _create_model():

    nrows = constants.IMAGE_HEIGHT
    ncols = constants.IMAGE_WIDTH
    img_channels = 3 # color channels
    output_size = 2

    model = Sequential()
    model.add(Dropout(0.35, input_shape=(nrows, ncols, img_channels)))
    model.add(Conv2D(filters=24, kernel_size=(5, 5), strides=(2, 2), padding='valid', activation='elu'))
    model.add(Conv2D(filters=36, kernel_size=(5, 5), strides=(2, 2), padding='valid', activation='elu'))
    model.add(Conv2D(filters=48, kernel_size=(5, 5), strides=(2, 2), padding='valid', activation='elu'))
    model.add(Conv2D(filters=64, kernel_size=(3, 3), strides=(1, 1), padding='valid', activation='elu'))
    model.add(Conv2D(filters=64, kernel_size=(3, 3), strides=(1, 1), padding='valid', activation='elu'))
    model.add(Dropout(0.35))

    model.add(Flatten())
    model.add(Dense(100, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(output_size))
    model.summary()

    model.compile(loss=keras.losses.mean_squared_error,
                  optimizer=keras.optimizers.Adam(lr=0.001),
                  metrics=['accuracy'])

    return model


def get_model():
    if (os.path.isfile(constants.FINAL_MODEL_FILEPATH)):
        model = keras.models.load_model('my_model.h5')
    else:
        model = _create_model()

    return model


def train_model(model):
    """
    Training data will consist 85%  of total data.
     The last 15% will be used for validation
    :param model: kenas cnn model
    :return:
    """

    X, Y = data_manager.read_data_from_file(split = True)

    X_train, X_valid, Y_train, Y_valid = train_test_split(X, Y, test_size = 0.15, random_state = 1)


    model = get_model()

    checkpoint = ModelCheckpoint('model-{epoch:03d}.h5', monitor='val_loss', verbose=1, mode='auto')

    model.fit(X_train, Y_train, epochs=8, batch_size=64, verbose=1,
              validation_data=(X_valid, Y_valid), callbacks=[checkpoint])

    #save the model after training
    model.save(constants.FINAL_MODEL_FILEPATH)


# model.summary()




