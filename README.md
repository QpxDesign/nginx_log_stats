## NGINX Log Stats
### Comb through NGINX logs instantly

### Usage
To run this, use `ngxav`.

If you're using the default NGINX Log Format, this should be working right out of the box.
You can use the following flags to search using different parameters:
- `-f/--file` - REQUIRED, specifcy the path to the file you wish to search through
- `-s/--search`- OPTIONAL, either REGEX or text to match lines
- `-b/--start_date`- OPTIONAL (must use with `-e/--end_date`), find all logs within certain timespan (use time format08/Nov/2023:08:04:05)
- `-e/--end_date`- OPTIONAL (must use with `-b/--start_date`), find all logs within certain timespan (use time format08/Nov/2023:08:04:05)
- `-w/--host`- OPTIONAL, match for specific host (like site.domain.com)
- `-r/--request`- OPTIONAL, find all entries for specific request (like GET /home/)
- `-st/--status`- OPTIONAL, find all entries for specific HTTP status code (like 200, 404, etc)
- `-u/--unique` - OPTIONAL, only show latest request of each IP address within log selection
- `-a/--analytics` - OPTIONAL, show a analytical view of your log selection, instead of just the raw logs

Example Run: `ngxav -f access.log -u`
### Contribute/Issues
We welcome contributions and bug reports/issues! Just submit a pull request to the repo - [Github](https://github.com/qpxdesign/nginginx_log_stats)

### License (MIT)
MIT License

Copyright (c) [2023] [Quinn Patwardhan]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
