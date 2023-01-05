#python script to implement slam algorithm and use it with airsim

import airsim
import numpy as np
import cv2
import time
import os
import tempfile


# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# Async methods returns Future. Call join() to wait for task to complete.
client.takeoffAsync().join()
client.moveToPositionAsync(-10, 10, -10, 5).join()

def get_image():
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthVis, False, False)])
    response = responses[0]
    img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)
    img_rgb = img1d.reshape(response.height, response.width, 3)
    return img_rgb

def get_depth():
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthPlanar, True)])
    response = responses[0]
    img1d = np.array(response.image_data_float, dtype=np.cfloat)
    img1d = 255/np.maximum(np.ones(img1d.size), img1d)
    img2d = np.reshape(img1d, (response.height, response.width))
    return img2d

def get_pose():
    pose = client.simGetVehiclePose()
    return pose

def slam():
    # initialize ORB detector
    orb = cv2.ORB_create()

    # initialize BFMatcher object using default params
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # initialize first frame
    first_frame = get_image()
    first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
    first_frame = cv2.resize(first_frame, (0,0), fx=0.5, fy=0.5)
    kp1, des1 = orb.detectAndCompute(first_frame, None)

    # initialize first pose
    first_pose = get_pose()

    # initialize first depth
    first_depth = get_depth()

    while True:
        # get current frame
        frame = get_image()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        kp2, des2 = orb.detectAndCompute(frame, None)

        # match descriptors
        matches = bf.match(des1, des2)

        # sort them in the order of their distance
        matches = sorted(matches, key = lambda x:x.distance)

        # draw first 10 matches
        img3 = cv2.drawMatches(first_frame, kp1, frame, kp2, matches[:10], None, flags=2)

        # show the image
        cv2.imshow('image', img3)
        cv2.waitKey(1)

        # get current pose
        pose = get_pose()

        # get current depth
        depth = get_depth()

        # calculate change in pose
        delta_x = pose.position.x_val - first_pose.position.x_val
        delta_y = pose.position.y_val - first_pose.position.y_val
        delta_z = pose.position.z_val - first_pose.position.z_val

        # calculate change in depth
        delta_depth = depth - first_depth

        # calculate change in rotation
        delta_qx = pose.orientation.x_val - first_pose.orientation.x_val
        delta_qy = pose.orientation.y_val - first_pose.orientation.y_val
        delta_qz = pose.orientation.z_val - first_pose.orientation.z_val
        delta_qw = pose.orientation.w_val - first_pose.orientation.w_val

        # update first frame
        first_frame = frame

        # update first pose
        first_pose = pose

        # update first depth
        first_depth = depth

        # print change in pose
        print(delta_x, delta_y, delta_z)

        # print change in depth
        print(delta_depth)

        # print change in rotation
        print(delta_qx, delta_qy, delta_qz, delta_qw)

        # wait for 1 second
        time.sleep(1)

# function to dodge obstacles
def dodge_obstacles():
    # get current pose
    pose = get_pose()

    # get current depth
    depth = get_depth()

    # get current frame
    frame = get_image()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)

    # get current position
    x = pose.position.x_val
    y = pose.position.y_val
    z = pose.position.z_val

    # get current rotation
    qx = pose.orientation.x_val
    qy = pose.orientation.y_val
    qz = pose.orientation.z_val
    qw = pose.orientation.w_val

    # get current depth
    d = depth[100, 100]

    # if depth is less than 2m
    if d < 2:
        # move up
        client.moveByVelocityAsync(0, 0, 1, 1).join()
        # move forward
        client.moveByVelocityAsync(1, 0, 0, 1).join()
        # move down
        client.moveByVelocityAsync(0, 0, -1, 1).join()
        # move backward
        client.moveByVelocityAsync(-1, 0, 0, 1).join()

    # if depth is greater than 2m
    else:
        # move forward
        client.moveByVelocityAsync(1, 0, 0, 1).join()

    # wait for 1 second
    time.sleep(1)

# function to land the drone safely
def land():
    # get current pose
    pose = get_pose()

    # get current position
    x = pose.position.x_val
    y = pose.position.y_val
    z = pose.position.z_val

    # if drone is above 1m
    if z > 1:
        # move down
        client.moveByVelocityAsync(0, 0, -1, 1).join()

    # if drone is below 1m
    else:
        # land
        client.landAsync().join()

while True:
    slam()
    dodge_obstacles()
    land()

# disconnect from the drone
client.enableApiControl(False)
client.armDisarm(False)

# reset the drone
client.reset()
