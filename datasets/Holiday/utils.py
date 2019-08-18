import os
import numpy as np


def fvecs_read(filename, c_contiguous=True):
    fv = np.fromfile(filename, dtype=np.float32)
    if fv.size == 0:
        return np.zeros((0, 0))
    dim = fv.view(np.int32)[0]
    assert dim > 0
    fv = fv.reshape(-1, 1 + dim)
    if not all(fv.view(np.int32)[:, 0] == dim):
        raise IOError("Non-uniform vector sizes in " + filename)
    fv = fv[:, 1:]
    if c_contiguous:
        fv = fv.copy()
    return fv


def get_groundtruth():
    """ Read datafile holidays_images.dat and output a dictionary
    mapping queries to the set of positive results (plus a list of all
    images)"""
    gt = {}
    allnames = set()
    for line in open("/Users/liang/Downloads/eval_holidays/holidays_images.dat", "r"):
        imname = line.strip()
        allnames.add(imname)
        imno = int(imname[:-len(".jpg")])
        if imno % 100 == 0:
            gt_results = set()
            gt[imname.split('.jpg')[0]] = gt_results
        else:
            gt_results.add(imname.split('.jpg')[0])
    return (allnames, gt)


if __name__ == '__main__':
    arr = fvecs_read('/Users/liang/Downloads/clust/clust_flickr60_k10000.fvecs')
    print(arr[:3])
    print(np.shape(arr))
    allnames, gt = get_groundtruth()
    import pickle
    with open('./Holiday/gt.pk', 'w') as pk_file:
        pickle.dump(gt, pk_file)
    print allnames
    print gt
    print len(gt.keys())