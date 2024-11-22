import sys
import os
import time
import json
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Auth.auth_Key import ncloud_accesskey, ncloud_secretkey
from Auth.signature import make_signature
from send_request import send_request
from Network.getVPCList import vpc_Name_Return
from Network.getSubnetList import subnet_Name_Return
  
def get_Server_List():
    # unix timestamp 설정
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    # Ncloud API Key 설정

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
    extracted_server = []
    

    #api 호출
    response = send_request(url=url + path, headers=http_header, method=method)
    real_data = json.loads(response)
    real_data_server = real_data["getServerInstanceListResponse"]["serverInstanceList"]
    for server in real_data_server:
        # vpc_no = subnet.get("vpcNo")  # 'vpcNo' 값 추출
        # if vpc_no == "25547":  # 문자열이므로 따옴표 사용
        server_name = server.get("serverName")  # 'subnetName' 값 추출
        server_cidr_pub = server.get("publicIp")  # 'subnet' 값 추출
        server_cidr_priv = server.get("subnetType")
        cpuCount = server.get("cpuCount")
        memSize = server.get("memorySize")
        pemKeyName = server.get("loginKeyName")
        vpc_no = server.get("vpcNo")
        subnet_no = server.get("subnetNo")
        nic_list = server.get("networkInterfaceNoList")
        
        
        vpc_name = vpc_Name_Return(vpc_no=vpc_no)
        subnet_name = subnet_Name_Return(subnet_no=subnet_no)
        
        extracted_server.append({
          "server_name": server_name,  # 'subnetName' 값 추출
          "Public IP": server_cidr_pub,  # 'subnet' 값 추출
          "Private IP": server_cidr_priv,
          "CPU": cpuCount,
          "Memory": memSize,
          "Key Name": pemKeyName,
          "vpc_name": vpc_name,
          "subnet_name": subnet_name,
          "NIC_List": nic_list
          
        })
    return extracted_server
    #데이터를 파이썬 딕션어리 데이터 타입으로 저장
    # response_txt = json.loads(response)
    # return response_txt

data_svr_list = get_Server_List()
print(data_svr_list)