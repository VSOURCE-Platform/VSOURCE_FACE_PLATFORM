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

import io
import os
import librosa
import soundfile
from urllib.request import urlopen

from .thin_resnet import resnet34
from .netVLAD import VLAD_pooling


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


def load_wav(vid_path, sr, isBytes=False, mode='train'):
    if isBytes:
        wav, sr_ret = soundfile.read(io.BytesIO(urlopen(vid_path).read()))
        wav = wav.T
        wav = librosa.resample(wav, sr_ret, sr)
        sr_ret = sr
    else:
        wav, sr_ret = librosa.load(vid_path, sr=sr)
    assert sr_ret == sr
    if mode == 'train':
        extended_wav = np.append(wav, wav)
        if np.random.random() < 0.3:
            extended_wav = extended_wav[::-1]
        return extended_wav
    else:
        extended_wav = np.append(wav, wav[::-1])
        return extended_wav

def lin_spectogram_from_wav(wav, hop_length, win_length, n_fft=1024):
    linear = librosa.stft(wav, n_fft=n_fft, win_length=win_length, hop_length=hop_length)  # linear spectrogram
    return linear.T


def load_data(path, isBytes=False, win_length=400, sr=16000, hop_length=160, n_fft=512, spec_len=250, mode='train'):
    wav = load_wav(path, isBytes=isBytes, sr=sr, mode=mode)
    linear_spect = lin_spectogram_from_wav(wav, hop_length, win_length, n_fft)
    mag, _ = librosa.magphase(linear_spect)  # magnitude
    mag_T = mag.T
    freq, time = mag_T.shape
    if mode == 'train':
        randtime = np.random.randint(0, time - spec_len)
        spec_mag = mag_T[:, randtime:randtime + spec_len]
    else:
        spec_mag = mag_T
    # preprocessing, subtract mean, divided by time-wise var
    mu = np.mean(spec_mag, 0, keepdims=True)
    std = np.std(spec_mag, 0, keepdims=True)
    res = (spec_mag - mu) / (std + 1e-5)
    res = np.array(res)
    res = np.expand_dims(res, -1)
    return res

class VoiceScore:
    def __init__(self, params):
        self.__graph = tf.Graph()

        with self.__graph.as_default():
            self.__sess = tf.Session(graph=self.__graph)
            self.input = tf.placeholder(tf.float32, [None, 257, None, 1], name='audio_input')
            self.emb = self.build_graph(self.input)
            self.__sess.run(tf.global_variables_initializer())
            self.__restore = tf.train.Saver()
            if os.path.isdir(params):
                meta_file = [os.path.join(params, x) for x in os.listdir(params) if os.path.splitext(x)[-1] == '.meta'][
                    0]
                f, ext = os.path.splitext(meta_file)
                self.__restore.restore(self.__sess, f)
            else:
                self.__restore.restore(self.__sess, params)

            self.params = params

    def build_graph(self, input_tensor):
        emb_ori = resnet34(input_tensor, is_training=False, kernel_initializer=tf.orthogonal_initializer())
        fc1 = tf.layers.conv2d(emb_ori, filters=512, kernel_size=[7, 1], strides=[1, 1], padding='SAME',
                               activation=tf.nn.relu, name='fc_block1_conv')

        x_center = tf.layers.conv2d(emb_ori, filters=10, kernel_size=[7, 1], strides=[1, 1], use_bias=True,
                                    padding='SAME', name='x_center_conv')
        pooling_output = VLAD_pooling(fc1, x_center, k_centers=10)

        fc2 = tf.layers.dense(pooling_output, 512, activation=tf.nn.relu, name='fc_block2_conv')
        fc2 = tf.nn.l2_normalize(fc2, 1)
        return fc2

    def cal_emb(self, path):
        return self.__sess.run(self.emb, feed_dict={self.input: [load_data(path, mode='eval')]})[0]

    def cal_score(self, audio_path1, audio_path2):
        audio_emb1 = self.__sess.run(self.emb, feed_dict={self.input: [load_data(audio_path1, mode='eval')]})[0]
        audio_emb2 = self.__sess.run(self.emb, feed_dict={self.input: [load_data(audio_path2, mode='eval')]})[0]
        score = np.sum(audio_emb1 * audio_emb2)
        return score

    def cal_score_from_http(self, audio_path1, audio_path2):
        audio_emb1 = self.__sess.run(self.emb, feed_dict={self.input: [load_data(audio_path1, isBytes=True, mode='eval')]})[0]
        audio_emb2 = self.__sess.run(self.emb, feed_dict={self.input: [load_data(audio_path2, isBytes=True, mode='eval')]})[0]
        score = np.sum(audio_emb1 * audio_emb2)
        return score

    def cal_score_with_mat(self, audio_mat1, audio_mat2):
        audio_emb1 = self.__sess.run(self.emb, feed_dict={self.input: [load_data_from_mat(audio_mat1, mode='eval')]})[0]
        audio_emb2 = self.__sess.run(self.emb, feed_dict={self.input: [load_data_from_mat(audio_mat2, mode='eval')]})[0]
        score = np.sum(audio_emb1 * audio_emb2)
        return score

    def cal_score_with_emb(self, audio_emb1, audio_emb2):
        return np.sum(audio_emb1 * audio_emb2)


def calculate_score(audio_path1, audio_path2,
                    ckpt_file='/Users/ecohnoch/Vggvox-TensorFlow/ckpt/Speaker_vox_iter_18000.ckpt'):
    x = tf.placeholder(tf.float32, [None, 257, None, 1], name='audio_input')
    emb_ori = resnet34(x, is_training=False, kernel_initializer=tf.orthogonal_initializer())
    fc1 = tf.layers.conv2d(emb_ori, filters=512, kernel_size=[7, 1], strides=[1, 1], padding='SAME',
                           activation=tf.nn.relu, name='fc_block1_conv')

    x_center = tf.layers.conv2d(emb_ori, filters=10, kernel_size=[7, 1], strides=[1, 1], use_bias=True, padding='SAME',
                                name='x_center_conv')
    pooling_output = VLAD_pooling(fc1, x_center, k_centers=10)

    fc2 = tf.layers.dense(pooling_output, 512, activation=tf.nn.relu, name='fc_block2_conv')
    fc2 = tf.nn.l2_normalize(fc2, 1)

    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver.restore(sess, ckpt_file)
        audio_emb1 = sess.run(fc2, feed_dict={x: [load_data(audio_path1, mode='eval')]})[0]
        audio_emb2 = sess.run(fc2, feed_dict={x: [load_data(audio_path2, mode='eval')]})[0]
        score = np.sum(audio_emb1 * audio_emb2)
    tf.reset_default_graph()
    return score
