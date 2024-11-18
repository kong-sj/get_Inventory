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
    print(response)
    subnet_list = response.get("subnetList", [])
    extracted_subnet = []
    
    # #VPC No 호출
    # resquest_Vpc_list = vpc_List()
    # response_Vpc_list = resquest_Vpc_list["getVpcListResponse"]
    # vpc_list = response_Vpc_list("vpcLlist", [])
    # vpc_No_List = [vpc["vpcNo"] for vpc in vpc_list]
    # print(vpc_No_List)
    
    for subnet in subnet_list:
        # vpc_no = subnet.get("vpcNo")  # 'vpcNo' 값 추출
        # if vpc_no == "25547":  # 문자열이므로 따옴표 사용
        subnet_name = subnet.get("subnetName")  # 'subnetName' 값 추출
        subnet_cidr = subnet.get("subnet")  # 'subnet' 값 추출
        subnet_type = subnet.get("subnetType")
        subnet_zone = subnet.get("zoneCode")
        extracted_subnet.append({
          "subnet_name": subnet_name,  # 'subnetName' 값 추출
          "subnet_cidr": subnet_cidr,  # 'subnet' 값 추출
          "subnet_type": subnet_type,
          "subnet_zone": subnet_zone
      })
    #데이터를 파이썬 딕션어리 데이터 타입으로 저장
    # response_txt = json.loads(response)
    # return response_txt
    return extracted_subnet
subnet_data = get_Subnet_List()
print(subnet_data)
