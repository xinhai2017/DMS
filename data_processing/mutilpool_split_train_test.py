import cv2  # 图像处理的库 OpenCv
import os
from fs import open_fs
import threading
from multiprocessing.pool import Pool

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

train_test_split_vatio = 0.2

path_root = "../../../chenh_data/save_faces/"

# 存储图片路径
path_save_face = "../../../chenh_data/split_train_test_face/"


def data_load_fs(path_root, category, path_save_face):
    root_fs = open_fs(os.path.join(path_root,category))
    img_list = []
    for image_index, image_path in enumerate(root_fs.walk.files(filter=["*.jpg"])):
        # print(path_root+category+image_path)
        img_list.append(split_images(path_root+category+image_path, category,image_index,path_save_face))
    # print(len(img_list))
    split_train_test_faces(category,path_save_face,img_list)

def split_images(image_path, category, image_index, save_path):

    img = cv2.imread(image_path)

    if img is None:
        os.remove(image_path)
        print('delete error image sucessed!')
    else:
        return img

def split_train_test_faces(category, save_path,img_list):
    # pass

    if not os.path.exists(os.path.join(save_path,"train")):
        os.makedirs(os.path.join(save_path,"train"))

    if not os.path.exists(os.path.join(save_path,"test")):
        os.makedirs(os.path.join(save_path,"test"))

    test_img = img_list[: int(len(img_list) * train_test_split_vatio)]
    train_img = img_list[int(len(img_list) * train_test_split_vatio): ]
    # print("%s test_img" %category, len(test_img))
    # print("%s train_img" %category, len(train_img))

    for index,test_image in enumerate(test_img):
        cv2.imwrite("%s/test/%s.%d.jpg" % (save_path, category, index), test_image)
        # print("%s test image save finished!" %category)

    for index,train_image in enumerate(train_img):
        cv2.imwrite("%s/train/%s.%d.jpg" % (save_path, category,index), train_image)
        # print("%s train image save finished!" %category)




pool = Pool(6)

result1 = pool.apply_async(data_load_fs,(path_root, "smoke", path_save_face))
result2 = pool.apply_async(data_load_fs,(path_root, "drink", path_save_face))
result3 = pool.apply_async(data_load_fs,(path_root, "phone", path_save_face))
result4 = pool.apply_async(data_load_fs,(path_root, "other", path_save_face))

pool.close()
pool.join()

# data_load_fs(path_root,"smoke",path_save_face)

# t1 = threading.Thread(target=data_load_fs, args=(path_root, "smoke", path_save_face))
# t2 = threading.Thread(target=data_load_fs, args=(path_root, "drink", path_save_face))
# t3 = threading.Thread(target=data_load_fs, args=(path_root, "phone", path_save_face))
# t4 = threading.Thread(target=data_load_fs, args=(path_root, "other", path_save_face))
#
#
# t1.start()
# t2.start()
# t3.start()
# t4.start()
#
# t1.join()
# t2.join()
# t3.join()
# t4.join()