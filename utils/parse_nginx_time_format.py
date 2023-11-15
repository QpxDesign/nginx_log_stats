from datetime import datetime

def parse_nginx_time_format(time):
    return datetime.strptime(time,"%d/%b/%Y:%H:%M:%S")
