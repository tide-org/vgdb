def filter_query_result(buffer_result, keep_all=False):
    lines_to_keep = []
    lines =  buffer_result.replace("\r","").replace("'", "''").replace("\\t", "    ").split("\n")
    for line in lines:
        if line.startswith('~"') or keep_all:
            lines_to_keep.append(line.lstrip('~"').rstrip('\\n"'))
    return lines_to_keep

def filter_lines_for_buffer(lines, buffer_name):
    if buffer_name.lower() == 'vg_disassembly':
        lines = filter_for_vg_disassembly(lines)
    return lines

def filter_for_vg_disassembly(lines):
    from filters.vg_disassembly import vg_disassembly as buffer_filter
    processor = buffer_filter()
    lines = processor.process_lines(lines)
    return lines
