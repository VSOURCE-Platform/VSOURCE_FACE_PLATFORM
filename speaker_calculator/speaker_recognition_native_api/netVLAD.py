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

import tensorflow as tf

def VLAD_pooling(feat, cluster_score, k_centers):
    num_features = feat.shape[-1]
    max_cluster_score = tf.reduce_max(cluster_score, -1, keepdims=True)
    exp_cluster_score = tf.exp(cluster_score - max_cluster_score)
    A = exp_cluster_score / tf.reduce_sum(exp_cluster_score, axis=-1, keepdims=True)

    A = tf.expand_dims(A, -1)
    # print('A: ', A)
    feat_broadcast = tf.expand_dims(feat, -2)
    # print('feat_broadcast: ', feat_broadcast)

    initializer = tf.contrib.layers.xavier_initializer()
    w = tf.get_variable('weights', shape=[k_centers, num_features], initializer=initializer)
    
    feat_res = feat_broadcast - w
    weighted_res = tf.multiply(A, feat_res)
    # print('Weighted_res: ', weighted_res)
    cluster_res  = tf.reduce_sum(weighted_res, [1, 2])

    cluster_l2 = tf.nn.l2_normalize(cluster_res, -1)
    outputs = tf.reshape(cluster_l2, [-1, int(k_centers * num_features)])
    # print('vlad output: ', outputs)
    return outputs