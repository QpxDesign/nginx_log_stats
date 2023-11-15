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