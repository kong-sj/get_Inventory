import os
import sys
import time
import json
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Auth.signature import make_signature
from send_request import send_request
from Auth.auth_Key import ncloud_accesskey, ncloud_secretkey, public


def get_BlockStorageInstnace(bs_name):
        # unix timestamp 설정
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    # 메소드 정보
    method = "GET"

    # API 서버 정보
    url = public

    # API URL 서버 목록 조회
    path = f"/vserver/v2/getBlockStorageInstanceList?regionCode=KR&responseFormatType=json&serverName={bs_name}"

    # http 호출 헤더값 설정
    http_header = {
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': ncloud_accesskey,
        'x-ncp-apigw-signature-v2': make_signature(ncloud_accesskey, ncloud_secretkey, method, path, timestamp)
    }

    #Subnet List API 호출
    response = send_request(url=url + path, headers=http_header, method=method)
    bs_data_json = json.loads(response)

    bs_response = bs_data_json["getBlockStorageInstanceListResponse"]['blockStorageInstanceList']
    extracted_bs_list= []
    for data in bs_response:
        bs_size = data.get("blockStorageSize")
        dev_name = data.get("deviceName")
        real_bs_size = int(bs_size / (1024 ** 3))
        extracted_bs_list.append({
          "BlockStorage_Name": data.get("blockStorageName"),
          "Device_name": dev_name,
          "BlockStorage_Size": f"{real_bs_size}GB"
        })

    return extracted_bs_list
  