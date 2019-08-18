# -*- coding=utf-8 -*-
from tqdm import tqdm
import argparse
import shutil
import multiprocessing
import os
url_perfix = 'http://vireo.cs.cityu.edu.hk/webvideo/videos/'


def video_list_parser(file_path):
    video_names = []
    with open(file_path, 'r') as f:
        for line in f:
            row = line.split('\t')
            video_names.append(row[-2])
    return video_names


def download_videos(process_id, video_names, save_dir):
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
    for video_name in tqdm(video_names):
        query_id = video_name.split('_')[0]
        video_url = url_perfix + query_id + '/' + video_name
        cur_save_dir = os.path.join(save_dir, query_id)
        if not os.path.exists(cur_save_dir):
            os.mkdir(cur_save_dir)
        cur_save_path = os.path.join(cur_save_dir, video_name)
        if os.path.exists(cur_save_path):
            continue
        os.system('wget --quiet \'%s\' -O %s' % (video_url, cur_save_path))


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-FIT', '--video_list_txt', type=str,
                        default='./video_list.txt', help='the txt path of frames')
    parser.add_argument('-SD', '--save_dir', type=str,
                        default='/mnt/cephfs_hl/vc/liangdong.tony/datasets/CC_WEB_VIDEO/Videos',
                        help='the save_dir')
    parser.add_argument('-NP', '--num_processes', type=int,
                        default=16,
                        help='the number of processes')

    args = vars(parser.parse_args())
    video_names = video_list_parser(args['video_list_txt'])
    num_processes = args['num_processes']
    num_id_per_process = int(len(video_names) / num_processes + 1)
    p = multiprocessing.Pool(processes=num_processes)
    result = []
    tmp_dir = os.path.join(os.getcwd(), 'tmp')
    save_dir = args['save_dir']
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    for i in range(num_processes):
        input_vids = video_names[num_id_per_process*i: num_id_per_process*(i+1)]
        print(len(input_vids))
        result.append(p.apply_async(download_videos , args=(i, input_vids, save_dir,)))
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    print 'All subprocesses done.'
    shutil.rmtree(tmp_dir)
