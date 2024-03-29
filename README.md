## NGINX Log Stats

### A multi-threaded, deep-search capable, full-featured, and intelligent NGINX log parser
### NO LONGER UPDATED - RE-WRITTEN IN RUST ([NGXAV-RS](https://github.com/QpxDesign/ngxav-rs))
### Install

Run this command to install the package from pip: `pip install nginx-log-stats`

### Usage

To run this, use `ngxav`.

If you're using the default NGINX Log Format, this should be working right out of the box.
You can use the following flags to search using different parameters:

- `-f/--file` - REQUIRED, specifcy the path to the file you wish to search through
- `-s/--search`- OPTIONAL, either REGEX or text to match lines
- `-b/--start_date`- OPTIONAL, find all logs within certain timespan (use time format 08/Nov/2023:08:04:05)
- `-e/--end_date`- OPTIONAL, find all logs within certain timespan (use time format 08/Nov/2023:08:04:05)
- `-w/--host`- OPTIONAL, match for specific host (like site.domain.com)
- `-r/--request`- OPTIONAL, find all entries for specific request (like GET /home/)
- `-st/--status`- OPTIONAL, find all entries for specific HTTP status code (like 200, 404, etc)
- `-u/--unique` - OPTIONAL, only show latest request of each IP address within log selection
- `-a/--analytics` - OPTIONAL, show a analytical view of your log selection, instead of just the raw logs
- `-l/--large <n>` - OPTIONAL, show the n-largest request bodys of log selection
- `-ref/--referer` - OPTIONAL, only show requests that have specifced http referer
- `-sa/--session_analytics` - OPTIONAL, show session-based analytics (a session is a series of user activity (requests) within a specific timespan between interactions)
- `--uaos` - OPTIONAL, see all requests from devices running specific OS, from useragent
- `--bot` - OPTIONAL, Show requests from bots (determined from user agent)
- `--nobot` - OPTIONAL, Show requests NOT from bots (determined from user agent)
- `--mobile` - OPTIONAL, Show requests from mobile (determined from user agent)
- `--nomobile` - Show requests NOT from mobile (determined from user agent)'
- `--ua_browser` - see all requests from specific browser
- `-t/--threads` - specify how many threads to use, will be all by default
- `-c/----conservememory` - specify wether or not to read files line by line to conserve memory (can't use with analytic commands)

#### Example Run: `ngxav -f access.log -a`

Output:

```
===~ LOG SELECTION STATS ~===
Total Requests: 70,759
Requests Per Min: 13.07
Average Body Transfer Speed: 3.05 MB/S
Total Body Size: 30MB

Top 5 Requests:
-GET /mtaAPI ~ 16,960
-GET /get-trains ~ 13,969
-GET /tripUpdatesAPI ~ 11,374
-GET / ~ 7,526
-GET /assets/TimelineIcon.svg ~ 5,594

Top 5 Hosts:
-api.marcmap.app ~ 29,795
-amtrak-api.marcmap.app ~ 18,942
-marcmap.app ~ 7,631
-localhost ~ 6,597
-quinnpatwardhan.com ~ 3,013

Top 5 IP Addresses:
<Redacted>
```

#### Example Run: `ngxav -f access.log -sa`

```
SESSION STATS
==============
3200 Total Unique Sessions
0.0003125 Avg Requests Per Session
0min Avg Session Length

MOST COMMON PATHS
=================
- 'amtrak-api.marcmap.app' (1191)
- 'api.marcmap.app' (439)
- 'amtrak-api.marcmap.app' -->  'marcmap.app' -->  'amtrak-api.marcmap.app' (373)
- 'quinnpatwardhan.com' (189)
- 'marcmap.app' (186)
```

### Contribute/Issues

We welcome contributions and bug reports/issues! Just submit a pull request to the repo - [Github](https://github.com/qpxdesign/nginginx_log_stats)

### Dependencies

- [user-agents](https://pypi.org/project/user-agents/)

### License (MIT)

MIT License

Copyright (c) [2023] [Quinn Patwardhan]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
