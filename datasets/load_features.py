import sys
sys.path.insert(0, '.')
import numpy as np
import pickle


def load_features(dataset_name):
    if dataset_name == 'Holiday':
        with open('./datasets/Holiday/features.pk') as pk_file:
            features_obj = pickle.load(pk_file)
        with open('./datasets/Holiday/gt.pk') as pk_file:
            gt_obj = pickle.load(pk_file)
        return features_obj, gt_obj
    elif dataset_name == 'CCWebVideo':
        with open('./datasets/CCWebVideo/features.pk') as pk_file:
            # vid2features
            features_obj = pickle.load(pk_file)
        with open('./datasets/CCWebVideo/gt.pk') as pk_file:
            gt_obj = pickle.load(pk_file)
        return features_obj, gt_obj
    else:
        print('do not support the {} dataset'.format(dataset_name))
        assert False


if __name__ == '__main__':
    features_obj, gt_obj = load_features('CCWebVideo')
    print(gt_obj)
    print(gt_obj.keys())
    print(np.shape(features_obj.values()))