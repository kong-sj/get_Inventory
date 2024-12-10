import sys
import os
import time
import json
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Auth.auth_Key import ncloud_accesskey, ncloud_secretkey, public, financial
from Auth.signature import make_signature
from send_request import send_request
from Network.getVPCList import vpc_Name_Return
from Network.getSubnetList import subnet_Name_Return
from Network.getNetworkInterfaceList import NIC_Ip_Return
from Storage.getStorageInstance import get_BlockStorageInstnace
from ServerImage.getServerImageProductList import get_OS_Release

def get_Server_List():

    # unix timestamp 설정
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    # 암호화 문자열 생성을 위한 기본값 설정
    method = "GET" 

    # API 서버 정보
    url = public

    # API URL 서버 목록 조회
    path = f"/vserver/v2/getServerInstanceList?regionCode=KR&responseFormatType=json"

    # http 호출 헤더값 설정
    http_header = {
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': ncloud_accesskey,
        'x-ncp-apigw-signature-v2': make_signature(ncloud_accesskey, ncloud_secretkey, method, path, timestamp)
    }
    extracted_server = []

    #api 호출 및 필요 데이터 필터링
    response = send_request(url=url + path, headers=http_header, method=method)
    real_data = json.loads(response)
    real_data_server = real_data["getServerInstanceListResponse"]["serverInstanceList"]
    for server in real_data_server:
        server_name = server.get("serverName")  # Server Name 값 추출
        server_cidr_pub = server.get("publicIp")  # Public IP 추출
        cpuCount = server.get("cpuCount")
        memSize = server.get("memorySize")
        pemKeyName = server.get("loginKeyName")
        vpc_no = server.get("vpcNo")
        subnet_no = server.get("subnetNo")
        nic_no = server.get("networkInterfaceNoList")
        vpc_name = vpc_Name_Return(vpc_no=vpc_no)
        subnet_name = subnet_Name_Return(subnet_no=subnet_no)
        priv_ip = NIC_Ip_Return(nic_no[0])
        spec_Code = server.get("serverSpecCode")
        block_storage =  get_BlockStorageInstnace(server_name)
        hypervisor_Type = server.get("hypervisorType")
        server_image_productCode = server.get("serverImageProductCode")
        os_release_name = get_OS_Release(server_image_productCode)
        memory_Size = int(memSize / (1024 ** 3))
        extracted_server.append({
          "vpc_name": vpc_name,
          "subnet_name": subnet_name,
          "server_name": server_name,
          "Public IP": server_cidr_pub,
          "Private_IP": priv_ip[0]["PrivateIP"],
          "Spec": spec_Code,
          "CPU": cpuCount,
          "Memory": memory_Size,
          "Key Name": pemKeyName,
          "Block Storage": block_storage,
          "Hypervisor_Type": hypervisor_Type,
          "OS_Release": os_release_name
        })
    return extracted_server