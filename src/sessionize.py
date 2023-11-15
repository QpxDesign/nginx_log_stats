from parse_nginx_time_format import parse_nginx_time_format
from parse_line import parse_line

def sessionize(lines):
    ip_occurances = {}
    output = {}
    SESSION_CUTOFF_MIN = 10
    for line in lines:
        parsed_line = parse_line(line)
        ip = parsed_line["ip_address"]
        if parsed_line["ip_address"] not in ip_occurances:
            ip_occurances[ip] = {
                    "ip_address":parsed_line["ip_address"],
                    "lines": [line],
                    "times": [parse_nginx_time_format(parsed_line["time"]).timestamp()]
                    }
        else:
            ip_occurances[ip]["lines"].append(line)
            ip_occurances[ip]["times"].append(parse_nginx_time_format(parsed_line["time"]).timestamp())
    for ip,entry in ip_occurances.items():
        sessions = []
        index = 0
        tmp = []
        for l in entry["times"]:
            if index == 0:
                tmp.append(entry["lines"][0])
            elif l - entry["times"][index-1] < SESSION_CUTOFF_MIN*60:
                tmp.append(entry["lines"][index])
            else:
                sessions.append(tmp)
                tmp = []
            index += 1
        ip_occurances[ip]["sessions"] = sessions
    return [value for value in ip_occurances.values()]