from user_agents import parse as ua_parse
import re

def decipher_ua_agent(line, desired_os, mobile_only, desired_ua_legitmacy, desired_browser):
    ua = re.findall('"(.*?)"',line)[3]
    parsed_ua = ua_parse(ua)
    if desired_os is not None and parsed_ua.os != desired_os:
        return False
    if parsed_ua.is_mobile:
        if mobile_only is not None and mobile_only.lower() == "true":
            return False
    if parsed_ua.is_bot:
        if desired_ua_legitmacy is not None desired_ua_legitmacy == "true":
            return False
    if desired_browser is not None and parsed_ua.browser != desired_browser:
        return False
    return True
