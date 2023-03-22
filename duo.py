import setup_path
import airsim
import sys
import time
import os
import tempfile
import numpy as np
import cv2
import pprint
import math

#---------------Connecting to Airsim , Vehical opened & API connected---------------#
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True,"Drone6")
client.enableApiControl(True,"Drone7")

#---------------Arming drone---------------#
print("arming the drone...")
client.armDisarm(True,"Drone6")
client.armDisarm(True,"Drone7")

#---------------Weather Conditions---------------#
wind = airsim.Vector3r(0,0,0)
client.simSetWind(wind)
time.sleep(1)

#---------------Taking off---------------#
d6 = client.takeoffAsync(vehicle_name="Drone6")
d7 = client.takeoffAsync(vehicle_name="Drone7")
d6.join()
d7.join()

#---------------Final Hover Height---------------#
z6 = -150
z7 = -150
print("make sure we are hovering at 150 meters...")
d6 = client.moveToPositionAsync(0,0,z6,2,vehicle_name="Drone6")
d7 = client.moveToPositionAsync(0,0,z7,2,vehicle_name="Drone7")
d6.join()
d7.join()

#---------------Camera angles , positions and view are adjusted for drone---------------#
cam6_pitch_angle = -89
cam7_pitch_angle = -89

camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam6_pitch_angle),0,0))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone6")
print("Camera angle adjusted for Drone6")
camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam7_pitch_angle),0,0))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone7")
print("Camera angle adjusted for Drone7")

time.sleep(2)

#---------------Planed path---------------#
d = 4 #image taking differrence
s = 1 #survey drone speed
x = -3
y6 = 13
y7 = 49

print("Going To survery start Point...")
d6 = client.moveToPositionAsync(x,y6+10,z6,4,vehicle_name="Drone6")
d7 = client.moveToPositionAsync(x,y7+12,z7,4,vehicle_name="Drone7")
d6.join()
d7.join()
time.sleep(5)

print(" - - - - - Starting Survey - - - - - ")
i = 1
x = -3
while(i <= 5):
	if (x == -3) :
		while(x <= 69):
			d6 = client.moveToPositionAsync(x,y6+10,z6,s,vehicle_name="Drone6")
			d7 = client.moveToPositionAsync(x,y7+12,z7,s,vehicle_name="Drone7")
			d6.join()
			d7.join()
			print("(Drone 6) Taking images ...")
			responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name="Drone6")
			response = responses[0]
			img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
			img_rgb = img1d.reshape(response.height, response.width, 3)
			filename = time.strftime("%Y%m%d-6-%H%M%S")
			airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
			time.sleep(1)
			print("(Drone 7) Taking images ...")
			responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name="Drone7")
			response = responses[0]
			img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
			img_rgb = img1d.reshape(response.height, response.width, 3)
			filename = time.strftime("%Y%m%d-7-%H%M%S")
			airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
			time.sleep(1)
			x = x + d
		x = 69
		print("Drone Repositioning camera...")
		camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam6_pitch_angle),0,math.radians(180)))
		client.simSetCameraPose("0",camera_pose,vehicle_name="Drone6")
		print("Camera angle adjusted for Drone6")
		d6 = client.rotateToYawAsync(180,vehicle_name="Drone6")
		d6.join()
		time.sleep(1)
		camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam7_pitch_angle),0,math.radians(-180)))
		client.simSetCameraPose("0",camera_pose,vehicle_name="Drone7")
		print("Camera angle adjusted for Drone7")
		d7 = client.rotateToYawAsync(-180,vehicle_name="Drone7")
		d7.join()
		time.sleep(1)
	elif(x == 69):
		while(x >= -3):
			d6 = client.moveToPositionAsync(x,y6+10,z6,s,vehicle_name="Drone6")
			d7 = client.moveToPositionAsync(x,y7+12,z7,s,vehicle_name="Drone7")
			d6.join()
			d7.join()
			print("(Drone 6) Taking images ...")
			responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name="Drone6")
			response = responses[0]
			img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
			img_rgb = img1d.reshape(response.height, response.width, 3)
			filename = time.strftime("%Y%m%d-6-%H%M%S")
			airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
			time.sleep(1)
			print("(Drone 7) Taking images ...")
			responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name="Drone7")
			response = responses[0]
			img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
			img_rgb = img1d.reshape(response.height, response.width, 3)
			filename = time.strftime("%Y%m%d-7-%H%M%S")
			airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
			time.sleep(1)
			x = x - d
		x = -3
		print("Drone Repositioning camera...")
		camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam6_pitch_angle),0,math.radians(-180)))
		client.simSetCameraPose("0",camera_pose,vehicle_name="Drone6")
		print("Camera angle adjusted for Drone6")
		d6 = client.rotateToYawAsync(-180,vehicle_name="Drone6")
		d6.join()
		time.sleep(1)
		camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam7_pitch_angle),0,math.radians(180)))
		client.simSetCameraPose("0",camera_pose,vehicle_name="Drone7")
		print("Camera angle adjusted for Drone7")
		d7 = client.rotateToYawAsync(180,vehicle_name="Drone7")
		d7.join()
		time.sleep(1)
	i = i + 1
	y6 = y6 + 4
	y7 = y7 - 4

print("Survey Complete for Drone6 & Drone7...")

#---------------sendind home & Landing drone---------------#
d6 = client.goHomeAsync(vehicle_name="Drone6")
time.sleep(5)
d7 = client.goHomeAsync(vehicle_name="Drone7")
time.sleep(5)
d6.join()
d7.join()

#---------------Disarming Drone---------------#
print("disarming the drone...")
client.armDisarm(False,"Drone6")
client.armDisarm(False,"Drone7")

#---------------Vehical closed & API disconnected---------------#
client.reset()
client.enableApiControl(False,"Drone6")
client.enableApiControl(False,"Drone7")