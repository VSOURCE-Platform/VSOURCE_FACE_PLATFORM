import os
import time

import cv2
import numpy as np
import tensorflow
import keras
from keras.applications.imagenet_utils import preprocess_input

from nets.retinaface import RetinaFace
from utils.anchors import Anchors
from utils.config import cfg_mnet, cfg_re50
from utils.utils import BBoxUtility, letterbox_image, retinaface_correct_boxes


#------------------------------------#
#   请注意主干网络与预训练权重的对应
#   即注意修改model_path和backbone
#------------------------------------#
class Retinaface(object):
    _defaults = {
        "model_path"        : 'model_data/retinaface_mobilenet025.h5',
        "backbone"          : 'mobilenet',
        "confidence"        : 0.5,
        "nms_iou"           : 0.45,
        #----------------------------------------------------------------------#
        #   是否需要进行图像大小限制。
        #   开启后，会将输入图像的大小限制为input_shape。否则使用原图进行预测。
        #   keras代码中主干为mobilenet时存在小bug，当输入图像的宽高不为32的倍数
        #   会导致检测结果偏差，主干为resnet50不存在此问题。
        #   可根据输入图像的大小自行调整input_shape，注意为32的倍数，如[640, 640, 3]
        #----------------------------------------------------------------------#
        "input_shape"       : [1280, 1280, 3],
        "letterbox_image"   : False
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    #---------------------------------------------------#
    #   初始化Retinaface
    #---------------------------------------------------#
    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        if self.backbone == "mobilenet":
            self.cfg = cfg_mnet
        else:
            self.cfg = cfg_re50
        self.bbox_util = BBoxUtility(nms_thresh=self.nms_iou)
        self.generate()
        self.anchors = Anchors(self.cfg, image_size=(self.input_shape[0], self.input_shape[1])).get_anchors()

    def generate(self):
        model_path = os.path.expanduser(self.model_path)
        assert model_path.endswith('.h5'), 'Keras model or weights must be a .h5 file.'

        self.retinaface = RetinaFace(self.cfg, self.backbone)
        self.retinaface.load_weights(self.model_path,by_name=True)
        print('{} model, anchors, and classes loaded.'.format(model_path))

    def detect_image(self, image):
        old_image = image.copy()

        image = np.array(image, np.float32)
        im_height, im_width, _ = np.shape(image)

        scale = [np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0]]
        scale_for_landmarks = [np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
                                            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
                                            np.shape(image)[1], np.shape(image)[0]]

        if self.letterbox_image:
            image = letterbox_image(image, [self.input_shape[1], self.input_shape[0]])
        else:
            self.anchors = Anchors(self.cfg, image_size=(im_height, im_width)).get_anchors()

        photo = np.expand_dims(preprocess_input(image),0)
        
        preds = self.retinaface.predict(photo)
        results = self.bbox_util.detection_out(preds, self.anchors, confidence_threshold=self.confidence)

        if len(results) <= 0:
            return old_image, []

        results = np.array(results)
        if self.letterbox_image:
            results = retinaface_correct_boxes(results, np.array([self.input_shape[0], self.input_shape[1]]), np.array([im_height, im_width]))
        
        results[:,:4] = results[:,:4]*scale
        results[:,5:] = results[:,5:]*scale_for_landmarks

        ans = []
        for b in results:
            confidence = b[4].astype(float)
            each_ans = {
                'box': [0, 0, 0, 0],
                'confidence': 0,
                'landmarks': []
            }
            text = "{:.4f}".format(b[4])
            b = list(map(int, b))

            each_ans['box'][0] = b[0]
            each_ans['box'][1] = b[1]
            each_ans['box'][2] = b[2]
            each_ans['box'][3] = b[3]
            each_ans['confidence'] = confidence
            
            cv2.rectangle(old_image, (b[0], b[1]), (b[2], b[3]), (0, 0, 255), 2)
            cx = b[0]
            cy = b[1] + 12
            cv2.putText(old_image, text, (cx, cy),
                        cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))

            print(b[0], b[1], b[2], b[3], b[4])
            cv2.circle(old_image, (b[5], b[6]), 1, (0, 0, 255), 4)
            cv2.circle(old_image, (b[7], b[8]), 1, (0, 255, 255), 4)
            cv2.circle(old_image, (b[9], b[10]), 1, (255, 0, 255), 4)
            cv2.circle(old_image, (b[11], b[12]), 1, (0, 255, 0), 4)
            cv2.circle(old_image, (b[13], b[14]), 1, (255, 0, 0), 4)
            landmarks = [
                (b[5], b[6]),
                (b[7], b[8]),
                (b[9], b[10]),
                (b[11], b[12]),
                (b[13], b[14]),
            ]
            each_ans['landmarks'] = landmarks
            ans.append(each_ans)
        return old_image, ans