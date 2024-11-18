import os
import sys
import time
import json
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# from getVPCList import vpc_List
from Auth.signature import make_signature
from send_request import send_request
from Auth.auth_Key import ncloud_accesskey, ncloud_secretkey

def get_Subnet_List():
    # unix timestamp 설정
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    # 메소드 정보
    method = "GET"

    # API 서버 정보
    url = "https://fin-ncloud.apigw.fin-ntruss.com"

    # API URL 서버 목록 조회
    path = "/vpc/v2/getSubnetList?regionCode=FKR&responseFormatType=json"

    # http 호출 헤더값 설정
    http_header = {
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': ncloud_accesskey,
        'x-ncp-apigw-signature-v2': make_signature(ncloud_accesskey, ncloud_secretkey, method, path, timestamp)
    }

    #Subnet List API 호출
    subnet_List_Response = send_request(url=url + path, headers=http_header, method=method)
    real_data = json.loads(subnet_List_Response)
    
    response = real_data["getSubnetListResponse"]
    subnet_list = response.get("subnetList", [])
    extracted_subnet = {}
    
    
    for subnet in subnet_list:
        subnet_no = subnet.get("subnetNo")
        subnet_name = subnet.get("subnetName")
        subnet_cidr = subnet.get("subnet")
        subnet_type = subnet.get("subnetType")
        subnet_zone = subnet.get("zoneCode")

        # subnet_no를 키로 사용
        extracted_subnet[subnet_no] = {
            "subnet_name": subnet_name,
            "subnet_cidr": subnet_cidr,
            "subnet_type": subnet_type,
            "subnet_zone": subnet_zone
        }
    return extracted_subnet
  
def subnet_Name_Return(subnet_no):
    response = get_Subnet_List()
    subnet = response.get(subnet_no)  # 딕셔너리에서 subnet_no로 직접 접근
    if subnet:
        return subnet["subnet_name"]
    return None



subnet = subnet_Name_Return("40569")
print(subnet)