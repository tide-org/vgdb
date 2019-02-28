function! buffer_piets#set_piets(...)
   let l:event_args = get(a:, 1, {})
   let l:piet_match_array_variable = get(l:event_args, "piet_match_array_variable", '')
   let l:current_filename_variable = get(l:event_args, "current_filename_variable", '')
   if l:piet_match_array_variable != ''
      let l:buffer_name = @%
      let l:piet_match_list = g:vg_config_dictionary["variables"][l:piet_match_array_variable]
      let l:current_filename = g:vg_config_dictionary["variables"][l:current_filename_variable]
      if len(l:piet_match_list) > 0
          for l:piet_match in l:piet_match_list
              let l:match_tuple = split(l:piet_match, ":")
              if l:match_tuple[0] ==? fnamemodify(l:current_filename, ":t")
                  execute "sign place 3 line=" . l:match_tuple[1] . " name=piet file=" . expand("%:p")
              endif
          endfor
      endif
   endif
endfunction
