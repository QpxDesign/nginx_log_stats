from sessionize import sessionize
from parse_line import parse_line

def sessions_from_ip(lines, ip):
    sessions = sessionize(lines)
    host_paths = []
    session_start_times = []
    session_end_times = []
    for session_entry in sessions:
        if session_entry["ip_address"] == ip:
            for session in session_entry["sessions"]:
                host_path = []
                if len(session) != 0 and len(session) != 1:
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
