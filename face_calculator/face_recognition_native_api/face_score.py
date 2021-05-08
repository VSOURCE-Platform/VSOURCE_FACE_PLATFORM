#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright 2019 Ecohnoch. All Rights Reserved.
# Modifications copyright Microsoft
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import unicode_literals

import tensorflow as tf
import numpy as np
import os
import cv2

from .resnet50 import resnet50

def load_img(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (112, 112))
    img = img.astype(np.float32)
    img -= 127.5
    img *= 0.0078125
    return img

def load_img2(img_path, save_size=112):
    img = cv2.imread(img_path)
    # print(img_path, os.path.getsize(img_path))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (save_size, save_size))
    img = img.astype(np.float32)
    img -= 127.5
    img *= 0.0078125
    return img

def load_img_list(img_path_list):
    ans = []
    for path in img_path_list:
        img = load_img(path)
        if img.shape[0] != 112:
            continue
        ans.append(img)
    return np.array(ans)

def set_mp(processes=8):
    import multiprocessing as mp

    def init_worker():
        import signal
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    global pool
    try:
        pool.terminate()
    except:
        pass

    if processes:
        pool = mp.Pool(processes=processes, initializer=init_worker)
    else:
        pool = None
    return pool

def face_path_list_to_array(facePathList, mp_pooler=None):
    try:
        ans = [mp_pooler.apply_async(load_img2, args=(ID, 112)) for ID in  facePathList]
        ans = np.array([p.get() for p in ans])
        return ans
    except Exception as e:
        print('****** Error: ', e)
        print(facePathList)
        return ans



class FaceScore:
    def __init__(self, params):
        self.__graph = tf.Graph()
        with self.__graph.as_default():
            self.__sess = tf.Session(graph=self.__graph)
            self.input = tf.placeholder(tf.float32, [None, 112, 112, 3], name='image_inputs')
            self.emb     = self.build_graph(self.input)
            self.__sess.run(tf.global_variables_initializer())
            self.__restore = tf.train.Saver()
            if os.path.isdir(params):
                meta_file = [os.path.join(params, x) for x in os.listdir(params) if os.path.splitext(x)[-1] == '.meta'][0]
                f, ext = os.path.splitext(meta_file)
                self.__restore.restore(self.__sess, f)
            else:
                self.__restore.restore(self.__sess, params)
            self.params = params

    def cal_face_emb(self, face_path):
        return self.__sess.run(self.emb, feed_dict={self.input: [load_img(face_path)]})[0]

    def cal_face_images(self, face_image1, face_image2):

        img1 = cv2.imdecode(np.asarray(bytearray(face_image1.read()), dtype="uint8"), cv2.IMREAD_COLOR)
        img2 = cv2.imdecode(np.asarray(bytearray(face_image2.read()), dtype="uint8"), cv2.IMREAD_COLOR)
        emb1 = self.cal_face_emb_from_mat(img1)
        emb2 = self.cal_face_emb_from_mat(img2)
        return self.cal_score_from_emb(emb1, emb2)

    def cal_face_emb_from_mat(self, face_mat):
        img = cv2.cvtColor(face_mat, cv2.COLOR_RGB2BGR)
        img = cv2.resize(img, (112, 112))
        img = img.astype(np.float32)
        img -= 127.5
        img *= 0.0078125
        return self.__sess.run(self.emb, feed_dict={self.input: [img]})
    
    def cal_mean_emb_from_face_list(self, face_list):
        return np.mean(
            self.__sess.run(self.emb, feed_dict={
                self.input: load_img_list(face_list)
            }), axis=0
        )

    def cal_mean_emb_from_face_list_with_mp(self, face_list, mp=32):
        mp_pooler = set_mp(mp)
        return np.mean(
            self.__sess.run(self.emb, feed_dict={
                self.input: face_path_list_to_array(face_list, mp_pooler)
            }), axis=0
        )
    def cal_emb_from_face_list_with_mp(self, face_list, mp=32):
        mp_pooler = set_mp(mp)
        return self.__sess.run(self.emb, feed_dict={self.input: face_path_list_to_array(face_list, mp_pooler)})
    
    def build_graph(self, input_tensor):
        emb = resnet50(input_tensor, is_training=False) 
        return emb
    
    def cal_score_from_emb(self, face_emb1, face_emb2):
        return np.sum(face_emb1*face_emb2)

    def cal_score(self, face_path1, face_path2):
        face_emb1 = self.__sess.run(self.emb, feed_dict={self.input: [load_img(face_path1)]})[0]
        face_emb2 = self.__sess.run(self.emb, feed_dict={self.input: [load_img(face_path2)]})[0]
        diff = np.subtract(face_emb1, face_emb2)
        score = np.sum(np.square(diff))
        # score = np.sum(face_emb1*face_emb2)
        return score