# 目的

为了帮助大家快速上手使用[百度人体分析-人流量统计（动态版）](https://cloud.baidu.com/doc/BODY/s/wk3cpyyog#%E8%AF%B7%E6%B1%82%E8%AF%B4%E6%98%8E)，节约大家的时间，而不是对着网站和使用说明文档鼓捣半天。



# 功能说明

你需要准备[百度AIP开放平台使用OAuth2.0授权调用开放API](https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjgn3)和待测试视频以及对应的参数。
按照下面步骤，将获得结果帧以及对应结果json文件，和合成的视频。



# 数据存放方式说明

你的原始视频数据放在`./videos/`中；

程序执行完后，`./pics/{video_name}/`中会存放你的crop后、截取后的关键帧，`./results/{video_name}/`中会存放你的结果图、对应结果人流信息（BBox、ID等）和合成的视频。



# 视频json文件参数说明

 `./conf/{video.name}.json`文件中，你需要准备几个参数： 

FPS（截取关键帧的频率，每秒多少帧）

crop：你需要检测的区域，格式为[width,height,left,top]

area：你进出口统计的区域，详见[人流量统计(动态版)](https://cloud.baidu.com/doc/BODY/s/wk3cpyyog)

case_id：这个任务的序号，并行的时候，需要不同的任务序号来作区分；如果仅同时运行一个任务，则填1就行。

```json
{
    "videoname" : "yaofang",
    "FPS" : 10,
    "crop" : [926,875,554,204],
    "area" : "1,1,100,1,100,100,1,100",
    "case_id" : 1
}
```



# 使用步骤

## 1. 环境部署

```bash
# 创建conda环境
conda create -n baidu_people_counting python=3.8 -y
# pip 安装环境
pip install -r requirements.txt
```



# 2. 获取你的百度token

先[获取](https://console.bce.baidu.com/ai/?_=1631883840248#/ai/body/app/list)并将你的`API Key` 和`Secret Key`填入`client_keys.json`文件中，然后执行如下指令，你将获得`./token.json`文件

```bash
python get_token.py
```



## 3. 准备好你要控制的参数，执行主程序

在`baidu_people_tracking.py`中修改你的视频名字，想处理的时段的起始时间`hh:mm:ss`和时长`duration`，然后运行，很快就能得到结果了

```bash
python baidu_people_tracking.py
```



# TODO

1. 主程序加上parser
2. 把更多可选项暴露出来，也保留一般选项作为default，以方便大家熟悉了之后更深入定制操作

