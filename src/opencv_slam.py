import cv2
import os
directory = r'/Users/samik/Desktop/Programming/DecentraliDrones/frames_tokyo'
os.chdir(directory)
cap = cv2.VideoCapture("/Users/samik/Desktop/Programming/DecentraliDrones/videoplayback.mp4")
success, image = cap.read()
frame_count = 0
while success:
    cv2.imwrite(f"/Users/samik/Desktop/Programming/DecentraliDrones/frames_tokyo/frame_{frame_count}.jpg", image)
    success, image = cap.read()
    frame_count += 1 
cap.release()
