from multiprocessing.pool import Pool
import cv2
import os
from fs import open_fs

# 视频文件路径
path_root ="./test_data/"

# 抓取图片保存路径
save_path = "./capture_images/"

def data_load_fs(path_root, category, save_path):
    root_fs = open_fs(os.path.join(path_root,category))
    for video_index,video_path in enumerate(root_fs.walk.files(filter=["*.mp4"])):
        # print("capturing images form video: ",video_path)
        capture_images(path_root + category + video_path, video_index, save_path + category)

def capture_images(video_file, video_index, save_path):
    vidcap = cv2.VideoCapture(video_file)

    if not os.path.exists(save_path):
        os.mkdir(save_path)

    success,image = vidcap.read()

    images =  []
    while success:
        success,image = vidcap.read()
        images.append(image)

    video_length = len(images)

    for num, image in enumerate(images[int(video_length * 0.25): int(video_length * 0.75) + 1]):
        cv2.imwrite("./%s/new%d%d.jpg" %(save_path, video_index, num), image)     # save frame as JPEG file

    print("images save finished!")

pool = Pool(3)

result = pool.apply_async(data_load_fs,(path_root,"drink",save_path))
future2 = pool.apply_async(data_load_fs,(path_root,"smoke",save_path))
future3 = pool.apply_async(data_load_fs,(path_root,"phone",save_path))

pool.close()
pool.join()

