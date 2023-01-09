
# Path: src/rl.py

#import libraries
import airsim
import tensorflow as tf
import numpy as np
import pprint

#model for the drone
class DroneModel:
    def __init__(self):
        #initialize the model
        self.model = tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(10)
        ])
        #compile the model
        self.model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
        #load the model
        self.model.load_weights('model.h5')
        #get the model summary
        self.model.summary()
        
    #predict the model
    def predict(self, image):
        return self.model.predict(image)

#connect to the drone
class Drone:
    def __init__(self):
        #connect to the drone
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        #initialize the model
        self.model = DroneModel()
        
    #takeoff the drone
    def takeoff(self):
        print("arming the drone...")
        self.client.armDisarm(True)
        state = self.client.getMultirotorState()
        s = pprint.pformat(state)
        print("state: %s" % s)
        airsim.wait_key('Press any key to takeoff')
        self.client.takeoffAsync().join()
        state = self.client.getMultirotorState()
        print("state: %s" % pprint.pformat(state))
        airsim.wait_key('Press any key to move vehicle to (-10, 10, -10) at 5 m/s')
        self.client.moveToPositionAsync(-10, 10, 10, 5).join()
        self.client.hoverAsync().join()
        airsim.wait_key('Press any key to get Lidar readings')
        
    #get the image from the drone
    def get_image(self):
        responses = self.client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])
        response = responses[0]
        img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) 
        img_rgb = img1d.reshape(response.height, response.width, 3)
        return img_rgb
    
    #get the lidar data from the drone
    def get_lidar(self):
        lidarData = self.client.getLidarData();
        if (len(lidarData.point_cloud) < 3):
            print("\tNo points received from Lidar data")
        else:
            points = self.parse_lidarData(lidarData)
            print("\tReading %d: time_stamp: %d number_of_points: %d" % (i, lidarData.time_stamp, len(points)))
            print("\t\tlidar position: %s" % (pprint.pformat(lidarData.pose.position)))
            print("\t\tlidar orientation: %s" % (pprint.pformat(lidarData.pose.orientation)))
        time.sleep(5)
        
    #parse the lidar data
    def parse_lidarData(self, data):
        points = np.array(data.point_cloud, dtype=np.dtype('f4'))
        points = np.reshape(points, (int(points.shape[0]/3), 3))
        return points

    #get the control from the model
    def get_control(self, image):
        return self.model.predict(image)

    #move the drone
    def move(self, control):
        self.client.moveByVelocityAsync(control[0], control[1], control[2], 5).join()
        self.client.hoverAsync().join()


#main function
def main():
    #initialize the drone
    drone = Drone()
    #takeoff the drone
    drone.takeoff()
    #get the image from the drone
    image = drone.get_image()
    #get the control from the model
    control = drone.get_control(image)
    #move the drone
    drone.move(control)

#run the main function
main()