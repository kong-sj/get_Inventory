import os
# 작업 디렉토리를 Financial로 변경
financial_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(financial_root)
import sys
import time
import json
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Auth.signature import make_signature
from send_request import send_request
from Auth.auth_Key import ncloud_accesskey, ncloud_secretkey, financial_lb
from Network import getVPCList, getSubnetList


def get_LB_List():
    # unix timestamp 설정
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    # 메소드 정보
    method = "GET"

    # API 서버 정보
    url = financial_lb

    # API URI
    path = "/vloadbalancer/v2/getLoadBalancerInstanceList?regionCode=FKR&responseFormatType=json"
    # http 호출 헤더값 설정
    http_header = {
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': ncloud_accesskey,
        'x-ncp-apigw-signature-v2': make_signature(ncloud_accesskey, ncloud_secretkey, method, path, timestamp)
    }

    #LB List API 호출
    LB_List_Response = send_request(url=url + path, headers=http_header, method=method)
    real_data = json.loads(LB_List_Response)
    
    response = real_data["getLoadBalancerInstanceListResponse"]['loadBalancerInstanceList']
    extracted_lb_list= []
    
    for LB_List in response:
        lb_subnet = []
        LB_name = LB_List.get("loadBalancerName")
        LB_ip = LB_List.get("loadBalancerIpList")
        LB_Domain = LB_List.get("loadBalancerDomain")
        LB_Type = LB_List.get("loadBalancerType")
        LB_Network_Type = LB_List.get("loadBalancerNetworkType")
        LB_Throughput_Type = LB_List.get("throughputType")
        LB_VPC_No = LB_List.get("vpcNo")
        LB_Subnet_no = LB_List.get("subnetNoList", [])  # 기본값으로 빈 리스트 설정에만 추가
        # LB_Subnet_no가 리스트 타입이라면 순차적으로 각 요소에 대해 subnet_Name_Return 호출
        if isinstance(LB_Subnet_no, list):
            for subnet_no in LB_Subnet_no:  # 리스트의 각 요소에 대해 반복
                subnet_name = getSubnetList.subnet_Name_Return(subnet_no)  # 함수 호출
                if subnet_name:  # 함수 반환값이 None이 아닌 경우에만 추가
                    lb_subnet.append(subnet_name)
        LB_VPC_Name = getVPCList.vpc_Name_Return(LB_VPC_No)
        extracted_lb_list.append({
          "LB_name": LB_name,
          "LB_IP": LB_ip,
          "LB_Domain": LB_Domain,
          "LB_Type": LB_Type,
          "LB_Network_Type": LB_Network_Type,
          "LB_Throughput_Type": LB_Throughput_Type,
          "VPC": LB_VPC_Name,
          "Subnet": lb_subnet
      })

    return extracted_lb_list
  

data = get_LB_List()
print(data)