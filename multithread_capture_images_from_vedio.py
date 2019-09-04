import cv2
import os
import threading
from fs import open_fs

# path_root ="./test_data/"
# save_path = "./test_save_images/"
path_root = "./../../../DMS/DSM-DATA/"
save_path = "./save_images/"

# def load_data(path_root,category):
#     for root,dirs,files in os.walk(os.path.join(path_root,category)):
#         for name in files:
#             print(os.path.join(root,name))
#         for name in dirs:
#             print(os.path.join(root,name))

def data_load_fs(path_root, category, save_path):
    root_fs = open_fs(os.path.join(path_root,category))
    for video_index,video_path in enumerate(root_fs.walk.files(filter=["*.mp4"])):
        print(video_path)
        capture_images(path_root + category + video_path, video_index, save_path + category)

def capture_images(video_file, video_index, save_path):
    print(video_file)
    vidcap = cv2.VideoCapture(video_file)
    print("reading drink video file: %s" %vidcap)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    success,image = vidcap.read()
    images =  []
    while success:
        success,image = vidcap.read()
        images.append(image)
        if cv2.waitKey(10) == 27:                     # exit if Escape is hit
            break
    # print(images)
    for num,image in enumerate(images[25:-25]):
        cv2.imwrite("./%s/%d_%d.jpg" %(save_path, video_index,num), image)     # save frame as JPEG file
    print("images save finished!")

t1 = threading.Thread(target=data_load_fs, args=(path_root, "drink", save_path))
t2 = threading.Thread(target=data_load_fs, args=(path_root, "smoke", save_path))
t3 = threading.Thread(target=data_load_fs, args=(path_root, "phone", save_path))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()