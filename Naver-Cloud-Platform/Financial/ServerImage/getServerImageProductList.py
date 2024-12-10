import os
import sys
import time
import json
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Auth.signature import make_signature
from send_request import send_request
from Auth.auth_Key import ncloud_accesskey, ncloud_secretkey, financial_svr


def get_OS_Release(producCode):
        # unix timestamp 설정
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    # 메소드 정보
    method = "GET"

    # API 서버 정보
    url = financial_svr

    # API URL 서버 목록 조회
    path = f"/vserver/v2/getServerImageProductList?regionCode=FKR&responseFormatType=json&productCode={producCode}"

    # http 호출 헤더값 설정
    http_header = {
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': ncloud_accesskey,
        'x-ncp-apigw-signature-v2': make_signature(ncloud_accesskey, ncloud_secretkey, method, path, timestamp)
    }

    #Subnet List API 호출
    response = send_request(url=url + path, headers=http_header, method=method)
    data_json = json.loads(response)

    response = data_json["getServerImageProductListResponse"]['productList']
    os_release_name = response[0]["productDescription"]

    return os_release_name