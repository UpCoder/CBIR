# Dataset
## Holidays dataset
- Download by bash
```bash
nohup wget -O ./Holiday/part1.tar.gz ftp://ftp.inrialpes.fr/pub/lear/douze/data/jpg1.tar.gz > ./logs/download_jpg1.log &
nohup wget -O ./Holiday/part2.tar.gz ftp://ftp.inrialpes.fr/pub/lear/douze/data/jpg2.tar.gz > ./logs/download_jpg1.log &
```
- Download Baidu

链接: https://pan.baidu.com/s/18esE4psVuo8ZAB_Tc1TV1A 提取码: v2yg

- Download [Google](https://drive.google.com/drive/folders/1_DeVw45sR9BoJe1xojUfUX0DB3BMeCJS?usp=sharing)

## [CCWebVideo](http://vireo.cs.cityu.edu.hk/webvideo/Download.htm)
我们分别提供官方提取的Fames和Videos的下载方式：
### Frames (4G)
- Download by python
```bash
nohup python ./download_frames.py --frame_info_txt=ShotListTxt --save_dir='custom_dir' --num_processes=16
``` 
请按照自己环境修改shot list和保存的目录，shot list ./datasets/CCWebVideos/ 下保存有一份。具体字段含义官网有解释。

- Download Baidu

链接: https://pan.baidu.com/s/1eMVjePpEqnCc1GawU8nszg 提取码: 7rza

- Download [Google](https://drive.google.com/open?id=1Cz1XlY1xnRpjmzkrotgJmu0AceCaAToS)
### Videos (80G)
由于Videos数据过大，我们只提供python版本的下载方式。网速正常情况下，大约5小时下载完成(16进程)。
- Download by python
```bash
nohup python ./download_videos.py --video_list_txt=VIDEOLIST --save_dir='custom_dir' --num_processes=16 > ./download_videos.log &
```
请按照环境修改video list和保存的目录，video list ./datasets/CCWebVideos/ 下保存有一份。
