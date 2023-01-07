import cv2
import os

VIDEO_NAME = 'tokyo_small'

directory = r'videos'
os.chdir(directory)
capture = cv2.VideoCapture(os.path.abspath(os.path.join(os.getcwd(), f'{VIDEO_NAME}.mp4')))

if not capture.isOpened():
    print("could not open")
    exit()

fps = capture.get(cv2.CAP_PROP_FPS)
print('frames per second =', fps)

frame_count = 0 # the frame count 
div_fact = 30 # how many frames are skipped until next frame is saved
i = 0 # frame id

while capture.isOpened():
    sucess, image = capture.read()
    
    if sucess and frame_count == 0:
        cv2.imwrite(f'./sim/videos/{VIDEO_NAME}_frames/frame_{i}.jpg', img=image)
        cv2.imwrite(os.path.abspath(os.path.join(os.getcwd(), f'{VIDEO_NAME}_frames/frame_{i}.jpg')), img=image)
        i+=1
        
    elif not sucess: 
        print("Err")
        break
    
    frame_count = (frame_count + 1) % div_fact
    if cv2.waitKey(1) & 0xFF == ord('z'): break

capture.release()
