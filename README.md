# End to End self driving using CNN from famous nvidia research paper for Euro Truck Simulator 2

CNN model is implemented using Keras.

The flow of program is quite simple:
First we have to collect training data. We use data_manager.py file for that. 
It runs an infinite loop while grabing game window screenshot (using PIL) and joystick values (using PyGame):
Grabbed image is resized.
Grabbed joystick values format is changed to match PyVJOY (https://github.com/tidzo/pyvjoy).

After collecting training data, we have to train the network.
Training is quite simple -  testing data is split into two parts  using scikit-learn ( training - 85% and validation - 15% ) and sent to model.fit function

At last, we test the network using deploy_network function ( main.py). It grabs a screenshot, processes (cut top, resize) it and sends it to the network. Network provides us with output - we multiply that output by MAX_PYVJOY value(to get correct format for pyvjoy library) and send it to the joystick. 


# Testing the network

Testing of the network real time can be seen [here](https://www.youtube.com/watch?v=DJMNs5P3aUw) 




