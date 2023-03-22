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
client.enableApiControl(True,"Drone1")
client.enableApiControl(True,"Drone2")
client.enableApiControl(True,"Drone3")
client.enableApiControl(True,"Drone4")
client.enableApiControl(True,"Drone5")

#---------------Arming drone---------------#
print("arming the drone...")
client.armDisarm(True,"Drone1")
client.armDisarm(True,"Drone2")
client.armDisarm(True,"Drone3")
client.armDisarm(True,"Drone4")
client.armDisarm(True,"Drone5")

#---------------Weather Conditions---------------#
wind = airsim.Vector3r(0,0,0)
client.simSetWind(wind)
time.sleep(1)

#---------------Taking off---------------#
d1 = client.takeoffAsync(vehicle_name="Drone1")

d2 = client.takeoffAsync(vehicle_name="Drone2")
d3 = client.takeoffAsync(vehicle_name="Drone3")
d4 = client.takeoffAsync(vehicle_name="Drone4")
d5 = client.takeoffAsync(vehicle_name="Drone5")
d1.join()
d2.join()
d3.join()
d4.join()
d5.join()

#---------------Final Hover Height---------------#
z1 = -30
z2 = -60
z3 = -90
z4 = -120
z5 = -180
print("make sure we are hovering at 3 , 6 , 9 , 12 and 18 meters respectively...")
d1 = client.moveToPositionAsync(0,0,z1,2,vehicle_name="Drone1")
d2 = client.moveToPositionAsync(0,0,z2,2,vehicle_name="Drone2")
d3 = client.moveToPositionAsync(0,0,z3,2,vehicle_name="Drone3")
d4 = client.moveToPositionAsync(0,0,z4,2,vehicle_name="Drone4")
d5 = client.moveToPositionAsync(0,0,z5,2,vehicle_name="Drone5")
d1.join()
d2.join()
d3.join()
d4.join()
d5.join()

#---------------Camera angles , positions and view are adjusted for drone---------------#
cam1_pitch_angle = -5
cam2_pitch_angle = -13         #-13
cam3_pitch_angle = -21           #-21
cam4_pitch_angle = -27           #-27
cam5_pitch_angle = -33         #-33

#---------------Planed path---------------#
d = 3 #image taking differrence
s = 1 #survey drone speed

print(" - - - - - Starting Survey - - - - - ")

camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam1_pitch_angle),0,0))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone1")
print("Camera angle adjusted for Drone1")
time.sleep(1)

camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam2_pitch_angle),0,0))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone2")
print("Camera angle adjusted for Drone2")
time.sleep(1)

camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam3_pitch_angle),0,0))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone3")
print("Camera angle adjusted for Drone3")
time.sleep(1)

camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam4_pitch_angle),0,0))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone4")

print("Camera angle adjusted for Drone4")
time.sleep(1)

camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam5_pitch_angle),0,0))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone5")
print("Camera angle adjusted for Drone5")
time.sleep(1)


