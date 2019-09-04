import cv2  # 图像处理的库 OpenCv
import os
from fs import open_fs
import threading
from multiprocessing.pool import Pool

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

path_root = "./split_train_test_face/"

def data_load_fs(path_root, category):
    root_fs = open_fs(os.path.join(path_root,category))
    for image_path in root_fs.walk.files(filter=["*.jpg"]):
        # print(path_root+category+image_path)
        delete_error_images(path_root+category+image_path,category)

def delete_error_images(image_path,category):

    img = cv2.imread(image_path)

    if img is None:
        os.remove(image_path)
        print('delete %s error image sucessed!' %category)

pool = Pool(6)

result1 = pool.apply_async(data_load_fs,(path_root, "train"))
result2 = pool.apply_async(data_load_fs,(path_root, "test"))

pool.close()
pool.join()
