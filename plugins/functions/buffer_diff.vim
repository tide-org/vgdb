function! buffer_diff#check_do_buffer_diff(...)
    let l:event_args = get(a:, 1, {})
    let l:cache_variable = l:event_args["buffer_cache_variable"]
    let l:buffer_name = @%
    let l:current_buffer = g:vg_config_dictionary["internal"]["buffer_caches"][l:buffer_name]
    let l:cache_buffer = g:vg_config_dictionary["variables"][l:cache_variable]
    execute "sign unplace * file=" . expand("%:p")
    if len(l:cache_buffer) > 0 && len(l:current_buffer) <= len(l:cache_buffer)
        let l:line_index = 0
        for l:line in l:current_buffer
            if l:line !=? l:cache_buffer[l:line_index]
                let l:line_number = l:line_index + 1
                execute "sign place 3 line=" . l:line_number . " name=wholeline_diff file=" . expand("%:p")
            endif
            let l:line_index += 1
        endfor
    endif
    let g:vg_config_dictionary["variables"][l:cache_variable] = l:current_buffer
endfunction
