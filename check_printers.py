import asyncio
import csv
from tabulate import tabulate
from pysnmp.hlapi.v3arch.asyncio import (
    get_cmd, SnmpEngine, CommunityData, UdpTransportTarget,
    ContextData, ObjectType, ObjectIdentity
)

async def get_toner_status(ip, community='public'):
    """
    This function take an ip of a printer and returns the toner status
    """
    base_oid = '1.3.6.1.2.1.43.11.1.1'
    level_oid = f'{base_oid}.9.1.1'  # prtMarkerSuppliesLevel
    max_oid   = f'{base_oid}.8.1.1'  # prtMarkerSuppliesMaxCapacity
    desc_oid  = f'{base_oid}.6.1.1'  # prtMarkerSuppliesDescription

    target = await UdpTransportTarget.create((ip, 161), timeout=2, retries=3)

    # Get toner level
    level_result = await get_cmd(
        SnmpEngine(),
        CommunityData(community, mpModel=0),
        target,
        ContextData(),
        ObjectType(ObjectIdentity(level_oid))
    )
    #get_cmd() returns (errorIndication, errorStatus, errorIndex, varBinds), varBinds[0][0] is oid, varBinds[0][1] is returned value
    level = int(level_result[3][0][1])
    

    # Get max capacity
    max_result = await get_cmd(
        SnmpEngine(),
        CommunityData(community, mpModel=0),
        target,
        ContextData(),
        ObjectType(ObjectIdentity(max_oid))
    )
    max_capacity = int(max_result[3][0][1])

    # Get description (optional)
    desc_result = await get_cmd(
        SnmpEngine(),
        CommunityData(community, mpModel=0),
        target,
        ContextData(),
        ObjectType(ObjectIdentity(desc_oid))
    )
    desc = str(desc_result[3][0][1])

    return {
        'ip': ip,
        'description': desc,
        'level': level,
        'max_capacity': max_capacity
    }

def load_ips_from_csv(file_path):
    ip_list = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            comment = row.get('comment', '').strip()
            if comment.lower() != 'disabled':
                ip_list.append({'ip': row['ip'].strip(), 'comment': comment})
    return ip_list

async def check_printers(file_path):
    ip_entries = load_ips_from_csv(file_path)
    table_data = []

    for entry in ip_entries:
        ip = entry['ip']
        comment = entry['comment']
        result = await get_toner_status(ip)

        if 'error' in result:
            table_data.append([ip, "ERROR", comment, "-", "-", "Unknown"])
        else:
            level = result['level']
            max_capacity = result['max_capacity']
            if level >= 0 and max_capacity > 0:
                percent = f"{round((level / max_capacity) * 100)}%"
            else:
                percent = "Unknown"

            table_data.append([
                result['ip'],
                result['description'],
                comment,
                level,
                max_capacity,
                percent
            ])

    headers = ["IP Address", "Description", "Comment", "Remaining", "Max Capacity", "Toner %"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

# Example usage
asyncio.run(check_printers('printers.csv'))
