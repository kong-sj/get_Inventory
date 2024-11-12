# import os
# import sys
# import time
# import json
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# from Auth.signature import make_signature
# from send_request import send_request
# from Auth.auth_Key import ncloud_accesskey, ncloud_secretkey
# from pprint import pprint

# def get_routeTable_List():
#     # unix timestamp 설정
#     timestamp = int(time.time() * 1000)
#     timestamp = str(timestamp)

#     # 메소드 정보
#     method = "GET"

#     # API 서버 정보
#     url = "https://fin-ncloud.apigw.fin-ntruss.com"

#     # API URL 서버 목록 조회
#     path = "/vpc/v2/getRouteTableList?regionCode=FKR&responseFormatType=json"
#     # http 호출 헤더값 설정
#     http_header = {
#         'x-ncp-apigw-timestamp': timestamp,
#         'x-ncp-iam-access-key': ncloud_accesskey,
#         'x-ncp-apigw-signature-v2': make_signature(ncloud_accesskey, ncloud_secretkey, method, path, timestamp)
#     }

#     #Route List API 호출
#     route_List_Response = send_request(url=url + path, headers=http_header, method=method)
#     real_data = json.loads(route_List_Response)
    
#     response_route_data = real_data["getRouteTableListResponse"]
#     route_list = response_route_data.get("routeTableList", [])
#     extracted_route_list = []
    
#     for route in route_list:
#         route_name = route.get("routeTableName")  # 'subnetName' 값 추출
#         route_no = route.get("routeTableNo")  # 'subnet' 값 추출
#         vpc_no = route.get("vpcNo")
#         extracted_route_list.append({
#           "route_name": route_name,  # 'subnetName' 값 추출
#           "route_no": route_no,  # 'subnet' 값 추출
#           "vpc_no" : vpc_no
#       })

#     #print(extracted_route_list)    #데이터를 파이썬 딕셔너리 데이터 타입으로 저장
#     return extracted_route_list


# def get_route_Table_Subnet_List():
#     all_extracted_route_subnet_list = []
#     route_Table_No = get_routeTable_List()
#     for route in route_Table_No:
#       route_no = route["route_no"]
#       route_name = route["route_name"]
#     # unix timestamp 설정
#       timestamp = int(time.time() * 1000)
#       timestamp = str(timestamp)

#       # 메소드 정보
#       method = "GET"

#       # API 서버 정보
#       url = "https://fin-ncloud.apigw.fin-ntruss.com"

#       # API URL 서버 목록 조회
#       path = f"/vpc/v2/getRouteTableSubnetList?regionCode=FKR&responseFormatType=json&routeTableNo={route_no}"

#       # http 호출 헤더값 설정
#       http_header = {
#           'x-ncp-apigw-timestamp': timestamp,
#           'x-ncp-iam-access-key': ncloud_accesskey,
#           'x-ncp-apigw-signature-v2': make_signature(ncloud_accesskey, ncloud_secretkey, method, path, timestamp)
#       }

#       #Route List API 호출
#       response = send_request(url=url + path, headers=http_header, method=method)
#       real_data = json.loads(response)
      
#       response_route_data = real_data["getRouteTableSubnetListResponse"]
#       route_subnet_list = response_route_data.get("subnetList", [])
#       extracted_route_subnet_list = []
      
#       for route_subnet in route_subnet_list:
#           subnet_name = route_subnet.get("subnetName")  # 'subnetName' 값 추출
#           subnet_cidr = route_subnet.get("subnet")  # 'subnet' 값 추출
#           vpc_no = route_subnet.get("vpcNo")
#           extracted_route_subnet_list.append({
#             "route_name": route_name,   # Route Name 추출
#             "subnet_name": subnet_name,  # 'subnetName' 값 추출
#             "subnet_cidr": subnet_cidr, # 'subnet' 값 추출
#             "vpc_no": vpc_no,
#             "route_no": route_no
#         })

#       all_extracted_route_subnet_list.extend(extracted_route_subnet_list)
#     # print(all_extracted_route_subnet_list)
#     return all_extracted_route_subnet_list

# ## getRouteList / 목적지 및 타겟타입 불러오기
# def get_Route_List():
#     all_extracted_route_list = []
#     # route_Table_No = get_routeTable_List()
#     # get_Vpc_No = get_routeTable_List()
#     # for route, vpc_no_inven in zip(route_Table_No, get_Vpc_No):
#     #     route_no = route["route_no"]
#     #     vpc_no = vpc_no_inven["vpc_no"]
#     for data in get_routeTable_List():
#         route_no = data["route_no"]
#         vpc_no = data["vpc_no"]      
#       # unix timestamp 설정
#         timestamp = int(time.time() * 1000)
#         timestamp = str(timestamp)

#         # 메소드 정보
#         method = "GET"

#         # API 서버 정보
#         url = "https://fin-ncloud.apigw.fin-ntruss.com"
#         # API URL 서버 목록 조회
#         path_Route_List = f"/vpc/v2/getRouteList?regionCode=FKR&responseFormatType=json&routeTableNo={route_no}&vpcNo={vpc_no}"
#         # print(route_no, vpc_no)
#         # http 호출 헤더값 설정
#         http_header = {
#             'x-ncp-apigw-timestamp': timestamp,
#             'x-ncp-iam-access-key': ncloud_accesskey,
#             'x-ncp-apigw-signature-v2': make_signature(ncloud_accesskey, ncloud_secretkey, method, path_Route_List, timestamp)
#         }        
#         #Route List API 호출
#         response = send_request(url=url + path_Route_List, headers=http_header, method=method)
#         real_data = json.loads(response)
                
