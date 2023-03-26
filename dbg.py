import math
import os
import time
import airsim
import numpy as np
#connecting airsim
client = airsim.MultirotorClient()
client.confirmConnection()
#connecting api's
client.enableApiControl(True,vehicle_name="drone6")
client.enableApiControl(True,vehicle_name="drone7")
#arming drone
client.armDisarm(True,vehicle_name="drone6")
client.armDisarm(True,vehicle_name="drone7")
#initial location setup
d6=client.takeoffAsync(vehicle_name="drone6")
d7=client.takeoffAsync(vehicle_name="drone7")
d6.join()
d7.join()
#setting heights
z6=-15
z7=-10
d6=client.moveToPositionAsync(0,0,z6,5,vehicle_name='drone6')
d6.join()
d6=client.moveToPositionAsync(0,0,z7,5,vehicle_name='drone7')
d7.join()
#Planing path
d = 3 #image taking differrence
s = 1 #survey drone speed
camera_pitch_angle6=-45 #camera pitch angle
camera_pitch_angle7=-30
radius=-22
k=1
theta=0
while(theta<=2*np.pi):
    x=radius-(radius*np.cos(theta)) 
    y=radius-(radius*np.sin(theta))
    #for camera pose defined function are
    #airsim.pose(position,orientation)
    #airpose.to_quaternion(pitch,roll,yaw)
    #client.simSetVehiclePose(pose of vehicle,Collision(bool),vehicle_name)
    #it sets a default setting for the position and orientatoin for camera
    d6=client.moveToPositionAsync(x,y-2,z6,s,vehicle_name='drone6')
    d6.join()
    d7=client.moveToPositionAsync(x,y-4,z7,s,vehicle_name='drone7')
    d7.join()
    vehicle_pose = airsim.Pose(airsim.Vector3r(x,y-2,z6),airsim.to_quaternion(0,0,theta))
    client.simSetVehiclePose(vehicle_pose,False,vehicle_name="drone6")
    camera_pose = airsim.Pose(orientation_val=airsim.to_quaternion(math.radians(camera_pitch_angle6),0,np.pi+theta))
    client.simSetCameraPose(0,camera_pose,vehicle_name='drone6')
    vehicle_pose = airsim.Pose(airsim.Vector3r(x,y-4,z7),airsim.to_quaternion(0,0,theta))
    client.simSetVehiclePose(vehicle_pose,False,vehicle_name="drone7")
    camera_pose = airsim.Pose(orientation_val=airsim.to_quaternion(math.radians(camera_pitch_angle7),0,np.pi+theta))
    client.simSetCameraPose(0,camera_pose,vehicle_name='drone7')
    print("Camera angle are adjusted for all Drone's")
    # take images now
    #function used is:-
    #simgetImages( *make request* ,vehicle name)
    #ImageRequest(camera name, image type, pixels as float(bool), compress(bool))
    print("Drones are Taking images ...")
    responces = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name='drone6')
    response = responces[0]
    #np.reshape :- Gives a new shape to an array without changing its data.
    img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)
    img_rgb = img1d.reshape(response.height, response.width, 3)
    #naming and saving obtained image
    filename = time.strftime("%Y%m%d-6-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    responces = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name='drone7')
    response = responces[0]
    img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)
    img_rgb = img1d.reshape(response.height, response.width, 3)
    filename = time.strftime("%Y%m%d-7-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    theta=theta+0.1
print("we have completed survey procss..")
d6=client.moveToPositionAsync(0,0,-3,2,vehicle_name='drone6')
d6.join()
d7=client.moveToPositionAsync(0,0,-3,2,vehicle_name='drone7')
d7.join()
time.sleep(2)
#send drones to initial position and land
print("disarming the drones...")
client.armDisarm(False,"drone6")
client.armDisarm(False,"drone7")
#shut down the API's
client.reset()
client.enableApiControl(False,"drone6")
client.enableApiControl(False,"drone7")