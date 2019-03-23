function! buffer_breakpoint#set_highlight_line(...)
   let l:event_args = get(a:, 1, {})
   let l:highlight_line_variable = l:event_args["highlight_line_variable"]
   let l:buffer_name = @%
   if l:highlight_line_variable != '' && g:vg_config_dictionary['variables'][l:highlight_line_variable] != ''
       let l:line_number = g:vg_config_dictionary['variables'][l:highlight_line_variable]
       execute "sign unplace 2"
       execute "sign place 2 line=" . l:line_number . " name=wholeline_breakpoint file=" . expand("%:p")
       execute ":" . l:line_number
   endif
endfunction