print("Going To 1st survery Point...")
x = -3
y = 5
# x = -3  y = 56
while(y <= 56):
    print("Going to next location to take images ...")
    d1 = client.moveToPositionAsync(x,y,z1,s,vehicle_name="Drone1")
    d2 = client.moveToPositionAsync(x,y+2,z2,s,vehicle_name="Drone2")
    d3 = client.moveToPositionAsync(x,y+4,z3,s,vehicle_name="Drone3")
    d4 = client.moveToPositionAsync(x,y+6,z4,s,vehicle_name="Drone4")
    d5 = client.moveToPositionAsync(x,y+8,z5,s,vehicle_name="Drone5")
    d1.join()
    d2.join()
    d3.join()
    d4.join()
    d5.join()
    time.sleep(1)

    print("(Drone 1) Taking RGB images ...")
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name="Drone1")
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
    img_rgb = img1d.reshape(response.height, response.width, 3)
    filename = time.strftime("%Y%m%d-1-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    # print("(Drone 1) Taking Depth images ...")
    # responses_depth = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, False, False)],vehicle_name="Drone1")
    # response_depth = responses_depth[0]
    # img1d = np.frombuffer(response_depth.image_data_uint8, dtype=np.uint8) 
    # img_depth = img1d.reshape(response_depth.height, response_depth.width, 3)
    # filename = time.strftime("1-%H%M%S-Depth")
    # airsim.write_png(os.path.normpath(filename + '.png'), img_depth)
    

    print("(Drone 2) Taking images ...")
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name="Drone2")
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
    img_rgb = img1d.reshape(response.height, response.width, 3)
    filename = time.strftime("%Y%m%d-2-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    # print("(Drone 2) Taking Depth images ...")
    # responses_depth = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, False, False)],vehicle_name="Drone2")
    # response_depth = responses_depth[0]
    # img1d = np.frombuffer(response_depth.image_data_uint8, dtype=np.uint8) 
    # img_depth = img1d.reshape(response_depth.height, response_depth.width, 3)
    # filename = time.strftime("2-%H%M%S-Depth")
    # airsim.write_png(os.path.normpath(filename + '.png'), img_depth)
    
    print("(Drone 3) Taking images ...")
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name="Drone3")
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
    img_rgb = img1d.reshape(response.height, response.width, 3)
    filename = time.strftime("%Y%m%d-3-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    # print("(Drone 3) Taking Depth images ...")
    # responses_depth = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, False, False)],vehicle_name="Drone3")
    # response_depth = responses_depth[0]
    # img1d = np.frombuffer(response_depth.image_data_uint8, dtype=np.uint8) 
    # img_depth = img1d.reshape(response_depth.height, response_depth.width, 3)
    # filename = time.strftime("3-%H%M%S-Depth")
    # airsim.write_png(os.path.normpath(filename + '.png'), img_depth)
    
    
    print("(Drone 4) Taking images ...")
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name="Drone4")
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
    img_rgb = img1d.reshape(response.height, response.width, 3)
    filename = time.strftime("%Y%m%d-4-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    # print("(Drone 4) Taking Depth images ...")
    # responses_depth = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, False, False)],vehicle_name="Drone4")
    # response_depth = responses_depth[0]
    # img1d = np.frombuffer(response_depth.image_data_uint8, dtype=np.uint8) 
    # img_depth = img1d.reshape(response_depth.height, response_depth.width, 3)
    # filename = time.strftime("4-%H%M%S-Depth")
    # airsim.write_png(os.path.normpath(filename + '.png'), img_depth)
    
    
    print("(Drone 5) Taking images ...")
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name="Drone5")
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
    img_rgb = img1d.reshape(response.height, response.width, 3)
    filename = time.strftime("%Y%m%d-5-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    # print("(Drone 5) Taking Depth images ...")
    # responses_depth = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, False, False)],vehicle_name="Drone5")
    # response_depth = responses_depth[0]
    # img1d = np.frombuffer(response_depth.image_data_uint8, dtype=np.uint8) 
    # img_depth = img1d.reshape(response_depth.height, response_depth.width, 3)
    # filename = time.strftime("5-%H%M%S-Depth")
    # airsim.write_png(os.path.normpath(filename + '.png'), img_depth)
    
    
    time.sleep(1)

    y = y + d

camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam1_pitch_angle),0,math.radians(-90)))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone1")
print("Camera angle adjusted for Drone1")
d1 = client.rotateToYawAsync(-90,vehicle_name="Drone1")

camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam2_pitch_angle),0,math.radians(-90)))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone2")
print("Camera angle adjusted for Drone2")
d2 = client.rotateToYawAsync(-90,vehicle_name="Drone2")

camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam3_pitch_angle),0,math.radians(-90)))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone3")
print("Camera angle adjusted for Drone3")
d3 = client.rotateToYawAsync(-90,vehicle_name="Drone3")

camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam4_pitch_angle),0,math.radians(-90)))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone4")
print("Camera angle adjusted for Drone4")
d4 = client.rotateToYawAsync(-90,vehicle_name="Drone4")

camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam5_pitch_angle),0,math.radians(-90)))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone5")
print("Camera angle adjusted for Drone4")
d5 = client.rotateToYawAsync(-90,vehicle_name="Drone5")

d1.join()
d2.join()
d3.join()
d4.join()
d5.join()

