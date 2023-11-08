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

args = parser.parse_args()

if args.file == None:
    raise Exception("File must be provided (your access.log).")

def keep_log(line):
    parsed_line = parse_line(line)
    if args.search is not None and re.search(r''+str(args.search),string=line) is None:
        return False
    if args.start_date is not None and args.end_date is None:
        if parsed_line['time'] < parse_nginx_time_format(args.start_date):
            return False
    if args.end_date is not None and args.start_date is None:
        if parsed_line['time'] > parse_nginx_time_format(args.end_date):
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
            "host":fields[5],
            "request":f'{fields[6]} {fields[7]}',
            "status":fields[9]
            }

def parse_nginx_time_format(time):
    return datetime.strptime(time,"%d/%b/%Y:%H:%M:%S")

if __name__ == "__main__":
    with open(f'./{args.file}', 'r') as f:
        final_lines = []
        lines = f.readlines()
        for line in lines:
            if keep_log(line):
                final_lines.append(line)
        for line in final_lines:
            print(line)
