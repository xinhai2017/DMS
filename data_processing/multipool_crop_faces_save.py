import dlib  # 人脸识别的库 Dlib
import cv2  # 图像处理的库 OpenCv
import os
from fs import open_fs
import threading
from multiprocessing.pool import Pool

os.environ["CUDA_VISIBLE_DEVICES"] = "0"


path_root = "../../../../chenh_data/capture_images/"

# 存储图片路径
# path_save_face = "../test_save_faces/"
path_save_face = "../../../../chenh_data/save_faces/"

# 读取图像的路径
# path_root = "./../../capture_images_from_video/test_save_images"
# path_root = "../test_save_images/"

# 存储图片路径
# path_save_face = "../test_save_faces/"


def data_load_fs(path_root, category, path_save_face):
    root_fs = open_fs(os.path.join(path_root, category))
    for image_index, image_path in enumerate(root_fs.walk.files(filter=["*.jpg"])):
        # print(image_path)
        print("Starting extract faces from ", category + image_path)
        face_cut(path_root + category + image_path, category, image_index, path_save_face + category)


def image2resizse():
    pass


def face_cut(image_path, category, image_id, save_path):
    # print(image_path)
    print("save face into ", save_path)
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # 0表示图片灰度化
    img = cv2.imread(image_path,0)
    # print("image: ",img)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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

    # if category != "smoke":
    #
    #     for num, face in enumerate(faces):
    #         # 计算矩形框大小
    #         # height = face.rect.bottom() - face.rect.top() + 150
    #         # width = face.rect.right() - face.rect.left() + 150
    #         # # 根据人脸大小生成空的图像
    #         # img_blank = np.zeros((height, width, 3), np.uint8)
    #         #
    #         # for i in range(height):
    #         #     for j in range(width):
    #         #         img_blank[i][j] = img[face.rect.top() + i][face.rect.left() - 60 + j]
    #         #
    #         # # 存在本地
    #         # # print("Save into to %s" %save_path)
    #         # cv2.imwrite("%s/%d%d.jpg" % (save_path, image_id, num), img_blank)
    #         cropped = img[face.rect.top()-40:face.rect.bottom()+40, face.rect.left()-40:face.rect.right()+40]
    #         cv2.imwrite("%s/%d%d.jpg" % (save_path, image_id, num), cropped)
    #         print("face save %s finished!" % category)
    # else:
    #     for num, face in enumerate(faces):
    #         # # 计算矩形框大小
    #         # height = face.rect.bottom() - face.rect.top() + 50
    #         # width = face.rect.right() - face.rect.left() + 50
    #         # # 根据人脸大小生成空的图像
    #         # img_blank = np.zeros((height, width, 3), np.uint8)
    #         #
    #         # for i in range(height):
    #         #     for j in range(width):
    #         #         img_blank[i][j] = img[face.rect.top() + 25 + i][face.rect.left() - 25 + j]
    #         #
    #         # # 存在本地
    #         # # print("Save into to %s" %save_path)
    #         # cv2.imwrite("%s/%d%d.jpg" % (save_path, image_id, num), img_blank)
    #         cropped = img[face.rect.top()-40:face.rect.bottom()+40, face.rect.left()-40:face.rect.right()+40]
    #         cv2.imwrite("%s/%d%d.jpg" % (save_path, image_id, num), cropped)
    #         print("face save %s finished!" % category)


# 删除文件夹中已有文件
# def clear_images():
#     imgs = os.listdir(path_save)
#
#     for img in imgs:
#         os.remove(path_save + img)
#
#     print("clean finish", '\n')


# clear_images()

pool = Pool(6)

result1 = pool.apply_async(data_load_fs,(path_root, "smoke", path_save_face))
result2 = pool.apply_async(data_load_fs,(path_root, "drink", path_save_face))
result3 = pool.apply_async(data_load_fs,(path_root, "phone", path_save_face))
result4 = pool.apply_async(data_load_fs,(path_root, "other", path_save_face))

pool.close()
pool.join()

# data_load_fs(path_root, "drink", path_save_face)

#t1 = threading.Thread(target=data_load_fs, args=(path_root, "smoke", path_save_face))
#t2 = threading.Thread(target=data_load_fs, args=(path_root, "drink", path_save_face))
#t3 = threading.Thread(target=data_load_fs, args=(path_root, "phone", path_save_face))

#t1.start()
#t2.start()
#t3.start()

#t1.join()
#t2.join()
#t3.join()