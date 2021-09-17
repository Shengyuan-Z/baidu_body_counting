# encoding:utf-8
import requests 
import json

if __name__ == "__main__":
    with open("./client_keys.json",'r') as f:
        client_info = json.load(f)
    ak = client_info['client_id']
    sk = client_info['client_secret']
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={ak}&client_secret={sk}'
    response = requests.get(host)
    if response:
        with open('./token.json','w') as f:
            json.dump(response.json(), f)
    print(response.json())
