import os
import argparse
import re
from datetime import datetime
import time
import json

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
parser.add_argument('-ref','--referer')
parser.add_argument('-a', '--analytics',help='See analytical view of of log selection', action='store_true')
parser.add_argument('-u','--unique',help='use this to only show one entry for every ip',action='store_true')
parser.add_argument('-l','--large',help='find largest <n> requests, use like -l 10')
parser.add_argument('-lst','--last',help='find all requests within the last <n> min')
parser.add_argument('-sa','--session_analytics',help='gather analytics by session instead of by line (see docs)',action='store_true')
parser.add_argument('-ip_ses','--ip_session',help='see all sessions from ip')

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
        if args.referer is not None and parsed_line["referer"] != args.referer:
            return False
        if args.last is not None and parse_nginx_time_format(parsed_line["time"]).timestamp() < (time.time()- float(args.last)*60):
            return False
        return True

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
                "request_time":re.sub("[^\d\.]", "",fields[15]) if len(fields) >= 10 else '-'
            }

    def unique_ips_only(lines):
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
                "top_5_ips":{},
                "average_body_byte_speed":0,
                "average_requests_per_minute":0,
                "total_data_transfered":0
                }
        for line in log_selection:
            parsed_line = parse_line(line)
            stats["request_count"] += 1
            try:
                stats["average_body_byte_speed"] += (float(parsed_line["body_bytes_sent"])/(float(parsed_line["request_time"])+.00001))
                stats["total_data_transfered"] += float(parsed_line["body_bytes_sent"])
            except:
                stats["average_body_byte_speed"] += 0

            if parsed_line["request"] not in stats["top_5_requests"]:
                stats["top_5_requests"][parsed_line["request"]] = {
                        "request_text":parsed_line["request"],
                        "count": 0
                        }
            stats["top_5_requests"][parsed_line["request"]]["count"] += 1

            if parsed_line["host"] not in stats["top_5_hosts"]:
                stats["top_5_hosts"][parsed_line["host"]] = {
                        "host_text":parsed_line["host"],
                        "count": 0
                        }

            if parsed_line["ip_address"] not in stats["top_5_ips"]:
                stats["top_5_ips"][parsed_line["ip_address"]] = {
                        "ip_text":parsed_line["ip_address"],
                        "count":0
                        }

            stats["top_5_ips"][parsed_line["ip_address"]]["count"] += 1
            stats["top_5_hosts"][parsed_line["host"]]["count"] += 1

        stats["average_body_byte_speed"] = stats["average_body_byte_speed"] / stats["request_count"]
        stats["average_requests_per_minute"] = stats["request_count"]/((parse_nginx_time_format(parse_line(log_selection[-1])["time"]) - parse_nginx_time_format(parse_line(log_selection[0])["time"])).total_seconds()/60)

        new_requests = []
        new_hosts = []
        new_ips = []
        for request,entry in stats["top_5_requests"].items():
            new_requests.append(entry)

        for host,entry in stats["top_5_hosts"].items():
            new_hosts.append(entry)

        for ip,entry in stats["top_5_ips"].items():
            new_ips.append(entry)

        new_hosts.sort(key=lambda x:x != None and x.get("count"),reverse=True)
        new_requests.sort(key=lambda x:x != None and x.get("count"),reverse=True)
        new_ips.sort(key=lambda x:x != None and x.get("count"),reverse=True)

        stats["top_5_requests"] = new_requests[:5]
        stats["top_5_hosts"] = new_hosts[:5]
        stats["top_5_ips"] = new_ips[:5]

        top_5_hosts_output = ""
        top_5_requests_output = ""
        top_5_ips_output = ""
        for item in stats["top_5_hosts"]:
            top_5_hosts_output += f"- {item['host_text']} ~ {format(item['count'],',d')} \n".replace('"','')

        for item in stats["top_5_requests"]:
            top_5_requests_output += f"- {item['request_text']} ~ {format(item['count'],',d')} \n".replace('"','')

        for item in stats["top_5_ips"]:
            if item["ip_text"] != "-":
                top_5_ips_output += f"- {item['ip_text']} ~ {format(item['count'],',d')} \n".replace('"','')

        print(f"""
===~ LOG SELECTION STATS ~===
Total Requests: {format (stats['request_count'], ',d')}
Requests Per Min: {round(stats['average_requests_per_minute'],2)}
Average Body Transfer Speed: {round(stats['average_body_byte_speed']/1024/1024,2)} MB/S
Total Data Transfered: {format_file_size(stats['total_data_transfered'])}

Top 5 Requests:
{top_5_requests_output}
Top 5 Hosts:
{top_5_hosts_output}
Top 5 IP Addresses:
{top_5_ips_output}
""")
    def sort_by_body_size(lines):
        parsed_lines = []
        for line in lines:
            if parse_line(line)["body_bytes_sent"] != None:
                parsed_lines.append({
                    "text":line,
                    "body_size":parse_line(line)["body_bytes_sent"]
                })
        parsed_lines.sort(key=lambda x:x != None and float(x.get("body_size")),reverse=True)
        ans = []
        for line in parsed_lines:
            ans.append(line["text"])
        return ans

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

    def format_file_size(size_in_bytes):
        if float(size_in_bytes) > 1024*1024*1024:
            return str(format(int(round(float(size_in_bytes)/1024/1024/1024,0)),",d")) + "GB"
        if float(size_in_bytes) > 1024*1024:
            return str(format (int(round(int(size_in_bytes)/1024/1024,2)),',d')) + "MB"
        return str(format (int(round(int(size_in_bytes)/1024,2)),',d')) + "KB"

    def sessions_from_ip(lines):
        sessions = sessionize(lines)
        print(args.ip_session)
        host_paths = []
        session_start_times = []
        session_end_times = []
        for session_entry in sessions:
            if session_entry["ip_address"] == args.ip_session:
                print(len(sessions))
                for session in session_entry["sessions"]:     
                    host_path = []
                    session_start_times.append(parse_line(session[0])["time"])
                    session_end_times.append(parse_line(session[-1])["time"])
                    for line in session:
                        if len(host_path) == 0 or host_path[-1] != parse_line(line)["host"]:
                            host_path.append(parse_line(line)["host"])     
                    host_paths.append(host_path)
        index = 0
        for path in host_paths:
             print('------------------------------')
             print(f"======= {session_start_times[index]}")
             print(str(path).replace('[','').replace(']','').replace(',', ' --> '))
             print(f"======= {session_end_times[index]}")
             print('------------------------------')
             index += 1
        
    def session_analysis(lines):
        sessions = sessionize(lines)
        stats = {
                "total_count":0,
                "host_paths":{},
                "average_request_count":0,
                "average_request_length":0,
                }
        for session_entry in sessions:
            stats["total_count"] += 1
            host_path = []
            for line in session_entry["lines"]:
                if len(host_path) == 0 or host_path[-1] != parse_line(line)["host"]:
                    host_path.append(parse_line(line)["host"])
            if str(host_path) not in stats["host_paths"]:
                stats["host_paths"][str(host_path)] = {
                    "path": str(host_path),
                    "count":1,
                }
            else:
                stats["host_paths"][str(host_path)]["count"] += 1
            stats["average_request_count"] += len(host_path)
            stats["average_request_count"] =  session_entry["times"][-1] - session_entry["times"][0]

        stats["average_request_count"] = stats["average_request_count"] / stats["total_count"]
        stats["average_request_length"] = stats["average_request_length"] / stats["total_count"]

        stats["host_paths"] = [value for value in stats["host_paths"].values()]
        stats["host_paths"].sort(key=lambda x:x != None and x.get("count"),reverse=True)
        sessions.sort(key=lambda x:x != None and len(x.get("sessions")),reverse=True)

        host_path_text = ""
        ips_text = ""
        for path_entry in stats["host_paths"][:5]:
            host_path_text += f"- {path_entry['path'].replace(',',' --> ')} ({path_entry['count']})\n"

        for s in sessions[:10]:
            ips_text += f"- {s['ip_address']} ({len(s['sessions'])})\n"


        print(f"""
SESSION STATS
==============
{stats['total_count']} Total Unique Sessions
{stats['average_request_count']} Avg Requests Per Session
{round(stats['average_request_length']/60)}min Avg Session Length

MOST COMMON PATHS
=================
{host_path_text.replace('[','').replace(']','')}

IPS WITH MOST SESSIONS
======================
{ips_text}
""")


    with open(f'{args.file}', 'r') as f:
        final_lines = []
        lines = f.readlines()
        for line in lines:
            if keep_log(line):
                final_lines.append(line)
        if args.session_analytics:
            session_analysis(final_lines)
            return
        if args.ip_session != None:
            sessions_from_ip(final_lines)
            return
        if args.unique:
            final_lines = unique_ips_only(final_lines)
        if args.analytics:
            generate_analytical_output(final_lines)
            return
        if args.large != None and args.large.isnumeric():
            l = sort_by_body_size(final_lines)
            for line in l[:int(args.large)]:
                print(f"{format_file_size(parse_line(line)['body_bytes_sent'])} {parse_line(line)['ip_address']} {parse_line(line)['host']} {parse_line(line)['request']}")
            return
        for line in final_lines:
            print(line)

if __name__ == "__main__":
    main()