print("Going To 2nd survery Point...")
x = -3
y = 56
# x = 69  y = 56
while(x <= 69):
    print("Going to next location to take images ...")
    d1 = client.moveToPositionAsync(x,y,z1,s,vehicle_name="Drone1")
    d2 = client.moveToPositionAsync(x,y+2,z2,s,vehicle_name="Drone2")
    d3 = client.moveToPositionAsync(x,y+4,z3,s,vehicle_name="Drone3")
    d4 = client.moveToPositionAsync(x,y+6,z4,s,vehicle_name="Drone4")
    d5 = client.moveToPositionAsync(x,y+8,z5,s,vehicle_name="Drone5")
    d1.join()
    d2.join()
    d3.join()
    d4.join()
    d5.join()
    time.sleep(1)

    print("(Drone 1) Taking images ...")
    responses = client.simGetImages([airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)],vehicle_name="Drone1")
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
    img_rgb = img1d.reshape(response.height, response.width, 3)
    filename = time.strftime("%Y%m%d-1-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    # print("(Drone 1) Taking Depth images ...")
    # responses_depth = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, False, False)],vehicle_name="Drone1")
    # response_depth = responses_depth[0]
    # img1d = np.frombuffer(response_depth.image_data_uint8, dtype=np.uint8) 
    # img_depth = img1d.reshape(response_depth.height, response_depth.width, 3)
    # filename = time.strftime("1-%H%M%S-Depth")
    # airsim.write_png(os.path.normpath(filename + '.png'), img_depth)
    
    
    print("(Drone 2) Taking images ...")
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name="Drone2")
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
    img_rgb = img1d.reshape(response.height, response.width, 3)
    filename = time.strftime("%Y%m%d-2-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    # print("(Drone 2) Taking Depth images ...")
    # responses_depth = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, False, False)],vehicle_name="Drone2")
    # response_depth = responses_depth[0]
    # img1d = np.frombuffer(response_depth.image_data_uint8, dtype=np.uint8) 
    # img_depth = img1d.reshape(response_depth.height, response_depth.width, 3)
    # filename = time.strftime("2-%H%M%S-Depth")
    # airsim.write_png(os.path.normpath(filename + '.png'), img_depth)
     
    print("(Drone 3) Taking images ...")
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name="Drone3")
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
    img_rgb = img1d.reshape(response.height, response.width, 3)
    filename = time.strftime("%Y%m%d-3-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    # print("(Drone 3) Taking Depth images ...")
    # responses_depth = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, False, False)],vehicle_name="Drone3")
    # response_depth = responses_depth[0]
    # img1d = np.frombuffer(response_depth.image_data_uint8, dtype=np.uint8) 
    # img_depth = img1d.reshape(response_depth.height, response_depth.width, 3)
    # filename = time.strftime("3-%H%M%S-Depth")
    # airsim.write_png(os.path.normpath(filename + '.png'), img_depth)
    
    
    print("(Drone 4) Taking images ...")
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name="Drone4")
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
    img_rgb = img1d.reshape(response.height, response.width, 3)
    filename = time.strftime("%Y%m%d-4-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    # print("(Drone 4) Taking Depth images ...")
    # responses_depth = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, False, False)],vehicle_name="Drone4")
    # response_depth = responses_depth[0]
    # img1d = np.frombuffer(response_depth.image_data_uint8, dtype=np.uint8) 
    # img_depth = img1d.reshape(response_depth.height, response_depth.width, 3)
    # filename = time.strftime("4-%H%M%S-Depth")
    # airsim.write_png(os.path.normpath(filename + '.png'), img_depth)
    
    
    print("(Drone 5) Taking images ...")
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name="Drone5")
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
    img_rgb = img1d.reshape(response.height, response.width, 3)
    filename = time.strftime("%Y%m%d-5-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    # print("(Drone 5) Taking Depth images ...")
    # responses_depth = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, False, False)],vehicle_name="Drone5")
    # response_depth = responses_depth[0]
    # img1d = np.frombuffer(response_depth.image_data_uint8, dtype=np.uint8) 
    # img_depth = img1d.reshape(response_depth.height, response_depth.width, 3)
    # filename = time.strftime("5-%H%M%S-Depth")
    # airsim.write_png(os.path.normpath(filename + '.png'), img_depth)
    
    
    time.sleep(1)
    
    x = x + d

camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam1_pitch_angle),0,math.radians(-180)))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone1")

print("Camera angle adjusted for Drone1")
d1 = client.rotateToYawAsync(-180,vehicle_name="Drone1")
camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam2_pitch_angle),0,math.radians(-180)))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone2")

print("Camera angle adjusted for Drone2")
d2 = client.rotateToYawAsync(-180,vehicle_name="Drone2")
camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam3_pitch_angle),0,math.radians(-180)))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone3")

