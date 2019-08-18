# Content-based Image Retrieval (CBIR)
## Requirements
- Python 2.7
- scipy 1.2.1
- numpy 1.16.2
## Dataset
  进入datasets，根据提示下载相关数据集
## Pipeline
### Task 1 Holiday
  执行下述命令，得到图像检索的mAP
```bash
python ./CBIR/main.py --dataset_name=Holiday 
```
### Task 2 CCWebVideo
- 下载作为baseline的特征
    - Baidu
    
        链接: https://pan.baidu.com/s/1LAVXsKIA-4MIvUCvbFJDJQ 提取码: hvhp 
    - [Google](https://drive.google.com/open?id=1A6bS4pU97hRfBBKD5CPO0hXY2KoC5cBS)
- 将 features.pk移动至./datasets/CCWebVideo 
- 执行下述命令，得到CCWebVideo检索的mAP
```bash
python ./CBIR/main.py --dataset_name=CCWebVideo 
``` 
