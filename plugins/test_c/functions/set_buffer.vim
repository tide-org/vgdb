function! set_buffer#for_filename(...)
   let l:args = get(a:, 1, {})
   let l:event_args = l:args["event_input_args"]
   let l:function_args = l:args["function_args"]
   let l:buffer_name = l:function_args["buffer_name"]
   let l:file_name = l:function_args["file_name"]
   let l:buffer_filename_variable = g:vg_config_dictionary["buffers"][l:buffer_name]["buffer_filename_variable"]
   if l:buffer_filename_variable
       let l:buffer_filename = g:vg_config_dictionary["variables"][l:buffer_filename_variable]
   endif
   let l:mapped_file_buffers = get(g:vg_config_dictionary["variables"], "mapped_filename_buffers", 0)
   if !l:mapped_file_buffers
       let g:vg_config_dictionary["mapped_file_buffers"] = {}
   endif
   if len(l:buffer_filename_variable)
       let l:buffer_window_number = l:mapped_file_buffers[l:buffer_name]
       if !l:buffer_window_number
           let l:buffer_window_number = set_buffer#find_window(l:buffer_name, 1)
           let g:vg_config_dictionary["variables"]["mapped_file_buffers"][l:buffer_name] = l:buffer_window_number
           set buftype=
           set modifiable
           execute l:buffer_window_number . "wincmd w"
           execute "silent edit! " . l:file_name
       endif
   endif
endfunction

function! set_buffer#find_window(bufname, ...)
    let l:switch_window = get(a:, 1, 0)
    let l:mapped_file_buffers = get(g:vg_config_dictionary["variables"], "mapped_file_buffers", "")
    if len(l:mapped_file_buffers) > 0
       let l:file_buffer_window = get(l:mapped_file_buffers, a:bufname, '')
       if len(l:file_buffer_window) > 0
           if l:switch_window
               execute l:file_buffer_window . 'wincmd w'
           endif
           return l:file_buffer_window
       endif
    endif

    let l:bufmap = map(range(1, winnr('$')), '[bufname(winbufnr(v:val)), v:val]')
    let l:filtered_buffers_map = filter(l:bufmap, 'v:val[0] =~ a:bufname')
    if len(l:filtered_buffers_map) > 0
        let l:found_window = filtered_buffers_map[0][1]
        if l:switch_window
            execute l:found_window . 'wincmd w'
        endif
        return l:found_window
    else
        return -1
    endif
endfunction
