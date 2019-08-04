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
   let l:mapped_file_buffers = get(g:vg_config_dictionary["internal"]["variables"], "mapped_filename_buffers", 0)
   if !l:mapped_file_buffers
       let g:vg_config_dictionary["internal"]["variables"]["mapped_file_buffers"] = {}
   endif
   if len(l:buffer_filename_variable)
       let l:buffer_window_number = l:mapped_file_buffers[l:buffer_name]
       if !l:buffer_window_number
           let l:buffer_window_number = vg_buffer_find#find_window_by_bufname(l:buffer_name, 1)
           let g:vg_config_dictionary["internal"]["variables"]["mapped_file_buffers"][l:buffer_name] = l:buffer_window_number
           set buftype=
           set modifiable
           execute l:buffer_window_number . "wincmd w"
           execute "silent edit! " . l:file_name
       else
            if findfile(l:file_name)
                let l:lines = readfile(l:filename)
                let g:vg_config_dictionary["internal"]["buffer_caches"][l:buffer_name] = l:lines
            else
                throw "error: unable to find file: " . l:file_name
            endif
            call vg_display#default_display_buffer(l:buffer_name)
       endif
   endif
endfunction
