import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import pandas as pd
from Network import getSubnetList, getRouteTable
from Server import getServerList

# Sample data to be exported
data_subnet = getSubnetList.get_Subnet_List()
data_route = getRouteTable.get_Route_List()
data_server = getServerList.get_Server_List()

# 데이터를 엑셀에 맞게 변환 (subnet_type 내에 있는 값들을 풀어서 저장)
excel_data = []
for item in data_subnet:
    excel_data.append({
        'Subnet Name': item['subnet_name'],
        'Subnet CIDR': item['subnet_cidr'],
        'Subnet Type Name': item['subnet_type']['codeName'],
        'Subnet Zone': item['subnet_zone']
        # 'Region': item['']x
    })
    print(excel_data)
    
for item in data_route:
    excel_data.append({
        'Dest_CIDR': item['dest_cidr'],
        'Target_name': item['target_name']
    })
    print(excel_data)

for item in data_server:
  excel_data.append({
    "Server Name": item['']
  })

# DataFrame으로 변환
df_network = pd.DataFrame(excel_data)

# 엑셀 파일로 저장
save_path = "/Users/mzc01-sjhong/OneDrive/Study/Develop/python-project/Naver-Cloud-Platform/Extracted_Excel/extracted_excel.xlsx"
with pd.ExcelWriter(save_path, engine='xlsxwriter') as writer:
    # 네트워크 데이터를 "Network" 시트에 저장
    df_network.to_excel(writer, sheet_name='Network', index=False)

print("엑셀 파일로 저장 완료!")