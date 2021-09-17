# encoding:utf-8
import os
import requests
import base64
import json
import time
from ffmpy import FFmpeg

src_file = './videos/yaofang.avi'
hh = 0
mm = 0
ss = 0
duration = 30

def post_baidu(pic_path, result_path, conf, url, access_token, QPS = 1, case_id = 1):
    filenames = os.listdir(pic_path)
    filenames.sort() # for the right sequence
    
    # parameters preparation
    params = {
            "area":conf['area'], # attention!!!
            "case_id": case_id,
            "case_init":'true',
            "dynamic":"true", 
            "image":'',
            "show":"true"
            }
    
    request_url = url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    time_delay = 1/QPS
    last_time = time.time()

    for file in filenames:
        with open(pic_path+file, 'rb') as fpic:
            img = base64.b64encode(fpic.read())
        params["image"] = img

        # for the limit of concurrence
        time.sleep(max(last_time + time_delay - time.time(), 0))
        last_time = time.time()

        response = requests.post(request_url, data=params, headers=headers)

        if response:
            try:
                # save img
                result_img = response.json()["image"]
                result_img = base64.b64decode(result_img)
                
                result_path_file = result_path + file.split('.')[0]
                with open(result_path_file + '.jpg', 'wb') as fimg:
                    fimg.write(result_img)

                # save json
                info = response.json()
                if 'image' in info.keys():
                    info.pop('image')
                # info = json.dumps(info)

                with open(result_path_file+ '.json', 'w') as fjson:
                    json.dump(info, fjson)
            
            except Exception as e:
                print(e, '\nFile:', file)
                print(response.json())

        # change the flag of being first picture
        params['dynamic'] = 'false'
                



if __name__ == '__main__':
    # read token from json
    with open("./token.json", 'r') as ftoken:
        access_token = json.loads(ftoken.read())['access_token']
    url = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/body_tracking'

    # get source file path and result path
    video_name = src_file.split('/')[-1].split('.')[0]
    pic_path = f'./pics/{video_name}/'
    result_path = f'./results/{video_name}/'

    # read config of the post task
    with open('./conf/'+video_name+'.json', 'r') as fconf:
        conf = json.loads(fconf.read())

    # crop video and save raw frames according to json
    [w, h, left, top] = conf["crop"]
    rate = conf["FPS"]
    
    ff = FFmpeg(
        inputs = {
            src_file: 
                [
                    '-ss', str(hh).zfill(2)+':'+str(mm).zfill(2)+':'+str(ss).zfill(2),
                    '-t', str(duration)
                ]
            } ,
        outputs = {
            f'{pic_path}/{video_name}-%04d.jpg': [
                    '-r', f'{rate}', 
                    '-vf', f'crop=w={w}:h={h}:x={left}:y={top}'
                ]
            }
    )
    ff.run()
    print('\nCMD:',ff.cmd,'\n')

    # post frame and receive results //// json should contain #channel for baidu
    post_baidu(pic_path, result_path, conf, url, access_token)

    # synthesize the result frames
    synth = FFmpeg(
        inputs = {
            f'{result_path}/{video_name}-%04d.jpg': [
                    '-f', 'image2'
                ]
        },
        outputs = {
            f'{result_path}/result_{video_name}.mp4': None
        }
    )
    synth.run()
    print('\nCMD:',synth.cmd,'\n')
