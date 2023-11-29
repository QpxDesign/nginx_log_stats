import re

def parse_line(line):
        fields = line.split(" ")
        return {
        "ip_address":fields[0],
        "time":fields[3].replace("[","") if len(fields) >= 3 else '-',
        "host":fields[5].replace('"',"") if len(fields) >= 5 else '-',
        "referer":fields[11].replace('"',''),
        "request":f'{fields[6]} {fields[7]}' if len(fields) >= 6 else '-',
        "status":fields[9] if len(fields) >= 9 else '-',
        "body_bytes_sent": fields[10] if fields[10].isnumeric() and len(fields) >= 10 else 0,
        "request_time":re.sub('"(.*?)"', "",line).split(" ")[12] if len(re.sub('"(.*?)"', "",line).split(" ")) >= 13 else '-'
        }
