import dlib  # 人脸识别的库 Dlib
import cv2  # 图像处理的库 OpenCv
import os
from fs import open_fs
import threading
from multiprocessing.pool import Pool

os.environ["CUDA_VISIBLE_DEVICES"] = "0"


path_root = "./capture_images/"

# 存储图片路径
path_save_face = "./save_faces/"

def data_load_fs(path_root, category, path_save_face):
    root_fs = open_fs(os.path.join(path_root, category))
    for image_index, image_path in enumerate(root_fs.walk.files(filter=["*.jpg"])):
        # print(image_path)
        print("Starting extract faces from ", category + image_path)
        face_cut(path_root + category + image_path, category, image_index, path_save_face + category)

def face_cut(image_path, category, image_id, save_path):
    # print(image_path)
    print("save face into ", save_path)
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # 0表示图片灰度化
    img = cv2.imread(image_path,0)
   
    # Dlib预测器
    detector_path = os.path.join('./data/dlib/', 'mmod_human_face_detector.dat')
    print("Load modeling!")
    detector = dlib.cnn_face_detection_model_v1(detector_path)

    # 检测人脸数量
    faces = detector(img, 1)

    for num, face in enumerate(faces):
        cropped = img[face.rect.top()-50:face.rect.bottom()+50, face.rect.left()-50:face.rect.right()+50]
        cv2.imwrite("%s/%d%d.jpg" % (save_path, image_id, num), cropped)
        print("face save %s finished!" % category)

pool = Pool(6)

result1 = pool.apply_async(data_load_fs,(path_root, "smoke", path_save_face))
result2 = pool.apply_async(data_load_fs,(path_root, "drink", path_save_face))
result3 = pool.apply_async(data_load_fs,(path_root, "phone", path_save_face))
result4 = pool.apply_async(data_load_fs,(path_root, "other", path_save_face))

pool.close()
pool.join()
