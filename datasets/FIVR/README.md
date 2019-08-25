# [Fine-grained Incident Video Retrieval (FIVR)](https://arxiv.org/abs/1809.04094)
## 环境配置
### 已有(root)
- conda
- python3.6 (conda activate py3)
- tensorflow-gpu(1.13.1)
- cuda10.0 (/usr/local/cuda)
### 需要配置
- 请队长使用root账号登陆，给队员创建账号，并分配root权限
## Run
- 队长使用root账号登陆server
- 在server执行
```bash
cd /home/camp/Jupyter
source activate
conda activate py3
pip install -r requirements.txt
jupyter notebook --no-browser --port=8888 --allow-root
```
- 队员在client执行，将server的jupyter端口映射到本地
```bash
ssh -N -f -L localhost:8888:localhost:8888 username@IP
```
## Dataset
- 数据集特征目录：/home/camp/FIVR/features/vcms_v1
- Annotation目录：/home/camp/FIVR/annotation
- 描述：我们提供视频的帧级别特征
    - 每个h5文件有两个group: images和names
    - images group 保存了每个视频帧的特征，id是视频id，value是帧特征
    - names group 保存了每个视频帧的名字，id是视频id，value是帧的名字，例如\[1.jpg, 2.jpg,...\]
- 一些关键词的解释
    - vid: 和视频一一对应。
    - name: 和视频一一对应，annotation中的使用的是name
    - 通过vid2name和name2vid可以确定他们之间的映射关系
- 三种相似的视频
    - Duplicate Scene Video (DSV)
    - Complementary Scene Video (CSV), 如果A，B两个视频描述的同一个事件，且时间上有overlap，则认为是彼此之间的相似关系是CSV
    - Incident Scene Video (ISV)，如果A，B两个视频描述的是同一个时间，时间上没有overlap，则认为彼此之间的相似关系是ISV
- 三个任务
    - DSVR：负责检索出DSV的相似
    - CSVR：负责检索出DSV+CSV的相似
    - ISVR：负责检索出DSV+CSV+ISV的相似