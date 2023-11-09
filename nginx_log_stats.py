import os
import argparse
import re
from datetime import datetime


parser = argparse.ArgumentParser(
                    prog='nginx_log_stats',
                    description='gives you a statsitcal view of NGINX requests from an access.log',
                    epilog='For support, contact Quinn (https://github.com/qpxdesign)')


parser.add_argument('-f', '--file', help='file to search in (your NGINX access.log)')
parser.add_argument('-s', '--search', help='General search term to match specific log lines (like for User Agents, specific IPs, etc), either plaintext or regex')
parser.add_argument('-b', '--start_date',help='find logs within given timespan, provide like 08/Nov/2023:08:25:12')
parser.add_argument('-e','--end_date', help='provide like 08/Nov/2023:08:25:12')
parser.add_argument('-w', '--host')
parser.add_argument('-r', '--request')
parser.add_argument('-st', '--status')
parser.add_argument('-a', '--analytics',help='See analytical view of of log selection', action='store_true')
parser.add_argument('-u','--unique',help='use this to only show one entry for every ip',action='store_true')

args = parser.parse_args()

if args.file == None:
    raise Exception("File must be provided (your access.log).")

def main():
    def keep_log(line):
        parsed_line = parse_line(line)
        if args.search is not None and re.search(re.compile(args.search),string=line) is None:
            return False
        if args.start_date is not None and args.end_date is None:
            if parse_nginx_time_format(parsed_line['time']) < parse_nginx_time_format(args.start_date):
                return False
        if args.end_date is not None and args.start_date is None:
            if parse_nginx_time_format(parsed_line['time']) > parse_nginx_time_format(args.end_date):
                return False
        if args.start_date is not None and args.end_date is not None and (parse_nginx_time_format(parsed_line['time']) > parse_nginx_time_format(args.end_date) or parse_nginx_time_format(parsed_line['time']) < parse_nginx_time_format(args.start_date)):
            return False
        if args.host is not None and parsed_line["host"] != args.host:
            return False
        if args.request is not None and args.request not in parsed_line["request"]:
            return False
        if args.status is not None and parsed_line["status"] != args.status:
            return False
        return True

    def parse_line(line):
        fields = line.split(" ")
        return {
                "ip_address":fields[0],
                "time":fields[3].replace("[",""),
                "host":fields[5].replace('"',""),
                "request":f'{fields[6]} {fields[7]}',
                "status":fields[9],
                "body_bytes_sent":re.sub("[^\d\.]", "",fields[10]),
                "request_time":re.sub("[^\d\.]", "",fields[15])
                }

    def unique_ips_only(lines,field):
        ip_occurances = {}
        for line in lines:
            unique_key = line.split(" ")[0]
            if unique_key not in ip_occurances:
                ip_occurances[unique_key] = line
        ans = []
        for address,entry in ip_occurances.items():
            ans.append(entry)
        return ans

    def parse_nginx_time_format(time):
        return datetime.strptime(time,"%d/%b/%Y:%H:%M:%S")

    def generate_analytical_output(log_selection):
        stats = {
                "request_count":0,
                "top_5_requests":{},
                "top_5_hosts":{},
                "average_body_byte_speed":0,
                "average_requests_per_minute":0,
                }
        for line in log_selection:
            parsed_line = parse_line(line)
            stats["request_count"] += 1
            try:
                stats["average_body_byte_speed"] += (float(parsed_line["body_bytes_sent"])/(float(parsed_line["request_time"])+.00001))
            except:
                stats["average_body_byte_speed"] += 0
            if parsed_line["request"] not in stats["top_5_requests"]:
                stats["top_5_requests"][parsed_line["request"]] = {
                        "request_text":parsed_line["request"],
                        "count": 1
                        }
            stats["top_5_requests"][parsed_line["request"]]["count"] += 1

            if parsed_line["host"] not in stats["top_5_hosts"]:
                stats["top_5_hosts"][parsed_line["host"]] = {
                        "host_text":parsed_line["host"],
                        "count": 1
                        }
            stats["top_5_hosts"][parsed_line["host"]]["count"] += 1

        stats["average_body_byte_speed"] = stats["average_body_byte_speed"] / stats["request_count"]
        stats["average_requests_per_minute"] = stats["request_count"]/((parse_nginx_time_format(parse_line(log_selection[-1])["time"]) - parse_nginx_time_format(parse_line(log_selection[0])["time"])).total_seconds()/60)

        new_requests = []
        new_hosts = []
        for request,entry in stats["top_5_requests"].items():
            new_requests.append(entry)

        for host,entry in stats["top_5_hosts"].items():
            new_hosts.append(entry)

        new_hosts.sort(key=lambda x:x != None and x.get("count"),reverse=True)
        new_requests.sort(key=lambda x:x != None and x.get("count"),reverse=True)

        stats["top_5_requests"] = new_requests[:5]
        stats["top_5_hosts"] = new_hosts[:5]

        top_5_hosts_output = ""
        top_5_requests_output = ""
        for item in stats["top_5_hosts"]:
            top_5_hosts_output += f"-{item['host_text']} ~ {format(item['count'],',d')} \n".replace('"','')

        for item in stats["top_5_requests"]:
            top_5_requests_output += f"-{item['request_text']} ~ {format(item['count'],',d')} \n".replace('"','')

        print(f"""
===~ LOG SELECTION STATS ~===
Total Requests: {format (stats['request_count'], ',d')}
Requests Per Min: {round(stats['average_requests_per_minute'],2)}
Average Body Transfer Speed: {round(stats['average_body_byte_speed']/1024/1024,2)} MB/S

Top 5 Requests:
{top_5_requests_output}
Top 5 Hosts:
{top_5_hosts_output}
""")
    with open(f'./{args.file}', 'r') as f:
        final_lines = []
        lines = f.readlines()
        for line in lines:
            if keep_log(line):
                final_lines.append(line)
        if args.unique:
            final_lines = unique_ips_only(final_lines)
        if args.analytics:
            generate_analytical_output(final_lines)
        else:
            for line in final_lines:
                print(line)

if __name__ == "__main__":
    main()
