import os
import toml
import json
import requests
from requests import Session


size = 0


def spider(data: dict,url,req_data,session: Session):
    global size
    if (data['data']['type']) == 'file':
        file_size = data['data']['files'][0]['size']
        file_name = data['data']['files'][0]['name']
        file_url = data['data']['files'][0]['url']
        size = size + file_size
        print(f"{file_name}")
        tmp = req_data['path'].split('/')
        tmp.pop()
        tmp.pop()
        tmp2 = '/'.join(tmp) + '/'
        req_data.update({'path': f"{tmp2}"})

    folder_len = data['data']['meta']['total']
    for _ in range(0, folder_len):
        folder_path = data['data']['files'][_]['name'] + '/'
        full_path = req_data['path'] + folder_path
        req_data.update({'path': f"{full_path}"})
        resp = session.post(url, data=json.dumps(req_data))
        resp_data = json.loads(resp.text)
        spider(resp_data,url,req_data,session)
        tmp = full_path.split('/')
        tmp.pop()
        tmp.pop()
        tmp = '/'.join(tmp) + '/'
        req_data.update({'path': f"{tmp}"})


class ReadConfig(object):
    def __init__(self, conf_path):
        self.alist_conf = toml.load(conf_path, _dict=dict)['Alist']
        self.url = self.alist_conf['url'] + '/api/public/path'
        self.password = self.alist_conf['pass']
        self.path = self.alist_conf['path']
        

    def req_data(self):
        data = {"path": f"{self.path}", "password": f"{self.password}"}
        return json.dumps(data)

    def create_session(self):
        headers = {'Content-Type': 'application/json'}
        session = requests.Session()
        session.headers.update(headers)
        return session


if  __name__ == "__main__":
    conf = ReadConfig('./config.toml')
    session = conf.create_session()
    data = json.loads(session.post(url=conf.url,data=conf.req_data()).text)
    spider(data,conf.url,json.loads(conf.req_data()),session)