#         response_route_data = real_data["getRouteListResponse"]
#         route_list = response_route_data.get("routeList", [])
#         extracted_route_subnet_list = []
        
#         for routeList in route_list:
#             dest_cidr = routeList.get("destinationCidrBlock")  # 'subnetName' 값 추출
#             target_name = routeList.get("targetName")  # 'subnet' 값 추출
#             target_type = routeList.get("vpcNo")
#             extracted_route_subnet_list.append({
#               "dest_cidr": dest_cidr,   # Route Name 추출
#               "target_name": target_name,  # 'subnetName' 값 추출
#               "target_type": target_type, # 'subnet' 값 추출
#               "route_no": route_no
#           })

#         all_extracted_route_list.extend(extracted_route_subnet_list)
#     # print(all_extracted_route_subnet_list)
#     return all_extracted_route_list


# data = []
# data_get_routeTable_List = get_routeTable_List()
# data_route_Table_Subnet_List = get_route_Table_Subnet_List()
# data_Route_List = get_Route_List()


# for item in data_get_routeTable_List:
#   data.append({
#       "route_name": item['route_name'],
#       "route_no": item['route_no'],
#       "vpc_no": item['vpc_no']
#   })


# for item in data_route_Table_Subnet_List:
#   data.append({
#     "subnet_name": item['subnet_name'],
#     "subnet_cidr": item['subnet_cidr'],
#     "route_no": item['route_no']
#   })


# for item in data_Route_List:
#   data.append({
#     "dest_cidr": item['dest_cidr'],
#     "target_name": item['target_name'],
#     "route_no": item['route_no']
#   })

# pprint(data)

##############
import os
import sys
import time
import json
from collections import defaultdict
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Auth.signature import make_signature
from send_request import send_request
from Auth.auth_Key import ncloud_accesskey, ncloud_secretkey
from pprint import pprint


def get_routeTable_List():
    timestamp = str(int(time.time() * 1000))
    method = "GET"
    url = "https://fin-ncloud.apigw.fin-ntruss.com"
    path = "/vpc/v2/getRouteTableList?regionCode=FKR&responseFormatType=json"

    http_header = {
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': ncloud_accesskey,
        'x-ncp-apigw-signature-v2': make_signature(ncloud_accesskey, ncloud_secretkey, method, path, timestamp)
    }

    route_List_Response = send_request(url=url + path, headers=http_header, method=method)
    real_data = json.loads(route_List_Response)
    route_list = real_data["getRouteTableListResponse"].get("routeTableList", [])
    
    return [
        {
            "route_name": route.get("routeTableName"),
            "route_no": route.get("routeTableNo"),
            "vpc_no": route.get("vpcNo")
        }
        for route in route_list
    ]


def get_route_Table_Subnet_List():
    all_extracted_route_subnet_list = []
    for route in get_routeTable_List():
        route_no = route["route_no"]
        timestamp = str(int(time.time() * 1000))
        method = "GET"
        url = "https://fin-ncloud.apigw.fin-ntruss.com"
        path = f"/vpc/v2/getRouteTableSubnetList?regionCode=FKR&responseFormatType=json&routeTableNo={route_no}"

        http_header = {
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': ncloud_accesskey,
            'x-ncp-apigw-signature-v2': make_signature(ncloud_accesskey, ncloud_secretkey, method, path, timestamp)
        }

        response = send_request(url=url + path, headers=http_header, method=method)
        real_data = json.loads(response)
        route_subnet_list = real_data["getRouteTableSubnetListResponse"].get("subnetList", [])
        
        all_extracted_route_subnet_list.extend([
            {
                "subnet_name": subnet.get("subnetName"),
                "subnet_cidr": subnet.get("subnet"),
                "vpc_no": subnet.get("vpcNo"),
                "route_no": route_no
            }
            for subnet in route_subnet_list
        ])
    return all_extracted_route_subnet_list


def get_Route_List():
    all_extracted_route_list = []
    for data in get_routeTable_List():
        route_no = data["route_no"]
        vpc_no = data["vpc_no"]
        timestamp = str(int(time.time() * 1000))
        method = "GET"
        url = "https://fin-ncloud.apigw.fin-ntruss.com"
        path = f"/vpc/v2/getRouteList?regionCode=FKR&responseFormatType=json&routeTableNo={route_no}&vpcNo={vpc_no}"

        http_header = {
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': ncloud_accesskey,
            'x-ncp-apigw-signature-v2': make_signature(ncloud_accesskey, ncloud_secretkey, method, path, timestamp)
        }

        response = send_request(url=url + path, headers=http_header, method=method)
        real_data = json.loads(response)
        route_list = real_data["getRouteListResponse"].get("routeList", [])
        
        all_extracted_route_list.extend([
            {
                "dest_cidr": routeList.get("destinationCidrBlock"),
                "target_name": routeList.get("targetName"),
                "target_type": routeList.get("vpcNo"),
                "route_no": route_no
            }
            for routeList in route_list
        ])
    return all_extracted_route_list


def combine_data():
    data = defaultdict(lambda: {"route_data": [], "subnet_data": [], "route_target_data": []})

    for item in get_routeTable_List():
        route_no = item["route_no"]
        data[route_no]["route_data"].append(item)

    for item in get_route_Table_Subnet_List():
        route_no = item["route_no"]
        data[route_no]["subnet_data"].append(item)

    for item in get_Route_List():
        route_no = item["route_no"]
        data[route_no]["route_target_data"].append(item)

    return data


# 실행 및 결과 확인
combined_data = combine_data()
for route_no, details in combined_data.items():
    print(f"Route No: {route_no}")
    pprint(details)
    print("\n" + "="*40 + "\n")