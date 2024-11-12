import sys
import os
import hashlib
import hmac
import base64
import requests
import time
import json

def	make_signature(access_key, secret_key, method, uri, timestamp):
    timestamp = str(timestamp)
    secret_key = bytes(secret_key, 'UTF-8')
    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest()).decode()
    return signingKey

def send_request(url, headers, method):
    r = requests.request(method, url, headers=headers)
    if r.status_code != 200:
        print('ERROR! {} {}'.format(r.status_code, r.text))
    return r.text
  
def call_serverlist():
    # unix timestamp 설정
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    # Ncloud API Key 설정
    ncloud_accesskey = "ncp_iam_BFASKR2l12lIt7545zGl"
    ncloud_secretkey = "ncp_iam_BFKSKRDJCq8wWVywTdxPlBNrsvAingMfBd"

    # 암호화 문자열 생성을 위한 기본값 설정
    method = "GET"

    # API 서버 정보
    url = "https://fin-ncloud.apigw.fin-ntruss.com"

    # API URL 서버 목록 조회
    path = "/vserver/v2/getServerInstanceList?regionCode=FKR&responseFormatType=json"

    # http 호출 헤더값 설정
    http_header = {
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': ncloud_accesskey,
        'x-ncp-apigw-signature-v2': make_signature(ncloud_accesskey, ncloud_secretkey, method, path, timestamp)
    }

    #api 호출
    response = send_request(url=url + path, headers=http_header, method=method)
    real_data = json.loads(response)
    return real_data
    #데이터를 파이썬 딕션어리 데이터 타입으로 저장
    # response_txt = json.loads(response)
    # return response_txt
print(call_serverlist())
