import os
import sys
import time
import json
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Auth.signature import make_signature
from send_request import send_request
from Auth.auth_Key import ncloud_accesskey, ncloud_secretkey, public


def NIC_Ip_Return(nic_no):
        # unix timestamp 설정
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    # 메소드 정보
    method = "GET"

    # API 서버 정보
    url = public

    # API URL 서버 목록 조회
    path = f"/vserver/v2/getNetworkInterfaceDetail?regionCode=KR&responseFormatType=json&networkInterfaceNo={nic_no}"

    # http 호출 헤더값 설정
    http_header = {
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': ncloud_accesskey,
        'x-ncp-apigw-signature-v2': make_signature(ncloud_accesskey, ncloud_secretkey, method, path, timestamp)
    }

    #Subnet List API 호출
    response = send_request(url=url + path, headers=http_header, method=method)
    nic_data_json = json.loads(response)

    response = nic_data_json["getNetworkInterfaceDetailResponse"]['networkInterfaceList']
    extracted_nic_list= []
    for data in response:
        privIP = data.get("ip")
        extracted_nic_list.append({
          "PrivateIP": privIP
      })

    return extracted_nic_list