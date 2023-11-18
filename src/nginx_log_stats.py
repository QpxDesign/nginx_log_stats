import argparse
import re
import time
from format_file_size import format_file_size
from generate_analytical_output import generate_analytical_output
from parse_line import parse_line
from parse_nginx_time_format import parse_nginx_time_format
from sort_by_body_size import sort_by_body_size
from session_analysis import session_analysis
from sessions_from_ip import sessions_from_ip
from unique_ips_only import unique_ips_only
from decipher_ua_agent import decipher_ua_agent

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
parser.add_argument('--uaos',help='see all requests from devices running specific OS, from useragent')
parser.add_argument('--bot',help='Show requests from bots (determined from user agent)',action='store_true')
parser.add_argument('--nobot',help='Show requests NOT from bots (determined from user agent)', action='store_true')
parser.add_argument('--mobile', help='Show requests from mobile (determined from user agent)', action='store_true')
parser.add_argument('--nomobile', help='Show requests NOT from mobile', action='store_true')
parser.add_argument('--ua_browser',help='see all requests from specific browser')

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
        if not decipher_ua_agent(line,args.uaos, args.mobile, args.nomobile, args.bot, args.nobot, args.ua_browser):
            return False
        return True

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
            sessions_from_ip(final_lines,ip=args.ip_session)
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
