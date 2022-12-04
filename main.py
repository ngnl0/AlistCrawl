import json
import requests

size = 0

def spider(data: dict):
    global size 
    if(data['data']['type']) == 'file':
        file_size = data['data']['files'][0]['size']
        file_name = data['data']['files'][0]['name']
        file_url = data['data']['files'][0]['url']
        size = size + file_size
        print(f"{file_name}")
        tmp = req_data['path'].split('/')
        tmp.pop()
        tmp.pop()
        tmp2 = '/'.join(tmp) + '/'
        req_data.update({'path':f"{tmp2}"})

    folder_len = data['data']['meta']['total']
    for _ in range(0,folder_len):
        folder_path = data['data']['files'][_]['name'] + '/'
        full_path = req_data['path'] + folder_path
        req_data.update({'path':f"{full_path}"})
        resp = requests.post(url,data=json.dumps(req_data),headers=headers)
        resp_data = json.loads(resp.text)
        spider(resp_data)
        tmp = full_path.split('/')
        tmp.pop()
        tmp.pop()
        tmp = '/'.join(tmp) + '/'
        req_data.update({'path':f"{tmp}"})


req_data = {
    "path": "/",
    # path password
    "password": "*********"
}
headers = {'Content-Type': 'application/json'}

url = "http://***.***.com/api/public/path"
resp = requests.post(url,data=json.dumps(req_data),headers=headers)
resp_data = json.loads(resp.text)
spider(resp_data)
print(f"Total files size:{size}")
