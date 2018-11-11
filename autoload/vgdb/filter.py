def filter_query_result(buffer_result, keep_all=False):
    lines_to_keep = []
    lines =  buffer_result.replace("\r","").replace("'", "''").replace("\\t", "    ").split("\n")
    for line in lines:
        if line.startswith('~"') or keep_all:
            lines_to_keep.append(line.lstrip('~"').rstrip('\\n"'))
    return lines_to_keep
