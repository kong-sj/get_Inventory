import sys
import os
import time
import json
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from Auth.signature import make_signature
from send_request import send_request
from Auth.auth_Key import ncloud_accesskey, ncloud_secretkey




def vpc_List():
    # unix timestamp 설정
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    # 암호화 문자열 생성을 위한 기본값 설정
    method = "GET"

    # API 서버 정보
    url = "https://fin-ncloud.apigw.fin-ntruss.com"

    # API URL 서버 목록 조회
    path = "/vpc/v2/getVpcList?regionCode=FKR&responseFormatType=json"

    # http 호출 헤더값 설정
    http_header = {
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': ncloud_accesskey,
        'x-ncp-apigw-signature-v2': make_signature(ncloud_accesskey, ncloud_secretkey, method, path, timestamp)
    }

    #api 호출
    subnet_List_Response = send_request(url=url + path, headers=http_header, method=method)
    real_data = json.loads(subnet_List_Response)
        
    return real_data
    #데이터를 파이썬 딕션어리 데이터 타입으로 저장
    # response_txt = json.loads(response)
    # return response_txt
    
    
print(vpc_List())
