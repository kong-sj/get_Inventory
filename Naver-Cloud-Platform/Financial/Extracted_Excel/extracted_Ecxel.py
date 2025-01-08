import os
financial_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(financial_root)
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import pandas as pd
from Network.getSubnetList import get_Subnet_List
from Network.getRouteTable import combine_data
from Network.getLoadBalancerList import get_LB_List
from Server.getServerList import get_Server_List


data_lb = get_LB_List()
data_subnet = get_Subnet_List()
data_route = combine_data()
data_server = get_Server_List()


excel_data_Network = []
excel_data_Server = []
excel_data_lb = []
excel_data_routing = []

for item in data_lb:
    excel_data_lb.append({
        "LB_name": item.get('LB_name'),
        "LB_IP": ", ".join(item.get('LB_IP', [])),  # 리스트를 문자열로 변환
        "LB_Domain": item.get('LB_Domain'),
        "LB_Type": item.get('LB_Type', {}).get('codeName'),
        "LB_Network_Type": item.get('LB_Network_Type', {}).get('codeName'),
        "LB_Throughput_Type": item.get('LB_Throughput_Type', {}).get('codeName'),
        "VPC": item.get('VPC'),
        "Subnet": ", ".join(item.get('Subnet', []))  # Subnet이 None일 수 있으니 기본값 처리
    })


for key, item in data_subnet.items():
    excel_data_Network.append({
        'Subnet Name': item['subnet_name'],
        'Subnet CIDR': item['subnet_cidr'],
        'Subnet Type Name': item['subnet_type']['codeName'],        'Subnet Zone': item['subnet_zone']
    })

    
for vpc_no, vpc_details in data_route.items():
    # 각 VPC의 route_data와 route_target_data를 매핑
    route_data = {route["route_no"]: route["route_name"] for route in vpc_details.get("route_data", [])}
    route_target_data = vpc_details.get("route_target_data", [])
    
    for route in route_target_data:
        route_no = route.get("route_no")  # route_no를 통해 route_name 매핑
        excel_data_routing.append({
            "VPC_No": vpc_no,
            "Route_Name": route_data.get(route_no, "Unknown"),  # 매핑된 route_name, 없으면 "Unknown"
            "Dest_CIDR": route.get("dest_cidr"),
            "Target_Name": route.get("target_name"),
            "Target_Type": route.get("target_type"),
        })


for item in data_server:
  excel_data_Server.append({
    "Server Name": item['server_name'],
    "Public IP": item.get('Public IP', ''),  # 공백으로 기본값 처리
    "Private IP": item['Private_IP'],
    "VPC": item['vpc_name'],
    "Subnet": item['subnet_name'],
    "Spec": item['Spec'],
    "CPU": item['CPU'],
    "Memory": item['Memory'],
    "Key name": item['Key Name'],
    'Block Storage': item['Block Storage'][0]['BlockStorage_Size'],
    "Hyper Visor": item['Hypervisor_Type']['code'],
    'OS': item['OS_Release']
  })


# DataFrame으로 변환
df_lb = pd.DataFrame(excel_data_lb)
df_network = pd.DataFrame(excel_data_Network)
df_routing = pd.DataFrame(excel_data_routing)
df_server = pd.DataFrame(excel_data_Server)


# 엑셀 파일로 저장
save_path = "/Users/mzc01-sjhong/OneDrive/Study/Develop/python-project/inventory/fin_extracted_excel.xlsx"
with pd.ExcelWriter(save_path, engine='xlsxwriter') as writer:
    # 네트워크 데이터를 "Network" 시트에 저장
    df_network.to_excel(writer, sheet_name='Network', index=False)
    # Server 데이터를 "server" 시트에 저장
    df_server.to_excel(writer, sheet_name='Server', index=False)
    # LoadBalancer 데이터를 "LoadBalancer" 시트에 저장
    df_lb.to_excel(writer, sheet_name='LoadBalancer', index=False)
    # Routing 데이터를 "Routing Table" 시트에 저장
    df_routing.to_excel(writer, sheet_name="Routing Table", index=False)
print("엑셀 파일로 저장 완료!")