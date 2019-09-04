from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import Pool
import cv2
import os
import threading
from fs import open_fs

path_root ="./test_data/"
save_path = "./test_save_images/"
# path_root = "./../../../DMS/DSM-DATA/"
# save_path = "./save_images/"

# def load_data(path_root,category):
#     for root,dirs,files in os.walk(os.path.join(path_root,category)):
#         for name in files:
#             print(os.path.join(root,name))
#         for name in dirs:
#             print(os.path.join(root,name))

def data_load_fs(path_root, category, save_path):
    root_fs = open_fs(os.path.join(path_root,category))
    for video_index,video_path in enumerate(root_fs.walk.files(filter=["*.mp4"])):
        # print(video_path)
        capture_images(path_root + category + video_path, video_index, save_path + category)

def capture_images(video_file, video_index, save_path):
    print(video_file)
    vidcap = cv2.VideoCapture(video_file)
    # print("reading drink video file: %s" %video_file)
    # print("reading drink video file: %s" %vidcap)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    success,image = vidcap.read()
    images =  []
    while success:
        success,image = vidcap.read()
        images.append(image)
        # if cv2.waitKey(10) == 27:                     # exit if Escape is hit
        #     break

    print(len(images))
    video_length = len(images)
    for num,image in enumerate(images[int(video_length * 0.25):int(video_length * 0.75) + 1]):
        cv2.imwrite("./%s/%d_%d.jpg" %(save_path, video_index, num), image)     # save frame as JPEG file
    print("images save finished!")

pool = Pool(3)

result = pool.apply_async(data_load_fs,(path_root,"drink",save_path))
future2 = pool.apply_async(data_load_fs,(path_root,"smoke",save_path))
future3 = pool.apply_async(data_load_fs,(path_root,"phone",save_path))
# data_load_fs(path_root,"drink",save_path)
# pool.join()
result.wait()  # 等待所有线程函数执行完毕

#放在这里打印可以提前预警，知道错误产生的原因
# print("ready %s" % result.ready())
# print("successful %s" % result.successful())
# print("i.get %s" % result.get())

# t1 = threading.Thread(target=data_load_fs, args=(path_root, "drink", save_path))
# t2 = threading.Thread(target=data_load_fs, args=(path_root, "smoke", save_path))
# t3 = threading.Thread(target=data_load_fs, args=(path_root, "phone", save_path))

# t1.start()
# t2.start()
# t3.start()

# t1.join()
# t2.join()
# t3.join()