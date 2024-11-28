import os
import sys
import time
import json
from collections import defaultdict
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Auth.signature import make_signature
from send_request import send_request
from Auth.auth_Key import ncloud_accesskey, ncloud_secretkey, public
from pprint import pprint


def get_routeTable_List():
    timestamp = str(int(time.time() * 1000))
    method = "GET"
    url = public
    path = "/vpc/v2/getRouteTableList?regionCode=KR&responseFormatType=json"

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
        url = public
        path = f"/vpc/v2/getRouteTableSubnetList?regionCode=KR&responseFormatType=json&routeTableNo={route_no}"

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
        url = public
        path = f"/vpc/v2/getRouteList?regionCode=KR&responseFormatType=json&routeTableNo={route_no}&vpcNo={vpc_no}"

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