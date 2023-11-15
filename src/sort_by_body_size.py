from parse_line import parse_line
 
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