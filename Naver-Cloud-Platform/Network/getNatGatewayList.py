import os
import sys
import time
import json
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Auth.signature import make_signature
from send_request import send_request
from Auth.auth_Key import ncloud_accesskey, ncloud_secretkey

def nat_GW_List():
    # unix timestamp 설정
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    # 메소드 정보
    method = "GET"

    # API 서버 정보
    url = "https://fin-ncloud.apigw.fin-ntruss.com"

    # API URL 서버 목록 조회
    path = "/vpc/v2/getNatGatewayInstanceList?regionCode=FKR&responseFormatType=json"

    # http 호출 헤더값 설정
    http_header = {
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': ncloud_accesskey,
        'x-ncp-apigw-signature-v2': make_signature(ncloud_accesskey, ncloud_secretkey, method, path, timestamp)
    }

    #Subnet List API 호출
    nat_GW_List_Response = send_request(url=url + path, headers=http_header, method=method)
    real_data = json.loads(nat_GW_List_Response)
    
    response = real_data["getNatGatewayInstanceListResponse"]['natGatewayInstanceList']
    extracted_nat_GW = []
  
    
    for nat_GW in response:
        nat_GW_name = nat_GW.get("natGatewayName")  # 'subnetName' 값 추출
        nat_GW_PubIP = nat_GW.get("publicIp")  # 'subnet' 값 추출
        nat_GW_priIP = nat_GW.get("privateIp")
        nat_GW_Zone = nat_GW.get("zoneCode")
        nat_GW_subnet = nat_GW.get("subnetName")
        extracted_nat_GW.append({
          "NAT_GW_Name": nat_GW_name,  # 'subnetName' 값 추출
          "NAT_GW_PublicIP": nat_GW_PubIP,  # 'subnet' 값 추출
          "NAT_GW_privateIP": nat_GW_priIP,
          "NAT_GW_Zone": nat_GW_Zone,
          "NAT_GW_Subnet": nat_GW_subnet
      })

    return extracted_nat_GW
nat_GW_data = nat_GW_List()
print(nat_GW_data)
