function! set_buffer#for_filename(...)
   let l:args = get(a:, 1, {})
   let l:event_args = l:args["event_input_args"]
   let l:function_args = l:args["function_args"]
   let buffer_filename_variable = g:vg_config_dictionary 
endfunction