print("Camera angle adjusted for Drone3")
d3 = client.rotateToYawAsync(-180,vehicle_name="Drone3")
camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam4_pitch_angle),0,math.radians(-180)))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone4")

print("Camera angle adjusted for Drone4")
d4 = client.rotateToYawAsync(-180,vehicle_name="Drone4")
camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam5_pitch_angle),0,math.radians(-180)))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone5")

print("Camera angle adjusted for Drone5")
d5 = client.rotateToYawAsync(-180,vehicle_name="Drone5")

d1.join()
d2.join()
d3.join()
d4.join()
d5.join()

print("Going To 3rd survery Point...")
x = 69
y = 56
# x = 69  y = 5
while(y >= 5):
    print("Going to next location to take images ...")
    d1 = client.moveToPositionAsync(x,y,z1,s,vehicle_name="Drone1")
    d2 = client.moveToPositionAsync(x,y+2,z2,s,vehicle_name="Drone2")
    d3 = client.moveToPositionAsync(x,y+4,z3,s,vehicle_name="Drone3")
    d4 = client.moveToPositionAsync(x,y+6,z4,s,vehicle_name="Drone4")
    d5 = client.moveToPositionAsync(x,y+8,z5,s,vehicle_name="Drone5")
    d1.join()
    d2.join()
    d3.join()
    d4.join()
    d5.join()
    time.sleep(1)

    print("(Drone 1) Taking images ...")
    responses = client.simGetImages([airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)],vehicle_name="Drone1")
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
    img_rgb = img1d.reshape(response.height, response.width, 3)
    filename = time.strftime("%Y%m%d-1-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    # print("(Drone 1) Taking Depth images ...")
    # responses_depth = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, False, False)],vehicle_name="Drone1")
    # response_depth = responses_depth[0]
    # img1d = np.frombuffer(response_depth.image_data_uint8, dtype=np.uint8) 
    # img_depth = img1d.reshape(response_depth.height, response_depth.width, 3)
    # filename = time.strftime("1-%H%M%S-Depth")
    # airsim.write_png(os.path.normpath(filename + '.png'), img_depth)
        
    print("(Drone 2) Taking images ...")
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name="Drone2")
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
    img_rgb = img1d.reshape(response.height, response.width, 3)
    filename = time.strftime("%Y%m%d-2-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    # print("(Drone 2) Taking Depth images ...")
    # responses_depth = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, False, False)],vehicle_name="Drone2")
    # response_depth = responses_depth[0]
    # img1d = np.frombuffer(response_depth.image_data_uint8, dtype=np.uint8) 
    # img_depth = img1d.reshape(response_depth.height, response_depth.width, 3)
    # filename = time.strftime("2-%H%M%S-Depth")
    # airsim.write_png(os.path.normpath(filename + '.png'), img_depth)
    
    
    print("(Drone 3) Taking images ...")
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name="Drone3")
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
    img_rgb = img1d.reshape(response.height, response.width, 3)
    filename = time.strftime("%Y%m%d-3-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    # print("(Drone 3) Taking Depth images ...")
    # responses_depth = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, False, False)],vehicle_name="Drone3")
    # response_depth = responses_depth[0]
    # img1d = np.frombuffer(response_depth.image_data_uint8, dtype=np.uint8) 
    # img_depth = img1d.reshape(response_depth.height, response_depth.width, 3)
    # filename = time.strftime("3-%H%M%S-Depth")
    # airsim.write_png(os.path.normpath(filename + '.png'), img_depth)

    
    print("(Drone 4) Taking images ...")
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name="Drone4")
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
    img_rgb = img1d.reshape(response.height, response.width, 3)
    filename = time.strftime("%Y%m%d-4-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    # print("(Drone 4) Taking Depth images ...")
    # responses_depth = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, False, False)],vehicle_name="Drone4")
    # response_depth = responses_depth[0]
    # img1d = np.frombuffer(response_depth.image_data_uint8, dtype=np.uint8) 
    # img_depth = img1d.reshape(response_depth.height, response_depth.width, 3)
    # filename = time.strftime("4-%H%M%S-Depth")
    # airsim.write_png(os.path.normpath(filename + '.png'), img_depth)
    
    
    print("(Drone 5) Taking images ...")
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name="Drone5")
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
    img_rgb = img1d.reshape(response.height, response.width, 3)
    filename = time.strftime("%Y%m%d-5-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    # print("(Drone 5) Taking Depth images ...")
    # responses_depth = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, False, False)],vehicle_name="Drone5")
    # response_depth = responses_depth[0]
    # img1d = np.frombuffer(response_depth.image_data_uint8, dtype=np.uint8) 
    # img_depth = img1d.reshape(response_depth.height, response_depth.width, 3)
    # filename = time.strftime("5-%H%M%S-Depth")
    # airsim.write_png(os.path.normpath(filename + '.png'), img_depth)
    
    
    time.sleep(1)
    time.sleep(1)

    y = y - d

camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam1_pitch_angle),0,math.radians(-270)))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone1")
print("Camera angle adjusted for Drone1")
d1 = client.rotateToYawAsync(-270,vehicle_name="Drone1")
camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam2_pitch_angle),0,math.radians(-270)))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone2")
print("Camera angle adjusted for Drone2")
d2 = client.rotateToYawAsync(-270,vehicle_name="Drone2")
camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam3_pitch_angle),0,math.radians(-270)))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone3")
print("Camera angle adjusted for Drone3")
d3 = client.rotateToYawAsync(-270,vehicle_name="Drone3")
camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam4_pitch_angle),0,math.radians(-270)))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone4")
print("Camera angle adjusted for Drone4")
d4 = client.rotateToYawAsync(-270,vehicle_name="Drone4")

camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam5_pitch_angle),0,math.radians(-270)))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone5")
print("Camera angle adjusted for Drone4")
d5 = client.rotateToYawAsync(-270,vehicle_name="Drone5")

d1.join()
d2.join()
d3.join()
d4.join()
d5.join()

print("Going To 1st survery Point...")
x = 69
y = 5
# x = -3  y = 5
while(x >= -3):
    print("Going to next location to take images ...")
    d1 = client.moveToPositionAsync(x,y,z1,s,vehicle_name="Drone1")
    d2 = client.moveToPositionAsync(x,y+2,z2,s,vehicle_name="Drone2")
    d3 = client.moveToPositionAsync(x,y+4,z3,s,vehicle_name="Drone3")
    d4 = client.moveToPositionAsync(x,y+6,z4,s,vehicle_name="Drone4")
    d5 = client.moveToPositionAsync(x,y+8,z5,s,vehicle_name="Drone5")
    d1.join()
    d2.join()
    d3.join()
    d4.join()
    d5.join()
    time.sleep(1)

    print("(Drone 1) Taking images ...")
    responses = client.simGetImages([airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)],vehicle_name="Drone1")
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
    img_rgb = img1d.reshape(response.height, response.width, 3)
    filename = time.strftime("%Y%m%d-1-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    # print("(Drone 1) Taking Depth images ...")
    # responses_depth = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, False, False)],vehicle_name="Drone1")
    # response_depth = responses_depth[0]
    # img1d = np.frombuffer(response_depth.image_data_uint8, dtype=np.uint8) 
    # img_depth = img1d.reshape(response_depth.height, response_depth.width, 3)
    # filename = time.strftime("1-%H%M%S-Depth")
    # airsim.write_png(os.path.normpath(filename + '.png'), img_depth)
    
    

    print("(Drone 2) Taking images ...")
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name="Drone2")
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
    img_rgb = img1d.reshape(response.height, response.width, 3)
    filename = time.strftime("%Y%m%d-2-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    # print("(Drone 2) Taking Depth images ...")
    # responses_depth = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, False, False)],vehicle_name="Drone2")
    # response_depth = responses_depth[0]
    # img1d = np.frombuffer(response_depth.image_data_uint8, dtype=np.uint8) 
    # img_depth = img1d.reshape(response_depth.height, response_depth.width, 3)
    # filename = time.strftime("2-%H%M%S-Depth")
    # airsim.write_png(os.path.normpath(filename + '.png'), img_depth)
    
    print("(Drone 3) Taking images ...")
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name="Drone3")
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
    img_rgb = img1d.reshape(response.height, response.width, 3)
    filename = time.strftime("%Y%m%d-3-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    # print("(Drone 3) Taking Depth images ...")
    # responses_depth = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, False, False)],vehicle_name="Drone3")
    # response_depth = responses_depth[0]
    # img1d = np.frombuffer(response_depth.image_data_uint8, dtype=np.uint8) 
    # img_depth = img1d.reshape(response_depth.height, response_depth.width, 3)
    # filename = time.strftime("3-%H%M%S-Depth")
    # airsim.write_png(os.path.normpath(filename + '.png'), img_depth)
    
    
    print("(Drone 4) Taking images ...")
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name="Drone4")
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
    img_rgb = img1d.reshape(response.height, response.width, 3)
    filename = time.strftime("%Y%m%d-4-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    # print("(Drone 4) Taking Depth images ...")
    # responses_depth = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, False, False)],vehicle_name="Drone4")
    # response_depth = responses_depth[0]
    # img1d = np.frombuffer(response_depth.image_data_uint8, dtype=np.uint8) 
    # img_depth = img1d.reshape(response_depth.height, response_depth.width, 3)
    # filename = time.strftime("4-%H%M%S-Depth")
    # airsim.write_png(os.path.normpath(filename + '.png'), img_depth)
    
    
    print("(Drone 5) Taking images ...")
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],vehicle_name="Drone5")
    response = responses[0]
    img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
    img_rgb = img1d.reshape(response.height, response.width, 3)
    filename = time.strftime("%Y%m%d-5-%H%M%S")
    airsim.write_png(os.path.normpath(filename + '.png'), img_rgb)
    # print("(Drone 1) Taking Depth images ...")
    # responses_depth = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, False, False)],vehicle_name="Drone5")
    # response_depth = responses_depth[0]
    # img1d = np.frombuffer(response_depth.image_data_uint8, dtype=np.uint8) 
    # img_depth = img1d.reshape(response_depth.height, response_depth.width, 3)
    # filename = time.strftime("5-%H%M%S-Depth")
    # airsim.write_png(os.path.normpath(filename + '.png'), img_depth)
    
    
    time.sleep(1)
    time.sleep(1)

    x = x - d

