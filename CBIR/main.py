# -*- coding=utf-8 -*-
import sys
sys.path.insert(0, '.')
import numpy as np
from datasets.load_features import load_features
from scipy.spatial.distance import cdist
from CBIR.evaluation import score_ap_from_ranks_1
import argparse


def retrieval_pipeline_simple(dataset_name):
    features_obj, gt_obj = load_features(dataset_name) # load features
    query_ids = gt_obj.keys()
    query_features = np.asarray([features_obj[query_id] for query_id in query_ids], np.float32)
    gallery_ids = features_obj.keys()
    gallery_features = np.asarray([features_obj[gallery_id] for gallery_id in gallery_ids], np.float32)
    # compute the distance
    dist = cdist(query_features, gallery_features, metric='euclidean')
    mAP = 0.0
    for i, query_id in enumerate(query_ids):
        # 归一化，将距离转化成相似度
        sim = np.round(1 - dist[i] / dist.max(), decimals=6)
        # 按照相似度的从大到小排列，输出index
        similarities = [(gallery_ids[s], sim[s]) for s in sim.argsort()[::-1] if not np.isnan(sim[s])]
        gt_vids = gt_obj[query_id]
        tp_ranks = []
        rank_shift = 0
        for idx, sim in enumerate(similarities):
            if sim[0] == query_id:
                rank_shift = -1
            elif sim[0] in gt_vids:
                tp_ranks.append(idx + rank_shift)
        ap = score_ap_from_ranks_1(tp_ranks, len(gt_vids))
        print('the AP of  {} is {:.4}'.format(query_id, ap))
        mAP += ap
    mAP /= len(query_ids)
    print('the mAP is {:.4f}'.format(mAP))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d_n', '--dataset_name', type=str,
                        default='Holiday', help='the name of dataset')
    args = vars(parser.parse_args())
    retrieval_pipeline_simple(args['dataset_name'])

