# -*- coding=utf-8 -*-
from tqdm import tqdm
import argparse
import shutil
import math
import h5py
import multiprocessing
import os
import cv2
import numpy as np
import requests
url_perfix = 'http://vireo.cs.cityu.edu.hk/webvideo/Keyframes/'


def shot_info_parser(file_path):
    serialID_ls, keyframeName_ls, videoID_ls, videoName_ls = [], [], [], []
    with open(file_path, 'r') as f:
        for line in f:
            row = line.split('\t')
            serialID_ls.append(row[0])
            keyframeName_ls.append(row[1])
            videoID_ls.append(row[2])
            videoName_ls.append(row[3])
    return serialID_ls, keyframeName_ls, videoID_ls, videoName_ls


def download_frames(process_id, vids, vid2keyframes, save_dir):
    '''
    保存为H5，一个文件夹对应一个文件
    :param process_id:
    :param vids:
    :param vid2keyframes:
    :param save_dir:
    :return:
    '''
    print 'Run task (%s)...' % (os.getpid())
    h5_path = os.path.join(save_dir, '{}.h5'.format(process_id))
    exisit_vids = []
    if os.path.exists(h5_path):
        h5_file = h5py.File(h5_path, 'r')
        images_group = h5_file.get('images')
        exisit_vids = images_group.keys()
        h5_file.close()
    with h5py.File(h5_path, 'a') as h5_file:
        if len(exisit_vids) == 0:
            images_group = h5_file.create_group('images')
            names_group = h5_file.create_group('names')
        else:
            images_group = h5_file.get('images')
            names_group = h5_file.get('names')
        tmp_dir = os.path.join(os.getcwd(), 'tmp')
        for vid in tqdm(vids):
            images = []
            KID = str(int(math.floor(int(vid / 100))))
            names = vid2keyframes.get(vid)
            for name in names:
                download_url = url_perfix + KID + '/' + name + '.jpg'
                save_path = os.path.join(tmp_dir, '{}.jpg'.format(name))
                os.system('wget --quiet \'%s\' -O %s' % (download_url, save_path))
                image = cv2.imread(save_path)[:, :, ::-1]
                images.append(image)
                os.remove(save_path)
            images_group.create_dataset(str(vid), data=np.asarray(images, np.float32))
            names_group.create_dataset(str(vid), data=np.asarray(names, dtype=str))


def download_frames_JPG(process_id, vids, vid2keyframes, save_dir):
    '''
    一个frame保存成一个JPG文件
    :param process_id: 当前的进程ID
    :param vids: 需要处理的VIDs
    :param vid2keyframes:
    :param save_dir: 保存的目录
    :return:
    '''
    print 'Run task (%s)...' % (os.getpid())
    cur_save_dir = os.path.join(save_dir, str(process_id))
    if not os.path.exists(cur_save_dir):
        os.mkdir(cur_save_dir)
    for vid in tqdm(vids):
        KID = str(int(math.floor(int(vid / 100))))
        names = vid2keyframes.get(vid)
        for name in names:
            download_url = url_perfix + KID + '/' + name + '.jpg'
            save_path = os.path.join(cur_save_dir, '{}.jpg'.format(name))
            if os.path.exists(save_path):
                continue
            r = requests.get(download_url)
            with open(save_path, 'wb') as f:
                # print('Write %s' % (name + '.jpg'))
                f.write(r.content)
            # os.system('wget --quiet \'%s\' -O %s' % (download_url, save_path))


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-FIT', '--frame_info_txt', type=str,
                        default='./Shot_Info.txt', help='the txt path of frames')
    parser.add_argument('-SD', '--save_dir', type=str,
                        default='/Volumes/My Passport/ld/datasets/CCWebVideo/FramesJPG',
                        help='the save_dir')
    parser.add_argument('-NP', '--num_processes', type=int,
                        default=16,
                        help='the number of processes')

    args = vars(parser.parse_args())
    serialID_ls, keyframeName_ls, videoID_ls, videoName_ls = shot_info_parser(args['frame_info_txt'])
    vid2keyframeNames = {}
    for keyframeName, videoID in tqdm(zip(keyframeName_ls, videoID_ls)):
        videoID = int(videoID)
        cur_value = vid2keyframeNames.get(videoID, [])
        cur_value.append(keyframeName)
        vid2keyframeNames[videoID] = cur_value
    vids = vid2keyframeNames.keys()
    vids.sort()
    save_dir = args['save_dir']
    num_processes = args['num_processes']
    num_id_per_process = int(len(vids) / num_processes + 1)
    p = multiprocessing.Pool(processes=num_processes)
    result = []
    tmp_dir = os.path.join(os.getcwd(), 'tmp')
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    for i in range(num_processes):
        input_vids = vids[num_id_per_process*i: num_id_per_process*(i+1)]
        print(len(input_vids))
        # result.append(p.apply_async(download_frames, args=(i, input_vids, vid2keyframeNames, save_dir, )))
        result.append(p.apply_async(download_frames_JPG , args=(i, input_vids, vid2keyframeNames, save_dir,)))
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    print 'All subprocesses done.'
    shutil.rmtree(tmp_dir)
