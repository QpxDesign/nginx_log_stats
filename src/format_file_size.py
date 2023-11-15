def format_file_size(size_in_bytes):
    if float(size_in_bytes) > 1024*1024*1024:
        return str(format(int(round(float(size_in_bytes)/1024/1024/1024,0)),",d")) + "GB"
    if float(size_in_bytes) > 1024*1024:
        return str(format (int(round(int(size_in_bytes)/1024/1024,2)),',d')) + "MB"
    return str(format (int(round(int(size_in_bytes)/1024,2)),',d')) + "KB"