angle = -360
camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam1_pitch_angle),0,math.radians(angle)))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone1")

print("Camera angle adjusted for Drone1")
d1 = client.rotateToYawAsync(angle,vehicle_name="Drone1")
camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam2_pitch_angle),0,math.radians(angle)))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone2")

print("Camera angle adjusted for Drone2")
d2 = client.rotateToYawAsync(angle,vehicle_name="Drone2")
camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam3_pitch_angle),0,math.radians(angle)))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone3")

print("Camera angle adjusted for Drone3")
d3 = client.rotateToYawAsync(angle,vehicle_name="Drone3")
camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam4_pitch_angle),0,math.radians(angle)))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone4")

print("Camera angle adjusted for Drone4")
d4 = client.rotateToYawAsync(angle,vehicle_name="Drone4")
camera_pose = airsim.Pose(airsim.Vector3r(0,0,0),airsim.to_quaternion(math.radians(cam5_pitch_angle),0,math.radians(angle)))
client.simSetCameraPose("0",camera_pose,vehicle_name="Drone5")

print("Camera angle adjusted for Drone5")
d5 = client.rotateToYawAsync(angle,vehicle_name="Drone5")

d1.join()
d2.join()
d3.join()
d4.join()
d5.join()

time.sleep(2)

print("Survey Complete for Drone1 , Drone2 , Drone3 , Drone4 & Drone5...")

#---------------sendind home & Landing drone---------------#
d1 = client.goHomeAsync(vehicle_name="Drone1")
time.sleep(5)

d2 = client.goHomeAsync(vehicle_name="Drone2")
time.sleep(5)

d3 = client.goHomeAsync(vehicle_name="Drone3")
time.sleep(5)

d4 = client.goHomeAsync(vehicle_name="Drone4")
time.sleep(5)

d5 = client.goHomeAsync(vehicle_name="Drone5")
time.sleep(5)

d1.join()
d2.join()
d3.join()
d4.join()
d5.join()

#---------------Disarming Drone---------------#
print("disarming the drone...")
client.armDisarm(False,"Drone1")
client.armDisarm(False,"Drone2")
client.armDisarm(False,"Drone3")
client.armDisarm(False,"Drone4")
client.armDisarm(False,"Drone5")

#---------------Vehical closed & API disconnected---------------#
client.reset()
client.enableApiControl(False,"Drone1")
client.enableApiControl(False,"Drone2")
client.enableApiControl(False,"Drone3")
client.enableApiControl(False,"Drone4")
client.enableApiControl(False,"Drone5")