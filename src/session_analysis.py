from sessionize import sessionize
from parse_line import parse_line

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
{round(stats['average_request_count'],2)} Avg Requests Per Session
{round(stats['average_request_length']/60)}min Avg Session Length

MOST COMMON PATHS
=================
{host_path_text.replace('[','').replace(']','')}

IPS WITH MOST SESSIONS
======================
{ips_text}
""")
