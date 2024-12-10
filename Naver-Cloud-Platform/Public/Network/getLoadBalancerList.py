import os
import sys
import time
import json
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Auth.signature import make_signature
from send_request import send_request
from Auth.auth_Key import ncloud_accesskey, ncloud_secretkey, public

def LB_List():
    # unix timestamp 설정
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    # 메소드 정보
    method = "GET"

    # API 서버 정보
    url = public

    # API URI
    path = "/vloadbalancer/v2/getLoadBalancerInstanceList?regionCode=KR&responseFormatType=json"
    print(url + path)
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
        LB_name = LB_List.get("loadBalancerName")
        LB_IP = LB_List.get("loadBalancerIpList")
        LB_Domain = LB_List.get("loadBalancerDomain")
        LB_Type = LB_List.get("loadBalancerType")
        LB_Network_Type = LB_List.get("loadBalancerNetworkType")
        LB_Throughput_Type = LB_List.get("throughputType")
        LB_VPC_No = LB_List.get("vpcNo")
        LB_Subnet_no = LB_List.get("loadBalancerSubnetList")
        extracted_lb_list.append({
          "LB_name": LB_name,
          "LB_IP": LB_IP,
          "LB_Domain": LB_Domain,
          "LB_Type": LB_Type,
          "LB_Network_Type": LB_Network_Type,
          "LB_Throughput_Type": LB_Throughput_Type
      })

    return extracted_lb_list


import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Server.getServerList import get_Server_List


data = get_Server_List()
print(data)