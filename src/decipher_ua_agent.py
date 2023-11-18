from user_agents import parse as ua_parse
import re

def decipher_ua_agent(line, desired_os, mobile_only, not_mobile, only_bots, no_bots, desired_browser):
    ua = re.findall('"(.*?)"',line)[3]
    parsed_ua = ua_parse(ua)

    if desired_os is not None and parsed_ua.os.family.lower() != desired_os.lower():
        return False
    if parsed_ua.is_mobile and not_mobile:
        return False
    if not parsed_ua.is_mobile and mobile_only:
        return False
    if parsed_ua.is_bot and no_bots:
        return False
    if not parsed_ua.is_bot and only_bots:
        return False
    if desired_browser is not None and parsed_ua.browser.lower() != desired_browser.lower():
        return False
    return True
